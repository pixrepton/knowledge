# Table Write ↔ Table Reader Cross Reference

- Timestamp: `2026-07-30 18:08:36 +02:00`
- Working directory: `C:\Users\compg\Desktop\top-code workspace\gmail-agent`
- Repo / SHA: `gmail-agent` @ `468d37ee6553b39bf6009939e9c87c13f3c183c7`
- Scope: all table definitions and table-touching writer/reader paths under `tools/gmail_audit` needed for active AI-OS workflow reconstruction, including `mailbox_memory`, `correlation_registry`, `agent_runtime`, `business_dictionary`, `event_spine`, `graph_store`, `operator_memory`.
- Exclusions: tests, fixtures, `__pycache__`, docs-only prose, deploy proof scripts as product writers/readers, in-memory test stores except where needed to confirm intended contract shape.

## Commands

```powershell
rg -l "CREATE TABLE" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit" -g "!**/__pycache__/**" -g "!**/tests/**"
```

Exit code: `0`

```powershell
rg -n "CREATE TABLE|CREATE INDEX|ALTER TABLE|INSERT INTO|DELETE FROM|SELECT .* FROM|UPDATE .* SET" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\business_dictionary" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\correlation_registry" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\mailbox_memory" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\agent_runtime" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\graph_store.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\operator_memory.py" -g "!**/__pycache__/**"
```

Exit code: `0`

```powershell
rg -n "^def |^class " "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\mailbox_memory\postgres.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\correlation_registry\store.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\agent_runtime\store.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\agent_runtime\checkpoint.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\agent_runtime\turn_journal.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\agent_runtime\jobs.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\divergence_loop.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\world_model.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\business_dictionary\store.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\business_dictionary\graph_store.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\event_spine\store.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\event_spine\emitter.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\event_spine\query.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\operator_memory.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\graph_store.py"
```

Exit code: `0`

```powershell
rg -n "PostgresMailboxMemoryStore\(|build_registry_store\(|publish_os_event\(|build_event_spine_store\(|record_handler_effect\(|upsert_term\(|process_outbox\(|AgentRunCheckpointStore|record_completed\(|fetch_learning_candidates\(|fetch_world_model_precedent_refs\(|fetch_similar_case_precedent_refs_v1\(" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit" -g "!**/tests/**"
```

Exit code: `0`

## Full Inventory

Legend:

- `SoT`: canonical durable source for this concern.
- `Projection`: derivative snapshot / view / convenience read model.
- `Audit`: append-only or write-only durable evidence / history.
- `Manual`: reachable only from CLI / operator / explicit maintenance path.
- `Conditional`: real code path exists, but only when a feature/mode/runtime branch is enabled.
- `MISSING_PRODUCER`: reader exists or table is designed for use, but no live producer was found.
- `SCHEMA_ONLY_DEAD`: DDL exists, but no writer or reader exists in product code.

### Correlation Registry

