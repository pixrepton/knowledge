# Supporting Registry Preview Plan — AI-OS-WORKFLOW-RECONSTRUCTION-AND-REGISTRY-01

- Status: `PASS`
- Scope: supporting registries preview only; no canonical artifacts or helper scripts mutated
- Timestamp: `2026-07-30T22:29:22+02:00`
- Repo SHA: `beb8309f52576df181c04e965e1353aedeba9de1`

## Scope

Preview and inconsistency triage for:

- `ENTRYPOINT_INVENTORY.md`
- `CROSS_REPO_CONTRACTS.md`
- `STATE_OWNERSHIP_MATRIX.md`
- `ARCHITECTURAL_RULES_AUDIT.md`

Cross-checked against:

- `WORKFLOW_REGISTRY.yaml`
- `WORKFLOW_EVIDENCE.jsonl`
- `WORKFLOW_GAPS.md`
- `PROGRESS.md`
- `_raw/projection_field_backend_producer_frontend_reader_cross_reference.md`
- `_raw/feature_flag_env_loader_branchpoint_live_value_cross_reference.md`
- `_raw/status_value_writer_consumer_cross_reference.md`
- `_raw/scheduler_timer_cron_actual_caller_cross_reference.md`

## Files Inspected

- `knowledge/system-atlas/workflows/ENTRYPOINT_INVENTORY.md`
- `knowledge/system-atlas/workflows/CROSS_REPO_CONTRACTS.md`
- `knowledge/system-atlas/workflows/STATE_OWNERSHIP_MATRIX.md`
- `knowledge/system-atlas/workflows/ARCHITECTURAL_RULES_AUDIT.md`
- `knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml`
- `knowledge/system-atlas/workflows/WORKFLOW_EVIDENCE.jsonl`
- `knowledge/system-atlas/workflows/WORKFLOW_GAPS.md`
- `knowledge/system-atlas/workflows/PROGRESS.md`
- `knowledge/system-atlas/workflows/_raw/projection_field_backend_producer_frontend_reader_cross_reference.md`
- `knowledge/system-atlas/workflows/_raw/feature_flag_env_loader_branchpoint_live_value_cross_reference.md`
- `knowledge/system-atlas/workflows/_raw/status_value_writer_consumer_cross_reference.md`
- `knowledge/system-atlas/workflows/_raw/scheduler_timer_cron_actual_caller_cross_reference.md`

## Facts

- `PROGRESS.md` still contains stale counters and interim checkpoints from before the current on-disk state (`180` evidence in older sections vs canonical `187`; reverse-audit `8/12` in older sections vs later `12/12 COMPLETE`).
- `ENTRYPOINT_INVENTORY.md` contains a self-contradictory gmail-agent route narrative: it says the 52 `api_app.py` routes are individually enumerated, but the preserved note still says individual route paths/handlers are "not yet enumerated line-by-line"; it also leaves the dynamic `/agent-chat` registration unresolved as either duplicate or distinct.
- Category 11 raw proof now gives stricter scheduler truth than `ENTRYPOINT_INVENTORY.md`: exactly 3 real Daszek WP-cron hooks plus the real Node B caller pattern (`signal_worker` loop ticks), whereas the inventory still foregrounds only VPS systemd timers and not the now-proven caller truth.
- `CROSS_REPO_CONTRACTS.md` is materially useful and mostly current, but still lacks stable contract IDs and a normalized schema for `producer`, `consumer`, `transport`, `durability`, `owner`, `workflow_ids`, `evidence_ids`, `runtime_status`, `recovery_path`.
- `STATE_OWNERSHIP_MATRIX.md` correctly flags real ambiguity around `calendar_risk`, proposal/execution state, and Daszek projection persistence, but these are not yet normalized into stable ownership records with IDs, explicit writer-bypass flags, or workflow attachments.
- `ARCHITECTURAL_RULES_AUDIT.md` already corrected the false `case_write_gateway` verdict and correctly documents multiple deliberate bypasses, but bypasses are still prose-only and not exported as stable machine-checkable rule rows.
- Reverse-audit category 9 proves additional supporting-registry-relevant truths not surfaced yet in the canonical supporting docs: `quality_readonly` and `validation_warnings` are contract-valid stored fields with no proven frontend reader; `recommended_next_action` and `open_questions` belong to a parallel mailbox-detail model, not the winning engagement-feed writer path.
- Reverse-audit category 10 proves a runtime-semantics defect that should be surfaced in supporting registries: `AGENT_RUNTIME_ENABLED` is loader-order-sensitive (`load_settings()` mutates env before `load_agent_runtime_settings()` reads it).
- Reverse-audit category 8 proves status/ownership edges that should be reflected in supporting docs: Daszek live bridge path is JSONL-based and terminal-without-retry; DB outbox path is richer but dormant; `FAILED_FINAL` in Cieplo is not actually terminal in retry semantics.

