# WORKFLOW_GAPS.md

Canonical atomic gap count: `78`
Legacy item count: `48`

## P0

1. **gap.agent-graph-execute-run.agent-concurrency-error-swallowed-as-generic-failure**
    `status`: `confirmed_open`
    `legacy_items`: `4`
    `workflow_ids`: `AGENT-GRAPH-EXECUTE-RUN`
    `evidence_ids`: `EV-00056`, `EV-00060`, `EV-00062`
    `producer`: gmail-agent/tools/gmail_audit/agent_runtime/agent_reconcile.py:run_agent_reconcile
    `consumer`: Reconcile warning and rebuild_result classification
    `break_point`: AgentConcurrencyError is caught by a generic exception block instead of a concurrency-specific branch.
    CAS conflicts lose their semantic signal.
    Business impact: Real concurrent-write races become hard to detect and triage.

2. **gap.agent-graph-execute-run.cas-conflict-mislabeled-as-agent-dry-run**
    `status`: `confirmed_open`
    `legacy_items`: `4`
    `workflow_ids`: `AGENT-GRAPH-EXECUTE-RUN`
    `evidence_ids`: `EV-00051`, `EV-00056`
    `producer`: gmail-agent/tools/gmail_audit/agent_runtime/agent_reconcile.py:run_agent_reconcile
    `consumer`: rebuild_result.update_reasons consumers
    `break_point`: CAS-conflict failures are mapped to update_reasons agent_dry_run.
    Intentional no-op and real concurrency failure collapse to the same label.
    Business impact: Operators can misread a failing live write as an expected dry run.

3. **gap.calendar-two-worlds-of-visits.customer-proposed-date-risk-is-cli-only**
    `status`: `confirmed_open`
    `legacy_items`: `6`
    `workflow_ids`: `CALENDAR-TWO-WORLDS-OF-VISITS`
    `evidence_ids`: `EV-00080`, `EV-00082`
    `producer`: calendar_runtime.infer_calendar_risk via manual operator CLI path
    `consumer`: calendar risk reasoning in planner and operators
    `break_point`: The only richer customer_proposed_date detection path is not wired into the automatic runtime.
    Automatic flows cannot surface the no-confirmed-date risk that manual tooling can detect.
    Business impact: Scheduling risk visible to an operator tool never reaches the autonomous path.

4. **gap.calendar-two-worlds-of-visits.schedule-visit-does-not-create-real-calendar-event**
    `status`: `confirmed_open`
    `legacy_items`: `6`
    `workflow_ids`: `CALENDAR-TWO-WORLDS-OF-VISITS`
    `evidence_ids`: `EV-00080`, `EV-00082`
    `producer`: execute_schedule_visit
    `consumer`: Google Calendar and downstream scheduling truth
    `break_point`: schedule-visit writes a text fact only and never calls the real calendar executor.
    Visit scheduling has no durable calendar side effect on the live path.
    Business impact: The system can state that a visit was scheduled without creating the actual calendar event.

5. **gap.case-engagement-resolve-and-agent-handoff.case-intelligence-failure-collapses-to-empty-agent-signal**
    `status`: `confirmed_open`
    `legacy_items`: `5`
    `workflow_ids`: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
    `evidence_ids`: `EV-00047`, `EV-00054`
    `producer`: agent_reconcile Block 1 degraded handoff fields
    `consumer`: execute_agent_run signal payload
    `break_point`: Failure paths emit empty/default understanding fields without a degraded marker.
    Failure and truly empty context share the same signal shape.
    Business impact: The agent can act on blank context while appearing to see no new information.

6. **gap.case-engagement-resolve-and-agent-handoff.case-intelligence-failure-preserves-reconciled-terminal-state-without-retry**
    `status`: `confirmed_open`
    `legacy_items`: `5`
    `workflow_ids`: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
    `evidence_ids`: `EV-00054`
    `producer`: gmail-agent/tools/gmail_audit/agent_runtime/agent_reconcile.py:run_agent_reconcile
    `consumer`: Journal dedup and terminal-state readers
    `break_point`: Terminal status remains reconciled and natural reprocessing is blocked by dedup.
    The system neither escalates nor retries after hidden intelligence-stage failure.
    Business impact: A recoverable failure can become a silently durable wrong state.

7. **gap.case-engagement-resolve-and-agent-handoff.case-intelligence-stage-exceptions-are-swallowed**
    `status`: `confirmed_open`
    `legacy_items`: `5`
    `workflow_ids`: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
    `evidence_ids`: `EV-00054`
    `producer`: gmail-agent/tools/gmail_audit/agent_runtime/agent_reconcile.py:run_agent_reconcile Block 1
    `consumer`: Case intelligence handoff into agent_signal
    `break_point`: Broad exception handling converts stage failure into an empty case_intelligence_result.
    Understanding, business reasoning, and decision-pipeline failures are masked instead of surfaced.
    Business impact: The agent continues after a hidden upstream failure.

8. **gap.case-scoped-rag-vs-global-rag.query-anything-counts-source-errors-as-success**
    `status`: `confirmed_open`
    `legacy_items`: `1`
    `workflow_ids`: `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP`
    `evidence_ids`: `EV-00006`
    `producer`: gmail-agent/tools/gmail_audit/agent_runtime/tools/handlers.py:query_anything
    `consumer`: query_anything turn_summary_pl source-count summary
    `break_point`: Failed sources are excluded only when their text starts with Brak, not when they contain error text.
    The total consulted-source count includes failed branches.
    Business impact: Operator-facing and model-facing summaries overstate how much knowledge was actually consulted.

9. **gap.case-scoped-rag-vs-global-rag.query-anything-rag-branch-call-signature-broken**
    `status`: `confirmed_open`
    `legacy_items`: `1`
    `workflow_ids`: `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP`
    `evidence_ids`: `EV-00001`, `EV-00002`
    `producer`: gmail-agent/tools/gmail_audit/agent_runtime/tools/handlers.py:query_anything
    `consumer`: gmail-agent/tools/gmail_audit/mailbox_memory/protocol.py:MailboxMemoryProtocol.fetch_semantic_chunk_candidates_for_case
    `break_point`: query_anything calls the case-scoped RAG protocol with a nonexistent kwargs contract.
    The RAG branch always raises before retrieval and falls into broad error handling.
    Business impact: The agent can claim case knowledge lookup happened when it structurally could not.

10. **gap.case-scoped-rag-vs-global-rag.query-anything-returns-ok-when-all-sources-fail**
    `status`: `confirmed_open`
    `legacy_items`: `1`
    `workflow_ids`: `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP`
    `evidence_ids`: `EV-00007`
    `producer`: gmail-agent/tools/gmail_audit/agent_runtime/tools/handlers.py:query_anything
    `consumer`: Any caller reading ToolResult.status only
    `break_point`: ToolResult.status is hardcoded to ok without checking branch failures.
    Total source failure is flattened into a success-shaped tool result.
    Business impact: Downstream planning can proceed with fabricated confidence in tool success.

11. **gap.case-scoped-rag-vs-global-rag.query-anything-similar-cases-import-broken**
    `status`: `confirmed_open`
    `legacy_items`: `1`
    `workflow_ids`: `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP`
    `evidence_ids`: `EV-00003`, `EV-00004`
    `producer`: gmail-agent/tools/gmail_audit/agent_runtime/tools/handlers.py:query_anything
    `consumer`: gmail-agent/tools/gmail_audit/similar_cases_precedent.py
    `break_point`: query_anything imports find_similar_cases even though that symbol does not exist.
    The similar-cases branch always raises ImportError and never returns precedent data.
    Business impact: The agent can represent precedent lookup as available while the branch is dead.

