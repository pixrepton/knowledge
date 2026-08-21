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
