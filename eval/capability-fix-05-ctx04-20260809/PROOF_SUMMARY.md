# CAPABILITY-FIX-05 - CTX-04 Proof Summary

Verdict: EVAL_EXPECTATION_WRONG

## Mechanical Audit

| Layer | Evidence | Conclusion |
| --- | --- | --- |
| Ground truth | CTX-04 requires: budget from first message remains present in case context. | The Understanding contract is budget-context retention, not generated proposal content. |
| Captured input | `prior_context.prior_facts.budget_pln_estimated = 40000-50000`. | Budget was part of frozen case context. |
| UnderstandingOutput | Captured Understanding includes `budget_pln_estimated`, `budzet (PLN): 40000-50000`, and customer intent with budget 40-50 tys. PLN. | Product preserved the required budget context. |
| Judge prompt/rubric | Understanding judge is limited to Understanding semantic quality and must inspect the whole output. | Failing because no proposal was provided is outside Understanding scope. |
| Judge result | `essence=FAIL missing_budget_context`; `current_state_change=FAIL no_proposal_details`. | Judge result contradicts capture evidence and over-applies a proposal-output expectation. |
| Scoring rule | `v5` adjudicates only when capture proves budget context is present; absent budget remains failing. | Fix is eval-only and deterministic. |

## Focused Result

| Case | Old outcome | New outcome | Implemented fix |
| --- | --- | --- | --- |
| CTX-04 | CAPABILITY | CLEAN_PASS | `v5_budget_context_adjudication` corrects `essence` and `current_state_change` false negatives from captured Understanding evidence. |

Focused old/new proof is in `focused-proof-ctx04.json`.

## Contract Integrity

- Runtime AI-OS was not changed.
- Corpus and ground truth were not changed.
- Judge config was not changed.
- v5 manifest declares an eval-only change from v4.
- `v5` remains non-comparable with older contracts unless explicitly selected.