12. **gap.daszek-feed-push-no-retry.feed-push-has-no-durable-retry**
    `status`: `confirmed_open`
    `legacy_items`: `6`
    `workflow_ids`: `DASZEK-FEED-PUSH-NO-RETRY`
    `evidence_ids`: `EV-00089`
    `producer`: best_effort_push_engagement_feed_after_hitl and feed push helpers
    `consumer`: Daszek operational feed
    `break_point`: Feed push failures are telemetry-only and not queued or retried durably.
    Feed refresh delivery is best-effort only.
    Business impact: Operator-facing state can remain stale after real backend decisions.

13. **gap.hitl-proposal-approval-dual-path.bridge-queue-send-ignores-operator-draft-payload**
    `status`: `confirmed_open`
    `legacy_items`: `11`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00158`
    `producer`: Daszek bridge_queue send row draft payload
    `consumer`: execute_hitl_send_from_bridge_row
    `break_point`: The async bridge send path also ignores the free-text operator-draft field.
    Both sync and async send variants drop the same edit channel.
    Business impact: Operators are shown an edit affordance that backend execution does not honor.

14. **gap.hitl-proposal-approval-dual-path.hitl-approve-ignores-operator-draft-payload**
    `status`: `confirmed_open`
    `legacy_items`: `11`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00158`
    `producer`: Daszek approve payload draft_pl or operator_draft_pl
    `consumer`: engagement_hitl_approve and approve_hitl_action
    `break_point`: The synchronous approve path never reads the only free-text operator-edit field found.
    Operator edits are accepted by transport and discarded by backend logic.
    Business impact: An operator can submit a correction that never reaches the outgoing email.

15. **gap.hitl-proposal-approval-dual-path.hitl-gmail-decision-status-does-not-distinguish-dry-run-from-live**
    `status`: `confirmed_open`
    `legacy_items`: `3`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00014`
    `producer`: gmail-agent/tools/gmail_audit/hitl_gmail_send.py:execute_hitl_gmail_send
    `consumer`: Downstream readers trusting decision_status only
    `break_point`: decision_status stays executed in both dry-run and live send branches.
    The status contract does not encode whether the side effect was simulated or real.
    Business impact: A dry run can be interpreted as production delivery.

16. **gap.hitl-proposal-approval-dual-path.hitl-gmail-dry-run-reports-executed-true**
    `status`: `confirmed_open`
    `legacy_items`: `3`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00013`
    `producer`: gmail-agent/tools/gmail_audit/hitl_gmail_send.py:execute_hitl_gmail_send
    `consumer`: HITL approval callers reading executed or effect_started
    `break_point`: Missing gmail.send scope returns executed true in bounded_dry_run.
    No-send branches produce a send-success shaped result.
    Business impact: Operators and downstream code can believe an email was sent when it was not.

17. **gap.hitl-proposal-approval-dual-path.materialize-idempotency-enforced-only-for-composite-plan**
    `status`: `confirmed_open`
    `legacy_items`: `10`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00143`
    `producer`: materialize_bridge.with_idempotency and WRITE_EXECUTORS dispatch
    `consumer`: create_case, link_existing, create_artifact, defer_operator proposal types
    `break_point`: Real idempotency enforcement exists only on the composite_plan branch.
    Four proposal types advertise a protection they do not actually receive.
    Business impact: Operators can trust a false duplicate-execution safety guarantee on write paths.

18. **gap.hitl-proposal-approval-dual-path.materialize-idempotency-records-only-ok-results**
    `status`: `confirmed_open`
    `legacy_items`: `10`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00143`
    `producer`: materialize idempotency record path
    `consumer`: Future duplicate attempts
    `break_point`: A side effect that succeeded under non-ok status is never recorded for idempotency.
    Non-ok partial successes remain rerunnable.
    Business impact: Duplicate materialization remains possible even when part of the write already happened.

19. **gap.hitl-proposal-approval-dual-path.materialize-idempotency-wrapper-silently-noops-without-db-url**
    `status`: `confirmed_open`
    `legacy_items`: `10`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00143`
    `producer`: materialize idempotency wrapper
    `consumer`: Any environment lacking db_url
    `break_point`: The wrapper silently stops enforcing idempotency when db_url is absent.
    Runtime protection can disappear by configuration without a surfaced error.
    Business impact: A safety contract can silently downgrade in an operator-invisible way.

20. **gap.hitl-proposal-approval-dual-path.materialize-path-lacks-durable-effect-receipt-before-post-effect-failures**
    `status`: `confirmed_open`
    `legacy_items`: `9`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00144`
    `producer`: materialize approval flow
    `consumer`: Retry, dedup, and audit layers
    `break_point`: No durable effect receipt is written before best-effort event emission and snapshot save.
    Partial successes cannot be authoritatively recognized on retry.
    Business impact: Operators lack a trustworthy receipt proving whether the side effect already happened.

21. **gap.hitl-proposal-approval-dual-path.materialize-post-effect-errors-leave-proposal-pending-and-rerunnable**
    `status`: `confirmed_open`
    `legacy_items`: `9`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00144`
    `producer`: materialize_bridge.approve_materialize_proposal post-effect CAS loop
    `consumer`: Re-approval guard status != pending
    `break_point`: Post-effect conflict or save failures return error before the pending proposal is patched.
    The same proposal can be reapproved and re-executed after a partial success.
    Business impact: Duplicate durable mutations become operator-triggerable.

22. **gap.hitl-proposal-approval-dual-path.materialize-side-effect-runs-before-approval-persistence**
    `status`: `confirmed_open`
    `legacy_items`: `9`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00144`
    `producer`: materialize_bridge.approve_materialize_proposal
    `consumer`: snapshot proposal state and idempotency guard
    `break_point`: execute_materialize_proposal mutates durable state before proposal approval is persisted.
    Durable side effects and proposal status can diverge on the same approval attempt.
    Business impact: Real case mutations can happen while the UI still shows a pending approval.

23. **gap.learning-loop-divergence-to-candidate-evidence-only.approved-learning-rules-affect-only-conditional-precedent-enrichment**
    `status`: `confirmed_open`
    `legacy_items`: `7`
    `workflow_ids`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
    `evidence_ids`: `EV-00108`, `EV-00181`
    `producer`: divergence_loop.fetch_approved_rules_for_family
    `consumer`: mailbox_memory_runtime.fetch_similar_case_precedent_refs_v1
    `break_point`: Approved rules feed only a conditional precedent-enrichment reader, not primary planning or policy control.
    The loop closes only as optional context enrichment.
    Business impact: Approved learning does not materially steer first-order behavior.

24. **gap.learning-loop-divergence-to-candidate-evidence-only.auto-approve-bypasses-confidence-threshold-on-observation-volume**
    `status`: `confirmed_open`
    `legacy_items`: `7`
    `workflow_ids`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
    `evidence_ids`: `EV-00107`
    `producer`: maybe_create_learning_candidate auto-approve logic
    `consumer`: learning_rule_candidates approval status
    `break_point`: One auto-approve branch checks parent observation volume only and skips confidence gating.
    Rules can be auto-approved without confidence evidence.
    Business impact: Incorrect rules can acquire approved status and later influence precedent selection.

