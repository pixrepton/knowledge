# P4-A MI-02 — multi-intent collapse adjudication + minimal fix

Owner: this directory. Frozen evidence: `.artifacts/fresh38-full-current-20260816T124100`.

## Verdict

`PRIMARY_CLASS = PRODUCT_WRONG` (understanding projection), not evaluator and not
measurement. First divergence is the `current_customer_intent` field, which collapsed
three customer intents into a single state-guess label.

## Frozen evidence

- Corpus MI-02 (`corpus-v2.json`): one message carries three intents:
  1. accept the offer,
  2. reschedule the on-site visit from Thursday to Friday,
  3. ask whether removal of the old furnace is included in the price.
- Ground truth `understanding.must` = recognize ALL three intents;
  `must_not` = serve only one or two of them.
- Captured `current_customer_intent` = `Klient odnosi sie do zlozonej oferty.`
  (one generic post-offer label). Judge `intent` dimension = `FAIL`, reason
  `missing required intent`, evidence `only one intent recognized`.
- The three intents were actually present elsewhere in the same capture
  (`open_loops`, `missing_information`), so this is a projection/synthesis
  collapse, not missing upstream recognition.

## Mechanism

`understanding_output._customer_intent_pl` falls back to the
`_CUSTOMER_STATE_INTENT_PL["post_offer"]` label when the richer business
interpretation is unavailable/empty. The explicit customer questions in
`thread_memory.unresolved_questions` (already PII-sanitized) were not considered
as a multi-intent source, so two of the three intents were dropped from the
scored intent field.

## Minimal fix (implemented)

When BusinessReasoning produced no usable interpretation and there are at least
two explicit customer questions, `_customer_intent_pl` now enumerates those
questions into `customer_intent_pl` / `current_customer_intent` instead of
collapsing to a single state label. Single-intent and ambiguous cases keep the
previous behavior.

Files:

- `gmail-agent/tools/gmail_audit/understanding_output.py`
- `gmail-agent/tools/gmail_audit/tests/test_rc_u1_intent_recommendation.py`

## Blast radius

- Localized to the operator/judge-facing intent projection; no change to
  BusinessReasoning semantics, policy, draft gate, provider selection, or case
  state.
- Only changes output when `business_interpretation` is unusable AND
  `unresolved_questions` has >= 2 items.

## Proof

- Focused RED then GREEN: `test_rc_u1_intent_recommendation.py` +
  `test_understanding_output.py` (18 passed).
- Broader focused Gate A across understanding/case-intelligence/projection
  contracts: 172 passed, 0 failed.
- Full package Gate A was attempted but did not finish in this environment
  (unrelated integration test stall); the affected deterministic surface is
  fully covered by the focused gate above.

## Accounting

- `fix_surface_status = IMPLEMENTED_IN_CODE` (focused Gate A).
- NOT re-qualified: capability re-proof is deferred to the bounded cohort
  re-proof and the single qualified Fresh38 step.

`P4A_PRODUCT_SHA = f6c3b6a0006c7185708c729d68b42ac14d3ceb79` (gmail-agent).