| Table | Create / migration symbol | Writer symbols | Reader symbols | Classification | Reachability |
|---|---|---|---|---|---|
| `_schema_version` | `correlation_registry/schema.py::CORRELATION_REGISTRY_MIGRATIONS`, `apply_correlation_registry_migrations` | `apply_correlation_registry_migrations` | `apply_correlation_registry_migrations` | `Migration-only` | bookkeeping table only; not product state |
| `topinstal_identities` | `correlation_registry/schema.py::CORRELATION_REGISTRY_SCHEMA_SQL` | `PostgresCorrelationRegistryStore.create_identity`, `merge_identity_metadata`, `update_identity_display_name`, `update_identity_primary_email`, `merge_identities` | `get_identity`, `find_identity_by_email`, `list_identities_recent`, duplicate-email helpers | `SoT` | live in entity-link / correlation flow |
| `topinstal_engagements` | same | `resolve_or_create_engagement`, `merge_engagement_metadata`, `merge_identities`, `merge_email_duplicate_group` | `get_engagement`, `find_recent_engagement_for_email`, `find_engagement_for_identity_recent`, `find_engagement_by_case_id`, `list_engagements_for_identity` | `SoT` | live in correlation + handoff |
| `correlation_links` | same | `upsert_link` via `correlation_registry/heuristics.py`, `entity_linker.py`, materialize / reconcile paths | `find_engagement_by_link`, `list_links_for_engagement`, snapshot/context pack builders, metrics SQL | `SoT` | live cross-repo identity and case linkage |
| `unified_os_events` | same | `event_spine.emitter.publish_os_event` from `api_app.py`, `agent_runtime.run.py`, `agent_runtime.materialize.py`, `agent_hitl_bridge.py`, `correlation_registry.service.py`, `sla_watcher.py`, telemetry emitters | `event_spine.query.fetch_*`, `PostgresEventSpineStore.claim_batch/get_by_id/mark_terminal`, API/event timeline readers | `Audit + queue` | live event journal; processor path is conditional |
| `event_spine_handler_effects` | same | `PostgresEventSpineStore.record_handler_effect` from `event_spine.processor` | no product reader found; only manual SQL/proof readers outside active runtime | `Audit` | conditional writer (processor enabled); write-only in product code |
| `identity_binding_suggestions` | same | `PostgresCorrelationRegistryStore.upsert_identity_binding_suggestion` via `correlation_registry/identity_binding.py` | `list_identity_binding_suggestions`, `get_identity_binding_suggestion`, `update_identity_binding_suggestion_status` | `Manual / operator queue` | real operator workflow, not automatic mainline |
| `identity_merge_log` | same | `merge_identities`, `merge_email_duplicate_group` | no product reader found | `Audit` | manual/operator audit trail |

### Agent Runtime And Learning

| Table | Create / migration symbol | Writer symbols | Reader symbols | Classification | Reachability |
|---|---|---|---|---|---|
| `operator_engagement_snapshots` | `agent_runtime/AGENT_RUNTIME_SCHEMA.sql`, migration `004_snapshot_storage_optimization.sql` | `PostgresOperatorEngagementStore.insert_snapshot`, `save_snapshot`, `soft_delete_snapshot` | `load_snapshot`, `load_snapshot_by_case_id`, `list_recent_snapshots`, `list_staging_engagement_ids` | `Projection / working SoT for operator desk` | live runtime state |
| `agent_runtime_turns` | `agent_runtime/AGENT_RUNTIME_SCHEMA.sql`, migration `002_turns_append_only.sql` | `PostgresAgentTurnJournal.append_turn` | `PostgresAgentTurnJournal.list_turns`, business pulse counters | `Audit` | live turn journal |
| `agent_run_checkpoints` | `agent_runtime/AGENT_RUNTIME_MIGRATIONS.sql`, `agent_runtime/checkpoint.py` | `AgentRunCheckpointStore.save_checkpoint` from `agent_runtime.graph.AgentGraphEngine` | `AgentRunCheckpointStore.load_latest` from `agent_runtime.run.execute_agent_run(resume_from=...)` | `Conditional recovery` | real writer and resume reader; only when checkpoint store is configured and resume path used |
| `agent_runtime_jobs` | `agent_runtime/AGENT_RUNTIME_JOBS.sql` | `PostgresAgentJobStore.record_completed` from `agent_runtime.agent_reconcile` | no product reader found | `Audit` | write-only completion log |
| `idempotency_log` | `agent_runtime/migrations/003_idempotency_log.sql`, `agent_runtime/idempotency.py::_ensure_idempotency_table` | `record_idempotency` via `_with_idempotency` in `agent_runtime/tools/write_executors.py` | `get_idempotency` via same executor wrapper | `Control / idempotency` | conditional live on write executors |
| `agent_proposal_records` | `agent_runtime/LEARNING_LOOPS_MIGRATIONS.sql` | `divergence_loop.record_agent_proposal` from `api_app.py`, `divergence_loop.process_operator_action` | `fetch_open_proposals_for_case`, `fetch_decision_queue`, candidate builders | `Learning evidence` | live |
| `operator_response_records` | same | `divergence_loop.record_operator_response` from `api_app.py`, `divergence_loop.process_operator_action` | joins in `fetch_open_proposals_for_case`, `fetch_decision_queue`, candidate builders | `Learning evidence` | live |
| `learning_rule_candidates` | same | `divergence_loop.maybe_create_learning_candidate`, `update_rule_application`, `_run_pattern_learner` | `fetch_learning_candidates`, `update_candidate_status`, `fetch_approved_rules_for_family` -> `similar_cases_precedent.fetch_learning_rule_precedent_refs` -> `mailbox_memory_runtime.fetch_similar_case_precedent_refs_v1` | `Conditional precedent store` | real conditional reader exists; not zero-consumer |
| `historical_corpus_messages` | same | `world_model.ingest_corpus_message` only | `world_model.distill_insights_from_corpus` | `MISSING_PRODUCER` | no caller of ingest function found |
| `historical_corpus_facts` | same | `world_model.ingest_corpus_fact` only | `world_model.distill_insights_from_corpus` | `MISSING_PRODUCER` | no caller of ingest function found |
| `world_model_insights` | same | `world_model.distill_insights_from_corpus`, `update_insight_status` only | `fetch_approved_insights_for_category` -> `similar_cases_precedent.fetch_world_model_precedent_refs` -> `mailbox_memory_runtime.fetch_similar_case_precedent_refs_v1`; also `fetch_insights` / `approved_insights_for_planner` manual readers | `Conditional reader + MISSING_PRODUCER` | consumer path exists; producer side is unwired |