25. **gap.learning-loop-divergence-to-candidate-evidence-only.business-outcome-capture-missing**
    `status`: `confirmed_open`
    `legacy_items`: `7`
    `workflow_ids`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
    `evidence_ids`: `EV-00109`
    `producer`: Production outcome pipeline
    `consumer`: Learning-loop later-outcome feedback
    `break_point`: No owner or runtime capture exists for sale value, margin, or win-loss business outcomes.
    The learning loop cannot correlate proposals with real commercial results.
    Business impact: The system cannot learn from actual business success or failure.

26. **gap.learning-loop-divergence-to-candidate-evidence-only.classify-operator-response-misclassifies-approve-when-proposal-type-missing**
    `status`: `confirmed_open`
    `legacy_items`: `2`
    `workflow_ids`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
    `evidence_ids`: `EV-00012`
    `producer`: gmail-agent/tools/gmail_audit/divergence_loop.py:classify_operator_response
    `consumer`: learning_rule_candidates writer path
    `break_point`: Missing proposal_type falls through to RESPONSE_DIVERGENT_ACTION instead of approve-match handling.
    Genuine approves can be recorded as divergence.
    Business impact: The learning loop can manufacture false disagreement from correct operator behavior.

27. **gap.learning-loop-divergence-to-candidate-evidence-only.fetch-open-proposals-uses-tuple-rows**
    `status`: `confirmed_open`
    `legacy_items`: `2`
    `workflow_ids`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
    `evidence_ids`: `EV-00008`, `EV-00010`, `EV-00011`
    `producer`: divergence_loop.fetch_open_proposals_for_case and api_app learning DB helpers
    `consumer`: divergence_loop._row_to_proposal
    `break_point`: Real call sites open psycopg connections without dict_row or equivalent row factory.
    Proposal rows arrive as tuples instead of the dict-like shape expected by downstream normalization.
    Business impact: Operator feedback used for learning starts from malformed source rows.

28. **gap.learning-loop-divergence-to-candidate-evidence-only.get-win-rate-uses-nonexistent-won-status**
    `status`: `confirmed_open`
    `legacy_items`: `8`
    `workflow_ids`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
    `evidence_ids`: `EV-00132`, `EV-00136`
    `producer`: business tool get_win_rate
    `consumer`: Any operator or agent flow reading rate_pct
    `break_point`: The tool counts won instead of completed in the real case lifecycle enum.
    Win-rate numerator is structurally zero or near zero.
    Business impact: Business-performance reporting can be fabricated downward while looking plausible.

29. **gap.learning-loop-divergence-to-candidate-evidence-only.revenue-forecast-consumes-broken-win-rate**
    `status`: `confirmed_open`
    `legacy_items`: `8`
    `workflow_ids`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
    `evidence_ids`: `EV-00136`, `EV-00164`
    `producer`: business_pulse.py:get_revenue_forecast
    `consumer`: Revenue forecast readers
    `break_point`: Revenue forecast multiplies pipeline value by the broken get_win_rate result.
    The downstream forecast inherits the same contract drift instead of rejecting degraded inputs.
    Business impact: Revenue forecast can be understated as confidently as the upstream win-rate defect.

30. **gap.learning-loop-divergence-to-candidate-evidence-only.row-to-proposal-drops-fields-on-tuple-rows**
    `status`: `confirmed_open`
    `legacy_items`: `2`
    `workflow_ids`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
    `evidence_ids`: `EV-00009`
    `producer`: gmail-agent/tools/gmail_audit/divergence_loop.py:_row_to_proposal
    `consumer`: gmail-agent/tools/gmail_audit/divergence_loop.py:classify_operator_response
    `break_point`: _row_to_proposal keeps only proposal_id when the row is not dict-shaped.
    proposal_type and other discriminating fields are silently discarded.
    Business impact: Later learning classification operates on a lossy record instead of the real operator action context.

## P1

