# Raw inventory — status value ↔ writer ↔ consumer (reverse-audit category 8)

Generated during the mechanical reverse-audit pass on 2026-07-30.

## Working directory

`C:\Users\compg\Desktop\top-code workspace`

## Repo SHA

- `knowledge`: `597b1091a296930ed32afb379ec19b8ab425d4fa`
- `gmail-agent`: `468d37ee6553b39bf6009939e9c87c13f3c183c7`
- `cieplo-orchestrator`: `e68f05386722b4034ca36bd39d169eba759f44e6`
- `kalk-top`: `9d56055be7f293ad17ffb624abc178617f46f5be`
- `top-instal-generator`: `7e5279551b3919b7ab84547227b3355f45c44bf4`

## Timestamp

`2026-07-30 20:35:08 +02:00`

## Scope

Static status-contract audit only:

- status definition
- writer
- transition
- persistence
- reader / consumer
- terminal meaning
- retry / recovery

Covered families:

- signal processing attempts
- case status
- engagement operational / HITL / materialize
- execution results
- Gmail send
- calendar vs `scheduled_visit`
- facts
- documents / drive ingest
- proposals
- Daszek bridge queue
- learning candidates
- world model insights
- Cieplo workflow / ingress
- event spine
- Business Dictionary outbox
- OfferDTO / generator / pricing fallback

## Exclusions

- no renewed handoff validation
- no renewed workspace orientation
- no return to reverse-audit category 7 or closed domains
- no full call-graph re-trace; only symbols needed to map status contracts
- no runtime mutation / no live side-effect execution
- no category 9+ work in this artifact

## Exact commands

All commands executed from `C:\Users\compg\Desktop\top-code workspace`.

```text
[0] rg -n "infer_case_status|infer_lifecycle_from_case_status|finalize_case|status = infer_case_status|lifecycle_state =" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\mailbox_memory_runtime.py"
[0] rg -n "stale|dormant|archived|pattern_candidate" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\divergence_loop.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\api_app.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\similar_cases_precedent.py"
[0] rg -n "skipped_policy|extraction_status|linkage_status" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\drive_ingest_runtime.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\drive_ingest_models.py"
[0] Get-Content 'C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\mailbox_memory_runtime.py' | Select-Object -Index (2050..2088)
[0] Get-Content 'C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\drive_ingest_runtime.py' | Select-Object -Index (680..845)
[0] Get-Content 'C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\pattern_learner.py' | Select-Object -Index (1..260)
[0] Get-Content 'C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\drive_ingest_runtime.py' | Select-Object -Index (2096..2122)
[0] rg -n "learning_rule_candidates|status\s*=\s*%s|fetch_approved_rules_for_family|pending_operator|pattern_candidate|approved|rejected|stale|dormant|archived" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\divergence_loop.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\api_app.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\similar_cases_precedent.py"
[0] rg -n "world_model_insights|pending_operator|approved|rejected|update_insight_status|fetch_approved_insights_for_category|approved_insights_for_planner" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\world_model.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\mailbox_memory_runtime.py"
[0] Get-Content 'C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\divergence_loop.py' | Select-Object -Index (250..690)
[0] rg -n "distill_insights_from_corpus\(|update_insight_status\(|fetch_approved_insights_for_category\(|approved_insights_for_planner\(" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit"
[0] Get-Content 'C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\api_app.py' | Select-Object -Index (1198..1260)
[0] rg -n "skipped_policy|removed" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit"
[0] rg -n "FAILED_FINAL|FAILED_RETRYABLE|retry_workflow|should_retry_workflow|should_skip_message_id" "C:\Users\compg\Desktop\top-code workspace\cieplo-orchestrator\src\topinstal_cieplo_worker"
[1] rg -n "decision_status=\"executed\"|bounded_dry_run|outcome_unknown|accepted|executing|execution_status = \"blocked\"|execution_status = \"skipped\"|proposal.status = \"executed\"|proposal.status = \"blocked\"" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\hitl_gmail_send.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\agent_hitl_bridge.py" "C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit\execution_runtime.py"
[0] rg -n --glob '*.php' --glob '*.py' "status|mode|degraded|fallback-docx|success|error|failed|completed|pending" "C:\Users\compg\Desktop\top-code workspace\top-instal-generator"
[0] rg -n --glob '*.php' --glob '*.py' "status|mode|success|error|failed|completed|pending|OfferDTO" "C:\Users\compg\Desktop\top-code workspace\kalk-top"
[0] Get-Content 'C:\Users\compg\Desktop\top-code workspace\top-instal-generator\core\application\GenerateOfferDocumentUseCase.php' | Select-Object -Index (60..230)
[0] Get-Content 'C:\Users\compg\Desktop\top-code workspace\kalk-top\core\application\CalculateOfferUseCase.php' | Select-Object -Index (160..190)
[0] Get-Content 'C:\Users\compg\Desktop\top-code workspace\kalk-top\core\domain\pricing\PricingEngine.php' | Select-Object -Index (30..60)
[0] Get-Date -Format 'yyyy-MM-dd HH:mm:ss K'
[0] git -C 'C:\Users\compg\Desktop\top-code workspace\knowledge' rev-parse HEAD
[0] git -C 'C:\Users\compg\Desktop\top-code workspace\gmail-agent' rev-parse HEAD
```

