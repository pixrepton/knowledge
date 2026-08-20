# P4-B SVC-05 — BR/gate diagnosis

Owner: this directory. Frozen evidence: `.artifacts/fresh38-full-current-20260816T124100`.

## Verdict

`PRIMARY_CLASS = PRODUCT_WRONG` (BusinessReasoning decision), not evaluator and
not measurement. First divergence is the DRAFT_GATE skip driven by
`recommended_next_action = escalate_review` + `reply_recommended = false`.

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

## Fix surface (candidate, not implemented)

For ambiguous `service_problem` messages whose only missing data is diagnostic
specifics, BusinessReasoning (or a deterministic normalize rule) should prefer a
clarifying `reply` over `escalate_review`.

Blast radius: all `service_problem` cases. This is an LLM/policy decision change
and requires a positive cohort (ambiguous service -> clarifying reply) plus a
negative cohort (genuine review/escalation cases stay escalated) before it can
be committed as product semantics. It is therefore deferred to the bounded
cohort re-proof step.

## Status

Diagnosis complete. Optional fix NOT implemented in this slice; it is a
semantic decision change pending cohort proof.