1. **gap.agent-graph-turn-loop.extract-facts-from-text-cannot-update-existing-fact-value**
    `status`: `confirmed_risk`
    `legacy_items`: `33`
    `workflow_ids`: `AGENT-GRAPH-TURN-LOOP`, `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
    `evidence_ids`: `EV-00180`
    `producer`: extract_facts_from_text tool via append_fact_rows
    `consumer`: Fact store rows keyed by fact_id
    `break_point`: Deterministic fact_id plus ON CONFLICT DO NOTHING prevents updates to an existing case and key pair.
    Later corrections silently no-op while the tool reports success.
    Business impact: Customer corrections can fail to supersede stale extracted facts.

2. **gap.agent-graph-turn-loop.preplan-subagent-selection-cannot-activate-document-or-draft-scopes**
    `status`: `confirmed_risk`
    `legacy_items`: `25`
    `workflow_ids`: `AGENT-GRAPH-TURN-LOOP`
    `evidence_ids`: `EV-00140`
    `producer`: graph.py select_sub_agent pre-planning call
    `consumer`: TOOL_SCOPE_MAP narrowing for document and draft scopes
    `break_point`: The pre-planning call passes an empty tool_name, so only general or policy can be returned.
    Two specialist scope branches never constrain planner offer sets.
    Business impact: Tool-choice narrowing is weaker than the architecture suggests for document and draft work.

3. **gap.agent-graph-turn-loop.request-human-handoff-handler-has-no-exposed-schema-or-caller**
    `status`: `confirmed_risk`
    `legacy_items`: `30`
    `workflow_ids`: `AGENT-GRAPH-TURN-LOOP`
    `evidence_ids`: `EV-00177`
    `producer`: agent_runtime/tools/handlers.py:request_human_handoff
    `consumer`: openai_tool_definitions and any direct caller
    `break_point`: The handler is registered but absent from tool_schemas specs and from any direct invocation.
    The handoff capability is live code with no reachable entrypoint.
    Business impact: The agent cannot intentionally invoke the human handoff tool even though the handler works.

4. **gap.agent-graph-turn-loop.semantic-policy-divergence-is-observed-but-never-enforced**
    `status`: `confirmed_risk`
    `legacy_items`: `26`
    `workflow_ids`: `AGENT-GRAPH-TURN-LOOP`
    `evidence_ids`: `EV-00141`
    `producer`: _observe_policy_plan
    `consumer`: Any branch that could block, correct, or escalate divergence
    `break_point`: Divergence metrics are written as telemetry only and never consulted for control.
    Planner and policy can disagree without a corrective action.
    Business impact: The system measures divergence but allows it to continue unchecked.

5. **gap.calendar-two-worlds-of-visits.calendar-signal-source-kind-does-not-match-registered-handler**
    `status`: `confirmed_risk`
    `legacy_items`: `24`
    `workflow_ids`: `CALENDAR-TWO-WORLDS-OF-VISITS`
    `evidence_ids`: `EV-00137`
    `producer`: build_calendar_signal
    `consumer`: SIGNAL_HANDLERS calendar dispatch
    `break_point`: Producer emits google_calendar while the registry exposes calendar.
    The substantial calendar reconcile handler is unreachable for signals emitted by this producer.
    Business impact: Recovery or replay paths can fail to route calendar signals correctly.

6. **gap.calendar-two-worlds-of-visits.create-calendar-event-action-proposal-has-no-producer**
    `status`: `confirmed_risk`
    `legacy_items`: `22`
    `workflow_ids`: `CALENDAR-TWO-WORLDS-OF-VISITS`
    `evidence_ids`: `EV-00131`
    `producer`: build_calendar_event_action_proposal
    `consumer`: execution_runtime.execute_action_proposal calendar-event executor
    `break_point`: The calendar-event proposal builder has zero callers in gmail-agent.
    A real executor exists behind a permanently uncreated proposal shape.
    Business impact: Calendar event creation capability is unavailable in practice despite existing execution code.

7. **gap.calendar-two-worlds-of-visits.visit-cancel-flow-has-no-confirmed-implementation**
    `status`: `confirmed_risk`
    `legacy_items`: `22`
    `workflow_ids`: `CALENDAR-TWO-WORLDS-OF-VISITS`
    `evidence_ids`: `EV-00131`
    `producer`: Visit cancellation intent
    `consumer`: Calendar runtime and proposal lifecycle
    `break_point`: No cancel creator or executor path was confirmed by exhaustive search.
    Cancellation is absent as a first-class workflow.
    Business impact: Cancelled visits can drift from calendar truth unless handled manually.

8. **gap.calendar-two-worlds-of-visits.visit-reschedule-flow-has-no-confirmed-implementation**
    `status`: `confirmed_risk`
    `legacy_items`: `22`
    `workflow_ids`: `CALENDAR-TWO-WORLDS-OF-VISITS`
    `evidence_ids`: `EV-00131`
    `producer`: Visit reschedule intent
    `consumer`: Calendar runtime and proposal lifecycle
    `break_point`: No reschedule creator or executor path was confirmed by exhaustive search.
    Reschedule is absent as a first-class workflow.
    Business impact: Date-change handling relies on manual work or unsupported paths.

9. **gap.case-engagement-resolve-and-agent-handoff.action-planning-precedes-full-understanding**
    `status`: `confirmed_risk`
    `legacy_items`: `18`
    `workflow_ids`: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
    `evidence_ids`: `EV-00066`, `EV-00067`
    `producer`: run_shared_downstream_stages stage ordering
    `consumer`: draft_reply and plan_actions
    `break_point`: Draft and action planning execute before the full understanding stage completes.
    Planning decisions are made on a pre-understanding intermediate state.
    Business impact: Action selection can be weaker than the best understanding the system later computes.

10. **gap.case-engagement-resolve-and-agent-handoff.finalize-case-persists-state-in-nontransactional-multiwrite-sequence**
    `status`: `confirmed_risk`
    `legacy_items`: `21`
    `workflow_ids`: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
    `evidence_ids`: `EV-00127`
    `producer`: finalize_case
    `consumer`: Thread memory, next action, and event log readers
    `break_point`: finalize_case persists related state through three independent store commits.
    Mid-sequence failure can leave partially updated case state without rollback.
    Business impact: Operators and downstream workers can observe mutually inconsistent case projections.

11. **gap.case-engagement-resolve-and-agent-handoff.threadpool-executor-is-serialized-by-immediate-result-awaits**
    `status`: `confirmed_risk`
    `legacy_items`: `17`
    `workflow_ids`: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
    `evidence_ids`: `EV-00068`
    `producer`: intake_shared_downstream.run_shared_downstream_stages
    `consumer`: Case intelligence latency
    `break_point`: Each submitted future is awaited before the next stage is even submitted.
    ThreadPoolExecutor adds complexity without delivering real concurrency.
    Business impact: Turn latency stays higher than the concurrency-oriented structure implies.

12. **gap.case-scoped-rag-vs-global-rag.gmail-agent-has-no-runtime-consumer-for-company-rag-service**
    `status`: `confirmed_risk`
    `legacy_items`: `14`
    `workflow_ids`: `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP`
    `evidence_ids`: `EV-00078`, `EV-00079`
    `producer`: rag-chat-asystent retrieval service
    `consumer`: gmail-agent agent runtime
    `break_point`: gmail-agent exposes only static local company text and has no HTTP client to the live RAG service.
    The global company-knowledge retrieval pipeline is unreachable from agent runtime.
    Business impact: The agent cannot use the richer company knowledge that the WordPress surface can reach.

13. **gap.daszek-command-outbox-drain.bridge-queue-failed-rows-become-operator-invisible**
    `status`: `confirmed_risk`
    `legacy_items`: `28`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`, `DASZEK-COMMAND-OUTBOX-DRAIN`
    `evidence_ids`: `EV-00164`, `EV-00165`
    `producer`: daszek_v2_bridge_queue_completion_ids and summary endpoints
    `consumer`: Operator queue summary and pending-row views
    `break_point`: Failed rows are treated as terminal like success and are excluded from all surfaced dashboard counts.
    Failure state exists in storage but has no operator-visible query surface.
    Business impact: Operators cannot distinguish a dropped failed action from a successful completion.

14. **gap.daszek-command-outbox-drain.db-command-outbox-has-no-confirmed-live-producer**
    `status`: `confirmed_risk`
    `legacy_items`: `20`
    `workflow_ids`: `DASZEK-COMMAND-OUTBOX-DRAIN`
    `evidence_ids`: `EV-00116`
    `producer`: daszek_command_outbox_enqueue
    `consumer`: wp_daszek_command_outbox claim or lease mechanics
    `break_point`: The DB-backed outbox has no confirmed live caller beyond a one-time migration helper.
    A more durable command transport exists but appears unfed in normal operation.
    Business impact: Operational resilience is weaker than the dormant mechanism suggests.

15. **gap.daszek-command-outbox-drain.live-bridge-command-flow-still-depends-on-jsonl-queue**
    `status`: `confirmed_risk`
    `legacy_items`: `20`
    `workflow_ids`: `DASZEK-COMMAND-OUTBOX-DRAIN`
    `evidence_ids`: `EV-00117`
    `producer`: daszek_v2_append_jsonl_store bridge_queue writers
    `consumer`: gmail-agent daszek_bridge_queue_drain
    `break_point`: The live Daszek to NodeB command path still runs through bridge_queue.jsonl rather than the DB outbox.
    Active traffic uses the weaker legacy queue shape.
    Business impact: Failed commands inherit file-queue durability and visibility limits instead of the stronger outbox design.

16. **gap.gmail-signal-worker-loop.shared-mailbox-polled-by-two-independent-workers**
    `status`: `confirmed_risk`
    `legacy_items`: `15`
    `workflow_ids`: `GMAIL-SIGNAL-WORKER-LOOP`, `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`
    `evidence_ids`: `EV-00170`
    `producer`: gmail-agent poller and cieplo-orchestrator poller
    `consumer`: Shared biuro.topinstal@gmail.com mailbox intake
    `break_point`: Two independent workers are intentionally configured against the same live mailbox account.
    Mailbox-level separation is handled by conventions and filters rather than isolated inboxes.
    Business impact: Duplicate or competing intake becomes a structural risk surface.

17. **gap.hitl-proposal-approval-dual-path.bridge-queue-failures-have-no-retry-or-dead-letter**
    `status`: `confirmed_risk`
    `legacy_items`: `28`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`, `DASZEK-COMMAND-OUTBOX-DRAIN`
    `evidence_ids`: `EV-00165`
    `producer`: gmail-agent drain_bridge_rows
    `consumer`: Failed bridge_queue rows
    `break_point`: Exceptions are terminalized in one completion call with no attempt counter, requeue, or dead-letter.
    One transient bridge failure permanently ends row processing.
    Business impact: A send or decision action can fail once and never be retried.

18. **gap.hitl-proposal-approval-dual-path.hitl-clarification-approval-contract-lacks-answer-payload-channel**
    `status`: `confirmed_risk`
    `legacy_items`: `12`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00148`
    `producer`: request_operator_clarification and /hitl/approve contract
    `consumer`: Next agent turn expecting clarification content
    `break_point`: Approval accepts action_id and operator_id only and has no explicit answer payload channel.
    Clarification resolution depends on some other ingress mechanism instead of the approve contract itself.
    Business impact: A blocker marked as clarification-required has no first-class way to receive the answer through the same workflow.

