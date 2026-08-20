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
| SVC-05 | CLOSED (`gmail-agent 0a407cb3`, `78603fb`, final `70c3d94`) | PRODUCT_FIX PASS; DOWNSTREAM_FIX PASS; FINAL_PROVIDER_LIVE_PROOF PASS (`.artifacts/svc05-final-live-proof-fix-20260820T113843/recovery-attempt-2`, SVC-05/SVC-02/MI-03 3/3 QUALIFIED) |
| INT-04 | EVALUATOR_FIXED (`c7eedf9`) | judge applicability focused tests |
| NEW-05 | EVALUATOR_FIXED (`c7eedf9`) | judge applicability focused tests |
| FU-01 | EVALUATOR_FIXED (`c7eedf9`) | judge applicability focused tests |
| MI-01 | EVALUATOR_FIXED (`c7eedf9`) | judge applicability focused tests |
| INT-05 | P1.4B_LIVE_PASS | live capture: no call_kalk_top |
| DOC-02 | P1.4B_LIVE_PASS | live capture: no call_kalk_top |
| NEW-03 | P1.4B_LIVE_PASS | live capture: no call_kalk_top |
| INT-01 | HISTORICAL_ONLY / REGRESSION_WATCH | watch green (`DRAFT_ACCEPTED`) |

## Remaining residuals

None. SVC-05 is closed: `PRODUCT_FIX = PASS`, `DOWNSTREAM_FIX = PASS`,
`FINAL_PROVIDER_LIVE_PROOF = PASS`. The final chain is
`collect_data -> DRAFT_ACCEPTED -> prepare_reply -> ask_for_missing_data/mail
-> generate_draft_reply -> HITL`, with no executed
`request_operator_clarification` and `operator_clarification_requested=false`.
The fix does not use `hvac_intent == "nieznane"`, a case id, or a global prompt
rewrite. CTX-03 and MI-02 are fixed in code and re-proved. Capability
re-qualification is intentionally not re-run as a full Fresh38.

## STOP

All 11 residuals are resolved or explicitly classified and SVC-05 is closed.
Do not run a full Fresh38. No next round of fixes without an operator decision.
