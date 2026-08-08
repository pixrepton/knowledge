# CURRENT_CALL_PATH

```text
source signal
  → Understanding / Brain 1 (case_intelligence_result)
  → DecisionCandidate
  → PolicyDecision (policy_decision.build_policy_decision)
  → ActionProposal v2 (action_proposal_v2.build_*)
  → attach_policy_and_proposals / persist_policy_action_spine
  → project_policy_action_envelope → PolicyActionEnvelopeV1
  → agent_reconcile → agent_signal.policy_action_envelope
  → graph._ground_current_signal → EngagementSnapshotV2.policy_action_envelope
  → openai_agent_client._compact_view → planner prompt
  → ToolCallPlan (+ correlate_tool_plan IDs)
  → tool execution → HITL / ExecutionResult
```

## Fresh 38 harness (expected absence)

```text
run_recovery_pf.run_planner
  → AgentGraphEngine + subject/snippet signal
  → NO attach_policy_and_proposals
  → NO policy_action_envelope
  → correlate_tool_plan → missing_policy_envelope (36/36 full)
```

Classification: `expected_absence` when `harness_mode=true`; `wiring_failure` when Brain1 present / `policy_required` without envelope.