19. **gap.hitl-proposal-approval-dual-path.materialize-create-artifact-has-no-confirmed-creator**
    `status`: `confirmed_risk`
    `legacy_items`: `32`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00179`
    `producer`: Proposal creator for proposal_type create_artifact
    `consumer`: execute_materialize_proposal create_artifact branch
    `break_point`: Executor branch exists but no live creator for create_artifact was confirmed.
    Artifact materialization is validator-ready and executor-ready but producer-missing.
    Business impact: Operators cannot reach a nominally supported artifact creation workflow.

20. **gap.hitl-proposal-approval-dual-path.materialize-create-case-has-no-confirmed-creator**
    `status`: `confirmed_risk`
    `legacy_items`: `32`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00179`
    `producer`: Proposal creator for proposal_type create_case
    `consumer`: execute_materialize_proposal create_case branch
    `break_point`: Executor branch exists but no live creator for create_case was confirmed.
    A first-class proposal type is only executor-deep, not producible.
    Business impact: Case creation must occur through other paths instead of this approval model.

21. **gap.hitl-proposal-approval-dual-path.materialize-defer-operator-has-no-confirmed-creator**
    `status`: `confirmed_risk`
    `legacy_items`: `32`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00179`
    `producer`: Proposal creator for proposal_type defer_operator
    `consumer`: execute_materialize_proposal defer_operator branch
    `break_point`: Executor branch exists but no live creator for defer_operator was confirmed.
    The defer-operator proposal type is schema-valid but unproducible.
    Business impact: A supposedly supported operator deferral path is unreachable in practice.

22. **gap.hitl-proposal-approval-dual-path.materialize-link-existing-has-no-confirmed-creator**
    `status`: `confirmed_risk`
    `legacy_items`: `32`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00179`
    `producer`: Proposal creator for proposal_type link_existing
    `consumer`: execute_materialize_proposal link_existing branch
    `break_point`: Executor branch exists but no live creator for link_existing was confirmed.
    A supported proposal type is structurally uncreatable.
    Business impact: Intended link-existing automation remains unavailable despite executor support.

23. **gap.hitl-proposal-approval-dual-path.proposal-execution-lifecycle-fragmentation-persists**
    `status`: `confirmed_risk`
    `legacy_items`: `16`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00074`, `EV-00075`, `EV-00076`, `EV-00110`, `EV-00111`
    `producer`: action_proposals_v2, materialize proposals, execution_runtime.ActionProposal
    `consumer`: Approval, execution, and recovery layers
    `break_point`: Multiple lifecycle shapes coexist with only partial convergence.
    Tooling and recovery logic must reason about several incompatible proposal contracts.
    Business impact: Operational behavior varies by lifecycle implementation instead of one stable approval model.

24. **gap.hitl-proposal-approval-dual-path.proposal-execution-restart-recovery-is-inconsistent-across-lifecycles**
    `status`: `confirmed_risk`
    `legacy_items`: `13`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00144`, `EV-00149`, `EV-00150`
    `producer`: Three coexisting proposal and execution result shapes
    `consumer`: Restart recovery and duplicate-call handling across approval flows
    `break_point`: Materialize, Gmail-send, and ExecutionResult paths implement different durability and restart guarantees.
    Restart semantics are a shape-specific property instead of a system contract.
    Business impact: Similar operator actions can recover safely or unsafely depending on which lifecycle shape they happen to use.

25. **gap.hitl-proposal-approval-dual-path.reconcile-warnings-reach-rest-response-but-have-no-ui-consumer**
    `status`: `confirmed_risk`
    `legacy_items`: `27`
    `workflow_ids`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
    `evidence_ids`: `EV-00163`
    `producer`: materialize approve API response reconcile.warnings
    `consumer`: daszek/public/app.js approveProposalViaApi or decideActionProposal
    `break_point`: The browser receives reconcile warnings but frontend code never reads them.
    Backend warnings are projected through transport and then silently dropped at UI.
    Business impact: Operators do not see important reconcile caveats after materialize approval.

26. **gap.kalk-top-calculate-offer-pipeline.call-kalk-top-quote-schema-advertises-ignored-arguments**
    `status`: `confirmed_risk`
    `legacy_items`: `31`
    `workflow_ids`: `KALK-TOP-CALCULATE-OFFER-PIPELINE`, `AGENT-GRAPH-TURN-LOOP`
    `evidence_ids`: `EV-00177`
    `producer`: call_kalk_top_quote schema
    `consumer`: call_kalk_top_quote handler
    `break_point`: Three declared tool arguments are ignored because the handler builds the request from snapshot only.
    OpenAI tool schema and runtime behavior diverge.
    Business impact: The LLM can reason over controls it does not actually possess.

27. **gap.learning-loop-divergence-to-candidate-evidence-only.world-model-producer-pipeline-has-no-callers**
    `status`: `confirmed_risk`
    `legacy_items`: `29`
    `workflow_ids`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
    `evidence_ids`: `EV-00176`, `EV-00181`
    `producer`: world_model ingest, distill, fetch, and update producer-side functions
    `consumer`: world_model_insights reader chain
    `break_point`: Reader path exists, but no caller builds or updates the corpus and insight tables it expects.
    world_model is producer-unwired instead of consumer-orphaned.
    Business impact: Historical learning insights are effectively absent despite a conditional reader path.

28. **gap.sla-watcher-decision-escalation.sla-watcher-has-no-confirmed-automatic-trigger**
    `status`: `confirmed_risk`
    `legacy_items`: `23`
    `workflow_ids`: `SLA-WATCHER-DECISION-ESCALATION`
    `evidence_ids`: `EV-00130`
    `producer`: sla_watcher.py
    `consumer`: Time-based escalation os_events
    `break_point`: Only a manual CLI caller was found despite the module docstring describing automatic scheduling.
    A correct escalation mechanism is dormant unless a human explicitly runs it.
    Business impact: Slow operator responses may never auto-escalate in live operation.

29. **gap.top-instal-generator-offer-document.document-converter-path-has-two-live-modes**
    `status`: `confirmed_risk`
    `legacy_items`: `19`
    `workflow_ids`: `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`
    `evidence_ids`: `EV-00101`
    `producer`: top-instal-generator converter dispatch
    `consumer`: Downstream document-format assumptions
    `break_point`: gotenberg and fallback-docx are both live terminal paths for one generation request.
    Conversion success and fallback delivery share the same high-level workflow.
    Business impact: Consumers need to inspect converter metadata instead of assuming one canonical output.

30. **gap.top-instal-generator-offer-document.legacy-direct-config-generation-path-remains-live**
    `status`: `confirmed_risk`
    `legacy_items`: `19`
    `workflow_ids`: `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`
    `evidence_ids`: `EV-00101`
    `producer`: TopInstal_GenerateOfferDocument_UseCase mode selection
    `consumer`: Document generation callers
    `break_point`: direct-config legacy mode remains live beside from-offer-dto.
    Two input contracts must be kept coherent for one document workflow.
    Business impact: Generator behavior can vary based on legacy adapter path instead of one canonical input.

## P2

