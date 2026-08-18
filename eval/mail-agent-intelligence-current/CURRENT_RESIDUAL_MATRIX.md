# CURRENT_RESIDUAL_MATRIX

Canonical current accounting for the 11 Frozen Fresh38 CAPABILITY residuals.
Baseline remains `27 CLEAN_PASS / 11 CAPABILITY` from
`.artifacts/fresh38-full-current-20260816T124100` (historical labels preserved).

P2 closeout changed **current** status of INT-01 and SVC-05 only.
K3 classes are not guessed here.

| case_id | frozen_base | frozen_quality_passed | frozen_failed_component | cluster | current_classification | current_root_cause_status | fix_surface_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INT-01 | CAPABILITY | True | draft (`DRAFT_GENERATION_FAILURE` / `reply_not_recommended`) | RC4/K1 + kalk contributor (historical) | `HISTORICAL_ONLY` / `REGRESSION_WATCH` | historical residual PRESERVED; current reproduction NO; current decision chain RECOVERABLE; `DRAFT_ACCEPTED` | `CURRENT_PRODUCT_FIX = NOT_JUSTIFIED`; `ACTIVE_FIX_QUEUE = NO`; `REGRESSION_COHORT = YES` |
| SVC-05 | CAPABILITY | True | draft (`DRAFT_GENERATION_FAILURE` / `reply_not_recommended`) | RC4/K1 | `CURRENT_PRODUCT_DIAGNOSIS_PENDING` | historical residual PRESERVED; current reproduction YES; causal chain RECOVERABLE; observability blocker REMOVED; first divergence `SKIPPED_PRE_DRAFTER` / `BR_ACTION_AND_REPLY_FLAG_NOT_ELIGIBLE` | PENDING focused BR/gate adjudication; not OBSERVABILITY_BLOCKED |
| INT-04 | CLEAN_PASS | False | understanding next_step BORDERLINE | K3 | `EVALUATOR_WRONG` | P3A COMPLETE; first divergence PRODUCT vs JUDGE; GT understanding met | no product fix from this canonical failure; P3B candidate = GT-unanchored judge dimension |
| NEW-05 | CLEAN_PASS | False | understanding next_step BORDERLINE | K3 | `EVALUATOR_WRONG` | P3A COMPLETE; first divergence PRODUCT vs JUDGE; GT understanding met | canonical failure is evaluator; secondary NBA title template is not the scored GT miss |
| FU-01 | CLEAN_PASS | False | understanding gaps BORDERLINE + minor escalation | K3 | `EVALUATOR_WRONG` | P3A COMPLETE; judge fails non-material gaps; GT 120m2/Krakow met | secondary: BR escalate vs GT escalation_expectation=none |
| MI-01 | CLEAN_PASS | False | understanding gaps+risks BORDERLINE | K3 | `EVALUATOR_WRONG` | P3A COMPLETE; two-intent GT met; judge completeness-of-lists not in GT | no product fix from this canonical failure |
| INT-05 | CAPABILITY | False | base via kalk error (no quality GT) | RC3 | UNEXPECTED_TOOL_USE (eligibility; endpoint status P1.4B) | ELIGIBILITY_REMOVED (P1.4A 2026-08-18) | HANDLER/PAYLOAD DONE; LIVE P1.4B PENDING |
| DOC-02 | CAPABILITY | True | base via kalk error x2 (only failing component) | RC3 | UNEXPECTED_TOOL_USE (eligibility; endpoint status P1.4B) | ELIGIBILITY_REMOVED (P1.4A 2026-08-18) | HANDLER/PAYLOAD DONE; LIVE P1.4B PENDING |
| NEW-03 | CAPABILITY | True | base via kalk error x2 + understanding gaps secondary | RC3 | UNEXPECTED_TOOL_USE primary (eligibility; endpoint status P1.4B) | ELIGIBILITY_REMOVED (P1.4A 2026-08-18) | HANDLER/PAYLOAD DONE; LIVE P1.4B PENDING |
| CTX-03 | CAPABILITY | False | understanding contradiction (supersession hides 120 vs 160) + kalk contributor | RC2 + kalk contributor | PRODUCT_AFFECTING (semantics; kalk path ELIGIBILITY_REMOVED P1.4A) | PROVEN mechanism / DESIGN_CONTRACT_PENDING | NOT_PROVEN (RP-29 high risk) |
| MI-02 | CAPABILITY | False | understanding multi-intent collapse | RC1 | PRODUCT_AFFECTING (semantics) | STRONGLY_SUPPORTED (input 3 intents -> generic output) | NOT_PROVEN (instructions) |

Supersedes: `.artifacts/mail-agent-intelligence-20260817/CURRENT_RESIDUAL_MATRIX.csv`
which still labelled INT-01/SVC-05 as `OBSERVABILITY_BLOCKED`.
