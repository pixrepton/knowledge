# Same-Class Timeout Audit — AIOS-RUNTIME-RELIABILITY-01

Bounded audit of one defect class only: **two or more independent, mutually unaware timeout
systems stacked on the same call, where the outer one can preempt the inner one's retry/fallback
and abandon in-flight work.**

This is not a general architecture audit. Paths that are correctly bounded are named and left
alone, per the task scope.

## Search performed

Production runtime under `gmail-agent/` (tests excluded):

```
ThreadPoolExecutor            future.result(timeout=      wait_for(
timeout=                      http_timeout                http_max_retries
requests.post(... timeout=    run_central_structured_stage
LLMRouter                     provider fallback/retry loops
```

`asyncio.wait_for` — no production hits.

## Live configuration the matrix is evaluated against

Read from the running `gmail-agent-nodeb-api` container, not from defaults:

```text
http_timeout            = 60      llm_primary_provider   = openai_chat
http_max_retries        = 4       llm_fallback_providers = (groq, cerebras)
http_retry_base_delay   = 2.0     groq_api_keys          = 4
anthropic_api_key       = UNSET   deepseek_api_key       = SET
```

## Matrix

| # | call_site | stage | outer_timeout | inner_timeout | retry | fallback | deadline_owner | outer_can_preempt_inner | can_leave_orphan_work | classification |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `gmail_intake._run_llm_with_timeout` | `intake_reasoning` | 60s `ThreadPoolExecutor` | 60s per HTTP attempt | 4/provider | 2 configured providers | **split — nobody** | **YES** (equal value, outer clock starts first) | **YES** — `shutdown(wait=False)`, `future.cancel()` cannot stop a running request | **DEFECT — P0, measured (6/38)** |
| 2 | `agent_runtime/tools/handlers._run_llm_extraction` | agent tool `extract_facts_from_text` → `signal_extraction` | 30s `ThreadPoolExecutor` | 60s per HTTP attempt | 4/provider | 2 configured providers | **split — nobody** | **YES, worse** (30s outer < 60s single attempt: outer *always* fires first) | **YES** — same abandon pattern | **DEFECT — same class, unmeasured** |
| 3 | `central_llm_stage._call_with_retry` | Anthropic branch of any central stage | `client_timeout+30` = 60s `ThreadPoolExecutor` | 60s `TopInstalLLMClient.timeout_sec` | 3 at this layer | falls through to groq chain | this wrapper | **YES** (equal values) | **YES** — `future.cancel()` no-op | **SAME CLASS — path inactive** (`anthropic_api_key` UNSET); hardened, not restructured |
| 4 | `agent_runtime/openai_agent_client._call_llm_with_timeout` | agent planner LLM | 45s `ThreadPoolExecutor` | **30s** SDK client timeout | endpoint loop | multi-endpoint | outer wrapper | **NO** — inner (30s) always fires before outer (45s) | bounded by the 30s inner timeout | **CORRECTLY BOUNDED — left alone** |
| 5 | `agent_runtime/graph.py:598` | agent turn tool execution | 45s shared pool | per-tool | none | none | this wrapper | **NO** after fix #2 (tool budget 30s < 45s) | shared pool, `max_workers=4` | **CORRECTLY NESTED — left alone** |
| 6 | `intake_shared_downstream` LLM pool | business/draft/case-intelligence/action-plan | none (`.result()` with no timeout) | stage budget per call | per stage | per stage | each inner stage | n/a — no outer timeout exists | no | **NO COLLISION — left alone** (each inner stage is independently bounded) |
| 7 | `groq_client._wait_for_runtime_cooldown` | any provider retry loop | n/a | n/a | n/a | n/a | none | n/a | no | **DEFECT — unbudgeted sleep** (found by the CASE-C/E fault-injection tests during this repair, see below) |

## Verdicts

**Fixed (proven same-class defects):**

- **#1** — the measured cause of `PRE_FIX_FIRST_ATTEMPT_RELIABILITY = 32/38`. Outer executor
  removed; the bound now lives in `run_central_structured_stage` and is shared with retry and
  fallback.
- **#2** — byte-identical mechanism with a worse ratio. Executor removed; the tool's 30s
  contract is preserved as a `stage_deadline`, so it still terminates well inside the 45s agent
  turn supervision (#5) but no longer forecloses its own retry/fallback or orphans a request.
- **#3** — inactive in this configuration but structurally identical. Rather than restructure a
  dormant path, `_call_with_retry` now clamps its `hard_timeout` to the remaining stage budget
  and stops retrying when the budget cannot fund another attempt. Duplicate ownership removed;
  the executor there remains, and is reported below as a known residual.
- **#7** — found while proving #1: the per-provider cooldown slept *after* the budget check, so a
  4th attempt could be issued with `timeout=0.0`. Cooldown and backoff sleeps are now clamped to
  the remaining window, and an attempt is never started with a non-positive timeout.

**Left alone (correctly bounded, per scope):**

- **#4** — inner 30s < outer 45s. The nesting order is correct; the outer wrapper cannot preempt
  the inner timeout.
- **#5** — generic per-turn tool supervision at a different layer, not an LLM retry collision.
  After #2 the innermost LLM budget (30s) is strictly below it.
- **#6** — no outer timeout exists, so there is nothing to collide; every stage submitted to the
  pool is bounded by its own stage deadline.

## Residual, reported not fixed

`central_llm_stage._call_with_retry` (#3) still uses a `ThreadPoolExecutor` whose `future.cancel()`
cannot stop an already-running Anthropic request. Its budget is now correct, so it can no longer
preempt the chain, but a cancelled attempt there can still leave one abandoned request. This path
is unreachable in the current configuration (`anthropic_api_key` UNSET) and removing the executor
would mean restructuring a dormant provider integration — outside this task's scope.

Status: `PROVEN_OPEN`, low severity, config-gated.
