# Reverse-audit category 9 — projection field ↔ backend producer ↔ frontend reader

- Timestamp: `2026-07-30 20:55:59 +02:00`
- Working directory: `C:\Users\compg\Desktop\top-code workspace`
- Scope: Daszek operational-feed projection path only: Node B backend field producers, Daszek v3 ingest/persistence/read path, and frontend readers/fallback readers for operational feed, case detail, note detail, system observability.
- Exclusions:
  - No re-run of category 7 or 8.
  - No full domain call-graph reconstruction.
  - No non-projection UI flows unrelated to operational feed (`agent-chat`, cohort analytics internals, generic system-health beyond snapshot meta).
  - No live runtime mutation; static reverse-audit only.
- Repo SHAs:
  - `gmail-agent`: `468d37ee6553b39bf6009939e9c87c13f3c183c7`
  - `daszek`: `672769d9496359dcfb7f2427d555ad34a2171b1a`
  - `knowledge`: `597b1091a296930ed32afb379ec19b8ab425d4fa`

## Exact commands

1. `rg -n "why_on_desk|what_changed_pl|draft_reply_pl|operator_questions_pl|snapshot_id|schema_name|action_items|case_details|quality_readonly|calendar_risk|validation_warnings" "gmail-agent/tools/gmail_audit/daszek_engagement_feed/case.py" "gmail-agent/tools/gmail_audit/daszek_engagement_feed/desk.py" "gmail-agent/tools/gmail_audit/daszek_engagement_feed/build.py" "gmail-agent/tools/gmail_audit/daszek_v3_operational_feed.py" "gmail-agent/tools/gmail_audit/daszek_v3_operational_feed_contract.py"`
   - exit code: `0`
2. `rg -n "why_on_desk|what_changed_pl|draft_reply_pl|operator_questions_pl|snapshot_id|action_items|case_details|quality_readonly|calendar_risk|validation_warnings|recommended_next_action_reason|recommended_next_action" "daszek/public/app.js" "daszek/includes/api-v3.php" "daszek/includes/api-v3-handlers.php"`
   - exit code: `0`
3. `Get-Content "gmail-agent/tools/gmail_audit/daszek_engagement_feed/case.py" | Select-Object -Index (95..175)`
   - exit code: `0`
4. `Get-Content "gmail-agent/tools/gmail_audit/daszek_engagement_feed/desk.py" | Select-Object -Index (40..100)`
   - exit code: `0`
5. `Get-Content "daszek/public/app.js" | Select-Object -Index (1098..1140)`
   - exit code: `0`
6. `Get-Content "daszek/public/app.js" | Select-Object -Index (4340..4515)`
   - exit code: `0`
7. `git -C gmail-agent rev-parse HEAD; git -C daszek rev-parse HEAD; git -C knowledge rev-parse HEAD`
   - exit code: `0`
8. `(Get-Content "knowledge/system-atlas/workflows/WORKFLOW_EVIDENCE.jsonl" | Select-Object -Last 1)`
   - exit code: `0`

## Field inventory

