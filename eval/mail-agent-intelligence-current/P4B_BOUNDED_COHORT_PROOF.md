# P4-B bounded cohort proof (runtime, current)

Owner: this directory. Runtime evidence: `.artifacts/fresh38-bounded-p4-20260820`
(RECOVERY_ATTEMPT, first-attempt evidence untouched). Runner provenance verified
`454f97eb…cff90e`, provider `deepseek-v4-flash`, SUT = current gmail-agent working tree
(includes P4-A MI-02 fix `f6c3b6a`).

## Results

| Case | Current runtime result |
| --- | --- |
| MI-02 | `current_customer_intent` now enumerates all three intents (accept offer, reschedule visit, furnace scope). Multi-intent collapse no longer reproduced. |
| SVC-05 | Defect reproduced: BusinessReasoning `escalate_review` + `reply_recommended=false`; draft gate `SKIP` (`REVIEW_REQUIRED_WITHOUT_REPLY_OR_COLLECT_DATA`); `SKIPPED_PRE_DRAFTER`. |
| INT-01 | `DRAFT_ACCEPTED` / `BR_ACTION_COLLECT_DATA`, `draft_produced=true`. No regression. |

## MI-02 status

Runtime re-proof confirms the intent field no longer collapses to a single
state label. `P4A_PRODUCT_SHA = f6c3b6a`. Capability re-qualification still
deferred to the single qualified Fresh38.

## SVC-05 status: BLOCKED_DECISION

Diagnosis is confirmed (current SVC-05 still over-escalates an ambiguous
service message to operator clarification instead of a bounded customer
clarification). The operator-authorized minimal semantic fix is **not
implemented** because no narrow deterministic rule exists without unacceptable
blast radius:

- The only deterministic discriminator that isolates SVC-05 is the extraction
  signal `hvac_intent == "nieznane"` with empty `hvac_intent_raw_evidence`.
  Extraction is not part of the BusinessReasoning contract; threading it into
  that contract is a wide cross-layer signature change.
- A BusinessReasoning-only rule (`business_area == service` +
  `customer_state_guess == unclear` + `escalate_review -> reply`) would also
  convert genuine escalations: SVC-01 (GT `escalate`), SVC-02 (GT `escalate`),
  MI-03 (GT `escalate`), and DEC-01 (legal/contract escalation,
  `lane = review_direct`).
- An LLM-prompt-only change would be heuristic and broad across the service
  class, which the program forbids without a proven +/- cohort.

Per operator instruction, this slice is stopped as `BLOCKED_DECISION` rather
than expanding service policy heuristically. SVC-05 remains an active product
residual with a proven, classifiable first divergence.
