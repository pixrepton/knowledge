# AI-OS Intelligence Spine Contract

Status: active contract with bounded implementation slices. Created:
2026-08-20. Current closeout writeback: 2026-08-21.

Purpose: preserve business decision semantics from BusinessReasoning through
tool execution without moving policy authority into the semantic layer.

## Core Rule

```text
Business layer says what to do and who it is for.
Policy says whether it is allowed and with what authority.
Envelope says which tools may realize that approved meaning.
Planner chooses how inside the envelope.
Execution verifies that the planner did not change the meaning.
HITL approves side effects, but does not change action target or intent.
```

## Current Flow

```text
BusinessReasoning
  -> ActionPlan
  -> Case Intelligence
  -> DecisionCandidate
  -> PolicyDecision
  -> ActionProposal v2
  -> PolicyActionEnvelopeV1
  -> effective_tools
  -> Planner
  -> Execution guard
  -> HITL
```

## Responsibility Table

| Layer | Owns | Must not own |
| --- | --- | --- |
| BusinessReasoning / Case Intelligence | Business meaning: `action_type`, target, channel, goal, missing information. | Approval, send authority, policy clearance. |
| PolicyDecision | Authority: allowed/denied, approval/HITL, dry-run/live limits, execution authority. | Rewriting customer-directed work into operator-directed work. |
| PolicyActionEnvelopeV1 | Read-only projection that combines business meaning and policy result into execution constraints. | Recomputing policy, creating new business meaning, deciding approval by semantic rule. |
| effective_tools | Physical affordance filter for tools offered to the planner. | Interpreting customer intent or weakening policy. |
| Planner | Selects one concrete tool and arguments inside the envelope. | Changing `action_type`, target, channel, or goal. |
| Execution guard | Blocks semantic/policy mismatches even if the planner returns a bad tool. | Repairing the decision silently. |
| HITL | Approves, rejects, or edits the side effect proposed by the system. | Changing the intended addressee or action semantics without a new decision. |

## Evidence Finding: allowed_tools Semantics

Current `agent_runtime.effective_tools.compute_effective_available_tools()`
filters the full `available_tools` tuple that would be sent to the planner.
Therefore `PolicyActionEnvelopeV1.allowed_tools` is currently a full planner
whitelist, not merely an action-tool whitelist.

Consequence: semantic envelopes must not narrow `allowed_tools` to a single
action tool unless it is intentional to hide every read-only helper for that
turn. The v1 pattern is:

```text
forbidden_tools: tools that cannot realize the decision meaning
allowed_tools: empty unless a full planner-turn whitelist is required
allowed_action_tools: action tools that may realize this decision meaning
```

`allowed_action_tools` is the action-only whitelist. It must not be treated as
a full planner-turn whitelist.

## Customer Missing-Data Invariant

For a business decision with:

```text
action_type = ask_for_missing_data
target = customer
channel = mail
```

the system must preserve customer-facing clarification through execution.

Allowed policy outcomes include requiring HITL or operator approval before the
message is sent. That approval comes from `PolicyDecision` and is propagated by
`PolicyActionEnvelopeV1`.

Forbidden semantic substitution:

```text
customer/mail/ask_for_missing_data
  -> request_operator_clarification
```

`request_operator_clarification` remains valid only when the missing input is
actually operator-held context or an operator decision.

## Fact-Use Contract

Case truth is `CaseContextPack.active_facts` plus
`CaseContextPack.conflicting_facts`, not message-level HVAC extraction alone.

Hybrid fact handling separates two axes:

```text
trust_state = confirmed | provisional | conflicted
decision_usable = true | false
decision_block_reason = fact_conflict | ""
```

Critical conflicts must block only actions that consume the conflicted fact.
They must not block the entire case by default.

Initial decision-critical fact keys:

- `customer_email`
- `address`
- `heated_area_m2`
- `device`
- `model`
- `service_date`
- `price`
- `amount`
- `warranty`
- `service_obligation`

Examples:

```text
heated_area_m2=180, trust_state=conflicted, decision_usable=false
```

This blocks calculations or offers that require heated area. It does not block
a customer reply that does not consume heated area, such as acknowledging
received documents.

Implemented bounded surface:

- `mailbox_memory.active_facts.annotate_decision_fact_use()`
- `mailbox_memory.active_facts.action_conflict_block()`
- `case_context_contract.build_case_context_pack_vnext()` annotates active
  facts after conflicts are finalized.

Focused proof on 2026-08-20:

- `test_slice3b_policy_execution_spine.py`
- `test_planner_execution_fidelity_01.py`
- `test_rp30_policy_enforcement.py`
- `test_active_facts_decision_usability.py`
- `test_split_conflicting_facts_tiebreak.py`
- `test_rp29_fact_supersession.py`
- `test_case_context_contract.py`
- `test_daszek_v3_operational_feed.py`

