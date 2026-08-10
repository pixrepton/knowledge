# FIX-RT01 — Deadline / retry / fallback model: before and after

## Before

Two independent timeout systems, neither aware of the other.

```text
gmail_intake.run_intake_reasoning
  └─ _run_llm_with_timeout
       executor = ThreadPoolExecutor(max_workers=1)
       future   = executor.submit(_call)
       return future.result(timeout=60)          # outer hard kill, hardcoded
       except FuturesTimeout: log INTAKE_LLM_TIMEOUT; return None
       finally: executor.shutdown(wait=False)    # abandons whatever is running
          │
          └─ run_central_structured_stage
               └─ groq_client.run_structured_stage
                    └─ request_structured_output
                         └─ _post_structured_with_router
                              └─ LLMRouter(providers).run()      # no clock at all
                                   ├─ openai_chat  ─ retry loop: 4 x requests.post(timeout=60)
                                   │                 backoff base 2.0 * 4**attempt
                                   ├─ groq (4 keys) ─ retry loop: 4 x requests.post(timeout=60)
                                   └─ cerebras     ─ unconfigured, instant skip
```

**The collision.** The outer hard kill (60s) was numerically identical to a single inner HTTP
attempt (`http_timeout=60`), and the outer clock started first. The inner design needs, worst
case, `4 attempts x 60s + backoff` per provider across two configured providers — minutes of
engineered resilience. None of it was reachable: the kill fired at or before the first attempt's
own timeout could surface, so attempt 2 and the entire `groq` fallback never ran.

**The orphan.** `future.cancel()` cannot stop a thread that is already inside a blocking
`requests.post`. The wrapper stopped *waiting*; the request kept going, its outcome never
observed, its connection and provider quota still consumed.

**What it cost.** Fresh38 first-attempt reliability `32/38 = 84.21%`. All six failures identical:
`INTAKE_LLM_TIMEOUT (timeout_sec=60)` → `parity_error=production_faithful_intake_invalid`.

The asymmetry that proved it was a product defect rather than a provider outage:
`signal_extractor.run_signal_extraction` calls the *same* chain with *no* outer envelope and
succeeded **38/38**, including on all six cases that failed at intake reasoning moments later.

## After

One owner. The stage creates a budget; everything below asks how much is left.

```text
run_central_structured_stage                     ← the only place a deadline is created
  with stage_deadline(stage_name, LLM_STAGE_BUDGET_SEC=180):
       │
       └─ LLMRouter.run()
            for each provider still to try:
                if remaining < LLM_MIN_ATTEMPT_SEC:      → skip, record deadline_exhausted, stop
                share = remaining / providers_still_to_try
                with provider_budget_scope(provider, share):
                    provider.call()
                        └─ retry loop:
                             if window < min_attempt:              → stop retrying
                             timeout = min(http_timeout, provider share, stage remaining)
                             if timeout <= 0:                      → stop
                             requests.post(..., timeout=timeout)
                             backoff = min(backoff, window - min_attempt)
                             cooldown = min(cooldown, window - min_attempt)
```

`gmail_intake._run_llm_with_timeout` no longer creates an executor. It calls the stage directly
and returns `None` only on `terminal_failure_reason == "stage_deadline_exhausted"` — the same
terminal contract the old timeout path had, so the frozen runner's parity handling is unchanged.
Every other provider error propagates exactly as before.

### Where the numbers come from

They are derived from a contract, not chosen to make a benchmark green.

- `LLM_STAGE_BUDGET_SEC = 180` — the budget must fit a real primary attempt, one retry, and a
  real fallback attempt at the configured `http_timeout=60`: `60 + backoff + 60 ≈ 130s`. 180
  leaves headroom for a second retry without letting one stalled stage dominate a case.
- `LLM_MIN_ATTEMPT_SEC = 5` — below this an attempt cannot produce a useful result; starting one
  only converts remaining budget into a guaranteed timeout and hides why the chain stopped.
- **Even split across providers still to try** — this is what keeps a slow primary from eating
  the fallback's turn, the precise failure that was measured. Unspent time rolls forward, so a
  fast failure costs the chain nothing and the last provider gets the whole remainder.

`config.py` rejects `LLM_STAGE_BUDGET_SEC <= HTTP_TIMEOUT` at load time — that configuration
*is* the original defect, so it is no longer expressible.

### Requirements check

| requirement | how it holds |
|---|---|
| hard upper bound still exists | the stage budget, owned by the stage, not a wrapper thread |
| retry/fallback actually has time | per-provider share reserves the fallback's turn |
| quick 429/5xx/provider errors fall through immediately | `_should_fast_fallback_status` unchanged; a fast failure spends nothing |
| a slow provider cannot consume unbounded total runtime | every attempt is clamped by remaining budget |
| remaining budget is respected | `attempt_timeout_sec` = min(configured, provider share, stage remaining) |
| terminal timeout is structured and attributable | `LLM_STAGE_BUDGET_FAILURE` + `terminal_failure_reason` + per-attempt records |
| no invisible retry-to-success | every attempt is recorded in `llm_provider_attempts` with its budget state |
| no orphan worker thread | the executors that abandoned work are gone from both proven sites |
| no secrets in telemetry | provider names, counts, durations only — no prompts, responses or keys |

## Orphan-work behaviour: before vs after

| | before | after |
|---|---|---|
| what stopped the wait | `future.result(timeout=60)` raising `FuturesTimeout` | the chain returning a terminal result |
| what stopped the work | nothing — `future.cancel()` is a no-op on a running thread | the work finishes or its own bounded HTTP timeout fires |
| observable outcome of the abandoned attempt | none, ever | recorded in `llm_provider_attempts` |
| threads left behind | one per timeout, from `shutdown(wait=False)` | none |

Test `test_case_f_no_orphan_work_survives_a_bounded_stage` asserts the property the old design
violated: when the stage returns, no injected provider call is still in flight, and the active
thread count has not grown.

## Telemetry

A production timeout previously produced one line: `INTAKE_LLM_TIMEOUT {"timeout_sec": 60}` —
enough to know a stage died, not enough to know which provider stalled, whether fallback was
reached, or how much budget was left.

Now, on a terminal stage failure:

```json
{
  "msg": "LLM_STAGE_BUDGET_FAILURE",
  "stage": "intake_reasoning",
  "terminal_failure_reason": "stage_deadline_exhausted",
  "provider": "openai_chat",
  "attempt": 2,
  "fallback_index": 1,
  "fallback_used": true,
  "retryable": true,
  "configured_stage_budget_ms": 180000,
  "elapsed_ms": 180012,
  "remaining_budget_ms": 0,
  "provider_attempts": [
    {"provider": "openai_chat", "status": "failed",  "error_class": "timeout",
     "latency_ms": 90003, "provider_budget_ms": 90000, "remaining_budget_ms": 89997},
    {"provider": "groq",        "status": "failed",  "error_class": "timeout",
     "latency_ms": 89995, "provider_budget_ms": 89997, "remaining_budget_ms": 0}
  ]
}
```

That answers "which provider consumed the budget and why did fallback not recover?" mechanically,
without reconstructing it from timestamps.

## A second defect found while proving the first

The CASE-C/E fault-injection tests caught `[12.0, 9.0, 5.0, 0.0]` — a fourth HTTP attempt being
issued with `timeout=0.0`. Cause: `_wait_for_runtime_cooldown` slept *after* the budget check, so
the cooldown spent the window the attempt was checked against. Both the cooldown and the retry
backoff are now clamped to `window - min_attempt`, and no attempt starts with a non-positive
timeout. Same defect class, one layer further down; it would have been invisible without
deterministic fault injection.
