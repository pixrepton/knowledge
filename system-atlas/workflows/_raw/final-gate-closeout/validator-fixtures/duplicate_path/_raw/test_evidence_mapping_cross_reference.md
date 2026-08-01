# Test Evidence Mapping Cross Reference

- timestamp: `2026-07-30 21:32:07 +02:00`
- working_directory: `C:\Users\compg\Desktop\top-code workspace`
- knowledge_repo_sha: `597b1091a296930ed32afb379ec19b8ab425d4fa`
- repo_sha:
  - `gmail-agent=468d37ee6553b39bf6009939e9c87c13f3c183c7`
  - `daszek=672769d9496359dcfb7f2427d555ad34a2171b1a`
  - `kalk-top=9d56055be7f293ad17ffb624abc178617f46f5be`
  - `cieplo-orchestrator=e68f05386722b4034ca36bd39d169eba759f44e6`
  - `top-instal-generator=7e5279551b3919b7ab84547227b3355f45c44bf4`
  - `fast-kalk=06a470da94db6069f42c0d20a860815212e80f00`
  - `rag-widget=c64707aac69bb4a6cc68e1f097aa8415a3b976a6`
  - `rag-chat-asystent=34e9ae2e597076756aa71051382fe18d058776a7`
- scope:
  - map each canonical workflow to direct unit tests, integration tests, end-to-end tests, chaos tests, proof scripts, synthetic-only/state-injection-only coverage, or explicit lack of direct test
  - distinguish executable test files from helpers, docs, fixtures, and bootstrap scripts
  - execute only bounded, local-safe, load-bearing commands
- exclusions:
  - no new call-graph reconstruction
  - no production mutation, deploy, or secret use
  - no browser E2E bring-up for `kalk-top`
  - no WordPress/bootstrap mutation for `fast-kalk`
  - no rerun of reverse-audit categories 1-12

## Status Legend

- `NO_DIRECT_TEST_FOUND` - only scripts/proofs/helpers/docs found; no direct test file for the workflow surface
- `SYNTHETIC_ONLY` - coverage exists only through mocks, in-memory stores, fixtures, or state injection; no live producer proof
- `PROOF_ONLY` - proof/harness/smoke exists, but no durable direct unit/integration suite was found for that workflow surface
- `UNIT_COVERED` - direct unit or contract tests found
- `INTEGRATION_COVERED` - multi-component or integration suite found
- `END_TO_END_COVERED` - end-to-end spec or end-to-end harness found on disk
- `CHAOS_COVERED` - explicit failure-mode / outage / timeout suite found

## Exact Commands

### 1. Repo SHA snapshot