## Assumptions

- Workspace-root SHA is the correct provenance anchor for these atlas documents.
- Current working-tree content is a stronger source of truth than stale counters inside `PROGRESS.md`.
- Supporting registries should be regenerated from normalized core artifacts, not incrementally patched in place.
- This preview does not attempt to settle unresolved runtime semantics that require live mutation or new probes.

## Proposed Changes

1. Regenerate `ENTRYPOINT_INVENTORY.md` from a normalized machine source with stable row IDs, not prose counters.
   Required row fields:
   - `entrypoint_id`
   - `repo`
   - `surface_type` (`HTTP_ROUTE|CLI|PROCESS_LOOP|WP_CRON|SYSTEMD_TIMER|CI_ONLY|PROOF_ONLY`)
   - `registration_site`
   - `runtime_caller`
   - `path_or_command`
   - `dynamic_registration`
   - `workflow_ids`
   - `evidence_ids`
   - `runtime_status`
   - `notes`

2. Split gmail-agent route accounting into 3 separate counters:
   - direct decorator registration sites
   - dynamic registration sites
   - unique `(method,path)` routes

3. Normalize scheduler truth into the entrypoint inventory:
   - include the 3 Daszek WP-cron hooks
   - include `signal_worker` loop as the active scheduler surface
   - include tick-callers (`maybe_heartbeat_operational_feed`, `maybe_worker_bridge_drain_tick`) as child rows or linked notes
   - keep VPS `systemd` timers as deployment-profile-only rows

4. Regenerate `CROSS_REPO_CONTRACTS.md` from stable contract records.
   Required row fields:
   - `contract_id`
   - `producer_repo`
   - `consumer_repo`
   - `producer_symbol`
   - `consumer_symbol_or_endpoint`
   - `transport`
   - `durability`
   - `auth`
   - `workflow_ids`
   - `evidence_ids`
   - `verification_status`
   - `recovery_or_replay`
   - `notes`

5. Add an explicit contract class for asymmetrical/live-vs-dormant parallel mechanisms.
   Examples:
   - Daszek JSONL bridge queue = live contract
   - Daszek DB outbox = dormant parallel contract
   - gmail-agent ↔ rag-chat-asystent missing edge = explicit `MISSING_CONSUMER`

6. Regenerate `STATE_OWNERSHIP_MATRIX.md` from stable state records.
   Required row fields:
   - `state_id`
   - `store_or_table`
   - `repo`
   - `writers`
   - `readers`
   - `source_of_truth`
   - `workflow_ids`
   - `evidence_ids`
   - `ownership_status` (`CLEAR|AMBIGUOUS|PROJECTION_ONLY|DORMANT|UNRESOLVED`)
   - `writer_bypasses`
   - `retry_or_rebuild_semantics`

7. Create first-class ownership rows for currently prose-only ambiguities:
   - `calendar_risk`
   - proposal/execution triple-model split
   - Daszek projection persistence exact-table unknown
   - Business outcome value absence

8. Regenerate `ARCHITECTURAL_RULES_AUDIT.md` from normalized rule records.
   Required row fields:
   - `rule_id`
   - `rule_name`
   - `declared_in`
   - `enforced_by`
   - `bypasses`
   - `workflows`
   - `evidence_ids`
   - `runtime_classification`
   - `open_risks`
   - `status`

9. Surface runtime-semantics findings inside supporting registries instead of burying them only in reverse-audit raw artifacts:
   - loader-order-sensitive `AGENT_RUNTIME_ENABLED`
   - `FAILED_FINAL` not-final retry contract
   - live JSONL bridge queue vs dormant DB outbox
   - projection fields with no reader (`quality_readonly`, `validation_warnings`)

10. Remove stale "next step" prose and old counters from regenerated supporting docs. Preserve history only in `_raw/` and `PROGRESS_HISTORY.md`, not in the canonical regenerated registries.

## Unresolved

- Unique `(method,path)` count for gmail-agent after considering dynamic `/agent-chat` registration remains unresolved in the current supporting docs.
- `TOPINSTAL-KERNEL-GRAPH.yaml` was not diffed against `CROSS_REPO_CONTRACTS.md` in this preview, so graph-vs-registry drift is not fully closed here.
- Exact Daszek projection persistence tables were not opened in this pass; only projection-only ownership semantics are proven.
- Full producer inventory for `execution_runtime.ActionProposal` beyond the named traced sites remains unresolved.
- Whether any lower-level hidden caller writes materialize status `rejected` remains unresolved at supporting-registry level; raw category 8 only disproved a proven live writer.