| Projection field | Backend producer(s) | Persistence / transport | Frontend reader(s) | Transition meaning | Runtime classification |
|---|---|---|---|---|---|
| `snapshot_id` | `build_operational_feed_snapshot`, `build_operational_feed_from_mailbox_store`, `build_engagement_feed_envelope` | `POST /wp-json/daszek/v3/operational-feed-snapshots` validates and upserts full payload; latest/detail/list readers expose it | `operationalFeedSnapshotMetaLine`, `startSystemViewLoad` (`feedMeta.snapshot_id`) | Canonical identity of one feed snapshot | `LIVE_COMPLETE` |
| `schema_name`, `schema_version` | `build_operational_feed_snapshot` | PHP validator enforces accepted values; stored in snapshot row | `operationalFeedSnapshotMetaLine` only reads `schema_version` | Contract/version signal, not operator business data | `LIVE_COMPLETE` |
| `feed.case_details` | `build_feed_from_engagement_snapshots` and mailbox feed builder fill `case_details[cid]`; builder injects into envelope | full snapshot persisted as one JSON object | `resolveOperationalFeedCaseDetail`, `buildCaseDetailPayloadFromFeedCase` | Embedded per-case detail payload used when live `/cases/{id}` fails or for snapshot-first detail | `LIVE_COMPLETE` |
| `feed.action_items` | `_dual_emit_action_items`, `snapshot_to_feed_tasks`, mailbox/task router projection | validated by Python + PHP; stored in snapshot feed | `getFeedActionItems`, `buildFeedDaySections` | Canonical action/task list for schema `1.3` operational feed | `LIVE_COMPLETE` |
| `feed.tasks` | `_dual_emit_action_items` legacy shim only | stored only as compatibility alias when present | `getFeedActionItems` fallback path if `action_items` absent | Legacy alias for older readers | `LEGACY_SHIM_LIVE` |
| `why_on_desk` on desk rows | `snapshot_to_desk_item`; mailbox builder also writes it from router/memory projection | stored inside `feed.desk[]` and desk-note fallback payload | desk search/filter, note card text, note fallback payload, case fallback summary | Honest explanation of why item is surfaced now | `LIVE_COMPLETE` |
| `why_on_desk` on case rows | `snapshot_to_feed_case`; mailbox builder also writes it | stored in `feed.cases[]` and embedded case details | `renderWhyOnDeskSection`, case search/fallback, note detail `why_you_see_it` fallback | Honest "why do I see this" explanation for case/detail | `LIVE_COMPLETE` |
| `what_changed_pl` | `snapshot_to_feed_case` from `case_understanding.what_changed_pl` | stored in `feed.cases[]` and embedded detail | `renderWhatChangedSection` | Operator-visible delta since last turn if fresh understanding exists | `LIVE_COMPLETE` |
| `draft_reply_pl` | `snapshot_to_feed_case`, `snapshot_to_desk_item`; mailbox feed can also emit | stored in case/note projection rows and embedded detail | `renderOperationalNoteRecord` (`hasDraft`), both `renderHitlOperatorActions` variants | Presence gates real "Wyślij odpowiedź" UI path and pre-fills textarea | `LIVE_COMPLETE` |
| `operator_questions_pl` | `snapshot_to_feed_case`, `snapshot_to_desk_item` from snapshot gaps | stored in case/note projection rows and embedded detail | both `renderHitlOperatorActions` variants | Human-facing clarification prompts when no draft is ready | `LIVE_COMPLETE` |
| `hitl_gate`, `hitl_pending`, `hitl_required`, `hitl_action_id`, `engagement_id` | `snapshot_to_feed_case`, `snapshot_to_desk_item`, `build_case_detail_from_engagement` | persisted inside snapshot rows / case detail | `renderHitlOperatorActions`, detail refresh helpers, approve/send button payloads | Drives operator-approval vs send UI branching | `LIVE_COMPLETE` |
| `recommended_next_step` / `primary_next_action_title_pl` | `snapshot_to_feed_case`, `snapshot_to_desk_item`; mailbox feed also derives from case summary | persisted in desk/case projection rows | visible on cards and used in fallback detail stubs | Read-only recommendation for next step | `LIVE_COMPLETE` |
| `recommended_next_action` inside mailbox-memory snapshot | mailbox `CaseContextPack` / pack snapshot, not engagement feed case-row producer | only available through embedded mailbox snapshot/live detail payload | `renderMailboxMemorySection` | Read-only recommendation from mailbox snapshot | `LIVE_READER_DIFFERENT_SOURCE` |
| `recommended_next_action_reason` | mailbox-memory snapshot/live detail only; no engagement-feed producer found | only via live detail or embedded mailbox snapshot | `renderMailboxMemorySection` | Explanation for mailbox snapshot recommendation | `READER_WITHOUT_ENGAGEMENT_FEED_WRITER` |
| `open_questions` | mailbox-memory snapshot/live detail only; no engagement-feed producer found | only via live detail or embedded mailbox snapshot | `renderMailboxMemorySection` | Open information requests in mailbox snapshot | `READER_WITHOUT_ENGAGEMENT_FEED_WRITER` |
| `calendar.calendar_risk` | no direct writer found in engagement-feed projection path; mailbox runtime has `calendar_runtime.py` producer outside this feed contract | may exist in live mailbox detail payload, not proven in operational-feed snapshot rows | `renderCalendarBlock` | Calendar-risk label for detail calendar section | `READER_WITHOUT_PROVEN_PROJECTION_WRITER` |
| `scheduled_visit` | fact writer exists (`write_executors.py`) but no direct projection field writer found in operational-feed snapshot | remains fact/memory state, not first-class projection field | no direct `scheduled_visit` UI field reader found in `app.js` | visit commitment is represented indirectly via facts/calendar, not direct projection field | `NOT_A_PROJECTION_FIELD_FALSE_POSITIVE` |
| `quality_readonly` | optional `build_operational_feed_snapshot(... quality_readonly=...)` | Python + PHP validate and persist `feed.quality_readonly` | no `app.js` reader found | Optional quality slice can be transported but is not surfaced in current frontend | `WRITER_WITHOUT_FRONTEND_READER` |
| `validation_warnings` | `daszek_v3_validate_operational_feed_desk_note_refs` mutates payload before upsert | stored in ingested snapshot payload | no `app.js` reader found | Ingest-time warning channel for missing desk-note refs | `WRITER_WITHOUT_FRONTEND_READER` |
| `feedMeta.case_count` in system view | derived in `startSystemViewLoad` from `snapshot.feed.cases.length` | not persisted separately; computed client-side | `renderSystemObservabilityDashboard` | lightweight observability summary, not a primary data contract | `CLIENT_DERIVED` |