## Full status-family inventory

| Family | Full status values | Writer(s) | Reader / consumer(s) | Transition meaning / terminal meaning | Runtime classification | Retry / recovery |
|---|---|---|---|---|---|---|
| Signal processing attempts | `started`, `reconciled`, `shadowed`, `skipped_duplicate`, `failed` | `signal_reconciler.reconcile_signal` via `SignalJournal.record_processing_attempt` | audit / journal readers only re-confirmed here; product consumer not retraced in this category | `started` is written before dispatch; success writes handler `processing_state`; exception writes terminal `failed` | `LIVE_AUDIT_STATUS` | no automatic retry found at attempt-status layer; replay remains manual |
| Case row status | `awaiting_review`, `awaiting_reply`, `active`, `waiting`, `open`; lifecycle mapping `qualification`, `waiting_for_client`, `new_lead` | `mailbox_memory_runtime.finalize_case` via `infer_case_status` + `infer_lifecycle_from_case_status` | snapshot / context-pack builders; existing known mismatch consumer `get_win_rate` expects `won` | non-terminal operational snapshot only; `waiting` is the only status mapped out of `qualification`; default falls back to `open` | `LIVE_WRITER_LIVE_READER` with known downstream vocabulary drift outside this category | later reconcile rewrites the same row; no dedicated retry state |
| Engagement operational status | `raw_inquiry`, `enriching`, `ready_for_quote`, `pending_operator`, `node_a_error` | tool handlers (`request_operator_clarification`, `request_human_handoff`, `report_gaps_and_stop`, `_proposal_result`, `call_kalk_top_quote`), `AgentMcpService.approve_hitl_action` | `AgentGraphEngine._is_loop_terminal`, Daszek frontend labels, feed snapshot readers | `pending_operator` is loop-terminal and HITL-blocking; `ready_for_quote` re-opens execution path; `node_a_error` remains terminal in graph loop | `LIVE_CONTROL_STATUS` | recovery is another approve / agent turn; no autonomous retry |
| HITL send state cache | `accepted`, `executing`, `executed`, `outcome_unknown` | `agent_hitl_bridge.execute_hitl_send_from_bridge_row` helpers on `_HITL_SEND_STATE_KEY` | same bridge executor on replay / duplicate call; execution-attention projection for `outcome_unknown` | `accepted -> executing -> executed|outcome_unknown`; terminal cache survives restarts | `LIVE_RECOVERY_STATE_MACHINE` | duplicate call polls 2s for terminal state; `outcome_unknown` deliberately not auto-retried |
| Gmail send `decision_status` | `accepted`, `executed`, `failed_before_execution`, `outcome_unknown` plus `mode=bounded_dry_run|live` | `approve_hitl_engagement` writes `accepted`; `execute_hitl_gmail_send` writes execution statuses | `_persist_hitl_send_result`, bridge replay logic, Daszek/UI responses | dry-run and real send both use `decision_status="executed"`; only `mode` disambiguates; `outcome_unknown` means side effect may already have started | `LIVE_AMBIGUOUS_STATUS` | recovery handled by cached HITL send state, not by `decision_status` alone |
| Materialize proposal status | `pending`, `approved`, `rejected` | `append_materialize_proposal` creates `pending`; `approve_materialize_proposal` patches `approved` after side effect | materialize approve route and snapshot readers | `pending` is the only executable state; `approved` is terminal receipt; `rejected` exists in schema only in this audit | `LIVE_PARTIAL_STATUS_FAMILY` | if CAS/save fails after side effect, proposal can remain `pending`; no confirmed reject route |
| `execution_runtime.ActionProposal.status` + `ExecutionResult.execution_status` | proposal: `proposed`, `approved`, `rejected`, `executed`, `failed`, `blocked`; result: `executed`, `failed`, `blocked`, `skipped` | `create_action_proposal`, `approve_action_proposal`, `reject_action_proposal`, `execute_action_proposal` | bridge-drain and CLI paths; downstream readers not exhaustively retraced here | terminal effect is often recorded only in `ExecutionResult`: dry-run `create_calendar_event` and Gmail label/archive can end as `execution_status="skipped"` while proposal stays `approved`; exceptions can leave proposal `approved` with result `failed` | `LIVE_SPLIT_STATUS_MODEL` | retry remains possible from proposal rows that never advance past `approved`; recovery semantics are per caller |
| Calendar vs text `scheduled_visit` | real calendar path has no shared status field in this family; text fact path writes fact value only; execution result for `create_calendar_event` uses `skipped|blocked|executed` | `CalendarRuntime.ingest_events`, `execute_schedule_visit`, `execute_action_proposal(create_calendar_event)` | calendar readers, planner blockers, downstream fact readers | there is no unified status contract between ingested calendar events and text `scheduled_visit`; calendar executor status lives in `ExecutionResult`, while `scheduled_visit` is only a fact payload | `LIVE_SPLIT_MODEL_WITH_MISSING_PRODUCER` | `create_calendar_event` retry depends on proposal path; `scheduled_visit` just rewrites fact text |
| Facts status | mailbox facts row default `active`; context-pack normalizes `active -> inferred`; conflict/gap surfaces use `confirmed`, `inferred`, `disputed`, `stale`, `rejected`, `unproven`, `weak_evidence`, `new` in projections | `mailbox_memory_runtime` writes row status `active`; projection builders synthesize projection-only statuses | `case_context_contract` consumers, snapshot builders | only `active` is a durable fact-row state confirmed here; richer statuses are projection-layer evidence classifications, not storage lifecycle states | `LIVE_STORAGE_PLUS_PROJECTION_STATUS` | projection recomputed on rebuild; no fact-row retry state |
| Mailbox / Drive document ingest | mailbox extraction: parser-origin statuses including `pending`, `ok`, `archive_container`, `unsupported_mime`, `failed`, `empty`; drive persisted extraction: `pending`, `extracted`, `empty`, `blocked`, `failed`, `skipped_folder`, `skipped_binary`, `skipped_policy`; drive linkage: `deterministic`, `inferred_high`, `inferred_medium`, `unresolved_candidate`, `removed` | mailbox: `mailbox_memory_runtime._build_documents_for_attachment`; drive: `DriveIngestRuntime._extract_candidate_content`, `map_extraction_status`, `process_removed_item` | `case_context_contract` reads parser / embedding / linkage status into context-pack summaries | `skipped_policy` and `removed` are written into persisted drive payloads even though the declared literal sets in `drive_ingest_models.py` do not include them; `skipped_policy` is terminal skip-by-policy, `removed` is terminal removal tombstone | `LIVE_CONTRACT_DRIFT` | later change-detection / reingest may replace rows; no dedicated repair state beyond new ingest run |
| Daszek bridge queue | live JSONL path: `pending`, `completed`, `failed`, `skipped`; dormant DB outbox sibling: `pending`, `retry`, `leased`, `completed`, `failed`, `skipped`, `dead_letter` | Daszek PHP appenders write `pending`; completion endpoints / Node-B drain write terminal states | `daszek_v2_bridge_queue_pending_rows`, completion summary, gmail-agent drain | live path treats `completed|failed|skipped` as equally terminal; only `pending` feeds further action | `LIVE_TERMINAL_WITHOUT_RETRY` on JSONL path; `DORMANT_RICHER_STATE_MACHINE` on DB path | JSONL path has no requeue / dead-letter; DB path has richer recovery semantics but no live feeder confirmed |
| Learning rule candidates | `pending_operator`, `approved`, `rejected`, `stale`, `dormant`, `archived`, `pattern_candidate` | `maybe_create_learning_candidate` writes `pending_operator` and auto-approve to `approved`; `update_candidate_status` writes `approved|rejected`; `pattern_learner.store_pattern_candidates` writes `pattern_candidate` | operator list/update API; `fetch_approved_rules_for_family`; `similar_cases_precedent` ignores `rejected|stale` | `pending_operator -> approved|rejected` is the live review path; `pattern_candidate` is a separate live writer branch; `stale/dormant/archived` were not found as live writers in this pass | `LIVE_MIXED_STATUS_FAMILY` | approval / rejection is manual; no automatic revival found for stale/dormant/archived |
| World model insights | `pending_operator`, `approved`, `rejected` | `distill_insights_from_corpus` inserts `pending_operator`; `update_insight_status` writes `approved|rejected` | `fetch_approved_insights_for_category`, `approved_insights_for_planner`, precedent enrichment | reader side is real; producer / status-update side has zero callers outside `world_model.py` in this audit | `READER_WIRED_PRODUCER_UNWIRED` | no live recovery trigger found because producer path itself is unwired |
| Cieplo workflow + ingress | workflow: `RECEIVED`, `FETCHED`, `PARSED`, `MAPPED_TO_CALC`, `CALCULATED`, `MAPPED_TO_GENERATOR`, `DOCUMENT_REQUESTED`, `PDF_READY`, `EMAIL_SENT`, `DONE`, `FAILED_RETRYABLE`, `FAILED_FINAL`; ingress: `NEW`, `DETECTED`, `PARSED`, `VALIDATED`, `DISPATCHED`, `PROCESSED_SUCCESS`, `PROCESSED_ERROR`, `VALIDATION_ERROR`, `PARSE_ERROR`, `IGNORED_NO_MATCH`, `IGNORED_DUPLICATE` | repository `create_workflow` / `transition`; runner writes failure states; ingress processor writes ingress statuses | retry API, `should_retry_workflow`, `should_skip_message_id`, event-spine workflow event mapper | `FAILED_FINAL` is still accepted by both manual retry API and `should_retry_workflow`; `PDF_READY` is also retryable; ingress terminality is separate from workflow_state terminality | `LIVE_TERMINAL_LABEL_DRIFT` | manual retry exists for `FAILED_RETRYABLE`, `FAILED_FINAL`, `PDF_READY`; no autonomous scheduler confirmed |
| Event spine | `pending`, `processing`, `processed`, `failed`, `skipped`; processor mode `off`, `shadow`, `active` | `event_spine.store.claim_batch`, `mark_terminal`, `EventProcessor.run_batch` | handler registry / CLI processor / store readers | `pending|failed -> processing -> processed|failed|skipped`; terminal states are explicit and durable | `LIVE_CLI_GATED_STATE_MACHINE` | retry occurs by reclaiming `failed` rows into `processing`; overall processor remains manual / env-gated |
| Business Dictionary outbox | `processed_at IS NULL` vs timestamp set | `BusinessDictionaryStore` inserts NULL; `GraphStore._mark_outbox_processed` stamps timestamp on success and on unsupported-op skip | `GraphStore.process_outbox`, CLI runner | NULL means pending / retryable; timestamp means terminal processed-or-skipped | `LIVE_NULLABLE_OUTBOX_STATUS` | failed rows stay NULL and will be retried by the same CLI-driven consumer |
| OfferDTO / generator / kalk pricing fallback | kalk pricing mode: `master`, `fallback`, `unknown`; generator request mode: `from-offer-dto`, `direct-config`; generator converter: `none`, `gotenberg`, `fallback-docx`; generator top-level `status`: always `success` on returned document payload | kalk pricing engine resolves `pricing_mode`; generator use case resolves request mode and converter mode, then always writes result `status='success'` | kalk use case warning/invariant check; generator consumers read `status`, `meta.mode`, `meta.converter`, `warnings` | generator returns `status='success'` even when PDF conversion failed and only DOCX fallback was returned; degraded condition lives only in `meta.converter='fallback-docx'` + warnings. Kalk fallback is better-separated: `pricing_mode` + `fallbackUsed` invariant warning | `LIVE_PARTIAL_SUCCESS_STATUS` | no server-side retry; consumers must inspect `warnings` / `meta.converter`, not `status` alone |

