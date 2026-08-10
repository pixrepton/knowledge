# POST-FIX Frozen SUT Manifest — Fresh38 after AIOS-RUNTIME-RELIABILITY-01

Frozen at: 2026-08-10T06:47:31Z
AI-OS task: `AIOS-RUNTIME-RELIABILITY-01`
Capture out-dir: `C:\top-code-session-scratch\fresh38-postfix-20260810T064731Z`

This is a **new** SUT and a **new** out-dir. Nothing is reused from the pre-fix run. The pre-fix
dataset (`knowledge/eval/fresh38-canonical-clean-20260810T011858Z`,
`PRE_FIX_FIRST_ATTEMPT_RELIABILITY = 32/38 = 84.21%`) is hash-locked and immutable; this run
cannot and must not alter it.

## Why a new manifest was required

The repair changed product runtime code (`llm_deadline.py`, `llm_provider_router.py`,
`groq_client.py`, `central_llm_stage.py`, `config.py`, `gmail_intake.py`, `signal_worker.py`,
`daszek_client.py`, `preclassifier.py`, `agent_runtime/tools/handlers.py`) and the capture
wrapper. Under the pre-fix run's own freeze rules, any such change invalidates that run and
requires a new manifest and a new out-dir from 0/38. That is exactly what this is.

## Repository state

| repo | branch | head |
|---|---|---|
| root | `repair/root-mcp-json-fix` | `da88f71e90127e9f129a3e26db0624135d9d57e4` |
| gmail-agent | `feature/aios-roadmap-1.4-2.4` | `a2ebeb96a9708d20504087ea62051cc403efc0c9` |
| knowledge | `docs/aios-residuals-wave-sync` | `687bed547c755829b397a19ee9adcbd88a66ee57` |

Unlike the pre-fix run, **every SUT component is committed**. There is no "uncommitted,
task-owned" product file in this manifest.

## Component hashes

| component | sha256 |
|---|---|
| `llm_deadline.py` *(new)* | `29d81513a8c6a64bcf6e5be7d26567b2532fa4d426308b51b13630a5e8723e28` |
| `llm_provider_router.py` | `ee55cc266d59b14f82b9d7bf2b110bdc33a95dd626710ba5831d60a6596e18c2` |
| `groq_client.py` | `026ec0b2ce3a0f4274637ded1329b97e9e160bdc075f6e22437afde3ee4516dc` |
| `central_llm_stage.py` | `81df4bb184042064cd71f6d1b93cfab02957f855361dd6679a29ebc0216e9651` |
| `config.py` | `9a1638a2a1cf65d6a9ae4e7024a9fb1767332d358e5a89c4fc14f62c52bd99e0` |
| `gmail_intake.py` | `2daa081adb7decdddbedada05b22c74c0d359f2cef862a8530c2e4b94af4ad94` |
| `signal_worker.py` | `2689e865e1bfef892b2882b83c83711c80fcadf19b8d01e089b849e4c1a8b744` |
| `daszek_client.py` | `50f05b49a2aa0c31b205fcb44511b753f28e868e2e5cf754c3c7adade2877922` |
| `preclassifier.py` | `2aae9759afcc23851d967971765cbd0ccd7a6c0ed1cb2ec3718596a728130c1e` |
| `signal_extractor.py` | `e31dddc35fccf4ae2b87029d64e11c3c57829ed06d0ba918cd6b86bef38ec5b4` |
| `agent_runtime/tools/handlers.py` | `2769e07b6e00826f54e1c7a3b67544f7ce36ec1091abeba11fda01e2498ff7c8` |
| `scripts/run_fresh38_case_batch.ps1` | `00b73c464900c910206d5190bf9c1a6f79b4345a28fafe7971464424dcdf82dd` |
| `corpus-v2.json` (capture corpus) | `6550a075d5180d492a35b983a4cdc30624756d80cc3b398ae75fa310c470c043` |
| recovery runner (canonical) | `8c2f3ddc8c5b31ecab5c0c9478485468a3945480f5c82bc0b4a65ef8f25abf13` |

Runner provenance: **VERIFIED** against the tracked pin in
`scripts/fresh38_runner_provenance.json`. The wrapper aborts the capture on mismatch, so this is
checked mechanically at every run rather than asserted here.

