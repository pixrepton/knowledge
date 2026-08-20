# P4-B bounded cohort proof (runtime, current)

Owner: this directory. Runtime evidence (pre-fix): `.artifacts/fresh38-bounded-p4-20260820`
and post-fix `.artifacts/svc05-bounded-20260820`
(both RECOVERY_ATTEMPT, first-attempt evidence untouched). Provider
`deepseek-v4-flash`, SUT = current gmail-agent working tree (includes P4-A MI-02
fix `f6c3b6a` and P4-B SVC-05 fix `0a407cb3`).

## Results

| Case | Current runtime result |
| --- | --- |
| MI-02 | `current_customer_intent` now enumerates all three intents (accept offer, reschedule visit, furnace scope). Multi-intent collapse no longer reproduced. |
| SVC-05 (pre-fix) | Defect reproduced: BusinessReasoning `escalate_review` + `reply_recommended=false`; draft gate `SKIP` (`REVIEW_REQUIRED_WITHOUT_REPLY_OR_COLLECT_DATA`); `SKIPPED_PRE_DRAFTER`. |
| SVC-05 (post-fix) | `recommended_next_action=collect_data`, `reply_recommended=true`, `draft_enabled=true` (2 customer clarification drafts), draft gate `RUN` / `BR_ACTION_COLLECT_DATA`, `DRAFT_ACCEPTED`. |
| INT-01 | `DRAFT_ACCEPTED` / `BR_ACTION_COLLECT_DATA`, `draft_produced=true`. No regression. |

## MI-02 status

Runtime re-proof confirms the intent field no longer collapses to a single
state label. `P4A_PRODUCT_SHA = f6c3b6a`. Capability re-qualification still
deferred to the single qualified Fresh38.

## SVC-05 status: FIXED

The diagnosis was confirmed and the minimal fix was implemented without using
the extraction signal `hvac_intent == "nieznane"`. The deterministic
`customer_clarification_possible` signal is derived inside the BusinessReasoning
contract from existing intake fields (`service`, `ambiguous_signal`, non-empty
`missing_information`, no forced review flags). It rewrites only
`escalate_review -> collect_data` for `unclear`/`waiting_for_data` states.

Post-fix bounded cohort (`SVC-05`, `SVC-01`, `SVC-02`, `MI-03`, `DEC-01`,
`CTX-05`) all qualified 6/6, plus an additional live `NEW-05` capture:

- SVC-05: `DRAFT_ACCEPTED` / `BR_ACTION_COLLECT_DATA`.
- SVC-01/SVC-02/MI-03/DEC-01: BusinessReasoning still recommends
  `escalate_review` (negative cohort no regression).

Focused tests: 89 passed, including
`tools/gmail_audit/tests/test_svc05_customer_clarification.py`.
