# P4 final accounting — 11 CAPABILITY

Owner: this directory. Date: 2026-08-20. Method: focused/bounded proofs only.
No full Fresh38 re-run (operator decision: the frozen 27/11 baseline is kept;
each of the 11 residuals is resolved locally and re-proved narrowly).

```text
FULL_RUN_QUALIFICATION = 38/38 PASS (frozen historical baseline)
FRESH38_MEASUREMENT_PROGRAM = CLOSED
FRESH38_RERUN = NO
COMMITTED_HARNESS_FULL_FRESH38 = NOT_RUN_AND_NOT_REQUIRED
```

## Accounting

| case | resolution | proof |
| --- | --- | --- |
| MI-02 | FIXED (`f6c3b6a`) | focused Gate A + runtime re-proof (bounded) |
| CTX-03 | FIXED (`gmail-agent 7683299`, `workspace e4c41e5`) | focused facts tests + runner contract test |
| SVC-05 | KNOWN_PRODUCT_RESIDUAL / DEFERRED_CONTRACT_GAP | bounded cohort reproduction; no narrow rule |
| INT-04 | EVALUATOR_FIXED (`c7eedf9`) | judge applicability focused tests |
| NEW-05 | EVALUATOR_FIXED (`c7eedf9`) | judge applicability focused tests |
| FU-01 | EVALUATOR_FIXED (`c7eedf9`) | judge applicability focused tests |
| MI-01 | EVALUATOR_FIXED (`c7eedf9`) | judge applicability focused tests |
| INT-05 | P1.4B_LIVE_PASS | live capture: no call_kalk_top |
| DOC-02 | P1.4B_LIVE_PASS | live capture: no call_kalk_top |
| NEW-03 | P1.4B_LIVE_PASS | live capture: no call_kalk_top |
| INT-01 | HISTORICAL_ONLY / REGRESSION_WATCH | watch green (`DRAFT_ACCEPTED`) |

## Remaining residuals

- SVC-05: true product residual (BusinessReasoning over-escalates an ambiguous
  service message). `DEFERRED_CONTRACT_GAP`; not fixed without a narrow rule.
- CTX-03 and MI-02 are fixed in code and re-proved; capability re-qualification
  is intentionally not re-run as a full Fresh38.

## STOP

All 11 residuals are resolved or explicitly classified. Do not run a full
Fresh38. No next round of fixes without an operator decision.
