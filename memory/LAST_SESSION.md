# Last Session

Updated: 2026-08-08 — **RAG-V2-LIVE-CUTOVER-READINESS-01**.

## Done this session

- **RAG-V2-LIVE-CUTOVER-READINESS-01** CLOSED `PARTIAL` / readiness for operator decision
  - Canonical ingest = `rag-v2-ingest-worker` (Docling), not Docling-in-every-API-image
  - Live plane: MinIO + Postgres DocumentVersion + Qdrant + Temporal wired via compose profile
  - Host Gate B companion **PASS** (`summary-20260808T081726.json`)
  - Dual-read + rollback **PASS**; recommendation **B staged cutover**
  - Gate A rag: **681 passed, 22 skipped**
  - Product default remains `RAG_CORE=legacy`; staged compose file opt-in only
  - Operator authorization recorded; **no auto global cutover**

## Prior this day

- **FACT-4.1-HIGH-01** CLOSED
- **FRESH38-RECAPTURE-01** CLOSED

## Still open

- Temporal container COMPLETE under Gate B (CPU Docling flake) — residual
- Image bake with lock SDKs (torch CDN) — interim commit/`Dockerfile.rag-v2-ingest`
- FACT-SUPERSESSION-WRITE-01 · GOV-06 · IQ-01 human labels

## Proof labels

`knowledge/eval/rag-v2-live-cutover-20260808/PROOF_SUMMARY.md` — RAG-01/09/12 `COMPLETE_BOUNDED` / `PROVEN_RUNTIME` with Activation `OPERATOR_DECISION_REQUIRED`.
