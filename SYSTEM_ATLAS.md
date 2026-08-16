# System Atlas

Status: active cross-repo map. Last updated: 2026-08-14.

Short domain overview. Package navigation: `system-atlas/INDEX.md`.
Case OS architecture: `gmail-agent/docs/core/CONSTITUTION_V2_1.md`.
Ownership contract: `source-of-truth.md` — do not duplicate it here.

## Ownership

| Area | Owner | Rule |
| --- | --- | --- |
| Mailbox, cases, engagements, runtime truth | `gmail-agent` | Operational SoT. |
| Operator UI and HITL projection | `daszek` | Projection-only; not write SoT. |
| HVAC logic and `OfferDTO` | `kalk-top` | Do not duplicate elsewhere. |
| Cieplo workflow | `cieplo-orchestrator` | Separate worker and DB. |
| RAG retrieval/ingest | `rag-chat-asystent` | Advisory/read path, not case SoT. |
| WordPress RAG surface | `rag-widget` | HTTP client only. |
| PDF/DOCX generation | `top-instal-generator` | Consumes contracts, does not own HVAC logic. |

## Runtime Direction

- Local Docker is the current execution environment.
- Production/VPS is suspended unless the operator explicitly reopens it.
- Current stability freeze protects proven local runtime behavior.

## Main Flows

1. Case OS ingress: Gmail / Drive / Calendar / Operator command → `gmail-agent` intake → signal worker → case/runtime state → Daszek projection → operator HITL → `gmail-agent` reconciliation. Architecture: `gmail-agent/docs/core/CONSTITUTION_V2_1.md`.
2. HVAC offer flow: form/Cieplo input → `kalk-top` → generator → operator/customer document path.
3. RAG flow: user/widget question → `rag-chat-asystent` → response; no case write ownership.

## Integration Rules

- New cross-repo HTTP edges require explicit contract impact analysis.
- OfferDTO changes start in `kalk-top` and then update consumers.
- Daszek UI state must be traceable back to Node B or its bounded local store.
- Runtime proof claims belong in the owning repo runbook, not in this atlas.