### Business Dictionary, Graph, Operator Memory

| Table | Create / migration symbol | Writer symbols | Reader symbols | Classification | Reachability |
|---|---|---|---|---|---|
| `business_dictionary_terms` | `business_dictionary/store.py` | `upsert_term` from `business_dictionary/cli.py` import/sync flows | `search_terms` from API + CLI, `get_stats` | `Manual knowledge surface` | writer side is CLI/manual; reader side is real API/CLI |
| `sync_outbox` | `business_dictionary/store.py` | `upsert_term` / `write_outbox_entry` in same transaction as term write | `business_dictionary.graph_store.process_outbox` via `business_dictionary/cli.py::run_outbox_process_cli` only | `Manual outbox` | no scheduler/worker/cron found |
| `graph_nodes` | `graph_store.py` | `PostgresGraphStore.upsert_many` from `drive_ingest_runtime`, `signal_reconciler`, `entity_linker` | `PostgresGraphStore.fetch_case_hints` from `mailbox_memory_runtime` | `Conditional graph projection` | live when graph store is configured |
| `graph_edges` | `graph_store.py` | same as `graph_nodes` | same as `graph_nodes` | `Conditional graph projection` | live when graph store is configured |
| `operator_memory` | `operator_memory.py` | `save_conversation_turn`, `save_preference`, `save_client_context` from `api_app.py` | `get_recent_conversation`, `get_preferences`, `get_client_context`, `build_operator_context_prompt`, `get_cost_summary`, `get_decisions` | `Operator memory` | live API/operator feature |

### Mailbox Memory And Drive

