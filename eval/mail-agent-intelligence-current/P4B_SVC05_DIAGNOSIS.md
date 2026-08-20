# P4-B SVC-05 — BR/gate diagnosis

Owner: this directory. Frozen evidence: `.artifacts/fresh38-full-current-20260816T124100`.

## Verdict

`PRIMARY_CLASS = PRODUCT_WRONG` (BusinessReasoning decision), not evaluator and
not measurement. First divergence is the DRAFT_GATE skip driven by
`recommended_next_action = escalate_review` + `reply_recommended = false`.
The fix is now implemented and runtime-proved (`0a407cb3`).

## Frozen evidence

- Input: `"Cos nie dziala, prosze o pomoc."` (ambiguous service problem).
- Ground truth: `draft_expected = true`, `escalation_expectation = propose`;
  `draft.must` = ask the customer what exactly is not working.
- Captured BusinessReasoning: `recommended_next_action = escalate_review`,
  `customer_state_guess = unclear`, `business_area = service`,
  `confidence_business = 0.3`.
- Draft gate (`draft_path_observability.evaluate_draft_gate`): `SKIP`,
  `BR_ACTION_AND_REPLY_FLAG_NOT_ELIGIBLE`.
- Downstream planner produced an internal
  `request_operator_clarification` (operator handoff), not a customer-facing
  clarifying reply. The scorer marked the draft component
  `DRAFT_GENERATION_FAILURE / reply_not_recommended`.

## Mechanism

BusinessReasoning instruction bias ("przy słabych dowodach preferuj
escalate_review") over-escalates an ambiguous service message that has no
diagnostic data, instead of recommending a bounded clarifying customer reply.
That single recommendation disables the reply drafter before it can ask the
customer "co dokładnie nie działa".

## Fix surface (implemented)

For ambiguous `service_problem` messages whose only missing data is diagnostic
specifics, `validate_business_reasoning_result` now derives a deterministic
`customer_clarification_possible` signal from the existing intake contract and
prefers `collect_data` over `escalate_review`.

The rule is general and one-directional:

- business area is `service`;
- intake review is required and carries `ambiguous_signal`;
- no forced human-review flags are present
  (`multiple_competing_signals`, `legal_or_compliance_risk`,
  `security_or_platform_risk`, `financial_document_without_payable_context`,
  `deadline_found_without_owner`);
- BusinessReasoning named concrete `missing_information`.

It does **not** key on `hvac_intent == "nieznane"`, a case id, or a global LLM
prompt. It only rewrites a conservative `escalate_review` into `collect_data`;
it can never downgrade an escalation into an unsafe live action, and it leaves
the intake `review_required` gate unchanged.

Blast radius is bounded by the negative cohort (SVC-01/SVC-02/MI-03/DEC-01
remain `escalate_review`) and by the draft-gate path (`collect_data` is allowed
under `review_required`, so the drafter runs).

## Status

Diagnosis complete and fix implemented. Post-fix runtime proof is in
`P4B_BOUNDED_COHORT_PROOF.md` and
`.artifacts/svc05-bounded-20260820/recovery-attempt-1/`.
