# AIOS-RUNTIME-RELIABILITY-01 — Final Repair Report

Scope: runtime reliability only. No capability residual repair was started, and no closed
program was reopened.

---

## A. PRE-FIX EVIDENCE

```text
FIRST_ATTEMPT_TOTAL       = 38
FIRST_ATTEMPT_VALID       = 32
FIRST_ATTEMPT_FAILURES    = 6
PRE_FIX_FIRST_ATTEMPT_RELIABILITY = 32/38 = 84.21%

failed: INT-05, NEW-04, FU-06, SVC-04, CTX-01, NEW-01
all six: INTAKE_LLM_TIMEOUT (timeout_sec=60)
         -> parity_error = production_faithful_intake_invalid
         -> classified PRODUCT_RUNTIME
```

Preserved before any code changed, committed as `knowledge:687bed5`:

- `PRE_FIX_BASELINE_LOCK.json` — SHA256 of all **116** files in the volatile capture out-dir
  plus every preserved report file, with the headline numbers locked.
- `verify_pre_fix_lock.py` — re-verifies hashes, headline, ledger self-agreement and
  FIRST_ATTEMPT purity. Gate `PRE_FIX_BASELINE_LOCK`: **PASS**.
- `raw-first-attempt-failures/` — the six failed one-CASE artifacts with stdout/stderr and
  `capture.log`, copied out of volatile session scratch into durable storage.

This number is final and was not touched by anything below.

---

## B. ROOT CAUSE

`gmail_intake._run_llm_with_timeout` wrapped the intake-reasoning LLM call in
`ThreadPoolExecutor(...).result(timeout=60)`. Underneath, the chain was configured for
`http_timeout=60` **per HTTP attempt** × `http_max_retries=4` **per provider**, across
`openai_chat → groq (4 keys) → cerebras`.

The outer hard kill was numerically identical to a single inner attempt and its clock started
first, so the inner retry/fallback machinery was structurally unreachable: the kill fired at or
before the first attempt's own timeout could surface. `future.cancel()` cannot stop a thread
inside a blocking `requests.post`, so the abandoned request kept running, unobserved.

The proof that this was a product defect and not a provider outage:
`signal_extractor.run_signal_extraction` calls the **same** chain with **no** outer envelope and
succeeded 38/38 — including on all six cases that failed at intake reasoning moments later.

Trigger: ordinary provider tail latency. Mechanism: the product's own timeout budgeting left no
room for its own resilience design to run.

---

## C. SAME-CLASS AUDIT

Full matrix in `SAME_CLASS_TIMEOUT_AUDIT.md`. Summary:

| # | site | verdict |
|---|---|---|
| 1 | `gmail_intake._run_llm_with_timeout` | **DEFECT — fixed** (the measured cause) |
| 2 | `agent_runtime/tools/handlers._run_llm_extraction` | **DEFECT — fixed** (30s outer vs 60s inner: worse ratio) |
| 3 | `central_llm_stage._call_with_retry` (Anthropic) | **same class, path inactive — hardened** |
| 4 | `agent_runtime/openai_agent_client._call_llm_with_timeout` | correctly bounded (30s inner < 45s outer) — **left alone** |
| 5 | `agent_runtime/graph.py` turn supervision | correctly nested — **left alone** |
| 6 | `intake_shared_downstream` LLM pool | no outer timeout, no collision — **left alone** |
| 7 | `groq_client._wait_for_runtime_cooldown` | **DEFECT — fixed** (unbudgeted sleep, found during proof) |

---

## D. IMPLEMENTED RUNTIME CHANGES

| file | change |
|---|---|
| `llm_deadline.py` *(new)* | `StageDeadline`, `ProviderBudget`, `stage_deadline()`, `provider_budget_scope()`, `attempt_timeout_sec()`, `retry_window_sec()`, `DeadlineExhausted` |
| `central_llm_stage.py` | `run_central_structured_stage` opens the one stage deadline; `log_stage_budget_failure` emits terminal provenance; `_call_with_retry` clamps its hard timeout and backoff to remaining budget |
| `llm_provider_router.py` | `LLMRouter.run` is budget-aware: per-provider share, pre-call budget check, `deadline_exhausted` attempts, consistent `terminal_failure_reason` on **both** terminal paths, budget fields in every attempt record |
| `groq_client.py` | both provider retry loops take per-attempt timeouts from the budget, stop retrying when it cannot fund an attempt, and clamp backoff **and** cooldown |
| `gmail_intake.py` | `_run_llm_with_timeout` no longer creates an executor; returns `None` only on `stage_deadline_exhausted`, with full telemetry |
| `agent_runtime/tools/handlers.py` | `_run_llm_extraction` keeps its 30s contract as a deadline, not a thread kill |
| `config.py` | `LLM_STAGE_BUDGET_SEC=180`, `LLM_MIN_ATTEMPT_SEC=5`; rejects `budget <= http_timeout` at load |
| `daszek_client.py` | `_DaszekSession` translates transport failures to `DaszekClientError` |
| `signal_worker.py` | `attach_daszek_projection_client(mandatory=)`, `_maybe_reattach_daszek` with bounded backoff, degradation in manifest/summary/logs |
| `preclassifier.py` | legal escalation requires a legal actor **and** an adversarial cue |

