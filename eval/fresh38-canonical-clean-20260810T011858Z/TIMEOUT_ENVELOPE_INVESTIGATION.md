# Timeout Envelope / Provider Chain Investigation

Triggered by operator instruction to distinguish, for the 6 first-attempt failures
(`INT-05, NEW-04, FU-06, SVC-04, CTX-01, NEW-01`), between:

1. provider-side latency/availability,
2. product timeout/retry-budget design, and
3. interaction of both.

No SUT/runner/config/corpus/judge/scorer changes were made to perform this investigation --
it is pure source-code and live-settings reading, plus re-interpretation of the already-frozen
Phase A evidence. Conclusion: the failures are **PRODUCT_RUNTIME** (a timeout/retry-budget
design defect), not `PROVIDER_AVAILABILITY`. `FIRST_ATTEMPT_LEDGER.json`/`.csv` updated
accordingly; the raw captured evidence (`one-CASE.json`, `capture.log`, stdout/stderr) is
untouched.

## The call chain, traced end to end

For the `intake_llm` lane, `gmail_intake.run_intake_reasoning()` does two things in sequence:

1. Calls `run_signal_extraction()` **again**, internally (`gmail_intake.py:2563`) -- this is a
   second, redundant extraction call on top of the harness's own separate `run_extraction()`
   step. It always succeeded (0 failures across all 38 first attempts, including the 6 that
   failed later). Not itself the failure point, but explains why 2 of the 3 `CONTEXT_ASSEMBLED`
   log lines per case precede the real failure by only a few seconds.
2. Calls `_run_llm_with_timeout()` (`gmail_intake.py:2453-2496`) -- **this is where every one
   of the 6 failures occurs.**

```python
LLM_HARD_TIMEOUT_SEC = 60      # central_llm_stage.py -- defined, but NOT what wraps this call
LLM_CLIENT_TIMEOUT_SEC = 30    # central_llm_stage.py -- defined as a parameter default,
                                # never actually read inside run_central_structured_stage()

def _run_llm_with_timeout(...):
    executor = ThreadPoolExecutor(max_workers=1)
    try:
        future = executor.submit(_call)              # _call -> run_central_structured_stage(...)
        return future.result(timeout=60)              # <-- literal, hardcoded 60
    except FuturesTimeout:
        get_logger("gmail_intake").error("INTAKE_LLM_TIMEOUT", extra={"x": {"timeout_sec": 60}})
        return None
```

`_run_llm_with_timeout` has **no retry loop of its own** -- one submit, one 60-second wait, done.

Inside that single 60-second window, `run_central_structured_stage()`
(`central_llm_stage.py:499`) builds the real provider chain and calls
`groq_client.run_structured_stage()` -> `request_structured_output()` ->
`_post_structured_with_router()` -> `LLMRouter(providers).run()`.

### Live provider chain (read from the running container's loaded settings, not defaults)

```text
http_timeout            = 60      # PER-HTTP-REQUEST timeout, requests.post(timeout=...)
http_max_retries        = 4       # PER-PROVIDER retry attempts
http_retry_base_delay   = 2.0     # exponential backoff base (base * 4**attempt between attempts)
llm_primary_provider    = openai_chat
llm_fallback_providers  = (groq, cerebras)
groq_api_keys           = 4 configured keys
cerebras / nvidia / openrouter = unconfigured (instant skip in LLMRouter.run())
```

`LLMRouter.run()` tries providers **in order**: `openai_chat` first, then `groq` (4 keys,
rotated), then `cerebras` (unconfigured, instant skip -- costs nothing). Each *configured*
provider's own call function (`_post_openai_chat_structured`, `_post_groq_structured`,
`groq_client.py:1290-1389` / `1421-1507`) is **itself** a retry loop:

```python
attempts = max(1, settings.http_max_retries)   # = 4
for attempt in range(1, attempts + 1):
    response = requests.post(url, ..., timeout=settings.http_timeout)   # = 60s, PER ATTEMPT
    ...
    if attempt >= attempts:
        raise last_error
    _sleep_before_retry(settings, attempt, ...)   # base_delay * 4**attempt backoff
```

## The defect