The machine-readable fingerprint for the run itself is `experiment-manifest.json` in the capture
out-dir; every one-CASE artifact carries a `one-<CASE>.manifest.json` sidecar bound to it.

## Runtime

```text
node_b_container   gmail-agent-nodeb-api
node_b_image       sha256:920e12797f052587889c57320252c681cd7fd7be3f14a55446bf992652fdd271
worker             gmail-agent-vps-gmail-agent-worker-1   state=running   restart_count=0
kalk-top           kalk-top-runtime (healthy)
daszek             daszek-local-wordpress + daszek-local-db  UP (restored during RT02 proof)
llm_backend        openai_chat
provider chain     openai_chat -> groq (4 keys) -> cerebras (unconfigured)
http_timeout       60      http_max_retries       4      http_retry_base_delay  2.0
LLM_STAGE_BUDGET_SEC 180   LLM_MIN_ATTEMPT_SEC    5
```

Host↔container SHA256 parity verified for all 11 changed files in **both** `gmail-agent-nodeb-api`
and the worker: **0 mismatches**.

The pre-fix manifest recorded the crash-looping worker as an unrelated pre-existing issue that was
"flagged only". It is now fixed and its restart count is part of this manifest.

## Gates

| gate | result |
|---|---|
| `GATE_A_GMAIL_AUDIT` — `python -m pytest tools/gmail_audit/tests -q` | **PASS** — 2444 passed, 15 skipped, 24 subtests passed, **0 failed** (445s) |
| `FRESH38_REUSE_GATE` — `scripts/tests/test_fresh38_reuse_gate.ps1` | **PASS**, 50.6s |
| `PRE_FIX_BASELINE_LOCK` — pre-fix dataset unchanged | **PASS** |

## Pre-run focused proof

The six cases that failed in the pre-fix run were re-run once each on this SUT, first attempt
only, no external retry, `-NoReuse`:

```text
INT-05 OK   NEW-04 OK   FU-06 OK   SVC-04 OK   CTX-01 OK   NEW-01 OK
6/6 first-attempt valid, zero parity_error, zero INTAKE_LLM_TIMEOUT
out-dir: C:\top-code-session-scratch\rt01-sixcase-proof-20260810T060646Z
```

This is **not** the canonical post-fix score. Its only purpose was to answer whether the runtime
failure class that produced the six failures had disappeared. It had.

Precisely: that proof ran on gmail-agent `8c710bb`, one commit before the SUT frozen here
(`a2ebeb9`). The difference is `a2ebeb9`, which makes `LLMRouter` label its in-loop terminal
raise with `terminal_failure_reason` as the pre-call path already did. It changes how a terminal
failure is *described*, not whether a case succeeds, and none of the six cases produced a terminal
failure. The full 38-case run below is the measurement that matters, and it runs entirely on
`a2ebeb9`.

## Amendment — why this run was restarted

A first attempt at this 38-case run was started at `06:19:43Z` and stopped at 9/38 (9 OK, 0 FAIL).
While it was in flight, printing the real `LLM_STAGE_BUDGET_FAILURE` payload — rather than
trusting the written description of it — exposed the inconsistent terminal labelling fixed in
`a2ebeb9`. The container code was frozen for the whole of that partial run, so it was internally
consistent, but its manifest would no longer have described the host SUT. For a task whose subject
is measurement integrity, that is not a number worth defending. The partial run was discarded and
this one started from 0/38 against the corrected SUT, with a new out-dir. No case from the
discarded run is reused here — `-NoReuse` and the manifest-hash gate make that mechanical rather
than a promise.

## Freeze rules for this run

1. Zero reuse of any `one-CASE.json` from any prior run — enforced mechanically by `-NoReuse`
   plus the manifest-hash reuse gate, not by convention.
2. New, empty out-dir before case 1/38.
3. No product, wrapper, runner, corpus, judge, scorer, threshold, provider-config or Docker image
   change between case 1/38 and case 38/38.
4. All 38 cases run once, as `FIRST_ATTEMPT`. No retry is permitted to alter the resulting number.
   A recovery attempt, if ever authorized, writes to `recovery-attempt-N/` and cannot overwrite
   first-attempt evidence.

`FROZEN_SUT_READY = YES`
