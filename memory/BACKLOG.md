# Backlog

Status: active only. Last updated: 2026-08-08 (FRESH38-RECAPTURE-01).

This file is not a proof history or phase archive. Canonical plan + residual narrative: `knowledge/docs/AI_OS_ROADMAP.md`.

## Open — residuals (after FRESH38 closeout)

| ID                   | Area              | Status          | Next action                                                                 |
| -------------------- | ----------------- | --------------- | --------------------------------------------------------------------------- |
| FACT-4.1-HIGH-01     | gmail-agent       | open, P2        | Ticketize HIGH gaps from `AIOS_4_1_FACT_SUPERSESSION_CONSUMER_AUDIT.md`     |
| GOV-06               | knowledge         | PARTIAL         | `.serena` policy monitor (tracked project.yml; cache gitignored)            |
| IQ-01-ADJUDICATED    | eval              | DEFERRED        | Human-adjudicated labels (conscious bound; machine_proposed only today)     |

## Closed — FRESH38-RECAPTURE-01 (2026-08-08)

| ID                   | Disposition        | Note |
| -------------------- | ------------------ | ---- |
| FRESH38-RECAPTURE-01 | COMPLETE / CONFIRMED_LOCAL | Empty `message.content` → retryable `empty_content` + fallback; Variant2 full Fresh 38 @ `gmail-agent:fea458f`; 38/38; `scoring_complete=true`; CLEAN_PASS=10 CAPABILITY=28; artifacts `knowledge/eval/fresh38-recapture-20260808/` |

## Closed — GOV-09 (2026-08-08)

| ID     | Disposition      | Note |
| ------ | ---------------- | ---- |
| GOV-09 | COMPLETE_BOUNDED | Auth OK; pushed gmail/daszek/rag/cieplo + knowledge clean `docs/aios-residuals-wave-sync`@`22832f3` (no poison `8ed364e3`). Old `docs/daszek-system-diagrams-refresh` remains unpushable (secret ancestry). Workspace root: no `origin` (N/A). |

## Closed — RESIDUALS-WAVE-02 (2026-08-07)

| ID                     | Disposition      | Note                                                                                          |
| ---------------------- | ---------------- | --------------------------------------------------------------------------------------------- |
| RAG-05                 | COMPLETE_BOUNDED | Temporal worker module + compose Temporal + live `start_ingest` PASS                          |
| RAG-12                 | COMPLETE_BOUNDED | Compose profile `rag-v2-data-plane` + Gate B smoke PASS (`RequireLiveAdapters`)               |
| RAG-01                 | COMPLETE_BOUNDED | Host live Docling PDFâ†’graph (`RAG_V2_DOCLING_LIVE=1`, 6 passed)                               |
| RAG-09                 | COMPLETE_BOUNDED | Opt-in `RAG_V2_LIVE_DATA_PLANE=1` when MinIO+Qdrant+Temporal soft-activated (default False)    |
| X1-01 / X1-02          | COMPLETE         | Live Playwright re-proof **2 passed** on HEAD                                                 |
| SPINE-WORKER-TICK-01   | COMPLETE_BOUNDED | Chunked idle drain + `AGENT_CHAT_JOBS_*` env; unit tests                                      |
| DASZEK-HITL-HARNESS-01 | COMPLETE         | `extractFunction` space markers; node HITL **16/16**                                          |
| GROQ-KEY-DEAD-01       | COMPLETE_BOUNDED | `AGENT_GROQ_API_KEY_DISABLED=1` + planner pool skip; recreate Node B                          |

## Closed â€” RESIDUALS-WAVE-01 (2026-08-07)

| ID     | Disposition       | Note                                                                           |
| ------ | ----------------- | ------------------------------------------------------------------------------ |
| RAG-02 | COMPLETE_BOUNDED  | Ephemeral MinIO live put/get (`scripts/rag_v2_ephemeral_data_plane_proof.ps1`) |
| RAG-04 | COMPLETE_BOUNDED  | Ephemeral Qdrant live upsert/search                                            |
| 4.2    | COMPLETE_BOUNDED  | Daszek superseded UI + live Drive ingest + pack keys                           |
| 4.4    | COMPLETE_BOUNDED  | `install_prep_projection` + feed + whitelist                                   |
| FG-01  | RESOLVED_OPTION_B | RFC resolved; Guardian joins mailbox `case_status` for SLA                     |
| FG-04  | COMPLETE_BOUNDED  | CLI `follow-up-guardian` + live oneshot Postgres (`checked=50`)                |
| IQ-01  | COMPLETE_BOUNDED  | Frozen dual-score PROTOCOL; machine_proposed labels only                       |
| PF-01  | COMPLETE_BOUNDED  | Exhaustive inventory `knowledge/docs/PF01_ENABLED_DRAFT_INVENTORY.md`          |

## Closed â€” hygiene 2026-08-07

| ID                         | Disposition         | Note                                                        |
| -------------------------- | ------------------- | ----------------------------------------------------------- |
| RAG-MANIFEST-DIRTY-01      | **CLOSED_REVERTED** | Only `created_at` timestamp noise; restored to HEAD         |
| root tracked `__pycache__` | **CLOSED**          | `git rm --cached scripts/__pycache__/` (already gitignored) |

## Closed â€” POST32-COMMIT-01 (2026-08-07)

| ID                                | Delivery         | Proof                                | Commit                                                    |
| --------------------------------- | ---------------- | ------------------------------------ | --------------------------------------------------------- |
| POST32-COMMIT-01                  | COMPLETE         | LOCAL_ONLY commits                   | multi-repo below                                          |
| GATEA-POST-6X-01                  | COMPLETE         | Gate A **2322**/14                   | `gmail-agent:b2f071d`                                     |
| E2E-FULLFLOW-ASSERT-01            | COMPLETE         | harness aligned to spine 6.3         | `workspace:1c5137e`                                       |
| E2E-FULLFLOW-FALSEPASS-01         | COMPLETE         | `step()` uses last tuple element     | `workspace:1c5137e`                                       |
| E2E-ASYNC-TRACK-01                | COMPLETE         | script tracked                       | `workspace:1c5137e`                                       |
| 4.3 / 5.1 / 5.2 / 6.1 / 6.2 / 6.3 | COMPLETE_BOUNDED | CONFIRMED_LOCAL + 6.2 PROVEN_RUNTIME | `gmail-agent:b2f071d`, `daszek:8929945`, `cieplo:49c8ef1` |

