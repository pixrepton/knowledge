# AI-OS 4.1 — Audit consumerów fact supersession

Status: **COMPLETE** (audit only). Date: 2026-08-05.  
Repo SoT: `gmail-agent` / `tools/gmail_audit`.  
Roadmap: `knowledge/docs/AI_OS_ROADMAP.md` slice **4.1** (sufit #18).  
Proof: `FOCUSED_LOCAL` inventory + cross-check against RP-29 / DQ-10 write path.  
Enrichment: independent explore pass (same day) — severity/parity corrections below.  
**Not claimed:** consumer fixes, Documents→facts (4.2), Gate B.

## Contract (current)

| Writer                                                      | Semantics                                                                                                              | Notes                                                           |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `PostgresMailboxMemoryStore.append_facts_with_supersession` | Prior `status='active'` for `(case_id, entity_scope, fact_key)` → `superseded` on value change; same value → unchanged | RP-29 / DQ-10                                                   |
| `PostgresMailboxMemoryStore.append_fact_rows`               | **Delegates to** `append_facts_with_supersession`                                                                      | Legacy name, correct semantics on Postgres                      |
| `InMemoryMailboxMemoryStore.append_facts_with_supersession` | Mirrors Postgres supersession                                                                                          | Correct for tests that call it                                  |
| `InMemoryMailboxMemoryStore.append_fact_rows`               | Append by `fact_id` only — **no supersession**                                                                         | **HIGH** Postgres/InMemory parity gap                           |
| `replace_message_facts`                                     | DELETE by `message_id` then INSERT                                                                                     | No cross-message supersession of remaining actives (**MEDIUM**) |
| `handlers._persist_facts`                                   | Prefer `append_facts_with_supersession`, else `append_fact_rows`                                                       | LOW on Postgres; MEDIUM if only legacy InMemory append          |

**Store read baseline:** `fetch_facts_for_case` (postgres + inmemory) returns **all** rows (active **and** superseded). Filtering is a **consumer** responsibility.

**Canonical live-fact filter:** `mailbox_memory_runtime.split_conflicting_facts` — drops `status=='superseded'`, then ranks remaining by confidence / `observed_at`. This is the **only** production read filter for mailbox-fact supersession.

**Protocol gap:** `mailbox_memory/protocol.py` declares `append_fact_rows` / `fetch_facts_for_case` but **not** `append_facts_with_supersession`.

---

## Consumers inventory

### A. Safe via `split_conflicting_facts` → `CaseContextPack.active_facts`

| Consumer                                                                                                        | File / symbol                                                 | Filters superseded?                    | Risk                                                          |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------- |
| Case context pack                                                                                               | `mailbox_memory_runtime.build_case_context_pack`              | **Yes** for `active_facts` / conflicts | LOW for active path; see hub note below                       |
| Daszek mailbox pack                                                                                             | `daszek_v3_operational_feed.assemble_mailbox_pack_dict`       | **Yes**                                | LOW                                                           |
| Context assembler / overlay (when fed `active_facts`)                                                           | `context_assembler`, `central_llm_stage._mailbox_case_loader` | Via pack                               | LOW                                                           |
| Reply drafter / coherence / deterministic gaps / Understanding `_facts_invalidated` / `_prior_known_state_rows` | various                                                       | Via pack                               | LOW                                                           |
| Operator feed projection                                                                                        | `feed_projection.build_canonical_operator_snapshot`           | Via pack for trays                     | LOW for active; MEDIUM if embedded snapshot fields unfiltered |

**Hub inconsistency:** `build_case_context_pack` still passes **raw** `facts` into `build_current_case_context_snapshot` → `build_case_snapshot` (no status filter). Pack `active_facts` are safe; embedded snapshot `key_facts` / open questions may not be.

### B. Direct `fetch_facts_for_case` / unfiltered lists — gaps

| Consumer                                         | File / symbol                                                              | Filters superseded?                                    | Risk                        | Why                                                                              |
| ------------------------------------------------ | -------------------------------------------------------------------------- | ------------------------------------------------------ | --------------------------- | -------------------------------------------------------------------------------- |
| Case snapshot builder                            | `mailbox_memory_runtime.build_case_snapshot`                               | **No**                                                 | **HIGH**                    | Ranking can prefer superseded; false conflicts / `open_questions`                |
| Current context snapshot                         | `build_current_case_context_snapshot`                                      | **No**                                                 | **HIGH**                    | Used inside pack path                                                            |
| Ingest / finalize snapshots                      | `MailboxMemoryRuntime.ingest_message` / `finalize_case`                    | **No**                                                 | **HIGH**                    | Persisted legacy snapshots                                                       |
| Hot-state snapshot                               | `case_snapshot_manager._build_case_snapshot_hot_state`                     | **No**                                                 | **HIGH**                    | `_select_last_facts` / `_fact_conflicts` ignore status → false `awaiting_review` |
| Drive projection refresh                         | `drive_ingest_runtime.refresh_case_projection`                             | Raw → `build_case_snapshot`                            | **HIGH**                    | Pack later filtered; snapshot JSON may not be                                    |
| Signal reconciler drive path                     | `signal_reconciler` → `build_case_snapshot`                                | **No**                                                 | **HIGH**                    | Same snapshot hub                                                                |
| Entity linker identity                           | `entity_linker._case_identity_profile` / `find_case`                       | **No**                                                 | **HIGH**                    | Stale NIP/phone/email/contract still match                                       |
| Invoice direction                                | `handlers._fetch_invoice_fields`                                           | **No** — first key wins                                | **HIGH**                    | Superseded `seller_nip`/`buyer_nip` can decide direction                         |
| Neo4j pilot                                      | `neo4j_pilot.build_case_projection_payload` / `_best_fact_value`           | **No**                                                 | **HIGH**                    | Graph location/contacts from superseded                                          |
| Drive `first_fact_value` / `collect_fact_values` | `drive_ingest_runtime.py`                                                  | **No**                                                 | **HIGH** when fed raw lists | Customer/graph projection                                                        |
| Similar-case precedents                          | `similar_cases_precedent._active_fact_keys`                                | Rejects `rejected`/`stale` only — **not** `superseded` | **HIGH**                    | Misnamed; keys inflate overlap                                                   |
| Precedent SQL JOIN                               | `fetch_resolved_cases_by_family_and_fact_keys` / `_fetch_resolved_via_sql` | **No** `f.status`                                      | **MEDIUM**                  | Overlap inflated                                                                 |
| Calendar API path                                | `calendar_runtime.CalendarRuntime.context_for_case`                        | **No**                                                 | **MEDIUM**                  | Daszek filters; this API does not                                                |
| Drive enrichment reference terms                 | `collect_drive_case_enrichment`                                            | **No**                                                 | **MEDIUM**                  | All historical values enter reference terms                                      |
| Context pack overlay fallback                    | `context_pack_overlay.facts_and_chunks_from_pack`                          | Fallback to `hot_state.snapshot.key_facts`             | **MEDIUM**                  | Can reintroduce unfiltered snapshot values                                       |
| vNext `normalize_facts`                          | `case_context_contract.normalize_facts`                                    | `superseded` ∉ allowed → remapped to **`inferred`**    | **MEDIUM–HIGH if leaked**   | Treats superseded as current                                                     |
| Merge executor read/write                        | `write_executors.execute_merge_cases`                                      | Raw read; write via `append_fact_rows`                 | **MEDIUM**                  | InMemory write bypasses supersession                                             |
| Pattern discovery                                | `pattern_discovery.find_regex_gaps`                                        | Raw SQL, no status                                     | **LOW–MEDIUM**              | Offline mining from superseded LLM rows                                          |

### C. Writers / side paths

| Path                                                                      | Risk                                  | Note                                   |
| ------------------------------------------------------------------------- | ------------------------------------- | -------------------------------------- |
| InMemory `append_fact_rows` (no supersede)                                | **HIGH** (parity)                     | Must match Postgres delegate semantics |
| `replace_message_facts` cross-message                                     | **MEDIUM**                            | Can leave dual actives across messages |
| `write_executors` / drive promote / snapshot apply via `append_fact_rows` | LOW on Postgres; **HIGH** on InMemory | Prefer explicit supersession API       |
| Document / drive extractors emit `status: "active"`                       | LOW                                   | Correct if write path supersedes       |

### D. Projection / UI surfaces

| Surface                                                         | Supersession-aware?                     |
| --------------------------------------------------------------- | --------------------------------------- |
| Daszek operational feed (`active_facts`, conflicts, trays)      | **YES** (via `split_conflicting_facts`) |
| FastAPI case context / ContextTraySet (from filtered pack)      | **YES** if upstream pack filtered       |
| Legacy/hot `mailbox_memory_snapshots` (`key_facts`, open loops) | **NO**                                  |
| Neo4j pilot graph                                               | **NO**                                  |

### E. Tests (appendix)

`test_rp29_fact_supersession.py`, `test_split_conflicting_facts_tiebreak.py`, plus pack/understanding/Daszek/Neo4j/entity-linker suites. Not counted as production consumers.

---

## Gaps summary (actionable for 4.2+)

1. **Sole read filter is `split_conflicting_facts`** — raw `fetch_facts_for_case` consumers treat superseded as live.
2. **`build_case_snapshot` / hot-state hub is HIGH** — false conflicts and wrong preferred values.
3. **Entity linker, invoice NIP, Neo4j `_best_fact_value`, drive `first_fact_value`, `_active_fact_keys`** — HIGH identity/commercial/projection risks.
4. **`normalize_facts` remaps `superseded` → `inferred`** — never treat as current.
5. **InMemory `append_fact_rows` ≠ Postgres** — test/runtime parity trap.
6. **`replace_message_facts` does not cross-message supersede**.

Historical raw note (writer duality, partially stale on readers):  
`knowledge/system-atlas/workflows/_raw/fact_key_producer_reader_supersession_cross_reference.md`.

---

## Recommendations for 4.2 (Documents→facts) — no implementation in 4.1

1. Store-level `fetch_active_facts_for_case` (or `include_superseded=`) and migrate HIGH consumers first.
2. Fix `build_case_snapshot` / hot-state to exclude superseded before ranking (same semantics as `split_conflicting_facts`).
3. Document→fact writes always via supersession API; citation/`evidence_ref` in metadata.
4. Operator UI: live conflicts only; superseded as read-only audit trail.
5. Harden: `_fetch_invoice_fields`, `EntityLinker`, `_active_fact_keys`, Neo4j, precedent SQL, `normalize_facts`.
6. InMemory `append_fact_rows` → delegate to supersession (match Postgres).
7. RED/GREEN proof: document field change supersedes prior active; Daszek/Understanding show only active; snapshot does not invent conflicts from superseded.

---

## Delivery / Proof

```text
Delivery: COMPLETE
Proof: FOCUSED_LOCAL (consumer inventory 2026-08-05; enriched same day)
```

All identified production consumers are listed above. Fixes remain **out of scope** for 4.1 (audit-only).

---

## Post-audit implementation note (Roadmap 32, 2026-08-06)

FACT-01…05 landed as `COMPLETE_BOUNDED` / `CONFIRMED_LOCAL` (`gmail-agent:b2bd4d4`):

- FACT-01 snapshot/hot-state supersession filter
- FACT-02 Neo4j readers (mocked/unit)
- FACT-03 Postgres↔InMemory `append_fact_rows` parity
- FACT-04 `normalize_facts` no longer remaps `superseded→inferred`
- FACT-05 hub `build_case_context_pack` passes filtered winners into embedded snapshot path

This audit document remains the consumer inventory SoT; status of fixes lives in `docs/AI_OS_ROADMAP.md` residual FACT table. Product UI/Drive gaps from the historical 4.2 row were closed in `RESIDUALS-WAVE-01`. Remaining Case OS correctness residual: **`FACT-SUPERSESSION-WRITE-01`** (write-side).

---

## Post-audit remediation — FACT-4.1-HIGH-01

Date: 2026-08-08. Fresh delta-audit on HEAD after FACT-01…05 / 4.2 / 4.2b.  
Delivery: **COMPLETE** / Proof: **CONFIRMED_LOCAL** (Gate A **2357 passed, 15 skipped**; bounded Postgres calendar/active reader proof).

### Canonical contract (current)

| API | Semantics |
| --- | --- |
| `fetch_facts_for_case` | HISTORY — active + superseded audit trail |
| `fetch_active_facts_for_case` (Postgres + InMemory Protocol) | CURRENT — `status != superseded` |
| `fetch_current_facts_for_case` / `is_live_fact` (`mailbox_memory/active_facts.py`) | Canonical current-state seam for consumers |

### Historical HIGH disposition

| Historical HIGH / MEDIUM | File / symbol | Disposition | Evidence |
| --- | --- | --- | --- |
| Snapshot / hot-state / pack hub | `build_case_snapshot`, `case_snapshot_manager`, ingest/finalize | **ALREADY_FIXED** (FACT-01/05) | `test_fact01_snapshot_supersession.py`, RP-29 pack tests |
| Entity linker | `entity_linker` | **ALREADY_FIXED** (4.2b) | `test_aios_4_2b_active_fact_consumers.py` |
| Invoice fields | `handlers._fetch_invoice_fields` | **ALREADY_FIXED** (4.2b) | same |
| Drive first/collect fact values + projection | `drive_ingest_runtime` | **ALREADY_FIXED** (4.2b) | same |
| Neo4j pilot | `neo4j_pilot` | **ALREADY_FIXED** (FACT-02) | `test_fact02_active_fact_projection.py` — **NO_CHANGE_REQUIRED** |
| Similar-case keys | `_active_fact_keys` + `fetch_current_facts_for_case` | **ALREADY_FIXED** (4.2b) | same |
| Precedent SQL JOIN (Postgres + fallback + InMemory) | `fetch_resolved_cases_by_family_and_fact_keys`, `_fetch_resolved_via_sql` | **CLOSED** | status filter + `test_fact_41_high_remaining_consumers.py` |
| Calendar API | `CalendarRuntime.context_for_case` + `_has_customer_proposed_date_fact` | **CLOSED** | `fetch_current_facts_for_case` + live-fact guard; FACT-41 tests |
| Pattern discovery | `pattern_discovery.find_regex_gaps` | **CLOSED** (LOW–MEDIUM) | SQL excludes superseded |
| Drive enrichment mailbox refs | `collect_drive_case_enrichment` | **ALREADY_FIXED** | uses `fetch_current_facts_for_case` |
| Daszek pack / document promote | feed + `document_intelligence_runtime` | **ALREADY_FIXED** | history fetch + `split_conflicting_facts` / audit |
| Postgres supersede UPDATE metadata (psycopg3) | `append_facts_with_supersession` | **CLOSED** (blocker found in live proof) | `_json_dump` + datetime coerce; bounded PG proof |
| `replace_message_facts` dual-active / merge write path | writers | **CLOSED** `FACT-SUPERSESSION-WRITE-01` | cross-message supersession; merge reassign+reconcile; legal same-message conflicts kept |

### Post-fix inventory (production)

```text
CURRENT_STATE consumers: 12
supersession-safe: 12
unsafe: 0
history consumers: 4 (fetch_facts_for_case call sites that split/audit intentionally)
```

### Write-side closeout — FACT-SUPERSESSION-WRITE-01 (2026-08-08)

```text
Delivery: COMPLETE
Proof: CONFIRMED_LOCAL
production current-fact write paths: audited
canonical/safe: all production CURRENT_FACT_WRITE paths
unsafe: 0
history-only / legal-conflict seeds: preserved
```

Canonical write identity: `(case_id, entity_scope, fact_key)`.
Cross-message value change → supersede; same value → idempotent; same-message distinct values → legal conflict.
`append_fact_rows` → `append_facts_with_supersession` (PG + InMemory).
`replace_message_facts` → retire extract snapshot (preserve `structured_document_parse`) → cross-message supersession.
Merge → `reassign_case_facts` + reconcile newest-wins except same-message multi-value.
No partial unique DB constraint (legal conflicts require >1 current candidate).

Unsafe = 0 required for ticket closure.