## Runtime classification summary

- `LIVE_AUDIT_STATUS`: signal attempt states, Business Dictionary outbox pending/processed marker.
- `LIVE_CONTROL_STATUS`: engagement operational statuses, event-spine processor statuses, Cieplo workflow / ingress states.
- `LIVE_RECOVERY_STATE_MACHINE`: HITL send cached states.
- `LIVE_AMBIGUOUS_STATUS`: Gmail send `decision_status="executed"` for both dry-run and live send.
- `LIVE_CONTRACT_DRIFT`: drive ingest persists `skipped_policy` / `removed` outside declared enum contract.
- `LIVE_PARTIAL_SUCCESS_STATUS`: generator top-level `status='success'` even on PDF-conversion degradation.
- `READER_WIRED_PRODUCER_UNWIRED`: `world_model_insights`.
- `DORMANT_OR_SCHEMA_ONLY`: `MaterializeProposalItem.status='rejected'`, learning `dormant|archived` (no live writer/consumer confirmed here), DB outbox richer statuses on dormant path.

## False positives adjudicated

- `api_app.py` worker-health `status="stale"` is a health endpoint status, not a `learning_rule_candidates` lifecycle.
- `snapshot_stale` in `api_app.py` is an error payload string, not a persisted workflow status.
- `top-instal-generator/vendor/**` status strings (PclZip / PhpWord internals) are library-local and excluded from product status-contract conclusions.
- `drive_change_detector.removed: bool` is a change-feed flag, not the persisted `linkage_status="removed"` tombstone.
- `PolicyDecision.requires_human` contains a `dry_run_only` branch, but `_status()` did not yield that literal in the inspected code; treated as dormant literal, not a confirmed live status.

## Unresolved

- No product reader was independently re-verified for the signal-processing-attempt status table in this category; only writer-side and audit usage were confirmed.
- No live DB/runtime probe was executed to show rows already persisted with `extraction_status='skipped_policy'` or `linkage_status='removed'`; this artifact proves the write path statically.
- `execution_runtime.ActionProposal.status` downstream readers were not exhaustively retraced; the confirmed split is at writer/persistence level.
- No hidden route/UI was found writing `MaterializeProposalItem.status='rejected'`, but a lower-level caller outside the searched symbols cannot be disproved from this pass alone.

## Evidence IDs

- `EV-00182` — this category-8 completion record.
