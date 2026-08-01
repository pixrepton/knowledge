# STATE_OWNERSHIP_MATRIX.md

Generated at: `2026-07-30T22:22:44.7551660+02:00`

| state_id | state_or_store | owner_repos | writer_workflows | reader_workflows | note |
| --- | --- | --- | --- | --- | --- |
| state.001 | Chroma collections (on ingest) | rag-chat-asystent | RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE | - | derived-from-workflow-state-io |
| state.002 | Chroma vector store (parent+child collections) | - | - | RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE | derived-from-workflow-state-io |
| state.003 | Gmail message/thread/attachment content (via gmail_intake fetch stages, not individually re-traced this pass) | - | - | GMAIL-SIGNAL-WORKER-LOOP | derived-from-workflow-state-io |
| state.004 | Google Calendar API (ingest_events) | - | - | CALENDAR-TWO-WORLDS-OF-VISITS | derived-from-workflow-state-io |
| state.005 | WP session store cache (calculate result + raw offer, keyed by session+fingerprint) | fast-kalk | FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH | - | derived-from-workflow-state-io |
| state.006 | WP transient/session store (Session_Store, exact backing not opened this pass) | - | - | FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH | derived-from-workflow-state-io |
| state.007 | WorkflowRow state transitions (own DB), cieplo_html/parsed_result/calc_request/offer_json/generator_request/generator_response/pdf_download_url/email_sent_at fields | cieplo-orchestrator | CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL | - | derived-from-workflow-state-io |
| state.008 | agent job-tracking table (via job_store.record_completed, unconditional, table name not yet confirmed) | gmail-agent | CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF | - | node-b-owned-or-adjacent |
| state.009 | agent_proposal_records + operator_response_records (unresponded proposal detection) | - | - | SLA-WATCHER-DECISION-ESCALATION | derived-from-workflow-state-io |
| state.010 | agent_proposal_records, operator_response_records (via classify_operator_response's row-shape-bug-affected fetch) | - | - | LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY | derived-from-workflow-state-io |
| state.011 | calendar_events/calendar_case_links tables (ingest_events) | gmail-agent | CALENDAR-TWO-WORLDS-OF-VISITS | - | node-b-owned-or-adjacent |
| state.012 | checkpoint store (if resume_from) | - | - | AGENT-GRAPH-EXECUTE-RUN | derived-from-workflow-state-io |
| state.013 | checkpoint store (per-turn) | gmail-agent | AGENT-GRAPH-TURN-LOOP | - | node-b-owned-or-adjacent |
| state.014 | cieplo-orchestrator's own WorkflowRow table (SEPARATE DB from gmail-agent/kalk-top) | - | - | CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL | derived-from-workflow-state-io |
| state.015 | conversation history (ConversationManager, on chat) | rag-chat-asystent | RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE | - | derived-from-workflow-state-io |
| state.016 | correlation registry (engagement resolution) | - | - | CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF | derived-from-workflow-state-io |
| state.017 | daszek bridge_queue.jsonl (live path, via REST get_v2_bridge_queue) | - | - | DASZEK-COMMAND-OUTBOX-DRAIN | projection-only |
| state.018 | daszek bridge_queue.jsonl (live path: 3+ PHP call sites append; gc'd at 90 days by daszek_v2_bridge_queue_gc) | daszek | DASZEK-COMMAND-OUTBOX-DRAIN | - | projection-only |
| state.019 | execution_runtime's own store (ActionProposal/ExecutionResult persistence, not independently opened this pass) | gmail-agent | HITL-PROPOSAL-APPROVAL-DUAL-PATH | - | node-b-owned-or-adjacent |
| state.020 | generated document artifact (storage location not traced) | top-instal-generator | TOP-INSTAL-GENERATOR-OFFER-DOCUMENT | - | derived-from-workflow-state-io |
| state.021 | gmail-agent case/engagement context pack (via node_b_read.py, when configured) | - | - | RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE | derived-from-workflow-state-io |
| state.022 | gmail-agent correlation registry (implicit, via engagement_id lookups) | - | - | FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH | derived-from-workflow-state-io |
| state.023 | gmail-agent correlation registry (via /internal/registry/links) | fast-kalk | FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH | - | derived-from-workflow-state-io |
| state.024 | gmail-agent unified_os_events (via /internal/os-events) | fast-kalk | FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH | - | derived-from-workflow-state-io |
| state.025 | in-memory BM25 index | - | - | RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE | derived-from-workflow-state-io |
| state.026 | ingest manifest + chunk manifest (local disk, JSON) | - | - | RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE | derived-from-workflow-state-io |
| state.027 | kits repository (find_kit) for direct-config mode | - | - | TOP-INSTAL-GENERATOR-OFFER-DOCUMENT | derived-from-workflow-state-io |
| state.028 | learning_rule_candidates (status, supporting_count, approved_at/by) | gmail-agent | LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY | - | node-b-owned-or-adjacent |
| state.029 | local company_context text file (context_assembler) | - | - | CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP | derived-from-workflow-state-io |
| state.030 | mailbox_memory fact scheduled_visit (execute_schedule_visit) | gmail-agent | CALENDAR-TWO-WORLDS-OF-VISITS | - | node-b-owned-or-adjacent |
| state.031 | mailbox_memory facts (execute_schedule_visit consumers) | - | - | CALENDAR-TWO-WORLDS-OF-VISITS | derived-from-workflow-state-io |
| state.032 | mailbox_memory pgvector chunks (case-scoped, via search_rag_knowledge) | - | - | CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP | derived-from-workflow-state-io |
| state.033 | mailbox_memory_raw_observations (Postgres, via RawObservationJournal -> store.append_raw_observation, EV-00027) — separate, earlier-stage raw-capture table, not a duplicate of the above (confirms brief.md's implied ambiguity was resolvable: these are two pipeline stages, not competing implementations) | gmail-agent | GMAIL-SIGNAL-WORKER-LOOP | - | node-b-owned-or-adjacent |
| state.034 | mailbox_memory_signals (Postgres, via SignalJournal.append -> store.append_signal, EV-00026) — the canonical post-normalization signal store | gmail-agent | GMAIL-SIGNAL-WORKER-LOOP | - | node-b-owned-or-adjacent |
| state.035 | mailbox_memory_signals (calendar source_kind, via ingest_events) | gmail-agent | CALENDAR-TWO-WORLDS-OF-VISITS | - | node-b-owned-or-adjacent |
| state.036 | mailbox_memory_signals.engagement_id (via patch_signal_engagement, unconditional) | gmail-agent | CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF | - | node-b-owned-or-adjacent |
| state.037 | manifest files (on ingest) | rag-chat-asystent | RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE | - | derived-from-workflow-state-io |
| state.038 | operator_engagement_snapshots (EngagementSnapshotV2, via ensure_engagement_snapshot BEFORE Block 3, and later execute_agent_run's own snapshot save IF Block 3 succeeds) | gmail-agent | CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF | - | node-b-owned-or-adjacent |
| state.039 | operator_engagement_snapshots (approve routes mutate snapshot state via their respective bridges) | gmail-agent | HITL-PROPOSAL-APPROVAL-DUAL-PATH | - | node-b-owned-or-adjacent |
| state.040 | operator_engagement_snapshots (load_snapshot) | - | - | AGENT-GRAPH-EXECUTE-RUN | derived-from-workflow-state-io |
| state.041 | operator_engagement_snapshots (save_snapshot, CAS via expected_version) | gmail-agent | AGENT-GRAPH-EXECUTE-RUN | - | node-b-owned-or-adjacent |
| state.042 | operator_engagement_snapshots (via build_operational_feed_from_engagement_store) | - | - | DASZEK-FEED-PUSH-NO-RETRY | derived-from-workflow-state-io |
| state.043 | operator_engagement_snapshots (via ensure_engagement_snapshot, read-before-write pattern assumed, not confirmed) | - | - | CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF | derived-from-workflow-state-io |
| state.044 | policy_decision / action_proposal_v2 tables (via policy_action_spine, EV-00073) | gmail-agent | HITL-PROPOSAL-APPROVAL-DUAL-PATH | - | node-b-owned-or-adjacent |
| state.045 | price book / buffer rules / selection rules repositories (Wp-backed, exact storage not opened) | - | - | KALK-TOP-CALCULATE-OFFER-PIPELINE | derived-from-workflow-state-io |
| state.046 | processing-attempt records inside SUBFLOW-GMAIL-SIGNAL-RECONCILE (table not independently re-confirmed this pass, citing prior-session OPERATOR_DECISIONS.md 2026-07-16 X14 finding only) | gmail-agent | GMAIL-SIGNAL-WORKER-LOOP | - | node-b-owned-or-adjacent |
| state.047 | session-keyed form-state snapshot table (persist_form_state_snapshot) | kalk-top | KALK-TOP-CALCULATE-OFFER-PIPELINE | - | kalk-top-owned-or-adjacent |
| state.048 | turn journal (Postgres-backed when settings.enabled, per build_turn_journal — not independently opened this pass) | gmail-agent | AGENT-GRAPH-EXECUTE-RUN | - | node-b-owned-or-adjacent |
| state.049 | turn journal (per-turn, durable) | gmail-agent | AGENT-GRAPH-TURN-LOOP | - | node-b-owned-or-adjacent |
| state.050 | unified_os_events (agent.run.started/agent.run.completed) | gmail-agent | AGENT-GRAPH-EXECUTE-RUN | - | node-b-owned-or-adjacent |
| state.051 | unified_os_events (dedup lookback) | - | - | SLA-WATCHER-DECISION-ESCALATION | derived-from-workflow-state-io |
| state.052 | unified_os_events (gmail_feed_push telemetry, via publish_gmail_feed_push_event) | gmail-agent | DASZEK-FEED-PUSH-NO-RETRY | - | node-b-owned-or-adjacent |
| state.053 | unified_os_events (sla.violation.critical / sla.violation.high) | gmail-agent | SLA-WATCHER-DECISION-ESCALATION | - | node-b-owned-or-adjacent |
| state.054 | whatever run_shared_downstream_stages writes durably before a mid-pipeline Block-1 exception — NOT CONFIRMED transactional or all-or-nothing; flagged as an open integrity question, not asserted either way | gmail-agent | CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF | - | node-b-owned-or-adjacent |
| state.055 | wp_daszek_command_outbox table (claim query exists in code; live caller/consumer of this specific table not found this pass) | - | - | DASZEK-COMMAND-OUTBOX-DRAIN | projection-only |
| state.056 | wp_daszek_command_outbox table (enqueue path confirmed reachable only from a one-time, no-confirmed-caller migration function; claim/lease/completion writes have a real implementation but no confirmed live producer feeding new rows) | daszek | DASZEK-COMMAND-OUTBOX-DRAIN | - | projection-only |