1. **gap.agent-graph-turn-loop.action-dictionary-resolution-docs-conflict-and-adjudication-incomplete**
    `status`: `needs_adjudication`
    `legacy_items`: `35`
    `workflow_ids`: `AGENT-GRAPH-TURN-LOOP`
    `evidence_ids`: `EV-00069`, `EV-00070`
    `producer`: ARCHITECTURE_DECISIONS.md and brief.md action-dictionary claims
    `consumer`: Architecture readers and future maintainers
    `break_point`: Current documentation disagrees on whether action-dictionary convergence fully resolves the older concern.
    The code partially supports one document but final adjudication is not locked.
    Business impact: Subsequent changes can optimize against contradictory architecture guidance.

2. **gap.calendar-two-worlds-of-visits.calendar-risk-has-three-independent-implementations**
    `status`: `confirmed_inconsistency`
    `legacy_items`: `34`
    `workflow_ids`: `CALENDAR-TWO-WORLDS-OF-VISITS`
    `evidence_ids`: `EV-00016`, `EV-00036`, `EV-00037`
    `producer`: calendar_runtime.py, mailbox_memory_runtime.py, gmail_intake.py
    `consumer`: Planner and context-pack calendar risk readers
    `break_point`: Three separate implementations compute calendar_risk with different expressive power.
    Richer risk states exist only in one path while live paths emit binary states.
    Business impact: Scheduling behavior depends on which implementation produced the risk field.

