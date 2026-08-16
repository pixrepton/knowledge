# Source Of Truth

Status: active. Last updated: 2026-08-14.

Ownership only. Case OS architecture and invariants live in
`gmail-agent/docs/core/CONSTITUTION_V2_1.md` — do not duplicate them here.

| Information | Owner | Non-owner |
| --- | --- | --- |
| Gmail / Drive / Calendar / Operator ingress | `gmail-agent` | Daszek, RAG, other product repos |
| Signal / event spine | `gmail-agent` | Daszek, RAG, docs |
| Agent Runtime, policy, HITL decisions | `gmail-agent` | Daszek (UI only) |
| Mailbox cases, engagements, runtime truth | `gmail-agent` | Daszek, RAG, docs |
| Operator projection and bounded HITL surface | `daszek` | write SoT; mailbox / policy / execution |
| HVAC calculation and `OfferDTO` | `kalk-top` | gmail-agent, RAG, generator |
| RAG knowledge retrieval | `rag-chat-asystent` | case state, OfferDTO |
| PDF/DOCX rendering | `top-instal-generator` | HVAC business logic |
| Cross-repo decisions and open work | `knowledge/memory/*` | repo-local memory banks |
| UI system diagrams manifest source | `knowledge/docs/daszek-system-diagrams.md` | generated manifest as source |

`daszek` is projection-only: it is not the write Source of Truth for cases,
decisions, or execution.

If docs conflict with code, tests, schemas or fresh proof, the lower-confidence document must be updated or deleted.
