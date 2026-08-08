# RAG-V2-LIVE-CUTOVER-READINESS-01 — proof summary

**proof_id:** `rag-v2-live-cutover-readiness-20260808`  
**date:** 2026-08-08  
**repos:** `rag-chat-asystent` (feature/aios-roadmap-1.4-2.4), workspace `scripts/`, `knowledge`  
**base_git_sha (rag):** `79071f0` (pre-commit worktree)

## Bounds (binding)

- Does **not** flip global product default `RAG_CORE=v2`.
- Staged cutover file remains opt-in: `docker-compose.rag-v2-staged-cutover.yml`.
- Final product influence requires operator decision gate (authorization received for staged activation **after** readiness proof).

## Architecture

```text
rag-backend (query/API)
rag-v2-ingest-worker (Docling + Temporal activities)  ← canonical ingest runtime
MinIO + Postgres DocumentVersion + Qdrant + Temporal
```

Docling is **not** required inside every API process; it is required live in the containerized ingest worker.

## Evidence table

| Component | Code | Live service | Real operation | Restart | Product active |
|-----------|------|--------------|----------------|---------|----------------|
| Docling (RAG-01) | yes | host + worker container | host PDF→graph; worker runs Docling in Temporal activity | worker restart OK | soft / opt-in |
| MinIO (RAG-02) | yes | compose | put/get + checksum via live ingest | retrieve after restart | opt-in plane |
| Postgres DV (RAG-03) | yes | graphstore | DocumentVersion persist in live ingest | yes | opt-in plane |
| Qdrant (RAG-04) | yes | compose | upsert + retrieve evidence | yes | opt-in plane |
| Temporal (RAG-05) | yes | compose + worker | start_ingest; activity live Docling (CPU, long) | worker restart | opt-in plane |
| RAG-12 Gate B | harness | compose profile | host companion PASS `summary-20260808T081726.json` | yes | n/a |
| RAG-09 | cutover gate | env flags | rollback proven process-local | n/a | **legacy default** |

## Gate results

| Gate | Result | Notes |
|------|--------|-------|
| Gate A (`pytest backend/tests -q`) | **PASS** `681 passed, 22 skipped` | 2026-08-08 |
| Gate B host companion | **PASS** | `knowledge/eval/rag-v2-live-cutover-20260808/summary-20260808T081726.json` — real PDF → Docling → MinIO → PG → Qdrant → retrieve → worker restart → retrieve |
| Gate B Temporal COMPLETE (container) | **PARTIAL** | Worker executes live Docling activities; COMPLETE under CPU load is slow / flaky vs RPC poll timeouts. Residual below. |
| Dual-read + rollback | **PASS** | `dual-read-rollback.json` — cutover gate + rollback to legacy; recommendation `B_STAGED_CUTOVER` |
| `/rag_v2/status` | **PASS** (when stack wired) | `live_data_plane=true`, adapters docling/minio/postgres/qdrant/temporal activated |

## Artifacts (tracked pointers)

- `knowledge/eval/rag-v2-live-cutover-20260808/summary-20260808T081726.json`
- `knowledge/eval/rag-v2-live-cutover-20260808/harness-20260808T081726.json`
- `knowledge/eval/rag-v2-live-cutover-20260808/dual-read-rollback.json`
- Raw logs: `C:\top-code-session-scratch\rag-v2-live-cutover\` (gitignored)

## Cutover decision

**READY_FOR_OPERATOR_CUTOVER_DECISION** with technical recommendation **B — staged cutover** (`technical_manual`, `price_list`) via opt-in compose file only.

Operator chat authorization for activation exists, but **global/default product flip is deferred** until Temporal container COMPLETE is stably green under Gate B (or operator explicitly accepts PARTIAL Temporal residual).

Suggested activation (when accepted):

```powershell
docker compose --profile rag-v2-data-plane `
  -f docker-compose.yml `
  -f docker-compose.rag-v2-data-plane.yml `
  -f docker-compose.rag-v2-staged-cutover.yml up -d
```

Rollback: omit staged-cutover file / `RAG_CORE=legacy`.

## Residuals

1. **Image bake:** `requirements-deploy.lock` includes minio/qdrant-client/temporalio; full image rebuild blocked by torch CDN timeouts — interim `Dockerfile.rag-v2-ingest` + `docker commit …:with-dataplane-sdk`.
2. **Temporal COMPLETE Gate B:** activity timeout raised to 30m; `max_concurrent_activities=1`; host RPC describe timeouts under load remain.
3. **Do not** set `RAG_CORE=v2` as compose default.

## Status labels (honest)

| Item | Delivery | Proof | Activation |
|------|----------|-------|------------|
| RAG-01 | COMPLETE_BOUNDED | PROVEN_RUNTIME (host + worker Docling path) | n/a |
| RAG-12 | COMPLETE_BOUNDED | PROVEN_RUNTIME (host E2E); Temporal COMPLETE PARTIAL | n/a |
| RAG-09 | COMPLETE_BOUNDED | PROVEN_RUNTIME (opt-in + rollback) | OPERATOR_DECISION_REQUIRED / staged file ready |
