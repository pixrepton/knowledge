# Backlog

Status: active only. Last updated: 2026-08-08 (RAG-WIDGET-ADMIN-SECURITY-CLOSEOUT-01).

This file is not a proof history or phase archive. Canonical plan + residual narrative: `knowledge/docs/AI_OS_ROADMAP.md`.

## Open — only real residuals (post write-side closeout)

| ID                       | Area              | Status   | Next action                                                                                      |
| ------------------------ | ----------------- | -------- | ------------------------------------------------------------------------------------------------ |
| RAG-TEMPORAL-COMPLETE-01 | rag-chat-asystent | open, P1 | Stabilize container Temporal COMPLETE under Gate B (blocker for authorized staged cutover)       |
| RAG-IMAGE-BAKE-01        | rag-chat-asystent | open, P2 | Reproducible image bake from lock (minio/qdrant/temporalio); interim docker-commit is not enough |
| IQ-01-ADJUDICATED        | eval              | DEFERRED | Human-adjudicated labels (optional measurement; not product)                                     |
| GOV-06                   | knowledge         | PARTIAL  | `.serena` policy monitor — ignore by default                                                     |

**RAG staged activation:** `STAGED_ACTIVATION_AUTHORIZED — BLOCKED_BY_TECHNICAL_GATE` (see `OPERATOR_DECISIONS.md`). Not an open “ask operator again” ticket.

**4.4 Install-prep:** `REJECTED_BY_OPERATOR / NO PRODUCT ACTIVATION` — scaffold may exist; do not develop.

## Closed — RAG-WIDGET-ADMIN-SECURITY-CLOSEOUT-01 (2026-08-08)

| ID                                    | Disposition                | Note                                                                                                                                                                                                 |
| ------------------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RAG-WIDGET-ADMIN-SECURITY-CLOSEOUT-01 | COMPLETE / CONFIRMED_LOCAL | P0-4 option namespace mismatch fixed; P0-5 nopriv+PIN removed; document admin = `manage_options` + nonce; Gate A jest 43/43 + PHP harness PASS; public chat remains anonymous without doc-admin caps |

## Closed — FACT-SUPERSESSION-WRITE-01 (2026-08-08)

| ID                         | Disposition                | Note                                                                                                                                                                                                                                                |
| -------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FACT-SUPERSESSION-WRITE-01 | COMPLETE / CONFIRMED_LOCAL | Canonical write supersession on `replace_message_facts` + merge `reassign_case_facts`; PG==InMemory; Gate A effective PASS; bounded PG proof PASS; illegal dual-active reconciled (4 groups / 12 rows); legal same-message conflicts preserved (50) |

## Closed — RAG-V2-LIVE-CUTOVER-READINESS-01 (2026-08-08)

| ID                               | Disposition      | Note                                                                                                                                                                                                               |
| -------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RAG-V2-LIVE-CUTOVER-READINESS-01 | COMPLETE_BOUNDED | Live plane + ingest worker + host Gate B PASS + dual-read/rollback; Activation `STAGED_ACTIVATION_AUTHORIZED — BLOCKED_BY_TECHNICAL_GATE`; proof `eval/rag-v2-live-cutover-20260808/`; **no** global `RAG_CORE=v2` |
| RAG-01 (redefined)               | COMPLETE_BOUNDED | Docling live in canonical containerized ingest worker                                                                                                                                                              |
| RAG-12 (host E2E bar)            | COMPLETE_BOUNDED | Real PDF→MinIO→PG→Qdrant→retrieve→restart; Temporal COMPLETE = residual `RAG-TEMPORAL-COMPLETE-01`                                                                                                                 |
| RAG-09                           | COMPLETE_BOUNDED | Opt-in + staged compose ready; product default legacy; staged auth already given                                                                                                                                   |

## Closed — FACT-4.1-HIGH-01 (2026-08-08)

| ID               | Disposition                | Note                                                                                                                   |
| ---------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| FACT-4.1-HIGH-01 | COMPLETE / CONFIRMED_LOCAL | Read-side CURRENT_STATE consumers safe (`unsafe=0`); Gate A **2357**/15; write residual → `FACT-SUPERSESSION-WRITE-01` |

## Closed — FRESH38-RECAPTURE-01 (2026-08-08)

| ID                   | Disposition                | Note                                                                                                                      |
| -------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| FRESH38-RECAPTURE-01 | COMPLETE / CONFIRMED_LOCAL | Measurement healthy: 38/38; CLEAN_PASS=10 CAPABILITY=28 → product **NOT QUALIFIED — CAPABILITY** (not a harness residual) |

## Closed — GOV-09 (2026-08-08)

| ID     | Disposition      | Note                                                                                                                                        |
| ------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| GOV-09 | COMPLETE_BOUNDED | Auth OK; remotes pushed; knowledge on clean `docs/aios-residuals-wave-sync` (no poison secret ancestry). Workspace root: no `origin` (N/A). |

## Closed — RESIDUALS-WAVE-02 (2026-08-07)

| ID                     | Disposition      | Note                                                                            |
| ---------------------- | ---------------- | ------------------------------------------------------------------------------- |
| RAG-05                 | COMPLETE_BOUNDED | Temporal worker module + compose Temporal + live `start_ingest` PASS            |
| RAG-12                 | COMPLETE_BOUNDED | Compose profile `rag-v2-data-plane` + Gate B smoke PASS (`RequireLiveAdapters`) |
| RAG-01                 | COMPLETE_BOUNDED | Host live Docling PDF→graph                                                     |
| RAG-09                 | COMPLETE_BOUNDED | Opt-in `RAG_V2_LIVE_DATA_PLANE`                                                 |
| X1-01 / X1-02          | COMPLETE         | Live Playwright re-proof **2 passed**                                           |
| SPINE-WORKER-TICK-01   | COMPLETE_BOUNDED | Chunked idle drain                                                              |
| DASZEK-HITL-HARNESS-01 | COMPLETE         | node HITL **16/16**                                                             |
| GROQ-KEY-DEAD-01       | COMPLETE_BOUNDED | dead key disable                                                                |

## Closed — RESIDUALS-WAVE-01 (2026-08-07)

| ID     | Disposition              | Note                                                                                              |
| ------ | ------------------------ | ------------------------------------------------------------------------------------------------- |
| RAG-02 | COMPLETE_BOUNDED         | Ephemeral MinIO live                                                                              |
| RAG-04 | COMPLETE_BOUNDED         | Ephemeral Qdrant live                                                                             |
| 4.2    | COMPLETE_BOUNDED         | Daszek superseded UI + live Drive                                                                 |
| 4.4    | **REJECTED_BY_OPERATOR** | Scaffold implemented in WAVE-01; **no product activation**; do not develop (`OPERATOR_DECISIONS`) |
| FG-01  | RESOLVED_OPTION_B        | Guardian joins mailbox `case_status` for SLA                                                      |
| FG-04  | COMPLETE_BOUNDED         | CLI oneshot live                                                                                  |
| IQ-01  | COMPLETE_BOUNDED         | Frozen dual-score; machine_proposed only                                                          |
| PF-01  | COMPLETE_BOUNDED         | Exhaustive draft inventory                                                                        |

## Closed — hygiene / POST32 (2026-08-07)

See prior sections in git history if needed. POST32 4.3/5.1/5.2/6.1/6.2/6.3 = CLOSED in HEAD.