| Table | Create / migration symbol | Writer symbols | Reader symbols | Classification | Reachability |
|---|---|---|---|---|---|
| `mailbox_memory_cases` | `mailbox_memory/schema.py` | `upsert_case`, `mutate_case` from `mailbox_memory_runtime`, `signal_reconciler`, `drive_ingest_runtime`, `execution_runtime`, `entity_linker`, `cieplo_orchestrator_hook` | `fetch_case`, `fetch_cases`, `fetch_case_by_message_id`, `fetch_resolved_cases_by_family_and_fact_keys` | `SoT` | live |
| `mailbox_memory_messages` | same | `upsert_message` from `mailbox_memory_runtime` | `fetch_message`, `fetch_any_message`, `fetch_messages_for_case`, `fetch_case_by_message_id` | `SoT` | live |
| `mailbox_memory_attachments` | same | `upsert_attachment` from `mailbox_memory_runtime._ingest_attachment` | direct SQL reader in `attachment_download.py`, plus document linkage by `attachment_id` | `Attachment catalog` | live |
| `mailbox_memory_documents` | same | `upsert_document` from attachment/document ingest | `fetch_documents_for_case`, direct SQL in `attachment_download.py` | `Document catalog` | live |
| `mailbox_memory_document_chunks` | same + vector DDL helper | `replace_document_chunks` from attachment/document ingest; vector-status updates | `fetch_chunks_for_case`, semantic retrieval helpers | `Retrieval cache` | live |
| `mailbox_memory_events` | same | `append_event` from `mailbox_memory_runtime` and related flows | `fetch_events_for_case`, `fetch_events`, `fetch_latest_adjudication_link_override` | `Audit / event journal` | live |
| `mailbox_memory_facts` | same | `replace_message_facts`, `append_fact_rows` | `fetch_facts_for_case`, precedent / context builders, calendar risk | `Fact SoT` | live; agent-tool path has separate supersession issue already filed |
| `mailbox_memory_snapshots` | same | `upsert_snapshot` from `mailbox_memory_runtime`, `signal_reconciler`, `drive_ingest_runtime` | `fetch_snapshot` | `Projection` | live |
| `mailbox_memory_thread_memory` | same | `upsert_thread_memory` from `mailbox_memory_runtime` | `fetch_thread_memory` | `Projection / cache` | live |
| `mailbox_memory_next_actions` | same | `upsert_next_action` from `mailbox_memory_runtime`, `signal_reconciler` | `fetch_next_action` from runtime, feed, rebuilders | `Projection` | live |
| `mailbox_memory_case_snapshot_versions` | same | `append_case_snapshot_version` from `case_snapshot_manager` | `fetch_case_snapshot_versions`, `fetch_latest_case_snapshot_version` from case/feed rebuild paths | `Audit / history` | live |
| `company_drive_documents` | same | `upsert_drive_document` from `drive_ingest_runtime` | `fetch_drive_documents_for_case`, `fetch_drive_documents`, `fetch_drive_document_by_item_id` | `Conditional reference store` | live when Drive ingest is enabled |
| `company_drive_document_chunks` | same + vector DDL helper | `replace_drive_document_chunks`, `_propagate_drive_document_case_id_to_chunks` from Drive ingest | `fetch_drive_chunks_for_case`, semantic candidate fetchers | `Conditional retrieval cache` | live when Drive ingest is enabled |
| `company_drive_facts` | same | `replace_drive_document_facts` from Drive ingest | `fetch_drive_facts_for_case`, `fetch_drive_facts_for_document` | `Conditional fact store` | live when Drive ingest is enabled |
| `drive_ingest_runs` | same | `upsert_drive_ingest_run` from `drive_ingest_runtime` | no repo reader found | `Audit` | write-only run log |
| `mailbox_memory_raw_observations` | same | `append_raw_observation` from `raw_observation_journal`, `calendar_runtime`, other signal adapters | `fetch_raw_observation`, `fetch_raw_observation_by_source_fingerprint`, `fetch_raw_observations_for_source` | `Raw observation journal` | live |
| `mailbox_memory_signals` | same + migration `AGENT_RUNTIME_MIGRATIONS.sql` | `append_signal` from `signal_journal`, `calendar_runtime` and other signal adapters; `patch_signal_engagement_id` on reconcile | `fetch_signal`, `fetch_signal_by_idempotency_key`, `fetch_signals_for_case`, `fetch_signals_for_source` | `Signal SoT` | live |
| `mailbox_memory_signal_processing_attempts` | same | `append_signal_processing_attempt` from `signal_journal` | `fetch_signal_processing_attempts` | `Audit` | live |
| `mailbox_memory_source_cursors` | same | `upsert_source_cursor` from `gmail_change_detector`, `drive_change_detector`, `gmail_historical_bootstrap` | `fetch_source_cursor`, `list_source_cursors` | `Control / cursor state` | live |
| `mailbox_memory_action_proposals` | same | `execution_runtime.create_action_proposal` and related helpers | `fetch_action_proposal`, `fetch_action_proposals` from execution/runtime/feed/analytics | `Legacy-but-live proposal store` | live |
| `mailbox_memory_policy_decisions` | same | `agent_runtime.policy_action_spine` | `fetch_policy_decision`, `fetch_policy_decisions` | `Policy decision store` | live |
| `mailbox_memory_action_proposals_v2` | same | `agent_runtime.policy_action_spine` | `fetch_action_proposal_v2`, `fetch_action_proposals_v2` | `Policy-gated proposal store` | live |
| `mailbox_memory_execution_results` | same | `execution_runtime`, `agent_hitl_bridge` | `fetch_execution_results` from feed/runtime/analytics | `Execution result store` | live |
| `mailbox_memory_calendar_events` | same | `calendar_runtime.upsert_calendar_event` | `fetch_calendar_events_for_case` from calendar context, feed, mailbox context | `Calendar projection` | live conditional on calendar ingest |
| `mailbox_memory_calendar_case_links` | same | `calendar_runtime.upsert_calendar_case_link` | no product reader found | `Auxiliary audit` | stores link reasons, but active readers use `mailbox_memory_calendar_events` only |
| `mailbox_memory_document_intelligence_results` | same | `mailbox_memory_runtime`, `drive_ingest_runtime`, `gmail_intake` via `upsert_document_intelligence_result` | `fetch_document_intelligence_for_case` from mailbox context / projection builders | `Document-intelligence projection` | live |
| `mailbox_memory_document_extracted_fields` | same | child writes inside `upsert_document_intelligence_result` | child reads inside `fetch_document_intelligence_for_case` | `Child projection table` | live |
| `mailbox_memory_document_conflicts` | same | none found | none found | `SCHEMA_ONLY_DEAD` | conflict data is kept in `mailbox_memory_document_intelligence_results.conflicts` and snapshot/projection code, not in this table |