## Validation Commands

Commands executed for this preview:

```powershell
git -C "C:\Users\compg\Desktop\top-code workspace" rev-parse HEAD
Get-Date -Format 'yyyy-MM-ddTHH:mm:ssK'
rg -n "workflow_id:|path_statuses:|code_path_statuses:|workflow_test_status:|runtime:|owner:|contract_statuses:|entrypoints:|evidence_ids:" "knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml"
rg -n "^#|^##|^###|route|counter|contract|ownership|bypass|Source of Truth|SoT|runtime|RUNTIME|dynamic" "knowledge/system-atlas/workflows/ENTRYPOINT_INVENTORY.md" "knowledge/system-atlas/workflows/CROSS_REPO_CONTRACTS.md" "knowledge/system-atlas/workflows/STATE_OWNERSHIP_MATRIX.md" "knowledge/system-atlas/workflows/ARCHITECTURAL_RULES_AUDIT.md"
rg -n "status:|COMPLETE|PARTIAL|reverse audit|12/12|17 workflows|48 gaps|187|180|supporting|ENTRYPOINT|CROSS_REPO|STATE_OWNERSHIP|ARCHITECTURAL_RULES" "knowledge/system-atlas/workflows/PROGRESS.md"
rg -n "route|counter|dynamic|scheduler|timer|cron|projection|feed|owner|ownership|contract|bridge_queue|outbox|bypass" "knowledge/system-atlas/workflows/_raw/projection_field_backend_producer_frontend_reader_cross_reference.md" "knowledge/system-atlas/workflows/_raw/scheduler_timer_cron_actual_caller_cross_reference.md" "knowledge/system-atlas/workflows/_raw/feature_flag_env_loader_branchpoint_live_value_cross_reference.md" "knowledge/system-atlas/workflows/_raw/status_value_writer_consumer_cross_reference.md"
rg -n "BROKEN_CALL|MISSING_CONSUMER|MISSING_PRODUCER|MISSING_EXECUTOR|DASZEK-COMMAND-OUTBOX-DRAIN|CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP|CALENDAR-TWO-WORLDS-OF-VISITS|route|contract|ownership|bypass|SoT" "knowledge/system-atlas/workflows/WORKFLOW_GAPS.md" "knowledge/system-atlas/workflows/WORKFLOW_EVIDENCE.jsonl"
Get-Content "knowledge/system-atlas/workflows/ENTRYPOINT_INVENTORY.md" | Select-Object -Index (68..82)
Get-Content "knowledge/system-atlas/workflows/ENTRYPOINT_INVENTORY.md" | Select-Object -Index (103..113)
Get-Content "knowledge/system-atlas/workflows/CROSS_REPO_CONTRACTS.md" | Select-Object -Index (60..87)
Get-Content "knowledge/system-atlas/workflows/STATE_OWNERSHIP_MATRIX.md" | Select-Object -Index (55..74)
Get-Content "knowledge/system-atlas/workflows/ARCHITECTURAL_RULES_AUDIT.md" | Select-Object -Index (126..149)
```

Suggested local checks for the integrator before merging supporting regenerations:

```powershell
python - <<'PY'
import json, pathlib
path = pathlib.Path(r"knowledge/system-atlas/workflows/_raw/subagents/supporting/identified_inconsistencies.json")
data = json.loads(path.read_text(encoding="utf-8"))
assert isinstance(data, list) and data
for row in data:
    for key in ["artifact", "issue_type", "severity", "details", "proposed_resolution"]:
        assert key in row and row[key]
print("supporting inconsistencies json: ok", len(data))
PY
```

## Proposed Merge Priority

1. Normalize supporting machine sources from core artifacts first.
2. Regenerate `ENTRYPOINT_INVENTORY.md` and `CROSS_REPO_CONTRACTS.md`.
3. Regenerate `STATE_OWNERSHIP_MATRIX.md`.
4. Regenerate `ARCHITECTURAL_RULES_AUDIT.md`.
5. Re-run atlas validator after supporting docs are replaced.

## Saved Files

- `knowledge/system-atlas/workflows/_raw/subagents/supporting/supporting_registry_plan.md`
- `knowledge/system-atlas/workflows/_raw/subagents/supporting/identified_inconsistencies.json`
