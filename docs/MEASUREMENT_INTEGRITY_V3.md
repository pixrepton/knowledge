# Measurement Integrity V3 — qualification contract (offline)

Status: **active**. Last updated: 2026-08-16 (added contract v5 + execution-channel L0 contract).  
Program: `AIOS-PHASE0-01` / `knowledge/docs/AI_OS_ROADMAP.md` Faza 0.1.

## Purpose

Separate **measurement** from **product** before any fresh-38 or RUN-A/B claim.

- Measurement answers: „czy capture + scorer + judge są wiarygodne?”
- Product answers: „czy system robi dobrą robotę?”

A `JUDGE_ERROR` or harness bug is **never** a capability pass.

## Primary outcomes (frozen)

| Outcome      | Meaning                                          | Counts as capability failure? |
| ------------ | ------------------------------------------------ | ----------------------------- |
| `CLEAN_PASS` | Scored components passed                         | No (success)                  |
| `CAPABILITY` | Scored component failed                          | Yes                           |
| `CAPACITY`   | Provider quota / rate limit                      | No                            |
| `DELIVERY`   | Network / timeout / unreachable dependency       | No                            |
| `HARNESS`    | Capture gap, judge unresolved, harness exception | No                            |

Implementation: `gmail-agent/tools/gmail_audit/eval_measurement_scoring.py`, `eval_final_rescore.py` (`_final_outcome`).

## JUDGE_ERROR → HARNESS (mandatory)

When Understanding judge status is `JUDGE_ERROR` or `JUDGE_UNAVAILABLE`:

- component `scored=False`
- final outcome **must** downgrade to `HARNESS`, never `CLEAN_PASS`

Proof: `tests/test_judge_error_is_not_a_pass.py`.

## Measurement contract versions

| Version | Semantics change                                  | Ground truth      |
| ------- | ------------------------------------------------- | ----------------- |
| v1      | baseline rescoring                                | corpus v1         |
| v2      | nonblocking tool-error bookkeeping                | derived corpus v2 |
| v3      | recommended draft variant + namespace diagnostics | same GT as v2     |
| v4      | ground-truth-only applicable dimensions           | same GT as v2     |
| v5      | adjudicate CTX budget-context judge false negatives when frozen capture proves budget context is present; do not require proposal details when GT only requires retained budget | same GT as v2 |

Implementation: `eval_final_rescore_versioned.py`.  
Offline proofs: `tests/test_measurement_integrity_v3.py`, `tests/test_measurement_integrity_v4.py`.

**Rule:** v3/v4 manifest may change totals vs v2 — that is **measurement change, not product change** when `ground_truth_changed_from_v2` is false.

## Execution-channel L0 contract (2026-08-16, REQUALIFIED)

The Fresh38 measurement channel requalified on `gmail-agent@37d4b37` (attempt
`fresh38_full_current_20260816T124100`, 38/38 QUALIFIED; four-case
`fresh38_fourcase_repair2_20260816T123000` 4/4 QUALIFIED). Precise causal labels — do not
collapse this into a generic "root cause" list:

- `ORIGINAL_ATTACH_COMPLETION_AUTHORITY_DEFECT = PROVEN` — the original channel treated the
  attach / docker-client process exit as the exact-Exec completion authority.
- `ATTACH_AS_EXEC_COMPLETION_AUTHORITY = INVALIDATED` — attach EOF / docker client EOF is
  **not** completion authority for the exact Exec.
- `AUTHENTICATED_CALLBACK_EOF = CANONICAL PROCESS-EXIT EDGE` — only the **authenticated
  callback EOF from the exact runner process** (token-bound socket, kernel FD close at
  `os._exit`) is the process-exit edge.
- `POST_CALLBACK_IMMEDIATE_EXECINSPECT_RACE = PROVEN` — immediately after the callback EOF the
  daemon can still reflect the exact Exec as `Running=true` (async state flip; proven CTX-04
  2026-08-12, INT-01 2026-08-16 on a healthy daemon). Terminal state is confirmed by Engine
  ExecInspect in a bounded 5 s window (re-inspect 0.5 s), fail-closed
  (`EXEC_STILL_RUNNING_AFTER_LIFECYCLE_EOF`) and the batch does not continue.
- `NPIPE_ERROR_PIPE_BUSY_231_GAP = PROVEN` — transient `ERROR_PIPE_BUSY (231)` on npipe
  `CreateFile`; bounded `WaitNamedPipe(pipe, 1000)` retry for error 231 only; other errors
  propagate (fail-closed).
- `HOST_SLEEP_ABORT_CAUSE = PROVEN_ENVIRONMENTAL` — the FU-07 17/38 abort was host sleep
  (battery critical); **NOT an L0 channel root cause**.