## Producer / reader mismatches and notable lifecycles

1. `operational-feed` snapshot wins over `/desk`, `/day`, `/cases` when available.
   - `loadAllData()` always fetches legacy v3 aliases and `operational-feed-snapshots/latest`, but if a snapshot is present then `feedWins=true` and the UI stops using `/desk`, `/day`, `/cases` for primary operational views.
   - Meaning: category 9 must treat the snapshot as the real runtime reader path for desk/day/cases.

2. `action_items` is canonical; `tasks` is only a compatibility shim.
   - Frontend calls `getFeedActionItems(feed)` and prefers `feed.action_items`; `feed.tasks` is only fallback.
   - The separate firm-task panel using `task_status` reads `state.data.tasks` or `mailboxCases`, not `operational-feed` action items.
   - Classification: apparent `status` vs `task_status` mismatch is a false positive for operational-feed.

3. Engagement-feed writes `recommended_next_step`, while mailbox-memory detail readers still look for `recommended_next_action`.
   - This is not a direct break on first-screen cards because cards read `primary_next_action_title_pl` / `recommended_next_step`.
   - But the mailbox-memory detail section (`renderMailboxMemorySection`) expects richer snapshot fields not emitted by the engagement-feed case-row mapper.
   - Classification: parallel read models, not one uniform field contract.

4. `draft_reply_pl` is a real control field, not cosmetic text.
   - Note cards use it to decide whether "Przejrzyj draft" should appear.
   - Detail HITL view uses it to enable real send UI and populate editable text.
   - This makes it a load-bearing producer/consumer pair.

5. `why_on_desk` is used across three surfaces.
   - card filtering/search,
   - detail "Dlaczego to widzę",
   - note detail fallback `why_you_see_it`.
   - Meaning: any future rename must preserve multiple readers, not just note cards.

6. `quality_readonly` and `validation_warnings` survive validation/persistence but disappear at UX level.
   - Both have proven writer + storage path.
   - No `app.js` reader was found.
   - Meaning: these fields are transport-live but operator-dormant.

## Runtime classification summary

- `LIVE_COMPLETE`
  - `snapshot_id`
  - `schema_version`
  - `case_details`
  - `action_items`
  - `why_on_desk`
  - `what_changed_pl`
  - `draft_reply_pl`
  - `operator_questions_pl`
  - `hitl_gate` / `hitl_pending` / `hitl_required` / `engagement_id`
  - `recommended_next_step`

- `LEGACY_SHIM_LIVE`
  - `feed.tasks`

- `LIVE_READER_DIFFERENT_SOURCE`
  - `recommended_next_action`

- `READER_WITHOUT_ENGAGEMENT_FEED_WRITER`
  - `recommended_next_action_reason`
  - `open_questions`

- `READER_WITHOUT_PROVEN_PROJECTION_WRITER`
  - `calendar.calendar_risk`

- `WRITER_WITHOUT_FRONTEND_READER`
  - `quality_readonly`
  - `validation_warnings`

- `CLIENT_DERIVED`
  - system-view `feedMeta.case_count`

- `NOT_A_PROJECTION_FIELD_FALSE_POSITIVE`
  - `scheduled_visit`

## False positives

1. `task_status` versus task `status`
   - The `task_status` reader belongs to the separate firm-task/mailbox-cases path, not to operational-feed `action_items`.

2. `scheduled_visit`
   - Real state exists, but not as a first-class field in the audited projection contract.
   - UI meaning is carried indirectly via facts/calendar, so this does not belong in the same class as missing projection readers.

3. `feed.tasks`
   - Not dead code by itself; it is an intentional compatibility alias retained for legacy schema readers.

## Unresolved

1. `calendar.calendar_risk`
   - Frontend reader is confirmed.
   - A mailbox-runtime producer exists elsewhere, but this reverse-audit slice did not prove a concrete writer into the currently winning operational-feed snapshot path.

2. `recommended_next_action_reason` and `open_questions`
   - Confirmed UI readers exist in mailbox-memory detail rendering.
   - This slice did not prove whether the live `/cases/{id}` path always populates them, only that the engagement-feed mapper does not.

## New findings suitable for registry/gap updates

1. `validation_warnings` is persisted but operator-invisible.
   - Daszek v3 ingest writes warning data into the snapshot payload.
   - No frontend surface reads or displays it.
   - Impact: feed ingest can detect broken `note_id` referential integrity while the operator sees a clean projection with no warning banner.

2. `quality_readonly` is transport-live but UI-dormant.
   - Optional quality slice is validated and stored.
   - No current frontend reader was found.

## Evidence IDs

- Existing evidence referenced during continuation: `EV-00182`
- New evidence to append after this artifact: `EV-00183`