```powershell
$repos = 'gmail-agent','daszek','kalk-top','cieplo-orchestrator','top-instal-generator','fast-kalk','rag-widget','rag-chat-asystent'; foreach ($r in $repos) { $sha = git -C "C:\Users\compg\Desktop\top-code workspace\$r" rev-parse HEAD; "$r`t$sha" }
```

- exit_code: `0`

### 2. Mechanical candidate scan

```powershell
$root = 'C:\Users\compg\Desktop\top-code workspace'
$workflows = @(
  @{ id='FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH'; repo='fast-kalk'; pattern='Topinstal_Lead_Widget_Calculator|Offer_Dispatch|register_sync|register_async|/internal/registry/links|/internal/os-events|offer-documents/generate|calculate-offer' },
  @{ id='KALK-TOP-CALCULATE-OFFER-PIPELINE'; repo='kalk-top'; pattern='CalculateOfferController|TopInstal_CalculateOffer_UseCase|calculate-offer' },
  @{ id='TOP-INSTAL-GENERATOR-OFFER-DOCUMENT'; repo='top-instal-generator'; pattern='GenerateOfferDocumentController|TopInstal_GenerateOfferDocument_UseCase|offer-documents/generate|fallback_docx|FALLBACK_DOCX_RETURNED' },
  @{ id='CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL'; repo='cieplo-orchestrator'; pattern='run_workflow_pipeline|KalkTopClient.calculate_offer|GeneratorClient.generate|retry_workflow|ingress_cieplo_app|PDF_READY' },
  @{ id='LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY'; repo='gmail-agent'; pattern='maybe_create_learning_candidate|learning_rule_candidates|process_operator_action|pattern_learner|world_model_insights' },
  @{ id='GMAIL-SIGNAL-WORKER-LOOP'; repo='gmail-agent'; pattern='run_signal_loop|signal_worker|build_gmail_signals|append_signal|signal-replay' },
  @{ id='GMAIL-RECONCILE-MODE-DISPATCH'; repo='gmail-agent'; pattern='_reconcile_gmail_signal|agent_runtime_reconcile_active|legacy_downstream_reconcile_active|reconcile mode misconfigured' },
  @{ id='CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF'; repo='gmail-agent'; pattern='run_agent_reconcile|resolve_engagement_for_case|ensure_engagement_snapshot|patch_signal_engagement' },
  @{ id='AGENT-GRAPH-EXECUTE-RUN'; repo='gmail-agent'; pattern='execute_agent_run|AgentRunResult|AgentConcurrencyError|agent.run.started|agent.run.completed' },
  @{ id='AGENT-GRAPH-TURN-LOOP'; repo='gmail-agent'; pattern='AgentGraphEngine|plan_next_tool|report_gaps_and_stop|tools_for_sub_agent' },
  @{ id='HITL-PROPOSAL-APPROVAL-DUAL-PATH'; repo='gmail-agent'; pattern='approve_hitl_engagement|approve_materialize_proposal|execute_materialize_proposal|agent_hitl_send_executed|action_proposal_rejected' },
  @{ id='CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP'; repo='gmail-agent'; pattern='query_anything|search_rag_knowledge|ContextHub|case-scoped|global rag' },
  @{ id='CALENDAR-TWO-WORLDS-OF-VISITS'; repo='gmail-agent'; pattern='CalendarRuntime|execute_schedule_visit|context_for_case|calendar_risk|scheduled_visit' },
  @{ id='DASZEK-COMMAND-OUTBOX-DRAIN'; repo='gmail-agent'; pattern='daszek_bridge_queue_drain|bridge_queue|complete_v2_bridge_queue_item|get_v2_bridge_queue' },
  @{ id='DASZEK-FEED-PUSH-NO-RETRY'; repo='gmail-agent'; pattern='post_v3_operational_feed_snapshot|best_effort_push_engagement_feed_after_hitl|maybe_push_operational_feed_after_reconcile|gmail.feed.pushed|gmail.feed.push_failed' },
  @{ id='RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE'; repo='rag-chat-asystent'; pattern='handle_chat_request|handle_chat_message|node_b_read|documents/upload|IntentRouter|knowledge_base_delta' },
  @{ id='SLA-WATCHER-DECISION-ESCALATION'; repo='gmail-agent'; pattern='sla_watcher|check_sla_violations|maybe_escalate|sla.violation' }
)
$out = foreach ($wf in $workflows) {
  $repoPath = Join-Path $root $wf.repo
  $hits = & rg -l -S -e $wf.pattern $repoPath 2>$null | Where-Object { $_ -match '(?i)(test|spec|e2e|chaos|proof|harness|script|deploy|smoke|regression)' } | Sort-Object -Unique
  [pscustomobject]@{ workflow_id=$wf.id; repo=$wf.repo; files=@($hits) }
}
$out | ConvertTo-Json -Depth 4 | Tee-Object -FilePath 'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\logs\20260730-212839\n3-candidate-scan.json'
```

- exit_code: `0`
- artifact: `_raw/logs/20260730-212839/n3-candidate-scan.json`

### 3. Path correction inside `gmail-agent`

```powershell
rg --files 'C:\Users\compg\Desktop\top-code workspace\gmail-agent' | rg 'test_signal_worker|test_agent_graph_engine|test_materialize_approve_harness|test_calendar_case_boundary|test_daszek_bridge_queue_drain|test_search_rag_knowledge_tool|test_signal_reconciler_runtime|test_reconcile_full_flow|daszek_503|test_daszek_v3_feed_runtime|test_agent_hitl_bridge'
```

- exit_code: `0`

### 4. Executed load-bearing test batch

```powershell
pytest 'tools/gmail_audit/tests/test_search_rag_knowledge_tool.py' 'tools/gmail_audit/tests/test_daszek_bridge_queue_drain.py' 'tools/gmail_audit/tests/test_signal_worker.py' 'tools/gmail_audit/tests/integration/test_reconcile_full_flow.py' 'tools/gmail_audit/tests/chaos/test_daszek_503.py' -q 2>&1 | Tee-Object -FilePath 'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\logs\20260730-212839\gmail-agent-n3.log'
```

- exit_code: `0`
- result: `69 passed in 79.11s`
- log: `_raw/logs/20260730-212839/gmail-agent-n3.log`

```powershell
pytest 'tests/test_workflow_e2e_mocked.py' -q 2>&1 | Tee-Object -FilePath 'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\logs\20260730-212839\cieplo-orchestrator-n3.log'
```

- exit_code: `1`
- result: `ImportError during collection: circular import between ingress.processor and workflow.repository`
- log: `_raw/logs/20260730-212839/cieplo-orchestrator-n3.log`

```powershell
pytest 'backend/tests/unit/test_handle_chat_message_use_case.py' -q 2>&1 | Tee-Object -FilePath 'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\logs\20260730-212839\rag-chat-asystent-n3.log'
```

- exit_code: `0`
- result: `7 passed in 25.05s`
- log: `_raw/logs/20260730-212839/rag-chat-asystent-n3.log`

```powershell
php 'core/application/harness/generate-offer-document.smoke.php' 2>&1 | Tee-Object -FilePath 'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\logs\20260730-212839\top-instal-generator-n3.log'
```

- exit_code: `0`
- result: `[PASS] generate-offer-document smoke: trace=smoke-trace-001, file=harness.pdf`
- log: `_raw/logs/20260730-212839/top-instal-generator-n3.log`

```powershell
node 'kalkulator/js/topinstalApi.regression.test.js' 2>&1 | Tee-Object -FilePath 'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\logs\20260730-212839\kalk-top-n3.log'
```

- exit_code: `0`
- result: `10 PASS lines across kalkulator/js and frontend/api clients`
- log: `_raw/logs/20260730-212839/kalk-top-n3.log`

```powershell
pytest 'tests/test_ingress_retirement.py' 'tests/test_cieplo_workflow_os_events.py' -q 2>&1 | Tee-Object -FilePath 'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\logs\20260730-212839\cieplo-orchestrator-unit-n3.log'
```

- exit_code: `0`
- result: `7 passed in 0.68s`
- log: `_raw/logs/20260730-212839/cieplo-orchestrator-unit-n3.log`

## Workflow Mapping

### FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH

- final_test_status: `[NO_DIRECT_TEST_FOUND, PROOF_ONLY]`
- direct_unit: none found
- integration: none found
- end_to_end_on_disk:
  - `fast-kalk/scripts/e2e-scenarios-smoke.php`
  - `fast-kalk/scripts/local-rest-smoke.php`
- proof_or_harness:
  - `fast-kalk/scripts/buffer-hydraulics-smoke.php`
  - `fast-kalk/scripts/os-event-w2-harness.php`
  - `fast-kalk/scripts/repro-calculate-502.php`
  - `fast-kalk/scripts/insulation-pending-test.php`
- executed_now: none
- classification_notes:
  - `scripts/configure-local.php` is bootstrap/config helper, not proof
  - all discovered coverage is script/harness style and depends on local WordPress/bootstrap state

### KALK-TOP-CALCULATE-OFFER-PIPELINE

- final_test_status: `[UNIT_COVERED, INTEGRATION_COVERED, END_TO_END_COVERED, PROOF_ONLY]`
- direct_unit_or_contract:
  - `kalk-top/core/application/harness/calc-request-contract.regression.php`
  - `kalk-top/core/application/harness/configurator-pump-offer.regression.php`
  - `kalk-top/kalkulator/js/topinstalApi.regression.test.js`
  - `kalk-top/scripts/configurator-hydraulics-calculate-offer-chain.regression.test.mjs`
- integration_or_e2e_on_disk:
  - `kalk-top/core/application/harness/rest-calculate-offer.e2e.php`
  - `kalk-top/tests/e2e/form-validation-gate.spec.ts`
  - `kalk-top/tests/e2e/full-journey.spec.ts`
- proof_or_smoke:
  - `kalk-top/scripts/verify-pump-chain-quick.ps1`
  - `kalk-top/wp-adapter/dev/SmokeAdminPage.php`
- executed_now:
  - `node kalkulator/js/topinstalApi.regression.test.js` -> exit `0`
- classification_notes:
  - browser and REST E2E require local env/bootstrap (`TOPINSTAL_REST_BASE_URL`, nonce, Playwright/browser surface)

### TOP-INSTAL-GENERATOR-OFFER-DOCUMENT

- final_test_status: `[PROOF_ONLY]`
- direct_unit: none found
- integration: none found
- end_to_end_on_disk:
  - `top-instal-generator/tools/runtime_e2e_runner.py`
  - `top-instal-generator/docs/RUNTIME_E2E_RESULTS.json`
- proof_or_smoke:
  - `top-instal-generator/core/application/harness/generate-offer-document.smoke.php`
- executed_now:
  - `php core/application/harness/generate-offer-document.smoke.php` -> exit `0`
- classification_notes:
  - live safe proof exists, but no dedicated unit/integration suite tied directly to this workflow surface was found

### CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL

- final_test_status: `[UNIT_COVERED, SYNTHETIC_ONLY]`
- direct_unit:
  - `cieplo-orchestrator/tests/test_cieplo_workflow_os_events.py`
  - `cieplo-orchestrator/tests/test_ingress_retirement.py`
- end_to_end_on_disk:
  - `cieplo-orchestrator/tests/test_workflow_e2e_mocked.py`
  - `cieplo-orchestrator/scripts/run_one_email_e2e.py`
- proof:
  - `cieplo-orchestrator/docs/P0_CP2_PHP_INGRESS_RETIREMENT_PROOF.md`
- executed_now:
  - `pytest tests/test_ingress_retirement.py tests/test_cieplo_workflow_os_events.py -q` -> exit `0`
  - `pytest tests/test_workflow_e2e_mocked.py -q` -> exit `1`
- classification_notes:
  - current mocked E2E is not usable as proof because it fails during collection on circular import before any scenario runs
  - no fresh live end-to-end success was proven in this batch

### LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY

- final_test_status: `[UNIT_COVERED]`
- direct_unit:
  - `gmail-agent/tools/gmail_audit/tests/test_divergence_loop.py`
  - `gmail-agent/tools/gmail_audit/tests/test_operator_action_connection_ownership_postgres.py`
  - `gmail-agent/tools/gmail_audit/tests/test_d1_mutating_routes_auth_gate.py`
- integration: none found
- end_to_end: none found
- classification_notes:
  - unit-only coverage for candidate creation / review boundaries; no end-to-end closed-loop learning proof found

### GMAIL-SIGNAL-WORKER-LOOP

- final_test_status: `[UNIT_COVERED, INTEGRATION_COVERED, CHAOS_COVERED, PROOF_ONLY]`
- direct_unit:
  - `gmail-agent/tools/gmail_audit/tests/test_signal_worker.py`
  - `gmail-agent/tools/gmail_audit/tests/test_signal_adapters.py`
  - `gmail-agent/tools/gmail_audit/tests/test_signal_runtime_settings.py`
  - `gmail-agent/tools/gmail_audit/tests/test_gmail_ingress_guard.py`
  - `gmail-agent/tools/gmail_audit/tests/test_gmail_historical_bootstrap.py`
- integration:
  - `gmail-agent/tools/gmail_audit/tests/integration/test_reconcile_full_flow.py`
- chaos:
  - `gmail-agent/tools/gmail_audit/tests/chaos/test_db_outage.py`
- proof_or_ops:
  - `gmail-agent/deploy/p0-vps-rollout.sh`
  - `gmail-agent/scripts/vps-signal-worker-soak-deploy.sh`
  - `gmail-agent/scripts/apply_worker_heartbeat_ddl.py`
- executed_now:
  - bounded pytest batch including unit/integration/chaos subset -> exit `0`

### GMAIL-RECONCILE-MODE-DISPATCH

- final_test_status: `[UNIT_COVERED]`
- direct_unit:
  - `gmail-agent/tools/gmail_audit/tests/test_signal_reconciler_runtime.py`
  - `gmail-agent/tools/gmail_audit/tests/test_signal_reconciler_agent_pr_d.py`
  - `gmail-agent/tools/gmail_audit/tests/test_process_snapshot_runtime_spine.py`
  - `gmail-agent/tools/gmail_audit/tests/test_agent_primary_mode_pr_f.py`
  - `gmail-agent/tools/gmail_audit/tests/test_digital_twin_cel_radlin_dod.py`
- integration_or_e2e: none found

### CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF

- final_test_status: `[UNIT_COVERED, PROOF_ONLY]`
- direct_unit:
  - `gmail-agent/tools/gmail_audit/tests/test_signal_reconciler_agent_pr_d.py`
  - `gmail-agent/tools/gmail_audit/tests/test_agent_pr_a_b_complete.py`
  - `gmail-agent/tools/gmail_audit/tests/test_registry_store_fallback_guard.py`
  - `gmail-agent/tools/gmail_audit/tests/test_slice2b1_feed_correctness.py`
- proof:
  - `gmail-agent/tools/gmail_audit/scripts/registry_store_fallback_guard_proof.py`

### AGENT-GRAPH-EXECUTE-RUN

- final_test_status: `[UNIT_COVERED, PROOF_ONLY]`
- direct_unit_or_contract:
  - `gmail-agent/tools/gmail_audit/tests/test_agent_mcp_pr_g.py`
  - `gmail-agent/tools/gmail_audit/tests/test_agent_pr_c_complete.py`
  - `gmail-agent/tools/gmail_audit/tests/test_agent_run_turn_journal_fallback_guard.py`
  - `gmail-agent/tools/gmail_audit/tests/test_engagement_snapshot_v2_contract.py`
  - `gmail-agent/tools/gmail_audit/tests/test_s2_identity_proof_generator.py`
- proof:
  - `gmail-agent/tools/gmail_audit/build_s2_identity_proof.py`
  - `gmail-agent/tools/gmail_audit/scripts/agent_run_turn_journal_fallback_guard_proof.py`

### AGENT-GRAPH-TURN-LOOP

- final_test_status: `[UNIT_COVERED, INTEGRATION_COVERED, CHAOS_COVERED]`
- direct_unit_or_contract:
  - `gmail-agent/tools/gmail_audit/tests/test_agent_graph_engine.py`
  - `gmail-agent/tools/gmail_audit/tests/test_agent_planner_endpoints.py`
  - `gmail-agent/tools/gmail_audit/tests/test_tool_reachability_contract.py`
  - `gmail-agent/tools/gmail_audit/tests/test_constitution.py`
  - `gmail-agent/tools/gmail_audit/tests/test_deepseek_agent_planner.py`
  - `gmail-agent/tools/gmail_audit/tests/test_planner_followup_contract.py`
  - `gmail-agent/tools/gmail_audit/tests/test_agent_episodic_memory.py`
- integration:
  - `gmail-agent/tools/gmail_audit/tests/integration/test_agent_e2e_flow.py`
- chaos:
  - `gmail-agent/tools/gmail_audit/tests/chaos/test_llm_timeout.py`
- false_positive_candidates_excluded:
  - `gmail-agent/tools/gmail_audit/tests/fixtures/measurement_contract_v1/*.json`

### HITL-PROPOSAL-APPROVAL-DUAL-PATH

- final_test_status: `[UNIT_COVERED, PROOF_ONLY]`
- direct_unit:
  - `gmail-agent/tools/gmail_audit/tests/test_agent_hitl_bridge.py`
  - `gmail-agent/tools/gmail_audit/tests/test_ai_native_v1_runtime.py`
  - `gmail-agent/tools/gmail_audit/tests/test_auth02_auth03_mutation_gate.py`
  - `gmail-agent/tools/gmail_audit/tests/test_daszek_bridge_queue_drain.py`
  - `gmail-agent/tools/gmail_audit/tests/test_materialize_approve_harness.py`
  - `gmail-agent/tools/gmail_audit/tests/test_os_event_w0.py`
- proof:
  - `test_materialize_approve_harness.py` acts as harness-style proof of side-effect reachability

### CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP

- final_test_status: `[UNIT_COVERED, SYNTHETIC_ONLY]`
- direct_unit_or_contract:
  - `gmail-agent/tools/gmail_audit/tests/test_search_rag_knowledge_tool.py`
  - `gmail-agent/tools/gmail_audit/tests/test_agent_graph_engine.py`
  - `gmail-agent/tools/gmail_audit/tests/test_constitution.py`
  - `gmail-agent/tools/gmail_audit/tests/test_deepseek_agent_planner.py`
  - `gmail-agent/tools/gmail_audit/tests/test_planner_followup_contract.py`
  - `gmail-agent/tools/gmail_audit/tests/test_eval_final_rescore.py`
- executed_now:
  - included in bounded pytest batch -> exit `0`
- classification_notes:
  - discovered coverage is tool/contract/planner-side and synthetic; no fresh proof of a live `query_anything` producer path

### CALENDAR-TWO-WORLDS-OF-VISITS

- final_test_status: `[UNIT_COVERED, SYNTHETIC_ONLY]`
- direct_unit:
  - `gmail-agent/tools/gmail_audit/tests/test_action_planner_contract.py`
  - `gmail-agent/tools/gmail_audit/tests/test_calendar_case_boundary.py`
  - `gmail-agent/tools/gmail_audit/tests/test_rc_d2_commitment_gating.py`
  - `gmail-agent/tools/gmail_audit/tests/test_split_conflicting_facts_tiebreak.py`
- classification_notes:
  - all found coverage is in-memory or mocked boundary testing; no live Google Calendar integration proof in this batch

### DASZEK-COMMAND-OUTBOX-DRAIN

- final_test_status: `[UNIT_COVERED, PROOF_ONLY]`
- direct_unit:
  - `gmail-agent/tools/gmail_audit/tests/test_daszek_bridge_queue_drain.py`
  - `gmail-agent/tools/gmail_audit/tests/test_daszek_client.py`
  - `gmail-agent/tools/gmail_audit/tests/test_bridge_action_decision.py`
  - `gmail-agent/tools/gmail_audit/tests/test_worker_bridge_drain.py`
  - `gmail-agent/tools/gmail_audit/tests/test_agent_hitl_bridge.py`
- proof:
  - `gmail-agent/tools/gmail_audit/scripts/bridge_outbox_replay_safety_proof.py`
  - `gmail-agent/tools/gmail_audit/scripts/daszek_local_133_proof.py`
- executed_now:
  - included in bounded pytest batch -> exit `0`

### DASZEK-FEED-PUSH-NO-RETRY

- final_test_status: `[UNIT_COVERED, CHAOS_COVERED, PROOF_ONLY]`
- direct_unit:
  - `gmail-agent/tools/gmail_audit/tests/test_daszek_v3_feed_runtime.py`
  - `gmail-agent/tools/gmail_audit/tests/test_daszek_engagement_feed_pr_e_complete.py`
  - `gmail-agent/tools/gmail_audit/tests/test_gmail_os_event_telemetry.py`
  - `gmail-agent/tools/gmail_audit/tests/test_materialize_approve_harness.py`
  - `gmail-agent/tools/gmail_audit/tests/test_signal_worker.py`
- chaos:
  - `gmail-agent/tools/gmail_audit/tests/chaos/test_daszek_503.py`
- proof:
  - `gmail-agent/tools/gmail_audit/scripts/daszek_local_133_proof.py`
- executed_now:
  - bounded pytest batch including `tests/chaos/test_daszek_503.py` -> exit `0`

### RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE

- final_test_status: `[UNIT_COVERED, INTEGRATION_COVERED, PROOF_ONLY]`
- direct_unit:
  - `rag-chat-asystent/backend/tests/unit/test_handle_chat_message_use_case.py`
  - `rag-chat-asystent/backend/tests/unit/test_handle_chat_kb_used_contexts.py`
  - `rag-chat-asystent/backend/tests/unit/test_intent_router.py`
  - `rag-chat-asystent/backend/tests/unit/test_node_b_read.py`
- integration_or_pipeline:
  - `rag-chat-asystent/backend/tests/test_ingest_delta_guard.py`
  - `rag-chat-asystent/backend/tests/test_ingest_etap6.py`
  - `rag-chat-asystent/backend/tests/test_ingest_gold_determinism.py`
  - `rag-chat-asystent/backend/tests/test_ingest_gold_smoke.py`
  - `rag-chat-asystent/backend/tests/test_ingest_ocr_fallback.py`
  - `rag-chat-asystent/dev/tests/backend/test_ingest.py`
  - `rag-chat-asystent/dev/tests/backend/test_ingest_jobs.py`
  - `rag-chat-asystent/dev/tests/backend/test_ingest_jobs_job_id_status.py`
- proof:
  - `rag-chat-asystent/scripts/rag_d1_boundary_proof.py`
- executed_now:
  - `pytest backend/tests/unit/test_handle_chat_message_use_case.py -q` -> exit `0`

### SLA-WATCHER-DECISION-ESCALATION

- final_test_status: `[UNIT_COVERED, SYNTHETIC_ONLY]`
- direct_unit:
  - `gmail-agent/tools/gmail_audit/tests/test_sla_watcher.py`
- classification_notes:
  - queue fetch is mocked; no scheduler-triggered integration proof found

## False Positives

- `gmail-agent/tools/gmail_audit/tests/fixtures/measurement_contract_v1/*.json` are fixtures, not tests
- `kalk-top/core/application/harness/harness-lib.php` is a helper, not a test
- `rag-chat-asystent/backend/tests/conftest.py` is test wiring, not a proof item
- `kalk-top/docs/runbooks/*.md`, `top-instal-generator/docs/*.md`, and `cieplo-orchestrator/docs/*.md` are documentary evidence, not executable test coverage
- `fast-kalk/scripts/configure-local.php` is environment bootstrap, not proof

## Unresolved

- `fast-kalk` still lacks a direct unit/integration test file for the full lead -> calculate -> register -> dispatch chain; only proof/harness scripts were found
- `cieplo-orchestrator/tests/test_workflow_e2e_mocked.py` is present but currently non-executable because collection fails on circular import before scenario runtime
- `kalk-top` has stronger end-to-end assets on disk than were freshly executed here; live browser/REST proof remains environment-gated
- `top-instal-generator` has a green smoke harness, but no direct unit/integration suite was found for the workflow surface itself

## Runtime Classification

- freshly_proven_locally:
  - `GMAIL-SIGNAL-WORKER-LOOP` (bounded test batch)
  - `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP` (tool contract batch)
  - `DASZEK-COMMAND-OUTBOX-DRAIN` (bounded test batch)
  - `DASZEK-FEED-PUSH-NO-RETRY` (bounded test batch including chaos)
  - `RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE` (unit batch)
  - `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT` (smoke proof)
  - `KALK-TOP-CALCULATE-OFFER-PIPELINE` (JS regression slice)
  - `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL` unit/event slice only, not end-to-end
- implemented_in_code_but_not_freshly_proven_end_to_end:
  - `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`
  - `GMAIL-RECONCILE-MODE-DISPATCH`
  - `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
  - `AGENT-GRAPH-EXECUTE-RUN`
  - `AGENT-GRAPH-TURN-LOOP`
  - `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
  - `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
  - `CALENDAR-TWO-WORLDS-OF-VISITS`
  - `SLA-WATCHER-DECISION-ESCALATION`

## Evidence IDs

- existing evidence referenced: `EV-00139`, `EV-00181`, `EV-00182`, `EV-00186`
- new evidence reserved for this artifact: `EV-00187`
