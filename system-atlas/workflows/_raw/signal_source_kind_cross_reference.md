# Raw inventory — gmail-agent signal source_kind ↔ registered handler cross-reference

Generated during the mechanical reverse-audit pass (2026-07-30). Source of truth for dispatch:
`gmail-agent/tools/gmail_audit/agent_runtime/signal_registry.py` (`SIGNAL_HANDLERS` dict, populated
by `@register_signal_handler(source_kind)` decorators), consumed by
`signal_reconciler.reconcile_signal` (line 234: `SIGNAL_HANDLERS.get(signal.source_kind)`, raises
`ValueError` on a miss — fail-closed, no fallback).

## Registered handlers (4, confirmed via decorator grep)

| source_kind | handler function | file:line |
|---|---|---|
| `gmail` | `_reconcile_gmail_signal` | `signal_reconciler.py:295` |
| `calendar` | `_reconcile_calendar_signal` | `signal_reconciler.py:819` |
| `operator_command` | (handler at) | `signal_reconciler.py:886` |
| `drive` | (handler at) | `signal_reconciler.py:1052` |

## `source_kind=` literal string occurrences found repo-wide (raw grep, unfiltered)

Every literal `source_kind="..."` / `source_kind='...'` assignment found via `rg` across all
non-test `.py` files, before classification:

- `"google_calendar"` — `calendar_signal_adapter.py:20,48` (`build_calendar_raw_observation`,
  `build_calendar_signal`) — **CanonicalSignal.source_kind, CONFIRMED MISMATCH vs registered
  `"calendar"`, see `EV-00137`.**
- `"operator_command"` — `api_app.py:256` — matches registered handler, no issue.
- `"manual"` — `api_app.py:2041`, `case_routing.py:172` — NOT independently verified this pass
  whether these reach `reconcile_signal` as a `CanonicalSignal.source_kind` or a different field
  (e.g. a case-origin tag analogous to `cieplo_orchestrated` below) — flagged open, not resolved.
- `"drive"` — `business_dictionary/cli.py:160`, `drive_ingest_runtime.py:1006,1524`,
  `drive_signal_adapter.py:37,84,105,128,151`, `signal_reconciler.py:1467` — matches registered
  handler, no issue; multiple producer sites confirmed consistent.
- `"cieplo_orchestrated"` — `cieplo_orchestrator_hook.py:131` — VERIFIED this pass to be a
  `mailbox_memory_cases` row-origin tag (`enrich_case_row_before_upsert(row, source_kind=...)`),
  NOT a `CanonicalSignal.source_kind` — different concept sharing an unfortunate parameter name.
  Not a bug. Resolved, not left ambiguous.
- `"google_workspace_export"`, `"binary_download"` — `drive_client.py:146,158` — appear to be
  Drive-API-internal transfer-method tags feeding INTO `drive_signal_adapter.py`'s normalization
  before the final `source_kind="drive"` is set — not independently confirmed this pass, flagged
  open.
- `"gmail_inbound"` — `mailbox_memory_runtime.py:342` — appears to be a `mailbox_memory` internal
  ingest-context tag, not confirmed as `CanonicalSignal.source_kind` — flagged open.
- `"node_b_generated"`, `"daszek_migration"` — `mailbox_memory_runtime.py:574`, `gmail_intake.py:3228`
  — CONFIRMED this pass (Domain 2 completeness revisit, `EV-00125`) to be `mailbox_memory_thread_memory.source_kind`
  values, a completely different table/concept from `CanonicalSignal.source_kind`. Not a bug —
  resolved via direct verification, not left ambiguous.
- `"case_customer"`, `"gmail_sender"` — `neo4j_pilot.py:1479,1486` — appear to be graph-node type
  labels in a Neo4j pilot module, unrelated to `CanonicalSignal.source_kind` — not independently
  opened this pass, flagged open (low priority — `neo4j_pilot.py` name suggests experimental/pilot
  status, not confirmed live).

## Result classification

- 1 CONFIRMED, DECISIVE mismatch: `"google_calendar"` (produced) vs `"calendar"` (registered) —
  `EV-00137`, added to `WORKFLOW_GAPS.md` item 19.
- 1 CONFIRMED non-issue (verified, not assumed): `"cieplo_orchestrated"` is a different field on a
  different object, correctly namespaced by context even though the parameter name collides.
- 1 CONFIRMED non-issue (verified via Domain 2 work already done): `"node_b_generated"`/
  `"daszek_migration"` belong to `mailbox_memory_thread_memory`, not `CanonicalSignal`.
- 4 still-open, NOT resolved this pass (explicitly listed, not silently dropped): `"manual"`,
  `"google_workspace_export"`/`"binary_download"` (likely pre-normalization tags, not final
  signal source_kind), `"gmail_inbound"`, `"case_customer"`/`"gmail_sender"` (neo4j_pilot.py).
  A future pass should open each producer site directly to confirm which object/field each
  belongs to before either closing or escalating them.