Closeout extension on 2026-08-21:

- `gmail-agent:c80be17` proves the missing consumer-side enforcement seam.
- `allowed_action_tools` mismatch is rejected by execution even when the tool is
  not globally forbidden.
- decision-safety metadata is preserved through the normalization boundaries
  needed by the actual dependent kalk/offer consumer.
- dependent kalk/offer action is blocked when it requires conflicted
  `heated_area_m2`.
- independent acknowledgement remains legal with the same conflict.
- final focused proof: `110 passed`.

## Non-Goals

- No Full Fresh38.
- No new parallel spine.
- No case-id special casing.
- No global BusinessReasoning prompt rewrite.
- No global "critical conflict blocks case" rule.
- No policy approval decision inside semantic constraints.

## CanonicalActionDecision (CAD) — Contract + First Enforced Slice (2026-08-21)

Program: `AI-OS INTELLIGENCE SPINE — CONTRACT + FIRST ENFORCED SLICE` (P0).
This section is the contract extension implemented by P0; it does not replace
the Core Rule above.

### Core invariant

```text
After CanonicalActionDecision is created for
  goal / action_type / target / channel,
no further layer may change goal, action_type, target or channel.
Downstream may execute, restrict, block, or request an explicit revision
(DecisionRevisionRequest) — it must not reinterpret the decision.
```

First enforced vertical slice:

```text
action_type = ask_for_missing_data
target      = customer
channel     = mail
```

### Lifecycle split

Two distinct mechanisms, separated by the existence of the CAD:

```text
BusinessDecisionProposal
  -> CanonicalizationFailure        # BEFORE CAD exists; no decision_id yet
  -> NEEDS_REVIEW                   # workflow state, never a new action_type

CanonicalActionDecision (FROZEN)
  -> DecisionRevisionRequest        # AFTER CAD exists; carries decision_id
  -> decision owner -> new CAD
```

- `CanonicalizationFailure` is emitted when a proposal cannot be canonicalized.
  It has `decision_state="NO_CANONICAL_DECISION"`. The workflow outcome is
  `NEEDS_REVIEW` (operational/review state). It is **never** converted into a
  different business action such as `escalate_review`.
- `DecisionRevisionRequest` is emitted when downstream discovers new evidence,
  a conflict, or an impossible precondition after the CAD was frozen. It
  references `decision_id` + `revision` and asks the decision owner for a new
  CAD. Downstream never changes target/action by itself.

### SituationUnderstanding is state, not a target owner

SituationUnderstanding states facts: customer asked X, missing_information=Y,
open_questions=Z, risks, lifecycle, evidence. It does not decide `target`.
The canonicalizer checks logical support of the proposal by the state of
things (e.g. `required_information` is a subset of `missing_information`; no
conflicted/uncertain fact is used as certainty), **not** a
`SituationUnderstanding.target == proposal.target` equality.

### BusinessDecisionProposal

New typed artifact derived from the existing BusinessReasoning result:

```text
goal, action_type, target, channel, required_information[],
confidence, reason, risk_class, proposal_id
```

`BusinessReasoningResult` itself is not extended in P0 (consumer inventory:
~80 files touch the recommendation surface; separate artifact instead).

### CanonicalActionDecision

```text
decision_id      = dec_<uuid4>            # stable across revisions
revision         = int (starts at 1)
semantic_hash    = SHA256(canonical JSON: schema_version, case_id,
                  situation_version, goal, action_type, target, channel,
                  required_information(sorted), semantic_status)
semantic_status  = FROZEN
```

`semantic_hash` excludes `created_at`, rationale text, confidence and
presentation fields. It is the basis for Semantic Conservation checks:
any downstream artifact may reference `decision_id`/`semantic_hash`; none may
change the canonical semantic signature.

### Layer re-roles (P0)

- `ActionPlan` consumes the CAD and answers "how to execute": it carries
  `canonical_decision_id` and its own execution vocabulary
  (`execution_step=prepare_reply`). It does not re-select business meaning.
- `Case Intelligence / NBA` carries `canonical_decision_id` and its own
  projection vocabulary (`case_guidance=ask_for_missing_data`); it keeps
  missing info, risks, readiness, lifecycle, open loops and evidence, but does
  not re-choose the business action after the CAD is frozen.
- Policy adds only authority: `execution_authority` (`prepare_only`),
  `approval_required`, `max_side_effect` (`local_draft`). Policy never changes
  `action_type/target/channel`.
- Safety for the planner comes from capability filtering: the envelope's
  `forbidden_tools` / `allowed_action_tools` are applied in
  `effective_tools`, so `request_operator_clarification` is **not offered**
  for frozen customer/mail actions (planner sees only `generate_draft_reply`
  as the action tool). No special-cased planner prompt path.
