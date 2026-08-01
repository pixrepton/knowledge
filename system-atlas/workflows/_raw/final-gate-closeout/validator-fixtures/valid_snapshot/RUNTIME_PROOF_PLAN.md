# RUNTIME_PROOF_PLAN.md

Generated at: `2026-07-30T22:22:44.7551660+02:00`

## FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH

- Trigger mode: `AUTOMATIC`
- Entry points: WordPress REST topinstal-lead/v1: POST /chat, POST /calculate, POST /register (topinstal-lead-widget.php:197-225, EV-00092)
- Suggested proof focus: prove the canonical entrypoint and first durable side effect for `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`.
- Current runtime note: RUNTIME_UNVERIFIED — fast-kalk's WordPress stack was not confirmed running in this session's Docker inspection (RUNTIME_BASELINE.md §2 lists only gmail-agent/rag-chat-asystent/daszek stacks as Up); this entire workflow is a static-code-only finding this pass.

## KALK-TOP-CALCULATE-OFFER-PIPELINE

- Trigger mode: `AUTOMATIC`
- Entry points: POST /wp-json/topinstal/v1/calculate-offer (CalculateOfferController.php:22-32, uniform for all callers, EV-00098)
- Suggested proof focus: prove the canonical entrypoint and first durable side effect for `KALK-TOP-CALCULATE-OFFER-PIPELINE`.
- Current runtime note: RUNTIME_UNVERIFIED — kalk-top-local Docker stack was not Up in this session's inspection (RUNTIME_BASELINE.md §2); static code read only.

## TOP-INSTAL-GENERATOR-OFFER-DOCUMENT

- Trigger mode: `AUTOMATIC`
- Entry points: POST /wp-json/topinstal/v1/offer-documents/generate (GenerateOfferDocumentController.php:17-27, EV-00100)
- Suggested proof focus: prove the canonical entrypoint and first durable side effect for `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`.
- Current runtime note: RUNTIME_UNVERIFIED — not confirmed running in this session's Docker inspection.

## CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL

- Trigger mode: `MANUAL_ONLY`
- Entry points: cieplo-worker poll CLI (cli/main.py:75-85, EV-00103) — manual/operator-triggered, not an autonomous scheduler
- Suggested proof focus: prove the canonical entrypoint and first durable side effect for `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`.
- Current runtime note: RUNTIME_UNVERIFIED — cieplo-local Docker stack not Up in this session's inspection (RUNTIME_BASELINE.md §2); static code read only.

## LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY

- Trigger mode: `AUTOMATIC`
- Entry points: divergence_loop.process_operator_action (already traced Domain 2, EV-00047 call chain) -> classify_operator_response -> maybe_create_learning_candidate, GET /learning/rule-candidates, POST /learning/rule-candidates/{id}/status (api_app.py:1204-1224, EV-00108) — operator review UI backend
- Suggested proof focus: prove the canonical entrypoint and first durable side effect for `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`.
- Current runtime note: RUNTIME_UNVERIFIED — the consumer-side correction in EV-00181 is still a static code trace, not a fresh runtime probe; enough to refute the prior 'zero consumer' claim, but not a live proof of production usage frequency.

## CALENDAR-TWO-WORLDS-OF-VISITS

- Trigger mode: `MIXED`
- Entry points: CalendarRuntime.ingest_events (calendar_runtime.py:35-77) — real Calendar->Signal bridge, LIVE_PATH (reachable via calendar-ingest CLI / SIGNAL_HANDLERS['calendar']), CalendarRuntime.context_for_case (calendar_runtime.py:113-124) — DORMANT_PATH in practice: only caller is a manual CLI (gmail_intake.py:1494, calendar-context command), agent_runtime.tools.write_executors.execute_schedule_visit (777-809) — LIVE_PATH (agent-triggered tool)
- Suggested proof focus: prove the canonical entrypoint and first durable side effect for `CALENDAR-TWO-WORLDS-OF-VISITS`.
- Current runtime note: RUNTIME_UNVERIFIED for ingest_events/execute_schedule_visit execution (not observed live this pass, only statically confirmed); EV-00080's CLI-only reachability of context_for_case is a structural/static finding, not requiring runtime proof to be conclusive.

## DASZEK-COMMAND-OUTBOX-DRAIN

- Trigger mode: `AUTOMATIC`
- Entry points: daszek/includes/api-v3-handlers.php: daszek_api_v2_append_action_decision (639-663, live REST write into bridge_queue.jsonl on operator approve/reject of an action proposal), plus 2 more append_jsonl_store('bridge_queue',...) call sites at lines 811, 1050 (not individually retraced), daszek/includes/store-v2-domain.php:917 (append_jsonl_store('bridge_queue',...), 3rd confirmed producer site), gmail-agent/tools/gmail_audit/daszek_bridge_queue_drain.py: maybe_worker_bridge_drain_tick (469-520+, called from the signal-worker loop, best-effort/non-fatal) -> fetch_remote_pending_bridge_rows -> DaszekClient.get_v2_bridge_queue(status='pending') / complete_v2_bridge_queue_item(queue_id,status,error) [REST, not direct DB], SEPARATE, PARALLEL, LIKELY-DORMANT mechanism (kept distinct, not merged): daszek/includes/command-outbox.php: daszek_command_outbox_enqueue, daszek_command_outbox_claim_batch, daszek_command_outbox_complete (DB-backed wp_daszek_command_outbox, claim/lease/dead-letter) — see gaps/runtime below, EV-00116/EV-00117
- Suggested proof focus: prove the canonical entrypoint and first durable side effect for `DASZEK-COMMAND-OUTBOX-DRAIN`.
- Current runtime note: RUNTIME_UNVERIFIED — not runtime-probed this pass, confirmed only via static code read of both sides of the contract; the JSONL-vs-DB-table liveness split is itself a static-analysis finding (3 independent methods) that would benefit from a live runtime check per RUNTIME_PROOF_PLAN.md.

## RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE

- Trigger mode: `AUTOMATIC`
- Entry points: POST /chat -> main.py:chat -> api/routes/chat_handler.py:handle_chat_request -> application/use_cases/handle_chat_message.py:handle_chat_message, POST /ingest -> api/handlers/ingest.py:ingest_documents_handler -> engine.py:RAGEngine.ingest_knowledge_base_delta -> _ingest_knowledge_base_delta_impl
- Suggested proof focus: prove the canonical entrypoint and first durable side effect for `RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE`.
- Current runtime note: not_proven

## SLA-WATCHER-DECISION-ESCALATION

- Trigger mode: `MANUAL_ONLY`
- Entry points: gmail_intake.py CLI subcommand 'sla-watcher' (--oneshot or --loop, lines 348-364) -> sla_watcher.sla_watcher_oneshot -> check_sla_violations + maybe_escalate
- Suggested proof focus: prove the canonical entrypoint and first durable side effect for `SLA-WATCHER-DECISION-ESCALATION`.
- Current runtime note: RUNTIME_UNVERIFIED -- not executed this pass (would require a live DB connection and real pending proposals); structurally sound based on direct code read.