3. **gap.case-engagement-resolve-and-agent-handoff.agent-runtime-enabled-branch-depends-on-loader-order**
    `status`: `confirmed_inconsistency`
    `legacy_items`: `45`
    `workflow_ids`: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`, `DASZEK-FEED-PUSH-NO-RETRY`
    `evidence_ids`: `EV-00184`
    `producer`: config.load_settings and load_agent_runtime_settings
    `consumer`: agent_runtime_reconcile_active and engagement_feed_source_enabled
    `break_point`: One settings loader mutates os.environ while the other reads raw env directly.
    Effective runtime branch selection depends on call order inside one process.
    Business impact: The same workspace can choose different agent or feed branches without any config file change.

4. **gap.cieplo-orchestrator-intake-to-review-email.cieplo-treats-docx-fallback-as-pdf-ready**
    `status`: `confirmed_inconsistency`
    `legacy_items`: `46`
    `workflow_ids`: `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`, `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`
    `evidence_ids`: `EV-00186`
    `producer`: top-instal-generator fallback-docx response
    `consumer`: cieplo-orchestrator workflow runner
    `break_point`: cieplo-orchestrator stores the URL into pdf_download_url and advances to PDF_READY without checking format metadata.
    Consumer state machine overstates document readiness after degraded conversion.
    Business impact: Internal review flow can claim PDF readiness while only a DOCX fallback exists.

5. **gap.cieplo-orchestrator-intake-to-review-email.failed-final-state-name-overstates-recoverability**
    `status`: `confirmed_inconsistency`
    `legacy_items`: `41`
    `workflow_ids`: `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`
    `evidence_ids`: `EV-00182`
    `producer`: WorkflowState.FAILED_FINAL naming
    `consumer`: Retry endpoint and operator interpretation
    `break_point`: FAILED_FINAL is explicitly accepted by retry logic despite its terminal name.
    Status naming and recovery contract diverge.
    Business impact: Operators can misread retryable rows as permanently dead.

6. **gap.cieplo-orchestrator-intake-to-review-email.mocked-e2e-test-fails-at-collection**
    `status`: `test_broken`
    `legacy_items`: `48`
    `workflow_ids`: `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`
    `evidence_ids`: `EV-00187`
    `producer`: tests/test_workflow_e2e_mocked.py
    `consumer`: Local pytest collection and workflow regression proof
    `break_point`: Circular import prevents the mocked E2E test from collecting, so scenarios never run.
    The intended end-to-end workflow test is currently non-executable.
    Business impact: A cross-step offer-generation path lacks the regression gate its filename implies.

7. **gap.daszek-feed-push-no-retry.feed-quality-readonly-has-no-ui-consumer**
    `status`: `confirmed_inconsistency`
    `legacy_items`: `44`
    `workflow_ids`: `DASZEK-FEED-PUSH-NO-RETRY`
    `evidence_ids`: `EV-00183`
    `producer`: build_operational_feed_snapshot quality_readonly field
    `consumer`: Daszek frontend app.js
    `break_point`: quality_readonly is valid in the contract and persisted, but no frontend reader exists.
    A live data slice is dormant at the operator surface.
    Business impact: Operators lose a designed read-only quality signal that backend code already provides.

8. **gap.daszek-feed-push-no-retry.operational-feed-validation-warnings-have-no-ui-consumer**
    `status`: `confirmed_inconsistency`
    `legacy_items`: `43`
    `workflow_ids`: `DASZEK-FEED-PUSH-NO-RETRY`
    `evidence_ids`: `EV-00183`
    `producer`: daszek_v3_validate_operational_feed_desk_note_refs
    `consumer`: Daszek frontend app.js
    `break_point`: validation_warnings are persisted into the snapshot but never read by the UI.
    Degraded projection quality is transport-live but presentation-silent.
    Business impact: Operators can see a clean desk even when feed validation already detected missing references.

9. **gap.fast-kalk-lead-widget-calculate-register-dispatch.fast-kalk-lacks-direct-end-to-end-test-for-lead-to-dispatch**
    `status`: `test_gap`
    `legacy_items`: `47`
    `workflow_ids`: `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`
    `evidence_ids`: `EV-00187`
    `producer`: fast-kalk test suite
    `consumer`: Lead to dispatch regression coverage
    `break_point`: No direct automated test file covers the full lead, calculate, register, and dispatch chain.
    Integration drift can accumulate across the full WordPress-to-offer path without one targeted test.
    Business impact: A key revenue-adjacent flow relies on indirect or manual coverage.

10. **gap.fast-kalk-lead-widget-calculate-register-dispatch.fast-kalk-treats-docx-fallback-as-pdf-ready**
    `status`: `confirmed_inconsistency`
    `legacy_items`: `46`
    `workflow_ids`: `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`, `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`
    `evidence_ids`: `EV-00186`
    `producer`: top-instal-generator fallback-docx response
    `consumer`: fast-kalk class-offer-dispatch.php generate_pdf helper
    `break_point`: fast-kalk reads only downloadUrl and ignores the producer's format and converter degradation markers.
    DOCX fallback is advanced as if PDF readiness were proven.
    Business impact: Customer or operator-facing dispatch can proceed on a degraded artifact while believing it is a PDF.

11. **gap.rag-chat-asystent-query-and-ingest-pipeline.graphrag-community-summary-enrichment-has-no-callers**
    `status`: `confirmed_inconsistency`
    `legacy_items`: `37`
    `workflow_ids`: `RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE`
    `evidence_ids`: `EV-00161`
    `producer`: ingest/community_summaries.py:build_community_summary
    `consumer`: Query-time GraphRAG components expecting community summaries
    `break_point`: The enrichment builder is never invoked by ingest or any other module.
    Retrieval-side GraphRAG cannot benefit from community-level summaries.
    Business impact: Query quality may remain below the intended GraphRAG design without visible failure.

12. **gap.rag-chat-asystent-query-and-ingest-pipeline.local-stack-has-no-automated-rag-api-url-override**
    `status`: `confirmed_inconsistency`
    `legacy_items`: `36`
    `workflow_ids`: `RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE`
    `evidence_ids`: `EV-00104`, `EV-00172`
    `producer`: docker-compose.daszek-local.yml and .env.daszek-local config
    `consumer`: rag-widget runtime configuration
    `break_point`: The local stack exposes no automated override path for HVAC_RAG_API_URL.
    Correct local routing depends on a manual wp-admin option change.
    Business impact: Local test environments are brittle and easy to misconfigure.

13. **gap.rag-chat-asystent-query-and-ingest-pipeline.rag-widget-defaults-to-vps-api-url-in-local-docker**
    `status`: `confirmed_inconsistency`
    `legacy_items`: `36`
    `workflow_ids`: `RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE`
    `evidence_ids`: `EV-00104`, `EV-00172`
    `producer`: rag-widget default HVAC_RAG_API_URL resolution
    `consumer`: Local Daszek-mounted rag-widget
    `break_point`: Default API URL points at a production VPS hostname instead of localhost.
    Local Docker runtime can target the wrong backend unless manually overridden.
    Business impact: Local validation may accidentally exercise a remote environment or simply fail.

14. **gap.top-instal-generator-offer-document.generator-success-status-masks-docx-fallback-degradation**
    `status`: `confirmed_inconsistency`
    `legacy_items`: `42`
    `workflow_ids`: `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`
    `evidence_ids`: `EV-00182`
    `producer`: GenerateOfferDocumentUseCase
    `consumer`: Downstream readers of top-level status
    `break_point`: Top-level status remains success when requested PDF generation degrades to DOCX fallback.
    Degraded conversion is encoded only in nested metadata and warning fields.
    Business impact: Consumers can classify degraded output as full success if they read status only.

## P3

1. **gap.api-surface.deprecation-metadata-is-applied-inconsistently-across-legacy-routes**
    `status`: `observation_only`
    `legacy_items`: `39`
    `evidence_ids`: `EV-00112`
    `producer`: api_app.py route decorators
    `consumer`: Route inventory and operators reading API surface
    `break_point`: identity/merge is the only route carrying FastAPI deprecated metadata.
    Legacy or dead routes are not consistently labeled at the framework surface.
    Business impact: Operators and maintainers cannot infer lifecycle status consistently from route metadata.

2. **gap.cross-cutting.best-effort-no-durable-retry-is-a-systemic-architecture-pattern**
    `status`: `observation_only`
    `legacy_items`: `40`
    `workflow_ids`: `DASZEK-FEED-PUSH-NO-RETRY`, `DASZEK-COMMAND-OUTBOX-DRAIN`, `GMAIL-SIGNAL-WORKER-LOOP`
    `evidence_ids`: `EV-00089`, `EV-00116`, `EV-00117`, `EV-00122`
    `producer`: Multiple cross-repo push and drain mechanisms
    `consumer`: Retry expectations across the platform
    `break_point`: Several workflows intentionally terminate after one failed attempt rather than entering durable retry.
    No-retry behavior is architectural and recurring, not incidental.
    Business impact: Operators may assume resilience that the platform does not promise.

3. **gap.fast-kalk-lead-widget-calculate-register-dispatch.customer-visible-price-is-fuzzed-range-not-canonical-total**
    `status`: `observation_only`
    `legacy_items`: `38`
    `workflow_ids`: `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`
    `evidence_ids`: `EV-00093`
    `producer`: fast-kalk map_offer_to_summary
    `consumer`: Customer-facing widget price display
    `break_point`: Public price display intentionally fuzzes the real kalk-top gross value into a range.
    Customer-visible price is not the canonical calculated total.
    Business impact: Any reasoning about seen price must distinguish display range from real offer value.

4. **gap.gmail-signal-worker-loop.gmail-signal-stage-failures-have-no-per-signal-retry**
    `status`: `observation_only`
    `legacy_items`: `40`
    `workflow_ids`: `GMAIL-SIGNAL-WORKER-LOOP`
    `evidence_ids`: `EV-00122`
    `producer`: signal_worker per-signal gmail_fetch and gmail_reconcile stages
    `consumer`: Failed signal ingestion attempts
    `break_point`: Individual signal-stage failures get one attempt and no retry or requeue.
    Poll-level list retries exist, but per-signal processing is still fire-once.
    Business impact: A transient failure on one message can permanently skip its intake without operator awareness.

## Migration Map

- legacy item `1` (P0 — confirmed defects with plausible real business impact) -> `gap.case-scoped-rag-vs-global-rag.query-anything-rag-branch-call-signature-broken`, `gap.case-scoped-rag-vs-global-rag.query-anything-similar-cases-import-broken`, `gap.case-scoped-rag-vs-global-rag.query-anything-counts-source-errors-as-success`, `gap.case-scoped-rag-vs-global-rag.query-anything-returns-ok-when-all-sources-fail`
- legacy item `2` (P0 — confirmed defects with plausible real business impact) -> `gap.learning-loop-divergence-to-candidate-evidence-only.fetch-open-proposals-uses-tuple-rows`, `gap.learning-loop-divergence-to-candidate-evidence-only.row-to-proposal-drops-fields-on-tuple-rows`, `gap.learning-loop-divergence-to-candidate-evidence-only.classify-operator-response-misclassifies-approve-when-proposal-type-missing`
- legacy item `3` (P0 — confirmed defects with plausible real business impact) -> `gap.hitl-proposal-approval-dual-path.hitl-gmail-dry-run-reports-executed-true`, `gap.hitl-proposal-approval-dual-path.hitl-gmail-decision-status-does-not-distinguish-dry-run-from-live`
- legacy item `4` (P0 — confirmed defects with plausible real business impact) -> `gap.agent-graph-execute-run.agent-concurrency-error-swallowed-as-generic-failure`, `gap.agent-graph-execute-run.cas-conflict-mislabeled-as-agent-dry-run`
- legacy item `5` (P0 — confirmed defects with plausible real business impact) -> `gap.case-engagement-resolve-and-agent-handoff.case-intelligence-stage-exceptions-are-swallowed`, `gap.case-engagement-resolve-and-agent-handoff.case-intelligence-failure-collapses-to-empty-agent-signal`, `gap.case-engagement-resolve-and-agent-handoff.case-intelligence-failure-preserves-reconciled-terminal-state-without-retry`
- legacy item `6` (P0 — confirmed defects with plausible real business impact) -> `gap.daszek-feed-push-no-retry.feed-push-has-no-durable-retry`, `gap.calendar-two-worlds-of-visits.customer-proposed-date-risk-is-cli-only`, `gap.calendar-two-worlds-of-visits.schedule-visit-does-not-create-real-calendar-event`
- legacy item `7` (P0 — confirmed defects with plausible real business impact) -> `gap.learning-loop-divergence-to-candidate-evidence-only.approved-learning-rules-affect-only-conditional-precedent-enrichment`, `gap.learning-loop-divergence-to-candidate-evidence-only.business-outcome-capture-missing`, `gap.learning-loop-divergence-to-candidate-evidence-only.auto-approve-bypasses-confidence-threshold-on-observation-volume`
- legacy item `8` (P0 — confirmed defects with plausible real business impact) -> `gap.learning-loop-divergence-to-candidate-evidence-only.get-win-rate-uses-nonexistent-won-status`, `gap.learning-loop-divergence-to-candidate-evidence-only.revenue-forecast-consumes-broken-win-rate`
- legacy item `9` (P0 — confirmed defects with plausible real business impact) -> `gap.hitl-proposal-approval-dual-path.materialize-side-effect-runs-before-approval-persistence`, `gap.hitl-proposal-approval-dual-path.materialize-post-effect-errors-leave-proposal-pending-and-rerunnable`, `gap.hitl-proposal-approval-dual-path.materialize-path-lacks-durable-effect-receipt-before-post-effect-failures`
- legacy item `10` (P0 — confirmed defects with plausible real business impact) -> `gap.hitl-proposal-approval-dual-path.materialize-idempotency-enforced-only-for-composite-plan`, `gap.hitl-proposal-approval-dual-path.materialize-idempotency-wrapper-silently-noops-without-db-url`, `gap.hitl-proposal-approval-dual-path.materialize-idempotency-records-only-ok-results`
- legacy item `11` (P0 — confirmed defects with plausible real business impact) -> `gap.hitl-proposal-approval-dual-path.hitl-approve-ignores-operator-draft-payload`, `gap.hitl-proposal-approval-dual-path.bridge-queue-send-ignores-operator-draft-payload`
- legacy item `12` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.hitl-proposal-approval-dual-path.hitl-clarification-approval-contract-lacks-answer-payload-channel`
- legacy item `13` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.hitl-proposal-approval-dual-path.proposal-execution-restart-recovery-is-inconsistent-across-lifecycles`
- legacy item `14` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.case-scoped-rag-vs-global-rag.gmail-agent-has-no-runtime-consumer-for-company-rag-service`
- legacy item `15` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.gmail-signal-worker-loop.shared-mailbox-polled-by-two-independent-workers`
- legacy item `16` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.hitl-proposal-approval-dual-path.proposal-execution-lifecycle-fragmentation-persists`
- legacy item `17` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.case-engagement-resolve-and-agent-handoff.threadpool-executor-is-serialized-by-immediate-result-awaits`
- legacy item `18` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.case-engagement-resolve-and-agent-handoff.action-planning-precedes-full-understanding`
- legacy item `19` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.top-instal-generator-offer-document.legacy-direct-config-generation-path-remains-live`, `gap.top-instal-generator-offer-document.document-converter-path-has-two-live-modes`
- legacy item `20` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.daszek-command-outbox-drain.db-command-outbox-has-no-confirmed-live-producer`, `gap.daszek-command-outbox-drain.live-bridge-command-flow-still-depends-on-jsonl-queue`
- legacy item `21` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.case-engagement-resolve-and-agent-handoff.finalize-case-persists-state-in-nontransactional-multiwrite-sequence`
- legacy item `22` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.calendar-two-worlds-of-visits.create-calendar-event-action-proposal-has-no-producer`, `gap.calendar-two-worlds-of-visits.visit-reschedule-flow-has-no-confirmed-implementation`, `gap.calendar-two-worlds-of-visits.visit-cancel-flow-has-no-confirmed-implementation`
- legacy item `23` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.sla-watcher-decision-escalation.sla-watcher-has-no-confirmed-automatic-trigger`
- legacy item `24` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.calendar-two-worlds-of-visits.calendar-signal-source-kind-does-not-match-registered-handler`
- legacy item `25` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.agent-graph-turn-loop.preplan-subagent-selection-cannot-activate-document-or-draft-scopes`
- legacy item `26` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.agent-graph-turn-loop.semantic-policy-divergence-is-observed-but-never-enforced`
- legacy item `27` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.hitl-proposal-approval-dual-path.reconcile-warnings-reach-rest-response-but-have-no-ui-consumer`
- legacy item `28` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.hitl-proposal-approval-dual-path.bridge-queue-failures-have-no-retry-or-dead-letter`, `gap.daszek-command-outbox-drain.bridge-queue-failed-rows-become-operator-invisible`
- legacy item `29` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.learning-loop-divergence-to-candidate-evidence-only.world-model-producer-pipeline-has-no-callers`
- legacy item `30` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.agent-graph-turn-loop.request-human-handoff-handler-has-no-exposed-schema-or-caller`
- legacy item `31` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.kalk-top-calculate-offer-pipeline.call-kalk-top-quote-schema-advertises-ignored-arguments`
- legacy item `32` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.hitl-proposal-approval-dual-path.materialize-link-existing-has-no-confirmed-creator`, `gap.hitl-proposal-approval-dual-path.materialize-create-case-has-no-confirmed-creator`, `gap.hitl-proposal-approval-dual-path.materialize-create-artifact-has-no-confirmed-creator`, `gap.hitl-proposal-approval-dual-path.materialize-defer-operator-has-no-confirmed-creator`
- legacy item `33` (P1 — confirmed architectural risks, unclear or lower immediate impact) -> `gap.agent-graph-turn-loop.extract-facts-from-text-cannot-update-existing-fact-value`
- legacy item `34` (P2 — confirmed inconsistencies/duplications, no shown harm yet) -> `gap.calendar-two-worlds-of-visits.calendar-risk-has-three-independent-implementations`
- legacy item `35` (P2 — confirmed inconsistencies/duplications, no shown harm yet) -> `gap.agent-graph-turn-loop.action-dictionary-resolution-docs-conflict-and-adjudication-incomplete`
- legacy item `36` (P2 — confirmed inconsistencies/duplications, no shown harm yet) -> `gap.rag-chat-asystent-query-and-ingest-pipeline.rag-widget-defaults-to-vps-api-url-in-local-docker`, `gap.rag-chat-asystent-query-and-ingest-pipeline.local-stack-has-no-automated-rag-api-url-override`
- legacy item `37` (P2 — confirmed inconsistencies/duplications, no shown harm yet) -> `gap.rag-chat-asystent-query-and-ingest-pipeline.graphrag-community-summary-enrichment-has-no-callers`
- legacy item `38` (P3 — asymmetries and observations worth tracking) -> `gap.fast-kalk-lead-widget-calculate-register-dispatch.customer-visible-price-is-fuzzed-range-not-canonical-total`
- legacy item `39` (P3 — asymmetries and observations worth tracking) -> `gap.api-surface.deprecation-metadata-is-applied-inconsistently-across-legacy-routes`
- legacy item `40` (P3 — asymmetries and observations worth tracking) -> `gap.cross-cutting.best-effort-no-durable-retry-is-a-systemic-architecture-pattern`, `gap.gmail-signal-worker-loop.gmail-signal-stage-failures-have-no-per-signal-retry`
- legacy item `41` (P2 addenda — EV-00182) -> `gap.cieplo-orchestrator-intake-to-review-email.failed-final-state-name-overstates-recoverability`
- legacy item `42` (P2 addenda — EV-00182) -> `gap.top-instal-generator-offer-document.generator-success-status-masks-docx-fallback-degradation`
- legacy item `43` (P2/P3 addenda — EV-00183) -> `gap.daszek-feed-push-no-retry.operational-feed-validation-warnings-have-no-ui-consumer`
- legacy item `44` (P2/P3 addenda — EV-00183) -> `gap.daszek-feed-push-no-retry.feed-quality-readonly-has-no-ui-consumer`
- legacy item `45` (P2 addendum — EV-00184) -> `gap.case-engagement-resolve-and-agent-handoff.agent-runtime-enabled-branch-depends-on-loader-order`
- legacy item `46` (P2 addendum â€” EV-00186) -> `gap.fast-kalk-lead-widget-calculate-register-dispatch.fast-kalk-treats-docx-fallback-as-pdf-ready`, `gap.cieplo-orchestrator-intake-to-review-email.cieplo-treats-docx-fallback-as-pdf-ready`
- legacy item `47` (P2 addendum - EV-00187) -> `gap.fast-kalk-lead-widget-calculate-register-dispatch.fast-kalk-lacks-direct-end-to-end-test-for-lead-to-dispatch`
- legacy item `48` (P2 addendum - EV-00187) -> `gap.cieplo-orchestrator-intake-to-review-email.mocked-e2e-test-fails-at-collection`