- Reference monitor (`graph.py`) blocks any plan that would change
  target/channel relative to the CAD (reason codes:
  `semantic_tool_forbidden_for_action_intent`,
  `canonical_semantic_drift`).

### P0 test surface

- Deterministic spine property suite
  (`test_canonical_action_decision_properties.py`): semantic conservation,
  review invariant, tool availability invariant, unsupported channel,
  forbidden tool, missing_info permutation, policy cannot retarget,
  CanonicalizationFailure -> NEEDS_REVIEW, decision_id/semantic_hash rules.
- Metamorphic LLM cohort (paraphrase, noise, prompt injection) is a separate
  P0.5 track and is not part of the deterministic gate.

### P0 closeout (2026-08-21) — semantic identity propagation + bounded proof

Delivery: `COMPLETE`. Proof: `PASS_LOCAL_BOUNDED`. Full Gate A: `PASS`
(0 failed). Semantic Conservation: `ENFORCED`. First CAD slice: `PROVEN`.
`FULL_FRESH38 = NOT_RUN`. P0.5 / P1 / P2 are **not** started (program order).

#### Semantic identity invariant (beyond canonical_decision_id)

Semantic identity of the first slice is preserved mechanically through every
downstream seam:

```text
CAD.semantic_hash
== ActionPlan.semantic_hash
== NBA.primary_next_action.semantic_hash
== APv2 raw proposal semantic_hash (lineage)
== PolicyActionEnvelopeV1.source_semantic_hash   # Policy + ToolEnvelope seam
== ToolCallPlan.semantic_hash                     # observed identity at execution
== ActionItem.source_semantic_hash                # materialized execution record
```

`source_semantic_hash` is projected from the APv2 record produced from the
CAD-driven ActionPlan; it is never recomputed downstream. The semantic hash
covers only the canonical payload (`case_id`, `situation_version`, `goal`,
`action_type`, `target`, `channel`, sorted `required_information`,
`schema_version`, `semantic_status`); it never includes transient metadata
(`created_at`, rationale, confidence, latency, provider, approval
timestamps).

Projection layers keep their own vocabulary: APv2 projects the frozen
customer/mail decision as `prepare_reply_draft` (execution vocabulary) while
`action_target=customer`, `action_channel=mail` and `source_semantic_hash`
stay frozen. Vocabulary labels are projections; the semantic signature is
the hash.

#### Runtime guard (reference monitor, fail closed)

Before an action tool executes, the reference monitor compares:

```text
expected = PolicyActionEnvelopeV1.source_semantic_hash
observed = ToolCallPlan.semantic_hash
```

- match -> consistent (existing tool-level checks still apply);
- mismatch -> DENY, `reason = canonical_semantic_drift`;
- missing observed hash -> existing correlation/forbidden-tool checks still
  apply (never a silent pass).

The planner client binds the plan to the hash of the envelope it was offered;
if the envelope changes between prompt and execution, the monitor denies.
Denial never rewrites the hash, never recomputes the decision downstream,
never substitutes a tool and never falls back to
`request_operator_clarification`.

#### Bounded runtime proof (CLOSEOUT-03)

One production-faithful trajectory through the `eval_planner_spine_handoff`
harness (no LLM call, no live send):

```text
Signal (service fault, missing diagnostic data)
-> SituationUnderstanding -> BusinessReasoning (collect_data)
-> BusinessDecisionProposal -> CanonicalActionDecision (FROZEN)
-> ActionPlan (execution_step=prepare_reply)
-> Case Intelligence / NBA (case_guidance=ask_for_missing_data)
-> DecisionCandidate -> Policy (allowed_with_review, approval required)
-> PolicyActionEnvelopeV1 (source_semantic_hash == CAD.semantic_hash)
-> effective_tools (generate_draft_reply offered;
   request_operator_clarification filtered: SEMANTIC_TOOL_FORBIDDEN)
-> Reference Monitor (consistent; canonical_semantic_drift=false)
-> generate_draft_reply (ok) -> HITL (draft_ready_for_approval)
```

Result: `action_type=ask_for_missing_data`, `target=customer`,
`channel=mail`; `canonical_decision_id` and `semantic_hash` identical at
every seam; `request_operator_clarification_executed=false`;
`live_send_executed=false`; `HITL_REQUIRED=true`.

Negative proof: a plan attempting `request_operator_clarification` against
the frozen customer/mail CAD is DENIED before execution
(`semantic_tool_forbidden_for_action_intent` +
`canonical_semantic_drift`; `hitl_gate.reason=
semantic_tool_mismatch:request_operator_clarification`).

Artifact:
`.artifacts/intelligence-spine-p0-closeout-20260821T193158/bounded-runtime-trajectory.json`.
Deterministic gates: `test_closeout_p0_bounded_runtime_slice.py` (3),
property suite (36 tests incl. closeout invariants).
