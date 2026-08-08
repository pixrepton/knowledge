# RAG-V2-FINAL-TECHNICAL-GATE-01 — proof summary

**proof_id:** `rag-v2-final-technical-gate-20260808`  
**date:** 2026-08-08  
**repos:** `rag-chat-asystent`, `knowledge`, workspace `scripts/` (unchanged harness)  
**label:** `proven_local`

## Bounds (binding)

- Does **not** set global product default `RAG_CORE=v2` for all intents.
- Staged allowlist only: `technical_manual,price_list` via opt-in `docker-compose.rag-v2-staged-cutover.yml`.
- Operator authorization already existed — **not** re-asked.
- Docling ingest for this Gate B was **container-only** (Temporal worker); no host Docling substitute.

## Residuals closed

| ID | Result | Evidence |
| --- | --- | --- |
| `RAG-IMAGE-BAKE-01` | **PASS** | Tracked `backend/Dockerfile.rag-v2-ingest` + `requirements-deploy.lock`; runtime image `rag-chat-asystent-rag-v2-ingest-worker:local` (not `dataplane-sdk` / `with-dataplane-sdk`); `image-bake-proof.json` |
| `RAG-TEMPORAL-COMPLETE-01` | **PASS** | 3/3 COMPLETE + restart/resume + idempotency; `temporal-3x.json` — OVERALL PASS |

## Gate results

| Gate | Result | Notes |
| --- | --- | --- |
| Gate A | **PASS** `684 passed, 22 skipped` | `python -m pytest backend/tests -q` |
| Gate B container-only | **PASS** | Temporal COMPLETE → EvidencePack → worker restart → retrieve; `gate-b-container-only-20260808T170906.json` |
| Dual-read + rollback | **PASS** | `dual-read-rollback.json` — recommendation `B_STAGED_CUTOVER` |
| Staged activation | **PASS** | container `/health` `rag_core=v2` + allowlist env |
| Product routing | **PASS** | `product-routing-proof.json` — TM/price serve, other abstain |
| Post-activation rollback | **PASS** | omit staged file → `rag_core=legacy` |
| Staged restore | **PASS** | re-include staged file → `rag_core=v2` |

## Architecture

```text
rag-backend (query/API; staged RAG_CORE=v2 allowlist)
rag-v2-ingest-worker (Docling + Temporal activities) ← canonical ingest
MinIO + Postgres DocumentVersion + Qdrant + Temporal
```

## Artifacts

- `temporal-3x.json`
- `image-bake-proof.json`
- `gate-b-container-only-20260808T170906.json`
- `dual-read-rollback.json`
- `product-routing-proof.json`
- `staged-activation-health.json`
- `post-activation-rollback-health.json`
- `staged-restored-health.json`
- Raw logs: `C:\top-code-session-scratch\rag-v2-final-tech-gate\` (gitignored)

## Decision status (exit)

```text
STAGED_ACTIVATION_EXECUTED
```

Allowlist: `technical_manual,price_list`. Local Docker only. No global default flip.