## False Positives / Adjudication Notes

- `agent_runtime/idempotency.py` contains a dynamic `CREATE TABLE IF NOT EXISTS {IDEMPOTENCY_LOG_TABLE}` string; naive regex incorrectly extracts a fake table name `IF`. Real table is `idempotency_log`.
- Simple `INSERT/SELECT/UPDATE/DELETE` greps undercount multiline SQL readers for some tables (`agent_run_checkpoints`, `agent_proposal_records`, `graph_nodes`, `graph_edges`), so final classification was made from symbol-level code reads, not line-token heuristics alone.
- `mailbox_memory_calendar_case_links` is not a missing writer; it is definitely written from `calendar_runtime`. The only open question was whether it has a product reader; no such reader was found.

## Key Findings

1. `business_dictionary.sync_outbox` is a real same-transaction outbox writer attached to `upsert_term`, but its consumer is CLI-only (`run_outbox_process_cli` -> `process_outbox`); no scheduler, worker, or cron was found.
2. `learning_rule_candidates` and `world_model_insights` both have real reader-side precedent hooks through `similar_cases_precedent.py` -> `mailbox_memory_runtime.py`; the older "zero consumer / complete orphan" wording is too strong.
3. The actual producer-side gap sits on `historical_corpus_messages`, `historical_corpus_facts`, and `world_model_insights`: the ingest/distill/update functions exist, but no caller of those producer functions was found.
4. `mailbox_memory_document_conflicts` is the only confirmed schema-only dead table in this pass.
5. The following tables are one-sided by design, not by missing SQL code: `agent_runtime_jobs`, `drive_ingest_runs`, `event_spine_handler_effects`, `identity_merge_log`, `mailbox_memory_calendar_case_links`.

## Unresolved

- No unresolved table remained after adjudicating writer/reader reachability; the remaining ambiguities are classification-level only (`mailbox_memory_calendar_case_links` is treated here as auxiliary audit rather than a formal defect).

## Evidence IDs

- Planned closeout evidence for this inventory: `EV-00181`
