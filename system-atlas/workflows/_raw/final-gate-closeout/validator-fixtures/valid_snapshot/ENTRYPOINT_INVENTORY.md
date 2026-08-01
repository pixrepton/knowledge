# ENTRYPOINT_INVENTORY.md

Generated at: `2026-07-30T22:22:44.7551660+02:00`

## Counters

| surface_type | count |
| --- | --- |
| CLI | 7 |
| HTTP_ROUTE | 11 |
| OTHER | 9 |
| PROCESS_LOOP | 3 |

## Entry Points

| entrypoint_id | workflow_id | surface_type | trigger_mode | runtime | path_or_command | runtime_evidence_ids |
| --- | --- | --- | --- | --- | --- | --- |
| ep.fast-kalk-lead-widget-calculate-register-dispatch.1 | FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH | HTTP_ROUTE | AUTOMATIC | UNVERIFIED | WordPress REST topinstal-lead/v1: POST /chat, POST /calculate, POST /register (topinstal-lead-widget.php:197-225, EV-00092) | - |
| ep.kalk-top-calculate-offer-pipeline.1 | KALK-TOP-CALCULATE-OFFER-PIPELINE | HTTP_ROUTE | AUTOMATIC | UNVERIFIED | POST /wp-json/topinstal/v1/calculate-offer (CalculateOfferController.php:22-32, uniform for all callers, EV-00098) | - |
| ep.top-instal-generator-offer-document.1 | TOP-INSTAL-GENERATOR-OFFER-DOCUMENT | HTTP_ROUTE | AUTOMATIC | UNVERIFIED | POST /wp-json/topinstal/v1/offer-documents/generate (GenerateOfferDocumentController.php:17-27, EV-00100) | - |
| ep.cieplo-orchestrator-intake-to-review-email.1 | CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL | CLI | MANUAL_ONLY | UNVERIFIED | cieplo-worker poll CLI (cli/main.py:75-85, EV-00103) — manual/operator-triggered, not an autonomous scheduler | EV-00103 |
| ep.learning-loop-divergence-to-candidate-evidence-only.1 | LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY | PROCESS_LOOP | AUTOMATIC | UNVERIFIED | divergence_loop.process_operator_action (already traced Domain 2, EV-00047 call chain) -> classify_operator_response -> maybe_create_learning_candidate | - |
| ep.learning-loop-divergence-to-candidate-evidence-only.2 | LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY | HTTP_ROUTE | AUTOMATIC | UNVERIFIED | GET /learning/rule-candidates, POST /learning/rule-candidates/{id}/status (api_app.py:1204-1224, EV-00108) — operator review UI backend | - |
| ep.gmail-signal-worker-loop.1 | GMAIL-SIGNAL-WORKER-LOOP | CLI | AUTOMATIC | CONFIRMED | gmail-agent/tools/gmail_audit/gmail_intake.py:signal-worker CLI subcommand -> run_signal_worker_command(args) | EV-00015 |
| ep.gmail-signal-worker-loop.2 | GMAIL-SIGNAL-WORKER-LOOP | PROCESS_LOOP | AUTOMATIC | CONFIRMED | gmail-agent docker service gmail-agent-vps-gmail-agent-worker-1, live Cmd confirmed EV-00015 | EV-00015 |
| ep.gmail-reconcile-mode-dispatch.1 | GMAIL-RECONCILE-MODE-DISPATCH | OTHER | AUTOMATIC | CONFIRMED | signal_reconciler._reconcile_gmail_signal (signal_reconciler.py:296-386), registered as SIGNAL_HANDLERS['gmail'] | EV-00041 |
| ep.case-engagement-resolve-and-agent-handoff.1 | CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF | OTHER | AUTOMATIC | CONFIRMED | signal_reconciler._reconcile_gmail_signal_agent (signal_reconciler.py:485-515) -> agent_reconcile.run_agent_reconcile (agent_reconcile.py:538-668+) | EV-00046 |
| ep.agent-graph-execute-run.1 | AGENT-GRAPH-EXECUTE-RUN | OTHER | AUTOMATIC | CONFIRMED | agent_runtime.run.execute_agent_run (run.py:120-263) — reached from CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF's Block 3 via SUBFLOW-CASE-INTELLIGENCE-TO-AGENT-HANDOFF | EV-00071 |
| ep.agent-graph-turn-loop.1 | AGENT-GRAPH-TURN-LOOP | PROCESS_LOOP | AUTOMATIC | CONFIRMED | AgentGraphEngine._run inner loop, graph.py:167-265, continuation of AGENT-GRAPH-EXECUTE-RUN | EV-00071 |
| ep.agent-graph-turn-loop.2 | AGENT-GRAPH-TURN-LOOP | CLI | AUTOMATIC | CONFIRMED | build_planner -> OpenAIToolPlanner.plan_next_tool, openai_agent_client.py:39-42,140-259 (EV-00138) | EV-00071 |
| ep.hitl-proposal-approval-dual-path.1 | HITL-PROPOSAL-APPROVAL-DUAL-PATH | HTTP_ROUTE | MANUAL_ONLY | CONFIRMED | POST /engagements/{engagement_id}/hitl/approve (api_app.py:1099) -> agent_hitl_bridge.approve_hitl_engagement | - |
| ep.hitl-proposal-approval-dual-path.2 | HITL-PROPOSAL-APPROVAL-DUAL-PATH | HTTP_ROUTE | MANUAL_ONLY | CONFIRMED | POST /engagements/{engagement_id}/materialize/approve (api_app.py:1137) -> agent_runtime.materialize_bridge.approve_materialize_proposal | - |
| ep.case-scoped-rag-vs-global-rag-gap.1 | CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP | OTHER | AUTOMATIC | CONFIRMED | agent_runtime.tools.handlers.search_rag_knowledge (WORKING, EV-00077) | - |
| ep.case-scoped-rag-vs-global-rag-gap.2 | CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP | OTHER | AUTOMATIC | CONFIRMED | agent_runtime.tools.handlers.query_anything RAG branch (BROKEN, EV-00001/02) | - |
| ep.case-scoped-rag-vs-global-rag-gap.3 | CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP | OTHER | AUTOMATIC | CONFIRMED | context_assembler.ContextAssembler.assemble (local-file-only, EV-00078) | - |
| ep.case-scoped-rag-vs-global-rag-gap.4 | CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP | HTTP_ROUTE | AUTOMATIC | CONFIRMED | rag-chat-asystent backend/api/routes/chat.py POST /chat, /api/chat (EV-00079, unreachable from gmail-agent) | - |
| ep.calendar-two-worlds-of-visits.1 | CALENDAR-TWO-WORLDS-OF-VISITS | CLI | MIXED | UNVERIFIED | CalendarRuntime.ingest_events (calendar_runtime.py:35-77) — real Calendar->Signal bridge, LIVE_PATH (reachable via calendar-ingest CLI / SIGNAL_HANDLERS['calendar']) | EV-00046 |
| ep.calendar-two-worlds-of-visits.2 | CALENDAR-TWO-WORLDS-OF-VISITS | CLI | MIXED | UNVERIFIED | CalendarRuntime.context_for_case (calendar_runtime.py:113-124) — DORMANT_PATH in practice: only caller is a manual CLI (gmail_intake.py:1494, calendar-context command) | EV-00046 |
| ep.calendar-two-worlds-of-visits.3 | CALENDAR-TWO-WORLDS-OF-VISITS | OTHER | MIXED | UNVERIFIED | agent_runtime.tools.write_executors.execute_schedule_visit (777-809) — LIVE_PATH (agent-triggered tool) | EV-00046 |
| ep.daszek-command-outbox-drain.1 | DASZEK-COMMAND-OUTBOX-DRAIN | HTTP_ROUTE | AUTOMATIC | UNVERIFIED | daszek/includes/api-v3-handlers.php: daszek_api_v2_append_action_decision (639-663, live REST write into bridge_queue.jsonl on operator approve/reject of an action proposal), plus 2 more append_jsonl_store('bridge_queue',...) call sites at lines 811, 1050 (not individually retraced) | - |
| ep.daszek-command-outbox-drain.2 | DASZEK-COMMAND-OUTBOX-DRAIN | OTHER | AUTOMATIC | UNVERIFIED | daszek/includes/store-v2-domain.php:917 (append_jsonl_store('bridge_queue',...), 3rd confirmed producer site) | - |
| ep.daszek-command-outbox-drain.3 | DASZEK-COMMAND-OUTBOX-DRAIN | CLI | AUTOMATIC | UNVERIFIED | gmail-agent/tools/gmail_audit/daszek_bridge_queue_drain.py: maybe_worker_bridge_drain_tick (469-520+, called from the signal-worker loop, best-effort/non-fatal) -> fetch_remote_pending_bridge_rows -> DaszekClient.get_v2_bridge_queue(status='pending') / complete_v2_bridge_queue_item(queue_id,status,error) [REST, not direct DB] | - |
| ep.daszek-command-outbox-drain.4 | DASZEK-COMMAND-OUTBOX-DRAIN | OTHER | AUTOMATIC | UNVERIFIED | SEPARATE, PARALLEL, LIKELY-DORMANT mechanism (kept distinct, not merged): daszek/includes/command-outbox.php: daszek_command_outbox_enqueue, daszek_command_outbox_claim_batch, daszek_command_outbox_complete (DB-backed wp_daszek_command_outbox, claim/lease/dead-letter) — see gaps/runtime below, EV-00116/EV-00117 | - |
| ep.daszek-feed-push-no-retry.1 | DASZEK-FEED-PUSH-NO-RETRY | HTTP_ROUTE | MANUAL_ONLY | CONFIRMED | agent_hitl_bridge.best_effort_push_engagement_feed_after_hitl (218-279), called from api_app.py POST /engagements/{id}/materialize/approve (line 1193) | EV-00088, EV-00119 |
| ep.rag-chat-asystent-query-and-ingest-pipeline.1 | RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE | HTTP_ROUTE | AUTOMATIC | UNVERIFIED | POST /chat -> main.py:chat -> api/routes/chat_handler.py:handle_chat_request -> application/use_cases/handle_chat_message.py:handle_chat_message | - |
| ep.rag-chat-asystent-query-and-ingest-pipeline.2 | RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE | HTTP_ROUTE | AUTOMATIC | UNVERIFIED | POST /ingest -> api/handlers/ingest.py:ingest_documents_handler -> engine.py:RAGEngine.ingest_knowledge_base_delta -> _ingest_knowledge_base_delta_impl | - |
| ep.sla-watcher-decision-escalation.1 | SLA-WATCHER-DECISION-ESCALATION | CLI | MANUAL_ONLY | UNVERIFIED | gmail_intake.py CLI subcommand 'sla-watcher' (--oneshot or --loop, lines 348-364) -> sla_watcher.sla_watcher_oneshot -> check_sla_violations + maybe_escalate | - |

## Notes

- Counters are generated from canonical workflow entrypoints, not preserved historical prose.
- Dynamic route deduplication outside workflow-scoped entrypoints remains intentionally excluded from this regenerated inventory.