- `DOCKER_INTERNAL_PREMATURE_ATTACH_EOF_TRIGGER = NOT_PROVEN_AND_NOT_REQUIRED` — we do not
  claim any internal Docker cause for an early attach EOF; none is required for the fix.

Exact invariant: **authenticated callback EOF from the exact runner process = process-exit
edge. Attach EOF / docker client EOF ≠ completion authority.**

### Harness identity (Proof Integrity, canonical)

```text
PROVEN_FULL_RUN_HARNESS = 3b3041e5
FULL_RUN_QUALIFICATION = 38/38 PASS

COMMITTED_HARNESS = 035534a7…
COMMITTED_HARNESS_RELATION =
  PROVEN HARNESS + BOUNDED NPIPE EDGE-PATH HARDENING

COMMITTED_HARNESS_DETERMINISTIC_GATES = PASS
COMMITTED_HARNESS_FULL_FRESH38 = NOT_RUN_AND_NOT_REQUIRED

MEASUREMENT_CONTRACT_CHANGE = 0
COMPLETION_AUTHORITY_CHANGE = 0
QUALIFICATION_SEMANTICS_CHANGE = 0

IMPLEMENTATION_HARDENING_AFTER_FULL_PROOF = YES
```

Interpretation: the committed harness is **not byte-identical** to the harness that produced
the 38/38 qualification. The full run is bound to `3b3041e5`; the committed wrapper
`035534a7…` adds bounded handling of transient `WaitNamedPipe` raises inside the 231 retry
(edge path not exercised by the qualified capture). Measurement/completion-authority/
qualification semantics are unchanged; the hardening is proven by deterministic regression
(`pipe_busy_once`, `pipe_busy_persistent`). Do not read `MEASUREMENT_CONTRACT_CHANGE = 0` as
"the harness is byte-identical to the full run".

Forbidden to regress to: `ExecCompletionTimeoutSeconds`, sleep-before-inspect, waiting for
`exec_die` as completion (`exec_die` is evidence/parity only), retry „na wynik”.

Implementation: `scripts/run_fresh38_case_batch.ps1` — committed harness wrapper
`035534a7…` (commit `4210ed5`, workspace, LOCAL_ONLY) — see Harness identity above. Regression:
`scripts/tests/test_fresh38_engine_lifecycle_channel.ps1` (scenarios `running_then_terminal`,
`pipe_busy_once`, `pipe_busy_persistent`).

## Frozen manifest

Build with:

```powershell
cd gmail-agent/tools/gmail_audit
python eval_measurement_manifest.py `
  --corpus tests/fixtures/measurement_contract_v1/corpus-v1.json `
  --metric-definitions path/to/metric-definitions.md `
  --harness-dir . `
  --judge-dir path/to/judge `
  --out ../../../../knowledge/eval/MEASUREMENT_MANIFEST.json
```

Canonical fixture hashes: `gmail-agent/tools/gmail_audit/tests/fixtures/measurement_contract_v1/fixture-manifest.json`.

Workspace copy (operator snapshot): `knowledge/eval/MEASUREMENT_MANIFEST.json`.

## Resilient batch harness (0.3)

`eval_capability_batch_harness.py` — one case failure does not abort the batch; failures classified to `CAPACITY` / `DELIVERY` / `HARNESS`.

CLI smoke:

```powershell
python eval_capability_batch_harness.py `
  --corpus tests/fixtures/measurement_contract_v1/corpus-v1.json `
  --json-out $env:TEMP\batch-report.json `
  --allow-failures
```

## Qualification gate before Fresh 38

1. `python -m pytest tools/gmail_audit/tests/test_judge_error_is_not_a_pass.py tools/gmail_audit/tests/test_measurement_integrity_v3.py tools/gmail_audit/tests/test_eval_capability_batch_harness.py -q`
2. `python ../../../../scripts/security_closeout_audit.py` → `verdict: PASS`
3. Manifest hashes match fixture-manifest (or rebuilt manifest committed to `knowledge/eval/`)

Only then: Faza 1.1 Fresh 38.

## Anti-patterns

- Treating `JUDGE_UNAVAILABLE` as BORDERLINE capability
- Mixing pre-fix and post-fix captures in one score
- Changing ground truth between RUN-A and RUN-B
- Calling harness exceptions „model quality”
- Treating host docker client exit as the exact Exec completion authority (callback EOF is the
  exit edge; the daemon flips `Running` asynchronously)

## Related code

| Module                             | Role                            |
| ---------------------------------- | ------------------------------- |
| `eval_measurement_scoring.py`      | deterministic component scoring |
| `eval_final_rescore.py`            | offline final-run rescoring     |
| `eval_final_rescore_versioned.py`  | v1–v5 contracts                 |
| `eval_understanding_judge.py`      | frozen semantic judge           |
| `eval_capability_batch_harness.py` | resilient per-case batch runner |
| `eval_measurement_manifest.py`     | frozen manifest builder         |
