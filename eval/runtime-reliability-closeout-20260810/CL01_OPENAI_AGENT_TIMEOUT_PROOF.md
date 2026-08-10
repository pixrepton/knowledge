# CL-01 — `openai_agent_client._call_llm_with_timeout`: verdict and proof

## Verdict

```text
PREVIOUS VERDICT : PASS_AS_IS  ("30s inner < 45s outer, correctly nested")
ACTUAL VERDICT   : FIX_REQUIRED  -> FIXED
```

The previous verdict compared the wrong two numbers. It treated `LLM_CLIENT_TIMEOUT_SEC = 30` as
"the inner mechanism", when 30s is the timeout of a **single HTTP attempt** and the SDK performs
up to **three** of them inside one `create()` call.

## Before — mechanical trace

```text
plan_next_tool(...)                                   # graph.py:234, NO enclosing timeout
  └─ for endpoint in endpoints:                       # visible fallback loop, backoff 2**index
       └─ _call_llm_with_timeout(...)
            executor  = ThreadPoolExecutor(max_workers=2)   # SHARED across the planner instance
            future    = executor.submit(client.chat.completions.create, timeout=30)
            return future.result(timeout=45)                # LLM_TIMEOUT_SEC
            except TimeoutError: raise LLMTimeoutError      # NO cancel() at all
```

| question | answer |
|---|---|
| outer timeout owner | `_call_llm_with_timeout` — `future.result(timeout=45)` |
| inner timeout owner | the OpenAI SDK — `options.timeout = 30`, applied **per attempt** |
| which clock starts first | the outer one (submit precedes the first HTTP request) |
| is 30s outer or inner | **inner**, and per-attempt — not per-call |
| is 45s outer or inner | **outer**, and per-call |
| number of retries | SDK `max_retries` default **2** → up to **3 attempts** per `create()`, plus SDK backoff |
| fallback behavior | endpoint loop in `plan_next_tool`, with `2**index` backoff |
| does cancellation stop real work | **no** — `cancel()` was never even called; the request ran to completion |
| can the outer preempt the inner | **yes** |

Verified in the running container, not from memory:

```text
openai version      : 1.109.1
max_retries default : 2
SDK retry loop      : for retries_taken in range(max_retries + 1)   # 3 attempts
timeout application : options.timeout re-applied per _build_request  # per attempt
```

### Maximum possible elapsed time, before

```text
inner (one create() call)  = 3 attempts x 30s + SDK backoff   ~= 90s+
outer envelope             = 45s
                             ^^^^ fires first, every time the inner needed its retries
```

So the outer envelope was **shorter than the mechanism it was supposed to bound** — the identical
defect class as RT01, in a module the earlier audit had cleared.

### Two consequences, not one

1. **Unreachable retry.** The SDK's own retry could never complete inside 45s.
2. **Orphaned work on a bounded shared pool.** `ThreadPoolExecutor(max_workers=2)` is created once
   per planner and shared. An abandoned request keeps occupying a slot until it finishes on its
   own. Two concurrent timeouts saturate the pool, after which `executor.submit()` **queues** —
   so a later planner call could exhaust its own 45s waiting in the queue without ever issuing a
   request. That is strictly worse than the intake case, which used a fresh single-use executor.

## After — the repair

Follows the existing stage-deadline model rather than enlarging a constant.

```text
plan_next_tool
  with stage_deadline("agent_planner", AGENT_PLANNER_BUDGET_SEC = 3 x 30s = 90s):
     for endpoint in endpoints:
         if not deadline.has_room_for_attempt(): -> PLANNER_BUDGET_EXHAUSTED, stop
         endpoint_budget = remaining / endpoints_still_to_try
         with provider_budget_scope(endpoint, endpoint_budget):
             _call_llm_with_timeout(...)
                 attempt_timeout = min(30, endpoint budget, stage remaining)
                 client.with_options(max_retries=0, timeout=attempt_timeout)   # real SDK only
                 client.chat.completions.create(...)      # on THIS thread
         backoff = min(2**index, remaining - min_attempt)
```

Key decisions:

- **No wrapper thread.** The call runs on the caller's thread, bounded by the HTTP timeout it
  hands the client. Nothing can be abandoned, and the shared pool is gone entirely.
- **`max_retries=0`.** The SDK's retry loop was an *invisible* second retry layer. Retry and
  fallback now belong exclusively to the endpoint loop, which is budgeted, logged and observable.
  `_build_client` also constructs with `max_retries=0`, so both injected and built clients agree.
- **Budget derived, not chosen.** `AGENT_PLANNER_BUDGET_SEC = 3 x LLM_CLIENT_TIMEOUT_SEC` — three
  real endpoint attempts at the configured per-attempt timeout.
- **Test doubles untouched.** `_bounded_client` only re-options genuine `openai` clients; a
  `MagicMock` would happily auto-create `with_options()` and hand back a *different* mock,
  silently detaching the call from whatever a test configured.

### Maximum possible elapsed time, after

```text
per attempt        = min(30s, endpoint share, stage remaining)
per endpoint       = exactly one attempt (max_retries=0)
whole planner call = <= 90s, plus at most one in-flight attempt already clamped by the remainder
cancellation       = not needed; nothing is abandoned
```

## Tests

`tools/gmail_audit/tests/test_agent_planner_deadline.py` — 10 tests:

- budget is derived from the per-attempt timeout and exceeds it;
- `LLM_TIMEOUT_SEC` is gone;
- **AST-level** assertion that the module creates no `ThreadPoolExecutor` and calls no `submit`
  (checked on the syntax tree, so prose describing the old design cannot satisfy or break it);
- a real SDK client is re-optioned with `max_retries=0`;
- an injected double is *not* re-optioned;
- per-attempt timeout is clamped by the remaining budget;
- an attempt refuses to start with no budget left;
- outside a deadline the configured timeout is unchanged;
- no orphan work survives a planner call (in-flight counter + thread count);
- the endpoint share reserves the fallback's turn (~half the budget for the first of two).

Existing planner suites re-run green: 51 tests across `chaos/test_llm_timeout.py`,
`test_agent_planner_endpoints.py`, `test_agent_pr_c.py`, `test_agent_pr_c_complete.py`,
`test_deepseek_agent_planner.py`, `test_agent_graph_engine.py`.
