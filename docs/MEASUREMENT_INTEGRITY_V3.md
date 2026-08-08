# Measurement Integrity V3 — qualification contract (offline)

Status: **active**. Last updated: 2026-08-04.  
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

Implementation: `eval_final_rescore_versioned.py`.  
Offline proofs: `tests/test_measurement_integrity_v3.py`, `tests/test_measurement_integrity_v4.py`.

**Rule:** v3/v4 manifest may change totals vs v2 — that is **measurement change, not product change** when `ground_truth_changed_from_v2` is false.

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

## Related code

| Module                             | Role                            |
| ---------------------------------- | ------------------------------- |
| `eval_measurement_scoring.py`      | deterministic component scoring |
| `eval_final_rescore.py`            | offline final-run rescoring     |
| `eval_final_rescore_versioned.py`  | v1–v4 contracts                 |
| `eval_understanding_judge.py`      | frozen semantic judge           |
| `eval_capability_batch_harness.py` | resilient per-case batch runner |
| `eval_measurement_manifest.py`     | frozen manifest builder         |
