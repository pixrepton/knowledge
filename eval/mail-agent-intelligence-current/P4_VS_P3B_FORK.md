# P4 vs P3B — execution fork (frozen)

Owner: this directory. Frozen: 2026-08-19 (point 1 of 8-step capability program).

This slice records **execution order only**. It does not rewrite frozen Fresh38
27/11 evidence and does not change residual case classifications.

```text
NEXT_EXECUTION = P4
NEXT_SLICE = P4-B_SVC-05
P3B = DEFERRED_TO_STEP_5
P3B.authorized_now = false
PRODUCT_CODE_CHANGE = 1  (P4-A MI-02 understanding intent projection only)
EVALUATOR_CHANGE = 0
GT_CHANGE = 0
SCORER_CHANGE = 0
JUDGE_CHANGE = 0
OPERATOR_DECISIONS_UPDATED = NO
```

Machine-readable: `P4_VS_P3B_FORK.json` (`schema_version: p4_vs_p3b_fork.v1`).

## Why P4 first

**Fact (P3A):** INT-04, NEW-05, FU-01, MI-01 are `EVALUATOR_WRONG` on frozen
`fresh38_full_current_20260816T124100`. v5 applied the frozen contract faithfully.

**Fact (matrix):** proven current product queue is MI-02, then SVC-05 diagnosis,
then CTX-03 (design contract, RP-29). K3 cases are not a product-fix queue.

**Conclusion:** product fixes first (steps 2–4), optional P3B at step 5, then
CTX-03 / P1.4B / full Fresh38. Do not mix evaluator and product fixes in one slice.

## Eight-step sequence (operator accepted)

| Step | ID                                                    | Status                   |
| ---- | ----------------------------------------------------- | ------------------------ |
| 1    | P4 vs P3B fork freeze                                 | COMPLETE (this document) |
| 2    | P4-A MI-02 — adjudication + minimal fix candidate     | COMPLETE (f6c3b6a)       |
| 3    | P4-B SVC-05 — BR/gate diagnosis + optional fix        | PENDING                  |
| 4    | Bounded cohort re-proof (MI-02, SVC-05, INT-01 watch) | PENDING                  |
| 5    | P3B — `GT_UNANCHORED_JUDGE_DIMENSION` on +/- cohort   | DEFERRED                 |
| 6    | P4-C CTX-03 — design contract, then fix               | PENDING                  |
| 7    | P1.4B live (parallel when RC3 in scope)               | PARKED                   |
| 8    | Full Fresh38 — one qualified experiment vs 27/11      | PENDING                  |

## P3B guardrails (when step 5 opens)

- Prove general class `GT_UNANCHORED_JUDGE_DIMENSION` on positive **and** negative cohort.
- Never `if case_id == FU-01` (or any case-id exception).
- Offline rescore of frozen captures preferred; do not use new Groq recapture as the
  reason frozen 27/38 failed.

## Unchanged invariants

- Frozen baseline: 27 CLEAN_PASS / 11 CAPABILITY (v5, threshold 34).
- INT-01: `HISTORICAL_ONLY / REGRESSION_WATCH`.
- `NO_MIXED_EXPERIMENT` binds step 8.
- `OPERATOR_DECISIONS.md` not updated from this technical fork.

## STOP

P4-A MI-02 is complete: adjudicated `PRODUCT_WRONG` and the minimal fix is
implemented in gmail-agent (`P4A_MI02_ADJUDICATION_AND_FIX.md`, `f6c3b6a`).
Next slice: **P4-B SVC-05** BR/gate diagnosis + optional fix.