Commits: `gmail-agent:8c710bb`, `gmail-agent:a2ebeb9`, `root:4d05018`, `root:da88f71`,
`knowledge:687bed5`.

---

## E. DEADLINE MODEL — BEFORE vs AFTER

Detail in `RT01_DEADLINE_MODEL.md`.

**Before:** two independent clocks. Outer `future.result(timeout=60)` vs inner
`http_timeout=60 × 4 attempts × 2 providers`. Outer always won; inner resilience unreachable.

**After:** one owner.

```text
stage budget (180s, owned by run_central_structured_stage)
  └─ per-provider share = remaining / providers still to try
       └─ per-attempt timeout = min(http_timeout, provider share, stage remaining)
       └─ retry only while the share can fund a real attempt
  └─ fallback only while the stage budget can fund a real attempt
```

The numbers are derived, not tuned to a benchmark: 180s is the floor needed for
`primary attempt + retry + fallback attempt` at `http_timeout=60`, and the even split across
untried providers is what reserves the fallback's turn. `config.py` makes the original defective
configuration (`budget <= http_timeout`) unexpressible.

---

## F. ORPHAN-WORK BEHAVIOUR — BEFORE vs AFTER

| | before | after |
|---|---|---|
| what stopped the wait | `FuturesTimeout` | the chain returning a terminal result |
| what stopped the work | nothing — `cancel()` is a no-op on a running thread | the work finishes, or its own bounded HTTP timeout fires |
| outcome of the abandoned attempt | never observed | recorded in `llm_provider_attempts` |
| threads left behind | one per timeout (`shutdown(wait=False)`) | none |

`test_case_f_no_orphan_work_survives_a_bounded_stage` asserts the violated property directly:
when the stage returns, no injected provider call is still in flight and the thread count has not
grown.

---

## G. WORKER CRASH-LOOP

Detail and logs in `RT02_WORKER_CRASHLOOP_PROOF.md`.

**Root cause, two faults in series:** `run_signal_loop` called `attach_daszek_client()` as a
*startup precondition* before the poll loop, and `DaszekClient` let raw
`requests.ConnectionError` escape — which subclasses `OSError`, so `main()`'s `except OSError`
logged "File/OS error in intake" and returned 1. Docker restarted it, forever.

**Ownership:** Daszek is projection; Node B owns operational truth;
`DASZEK_OPERATIONAL_FEED_AUTO_PUSH` is an optional projection push. Classification:
`OPTIONAL_DEPENDENCY_HANDLING` + `STARTUP_FAILURE_POLICY`. The repair weakens, not strengthens,
Node B → Daszek coupling. An explicit `--push-daszek` still fails fast.

**Proof:**

| | before | after |
|---|---|---|
| restart count | **692**, climbing | **0** |
| state | `restarting` | `running` |
| reached the poll loop | never | yes |
| outage visible as | "File/OS error in intake" | `DASZEK_DEPENDENCY_DEGRADED`, `required=false` |
| recovery | container restart roulette | automatic, `DASZEK_DEPENDENCY_RECOVERED` after 3 bounded attempts, no restart |

Canonical processing continued while degraded (`GET /profile ok (200)`, `GET /history ok (200)`,
`BP_EXECUTED`, `sla_watcher`). Daszek was then restored and recovery observed live. No business
data was mutated to produce this proof.

---

## H. FRESH38 MEASUREMENT INTEGRITY

Reuse previously required only "artifact exists and has no `parity_error`" — with no proof the
artifact came from the same SUT. That silently mixed two preclassifier states into one "clean"
21/38 result.

Now every capture computes an `experiment_manifest_hash` over wrapper, runner, scoring helper,
corpus, container image, mode and the SHA256 of every hot-synced product file. Each case gets a
`one-<CASE>.manifest.json` sidecar bound to it. Reuse requires an exact match; otherwise
`REUSE_REJECT_SUT_MISMATCH` and a recapture. `-NoReuse` refuses even a matching artifact.