**The outer hard-kill (`future.result(timeout=60)`) is numerically identical to the inner
per-HTTP-attempt timeout (`settings.http_timeout=60`), and the outer clock starts before the
inner one.** The inner mechanism is architected to need, in the worst case, up to
`4 attempts x 60s + backoff` **per provider**, across **two configured providers**
(`openai_chat` then `groq`) before giving up -- structurally several minutes of designed
resilience. None of that is reachable: the outer envelope kills the whole call at the 60-second
mark, which arrives at or before the very first HTTP attempt's own timeout could ever fire on
its own. Concretely: if the first `openai_chat` request doesn't return quickly, the outer kill
fires while attempt 1 of 4 is still in flight -- attempt 2, and the entire `groq` fallback
(4 live keys, proven working by this run's own preflight smoke test and by the fact groq clearly
serves other successful calls), never get invoked. `future.cancel()` on an already-running
thread doesn't stop the underlying blocking HTTP call either -- it just stops the caller from
waiting on it; whatever the thread was doing is abandoned, orphaned, and its outcome is never
observed by production code.

### Confirming comparison: extraction has no outer envelope at all

`signal_extractor.run_signal_extraction()` calls `run_central_structured_stage()` **directly**,
with no `ThreadPoolExecutor`/hard-timeout wrapper whatsoever (`signal_extractor.py:86-100`). It
goes through the *exact same* `openai_chat -> groq -> cerebras` router chain, same settings, same
live account. It succeeded on **all 38/38 first attempts** in this run, including on the 6 cases
where intake_reasoning later failed in the very same case. This is the strongest available
evidence that the underlying provider chain itself is not systemically broken -- extraction,
which has full access to its own advertised retry-and-fallback resilience, absorbed whatever
transient conditions existed; intake_reasoning, whose resilience is foreclosed by its own outer
wrapper, could not.

## Distinguishing the three dimensions, as asked

**1. Provider-side latency/availability** -- real, but secondary and not separately provable as
"outage" from this evidence. Something made the *first* `openai_chat` HTTP attempt not return
within roughly a minute in 6 of 38 real calls (scattered, non-consecutive, no shared input
characteristic across `INT/NEW/FU/SVC/CTX` case families). A preflight smoke call through the
same chain returned in 5.6s minutes before this run, and 32/38 other real calls this run
completed normally -- consistent with ordinary tail latency on a live API, not a sustained
outage. This is not, by itself, a product defect; it is an expected characteristic of any
external LLM dependency.

**2. Product timeout/retry-budget design -- proven, and the dominant, actionable cause.** The
system already contains real engineering investment in resilience (per-provider retry with
exponential backoff, a 3-provider fallback chain, a 4-key Groq pool) but an unrelated, tighter
outer envelope in `gmail_intake.py` makes essentially all of that resilience unreachable for this
one call type. This is a code-level defect with a precise location and a mechanical proof
(`http_timeout == outer hard-kill == 60`), independent of anything the provider did. It is also
asymmetric with the rest of the codebase: extraction, using the identical chain, has no such
outer collision and never failed.

**3. Interaction of both** -- yes, in the sense that a provider-side hiccup is the trigger, but
the interaction is one-directional and the fix is entirely on the product side: *any* transient
slowness on the first attempt of `openai_chat`, however ordinary, is converted into a guaranteed,
unrecoverable, user-visible failure, because the product's own timeout budgeting leaves no room
for its own retry/fallback design to ever run. Removing or widening the outer envelope (or
coordinating it with the inner chain's real worst-case duration, the way extraction's absence of
an outer envelope already does) would very likely have let the same six calls fall through to the
`groq` fallback silently, the same way extraction's calls did.

## What this changes

- `FIRST_ATTEMPT_LEDGER.json` / `.csv`: `failure_class` for all 6 failing cases corrected from
  `PROVIDER_AVAILABILITY` to `PRODUCT_RUNTIME`, with a `failure_class_note` pointing here.
  `FIRST_ATTEMPT_RELIABILITY` itself is unchanged (`32/38 = 84.21%`) -- this is a re-labeling of
  *why* the 6 failures happened, not a change to which cases failed.
- `production_would_fail = true` still holds for all 6 -- this is real, unmodified production
  code and a real, currently-live timeout/config value; a live customer email would fail
  identically today.

## Not done (out of scope for this investigation)

No code was changed. No timeout constant was widened. No retry logic was added. This is a
finding for the operator to act on, not a fix applied during a frozen measurement run.
