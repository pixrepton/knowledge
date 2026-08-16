# Backlog

Status: active only. Last updated: 2026-08-16 (Fresh38 measurement requalified; capability below threshold).

This file is not a proof history or phase archive. Canonical plan + residual narrative: `knowledge/docs/AI_OS_ROADMAP.md`.

## Current residual status

```text
AI_OS_INFRASTRUCTURE_CLEANUP = COMPLETE_LOCAL
CAPABILITY_PROGRAM_READINESS = GO
OPERATOR-COMMAND-RECONCILE-BYPASS-01 = CLOSED
REQUIRED_OPEN = 0
UNKNOWN_NEEDS_PROOF = 0
FRESH38_MEASUREMENT_QUALIFICATION = REQUALIFIED
FULL FRESH38 AGAINST CURRENT CODE = RUN (2026-08-16, 38/38 capture QUALIFIED)
CURRENT CAPABILITY BASELINE = 27 CLEAN_PASS / 11 CAPABILITY (v5, threshold 34) → NOT QUALIFIED — CAPABILITY
NEXT = 11-CAPABILITY focused analysis (product), not a new residual wave
```

| ID                               | Area        | Status   | Next action                                                                                  |
| --------------------------------- | ----------- | -------- | --------------------------------------------------------------------------------------------- |
| `OPERATOR-COMMAND-RECONCILE-BYPASS-01` | gmail-agent | **CLOSED** | `run_operator_command_spine()` now routes newly appended operator commands through `reconcile_signal()`/registered `operator_command` handler; Gate A gmail-agent passed with 0 failed. |
| `FRESH38-CAPABILITY-11-ANALYSIS-20260816` | gmail-agent | **OPEN — next program** | Focused per-case analysis/proof for the 11 CAPABILITY cases (INT-01, INT-04, INT-05, NEW-03, NEW-05, FU-01, SVC-05, DOC-02, CTX-03, MI-01, MI-02) before any product change. Measurement is green; product is below threshold. |
| `FRESH38-L0-REPAIR-COMMIT-20260816` | workspace | **CLOSED** | L0 repair committed `4210ed5` (workspace, LOCAL_ONLY): `scripts/run_fresh38_case_batch.ps1` + `scripts/tests/test_fresh38_engine_lifecycle_channel.ps1` (incl. behavioral 231 scenarios). |
| `TASK-ENGINE-SCOPE-UPDATE` | workspace (scripts) | **OPEN — procedural debt** | Task engine lacks a supported operation for scope/adoption updates; consolidation required direct JSON mutation of checkpoints. Desired future capability: canonical `task-scope-add` / `task-adopt-path` with validation, ownership safeguards, audit trail, checkpoint integration. Not a blocker for consolidation PASS; do not implement in closeout. |
| IQ-01-ADJUDICATED                | eval        | DEFERRED | Human-adjudicated labels (optional measurement; not product)                                 |
| GOV-06                           | knowledge   | PARTIAL  | `.serena` policy monitor — ignore by default                                                 |

**Superseded (2026-08-16):** `FULL FRESH38 AGAINST CURRENT CODE = NOT_RUN` and
`CURRENT CAPABILITY BASELINE = NOT_REQUALIFIED` — replaced by the requalified measurement and
the v5 capability baseline above. Historical baselines (13 Aug 23/15, 08 Aug 10/28) remain
historical evidence, not the current baseline.

**Non-blocking harness notes (audit `AI-OS-FINAL-INFRA-CLOSEOUT-01`, not tracked as gating residuals):** gmail-agent `tests/test_aios_canonical_runtime_ingress.py` has no `MAILBOX_MEMORY_TEST_DATABASE_URL`-style skip gate unlike its Postgres-test siblings (unconditional live-DB dependency; ~140s of Gate A wall-clock, fails ungracefully instead of skipping when DB is briefly down); rag-chat-asystent `backend/engine.py:79` ORs `PYTEST_CURRENT_TEST` into `use_fake_embeddings`, so a test trying to opt into real embeddings via `USE_FAKE_EMBEDDINGS=0` silently still gets fake ones unless it also `monkeypatch.delenv("PYTEST_CURRENT_TEST")`; `daszek_engagement_feed/desk.py:58` has a dead-by-coincidence membership gate (`DESK_OPERATIONAL_CODES` happens to equal the full `OperationalStatus.code` Literal today — reactivates silently if a status code is ever added without updating both).

**RAG staged activation:** `STAGED_ACTIVATION_EXECUTED` (see `OPERATOR_DECISIONS.md`). Allowlist `technical_manual,price_list` only. **No** global `RAG_CORE=v2`.

**4.4 Install-prep:** `REJECTED_BY_OPERATOR / NO PRODUCT ACTIVATION` — scaffold may exist; do not develop.

## Closed — RAG-V2-FINAL-TECHNICAL-GATE-01 (2026-08-08)

| ID                             | Disposition             | Note                                                                                                                                                                                                                 |
| ------------------------------ | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RAG-V2-FINAL-TECHNICAL-GATE-01 | COMPLETE / proven_local | Closed `RAG-TEMPORAL-COMPLETE-01` + `RAG-IMAGE-BAKE-01`; container-only Gate B; dual-read; staged activate/rollback/restore; proof `eval/rag-v2-final-technical-gate-20260808/`; status `STAGED_ACTIVATION_EXECUTED` |
| RAG-TEMPORAL-COMPLETE-01       | COMPLETE / proven_local | 3/3 COMPLETE + resume + idempotency on tracked ingest worker                                                                                                                                                         |
| RAG-IMAGE-BAKE-01              | COMPLETE / proven_local | Tracked `Dockerfile.rag-v2-ingest` + lock; runtime `:local` (not docker-commit tags)                                                                                                                                 |

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
