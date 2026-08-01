# Raw inventory — fact key ↔ producer ↔ reader ↔ supersession/invalidation (reverse-audit category 6)

Generated during the mechanical reverse-audit pass (2026-07-30), continuation session.

## Command used

```
rg -n "def append_fact_rows|def replace_message_facts|def fetch_facts_for_case" gmail-agent/tools/gmail_audit/mailbox_memory/
rg -n "ON CONFLICT.*fact" gmail-agent/tools/gmail_audit/mailbox_memory/postgres.py
rg -rn "append_fact_rows\(|replace_message_facts\(" gmail-agent/tools/gmail_audit --type py -g '!*test*'
```

## Scope

`mailbox_memory_facts` table writers and their supersession semantics (does a second write for
the same `case_id`+`fact_key` update, silently no-op, or duplicate?). Individual `fact_key`
literal producers (e.g. `document_field_extractor.py`'s per-field branches) were NOT exhaustively
enumerated one-by-one — the surface is large (dozens of keys across intake_schema.py,
document_field_extractor.py, case_coherence.py's `STABLE_FACT_KEYS`) and none showed an anomaly
in spot-checks; the decisive, previously-unflagged finding is at the writer-mechanism level, not
a specific key mismatch.

## Two writers, two different supersession semantics

| writer | conflict target | conflict behavior | caller |
|---|---|---|---|
| `replace_message_facts(message_id, rows)` | N/A — `DELETE FROM mailbox_memory_facts WHERE message_id = ...` then `INSERT ... ON CONFLICT (fact_id) DO UPDATE SET` (full upsert) | correctly supersedes: old facts for that message are deleted first, every column of a re-inserted row is refreshed | `mailbox_memory_runtime.py:445` — the main document/message-ingestion pipeline |
| `append_fact_rows(rows)` | `fact_id` | `ON CONFLICT (fact_id) DO NOTHING` — silent no-op on any repeat `fact_id` | `agent_runtime/tools/handlers.py`'s `_persist_facts`, the sole executor behind the LLM-facing `extract_facts_from_text` tool |

## Decisive finding

`_agent_fact_row` (`handlers.py:1140-1166`) computes `fact_id = stable_id("fact", case_id,
fact_key)` — deterministic on `case_id` + `fact_key` ONLY, with no `message_id` or timestamp
component. Combined with `append_fact_rows`'s `ON CONFLICT (fact_id) DO NOTHING`, this means: once
the agent's `extract_facts_from_text` tool has recorded a value for a given `(case_id, fact_key)`
pair ONE time, it can NEVER update that value again through this tool — not from a later message,
not from a genuinely different customer-supplied correction, not on any subsequent call. The
write silently no-ops; `ToolResult` still reports success; nothing signals to the agent or
operator that the "new" value was discarded and the old one kept.

This is the mirror-image of `append_materialize_proposal`'s pattern (category 5) but inverted:
there, a real executor has no creator; here, a real (repeatable) producer path has its updates
silently swallowed by the storage layer's conflict policy. The main ingestion pipeline
(`replace_message_facts`) does NOT have this problem — it correctly handles updates by deleting
and re-inserting per-message.

## Classification

`CONTRACT_DRIFT` / silent-update-loss defect, scoped specifically to the agent-tool
(`extract_facts_from_text`) write path. Not a crash risk; a data-staleness risk — a customer
correction extracted by the agent via this specific tool is silently discarded if a fact with the
same key was ever recorded before for that case, with no error surfaced anywhere.

## Unresolved / not independently re-verified this pass

- Whether any reader (`fetch_facts_for_case` or downstream consumers) cross-checks `observed_at`
  or otherwise detects a fact is stale — not traced; if a reader already prefers the most recent
  `observed_at` among duplicate-key rows this could be less severe, but `append_fact_rows`
  prevents a NEW row from ever being written for a repeat key in the first place, so there would
  be no newer row to prefer.
- Full one-by-one enumeration of every `fact_key` literal producer across the whole codebase
  (dozens of keys) was not performed — the scope of this pass was the writer-mechanism level.

## Evidence

`EV-00180` (this category's summary record). New gap filed, `WORKFLOW_GAPS.md`.