`FIRST_ATTEMPT` and `RECOVERY_ATTEMPT` are permanently separated — recovery writes under
`recovery-attempt-N/` and cannot overwrite first-attempt evidence. Historical artifacts untouched.

The hot-sync list — itself the original contamination vector — did not cover six files this repair
touches; they were added, and absent files are now reported as `missing_hot_files`. Provisioning
failures are no longer silent: the wrapper aborts if docker is unavailable, if any `docker cp`
returns non-zero, or if the container image id cannot be resolved.

Proof: `scripts/tests/test_fresh38_reuse_gate.ps1` (docker stubbed) asserts end-to-end that an
unverified runner aborts, a matching SUT reuses, a changed SUT is rejected and recaptured, a
recovery run leaves the first-attempt artifact byte-identical, and `-NoReuse` bypasses reuse.
Gate `FRESH38_REUSE_GATE`: **PASS**.

---

## I. RUNNER PROVENANCE

Before: the wrapper preferred an opaque session-scratch copy
(`C:\top-code-session-scratch\exit2-fresh38-...\run_recovery_pf.PATCHED.py`) and fell back to the
`.artifacts` harness without comparing them. They happened to be byte-identical
(`8c2f3ddc…`), but nothing checked that.

After: `.artifacts/ai-os-post-stage6-fresh-baseline/harness/run_recovery_pf.py` is the single
canonical source; the scratch path is no longer consulted. Its SHA256 is pinned in the **tracked**
`scripts/fresh38_runner_provenance.json`, verified at every capture, and a mismatch **aborts** the
run. There are not two diverging canonical runners.

**Residual:** `.artifacts/` is deliberately gitignored (`/.artifacts/`), so the runner *bytes*
remain untracked. Its *identity* is now tracked and mechanically enforced, which is the second
option the task allowed. Flagged below.

---

## J. PRECLASSIFIER VERIFY — **FIXED**

Bounded semantic verification, as instructed. The rule matched bare `"prawnik"`/`"prawnika"` by
plain substring. Negative examples proved it over-broad — three ordinary heat-pump leads were all
routed to `review_direct`, skipping the reasoning lane:

- "mój sąsiad jest prawnikiem i polecił Państwa firmę" (a referral)
- "jestem prawnikiem, potrzebuję wyceny pompy ciepła" (the sender's profession)
- "nasz prawnik prowadzi księgowość" (incidental bookkeeping)

Tightened to a general rule: a legal actor escalates only alongside an adversarial cue (court,
lawsuit, claim, damages, legal steps, pre-court demand). Unambiguous tokens are unchanged. No
case-ID or fixture-specific logic. 13 regression tests in `test_preclassifier_legal_scope.py`
(4 negatives, 8 positives, plus the pre-existing escalation test still passing).

---

## K. TESTS

| suite | result |
|---|---|
| `test_llm_stage_deadline.py` — CASE A–F fault injection + HTTP boundary | 22 passed |
| `test_daszek_dependency_degradation.py` — RT02 degradation/backoff/recovery | 9 passed |
| `test_preclassifier_legal_scope.py` — legal scope negatives/positives | 13 passed |
| `scripts/tests/test_fresh38_reuse_gate.ps1` — measurement provenance | PASS |
| **Gate A** — `python -m pytest tools/gmail_audit/tests -q` | **2444 passed, 15 skipped, 24 subtests passed, 0 failed** |

Fault injection covers: A fast success · B quick retryable failure reaching fallback · C stalled
primary bounded with fallback still served · D all providers unavailable, bounded, no infinite
retry · E deadline exhausted, fail-closed with structured provenance · F no orphan work survives
a bounded stage. Timing assertions are budget-ordering assertions, not millisecond assumptions.

Two defects were found *by* these tests rather than by inspection: the unbudgeted provider
cooldown (attempt issued with `timeout=0.0`), and the inconsistent `terminal_failure_reason` on
the router's in-loop terminal path.

---

## L. SIX-CASE LIVE PROOF

One first attempt each, `-NoReuse`, no retry-to-green. Detail in `SIX_CASE_LIVE_PROOF.md`.

```text
INT-05 OK   NEW-04 OK   FU-06 OK   SVC-04 OK   CTX-01 OK   NEW-01 OK
6/6 first-attempt valid · zero parity_error · zero INTAKE_LLM_TIMEOUT
```

Read narrowly: six cases passing once is not a reliability rate. What it establishes is negative
and specific — the mechanism that made these six fail did not recur under conditions that
previously triggered it in 6 of 38 attempts. That was the gate for spending a full run.

---

## M. POST-FIX FRESH38

New frozen SUT, new out-dir, zero reuse, all 38 run once as first attempts. Detail in
`POST_FIX_FIRST_ATTEMPT_RESULT.md`; ledger in `POST_FIX_FIRST_ATTEMPT_LEDGER.json` / `.csv`.

```text
PRE_FIX_FIRST_ATTEMPT_RELIABILITY  = 32/38 =  84.21%
POST_FIX_FIRST_ATTEMPT_RELIABILITY = 38/38 = 100.00%
```

| | PRE-FIX | POST-FIX |
|---|---|---|
| failures | 6 | **0** |
| `INTAKE_LLM_TIMEOUT` | 6 | **0** |
| the six former failures | all failed at `intake_reasoning_error` | all valid at `stage_reached = full` |

Neither number was altered by a retry. The pre-fix baseline was re-verified **after** this run —
`PRE_FIX_BASELINE_LOCK: PASS`, still `32/38`, 26 preserved files unchanged.

The most informative artifact is `NEW-05`, which fired the new `LLM_STAGE_BUDGET_FAILURE`
telemetry and still produced a valid capture. Its record shows the per-provider budget share
splitting the remainder evenly across five providers (`171960/5`, `171678/4`, `171400/3`,
`171125/2`), every failure returning in 152–282 ms, the whole chain costing 8.9 s of a 180 s
budget, and `terminal_failure_reason = provider_chain_failed` — correctly *not* a deadline
exhaustion, with 171 s still unspent. The model, the fast-fallthrough requirement and the
`a2ebeb9` labelling fix are all validated on live traffic rather than only in test doubles.

That record also exposed a real pre-existing production problem, reported not fixed: `openai_chat`
returned `quota_exhausted` and at least one of the four `GROQ_API_KEY` values is invalid
(`401 … Invalid API Key`). The repaired runtime absorbed it, but the provider pool is degraded and
should be triaged separately as a credentials/quota matter.

**Caveat:** `38/38` is one run of 38 cases on one day against a live external provider chain. It
bounds the failure rate loosely, and provider tail latency remains variable. What changed
structurally is that such latency now has coordinated retry and fallback to absorb it.

---

## N. REMAINING RUNTIME DEFECTS

**PROVEN_OPEN**

1. `central_llm_stage._call_with_retry` still uses a `ThreadPoolExecutor` whose `future.cancel()`
   cannot stop a running Anthropic request. Its budget is now correct so it can no longer preempt
   the chain, but a cancelled attempt there can still abandon one request. Unreachable in the
   current configuration (`anthropic_api_key` UNSET); removing the executor means restructuring a
   dormant provider integration — outside this task's scope. Low severity, config-gated.
2. Fresh38 runner bytes live under gitignored `.artifacts/`. Identity is tracked and enforced, but
   the bytes are not recoverable from the repo alone. Deliberate trade-off with the existing
   `.artifacts` convention; recorded rather than silently accepted.
3. The hot-sync file list is still hand-maintained. It is now fingerprinted, so a *listed* file
   that changes cannot alter the SUT without changing the manifest hash — but a product file that
   is never listed still would not be detected. Bounded improvement made (six files added, missing
   files reported); a derived list would be a larger change than this task's scope.

4. **Degraded LLM provider pool** (pre-existing, surfaced by the new telemetry, out of this
   task's scope): `openai_chat` returned `quota_exhausted` and at least one of the four
   `GROQ_API_KEY` values is rejected as invalid (`401 … Invalid API Key`). The repaired runtime
   absorbed it — `NEW-05` still produced a valid capture and the run finished 38/38 — but this is a
   live credentials/quota risk that was previously invisible. Needs operator triage, not a code
   change.

**UNKNOWN_NEEDS_PROOF**

5. The 180s stage budget is derived from the current provider chain shape
   (`http_timeout=60`, one live fallback). It has not been validated against a sustained
   multi-provider outage in production traffic, only against deterministic fault injection and one
   38-case live run.

**NONE_PROVEN** for every other path in the same-class audit; items 4, 5 and 6 of that matrix were
examined and found correctly bounded.

---

## Status

The Capability Program is **not** complete. `CAPABILITY-QUALIFICATION-20260809` remains **BLOCKED**
with an open blocker, its Phase A/B evidence committed, and Phase C / Understanding judge / v5
capability scoring **not started**. This task delivered runtime reliability repair and a post-fix
first-attempt measurement only.
