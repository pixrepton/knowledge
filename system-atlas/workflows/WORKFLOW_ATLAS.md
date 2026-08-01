# WORKFLOW_ATLAS.md

Generated at: `2026-07-30T22:22:44.7551660+02:00`

## Summary

- Workflows: `17`
- Subflows: `4`
- Evidence rows: `187`
- `ATLAS-GLOBAL` evidence rows: `13`
- Atomic gaps: `78`
- Legacy gap items: `48`

Evidence type counts:

| Type | Count |
| --- | --- |
| ABSENCE_SEARCH | 20 |
| CODE | 150 |
| CONFIG | 1 |
| GRAPH | 6 |
| RUNTIME | 7 |
| SYNTHESIS | 1 |
| TEST | 2 |

Gap priority counts:

| Priority | Count |
| --- | --- |
| P0 | 30 |
| P1 | 30 |
| P2 | 14 |
| P3 | 4 |

## Workflows

| workflow_id | owner | path_statuses | contract_statuses | runtime | trigger | test_status | evidence | gaps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH | fast-kalk | LIVE_PATH, CONDITIONAL_PATH | - | UNVERIFIED | AUTOMATIC | NO_DIRECT_TEST_FOUND, PROOF_ONLY | 17 | 3 |
| KALK-TOP-CALCULATE-OFFER-PIPELINE | kalk-top | LIVE_PATH | - | UNVERIFIED | AUTOMATIC | UNIT_COVERED, INTEGRATION_COVERED, END_TO_END_COVERED, PROOF_ONLY | 12 | 1 |
| TOP-INSTAL-GENERATOR-OFFER-DOCUMENT | top-instal-generator | LIVE_PATH, CONDITIONAL_PATH | - | UNVERIFIED | AUTOMATIC | PROOF_ONLY | 14 | 5 |
| CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL | cieplo-orchestrator | CONDITIONAL_PATH | - | UNVERIFIED | MANUAL_ONLY | UNIT_COVERED, SYNTHETIC_ONLY | 14 | 4 |
| LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY | gmail-agent | LIVE_PATH, CONDITIONAL_PATH | - | UNVERIFIED | AUTOMATIC | UNIT_COVERED | 10 | 9 |
| GMAIL-SIGNAL-WORKER-LOOP | gmail-agent | LIVE_PATH | - | CONFIRMED | AUTOMATIC | UNIT_COVERED, INTEGRATION_COVERED, CHAOS_COVERED, PROOF_ONLY | 21 | 3 |
| GMAIL-RECONCILE-MODE-DISPATCH | gmail-agent | LIVE_PATH, CONDITIONAL_PATH | - | CONFIRMED | AUTOMATIC | UNIT_COVERED | 9 | 0 |
| CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF | gmail-agent | LIVE_PATH | - | CONFIRMED | AUTOMATIC | UNIT_COVERED, PROOF_ONLY | 27 | 8 |
| AGENT-GRAPH-EXECUTE-RUN | gmail-agent | LIVE_PATH, CONDITIONAL_PATH | - | CONFIRMED | AUTOMATIC | UNIT_COVERED, PROOF_ONLY | 12 | 2 |
| AGENT-GRAPH-TURN-LOOP | gmail-agent | LIVE_PATH | - | CONFIRMED | AUTOMATIC | UNIT_COVERED, INTEGRATION_COVERED, CHAOS_COVERED | 11 | 6 |
| HITL-PROPOSAL-APPROVAL-DUAL-PATH | gmail-agent | LIVE_PATH, CONDITIONAL_PATH | - | CONFIRMED | MANUAL_ONLY | UNIT_COVERED, PROOF_ONLY | 33 | 20 |
| CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP | gmail-agent | LIVE_PATH | BROKEN_CALL, MISSING_CONSUMER | CONFIRMED | AUTOMATIC | UNIT_COVERED, SYNTHETIC_ONLY | 12 | 5 |
| CALENDAR-TWO-WORLDS-OF-VISITS | gmail-agent | LIVE_PATH, DORMANT_PATH | MISSING_PRODUCER | UNVERIFIED | MIXED | UNIT_COVERED, SYNTHETIC_ONLY | 23 | 7 |
| DASZEK-COMMAND-OUTBOX-DRAIN | daszek | LIVE_PATH | - | UNVERIFIED | AUTOMATIC | UNIT_COVERED, PROOF_ONLY | 11 | 5 |
| DASZEK-FEED-PUSH-NO-RETRY | gmail-agent | LIVE_PATH | - | CONFIRMED | MANUAL_ONLY | UNIT_COVERED, CHAOS_COVERED, PROOF_ONLY | 23 | 5 |
| RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE | rag-chat-asystent | LIVE_PATH | - | UNVERIFIED | AUTOMATIC | UNIT_COVERED, INTEGRATION_COVERED, PROOF_ONLY | 14 | 3 |
| SLA-WATCHER-DECISION-ESCALATION | gmail-agent | LIVE_PATH | - | UNVERIFIED | MANUAL_ONLY | UNIT_COVERED, SYNTHETIC_ONLY | 2 | 1 |

## Subflows

### SUBFLOW-CASE-INTELLIGENCE-TO-AGENT-HANDOFF

FORMAL BOUNDARY: Domain 2 (Case/memory) -> Domain 3 (Understanding/decision/planner/agent runtime). Everything before this subflow is Case/Identity/Engagement/Intelligence resolution; everything after is the agent execution loop itself. Location: agent_runtime/agent_reconcile.py:606-650, inside run_agent_reconcile, after Block 1 (case intelligence) and Block 2 (policy envelope) have both resolved (successfully or degraded, EV-00054/55) and before Block 3 (EV-00056) invokes execute_agent_run.

- evidence_ids: EV-00047, EV-00054, EV-00055

### SUBFLOW-CASE-LINK-ROUTE-DECISION

Shared deterministic case-linking + routing decision used before choosing agent vs staging vs legacy reconcile. Not gmail-specific despite being reached first from the gmail dispatcher — orchestrator.route_signal takes any source_kind.

- evidence_ids: EV-00042, EV-00043, EV-00123, EV-00124
- notes: 2 residual notes

### SUBFLOW-SHARED-DOWNSTREAM-STAGES

The canonical "Case Intelligence pipeline" — intake_shared_downstream.run_shared_downstream_stages (intake_shared_downstream.py:122-321). Called from BOTH the legacy reconcile path (_reconcile_gmail_legacy_prepare) AND the agent-runtime path (_run_mailbox_intelligence_downstream, EV-00045) — genuinely shared, not duplicated logic. This IS "Brain 1" per ARCHITECTURE_DECISIONS.md's informal framing; not used as a formal name here since it is not a literal identifier in THIS file (contrast SUBFLOW's sibling _BRAIN1_OWNED_SNAPSHOT_FIELDS in graph.py, EV-00065, which is literal).

- evidence_ids: EV-00066, EV-00067, EV-00068, EV-00069, EV-00070, EV-00071
- notes: 3 residual notes

### SUBFLOW-GMAIL-SIGNAL-RECONCILE

Durable, per-signal reconcile pipeline shared by every source_kind (gmail, drive, calendar, ...). Entry: signal_reconciler.reconcile_signal(signal, runtime_context, dry_run).

- evidence_ids: EV-00019, EV-00020
- notes: 1 residual notes
