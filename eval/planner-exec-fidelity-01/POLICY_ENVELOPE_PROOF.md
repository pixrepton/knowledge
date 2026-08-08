# POLICY_ENVELOPE_PROOF

## Production

- Created: `policy_decision` + `action_proposal_v2` via `attach_policy_and_proposals`
- Persisted: `persist_policy_action_spine`
- Projected: `project_policy_action_envelope`
- Injected: `agent_reconcile.build_policy_action_envelope_handoff` → signal → snapshot
- Correlated: `correlate_tool_plan` → `policy_decision_id` / `action_proposal_id` on `ToolCallPlan`

## Absence classes (`envelope_presence.classify_envelope_presence`)

| Status | Meaning |
|---|---|
| `present_current` | usable envelope |
| `present_stale` | stale/expired proposal |
| `expected_absence` | harness / no Brain1 / not required |
| `wiring_failure` | Brain1 or `policy_required` without envelope |
| `store_unavailable` | store/API missing |

## Enforcement

When `wiring_failure` and tool ∈ `{generate_draft_reply, propose_mutation}` → fail-closed `POLICY_ENVELOPE_MISSING`.

## Fresh 38

36/36 full cases = harness `expected_absence` (measurement coverage gap), not alone proof of production wiring failure.
