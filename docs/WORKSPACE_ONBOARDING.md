# Workspace Onboarding

Status: active router. Last updated: 2026-07-14.

## What This Workspace Is

TOP-INSTAL AI-OS is a multi-repo local workspace:

- `gmail-agent/` - Node B operational SoT for mailbox, cases, engagements and runtime truth.
- `daszek/` - Node A projection-only operator UI and HITL surface.
- `kalk-top/` - HVAC calculation and `OfferDTO` owner.
- `rag-chat-asystent/` - RAG backend and ingest.
- `rag-widget/` - WordPress RAG client.
- `cieplo-orchestrator/` - separate Cieplo workflow worker.
- `top-instal-generator/` - PDF/DOCX generation.
- `fast-kalk/` - lead widget.
- `knowledge/` - cross-repo routing, policies, decisions and current state.

## Cold-Start

Canonical cold-start order lives in `knowledge/INDEX.md` §Cold-Start (this file is one step in that order). Do not duplicate the sequence here.

Manual session context is generated outside repo by `scripts/run-session-start-hooks.ps1`.

## Runtime Defaults

- Local Docker is the default environment.
- Production/VPS/SSH/deploy is suspended unless explicitly requested.
- Do not run runtime proofs for documentation-only cleanup.
- Do not duplicate endpoint, DDL, route or module inventories in docs; inspect source/tests/generators.

## Deep Manuals

- Node B: `gmail-agent/docs/core/PROJECT_README.md`
- Node A: `daszek/docs/core/PROJECT_README.md`
- HVAC: `kalk-top/docs/architecture/APPLICATION_WORKFLOW_AND_ENGINES_README.md`

## Active Policies

- Engineering: `knowledge/ENGINEERING_POLICY.md`
- Tooling: `knowledge/TOOLING_POLICY.md`
- Documentation: `knowledge/DOCUMENTATION_POLICY.md`
- Session memory: `knowledge/SESSION_MEMORY_POLICY.md`

## Proof Vocabulary

Use precise labels:

- `implemented in code`
- `runtime enabled`
- `freshly proven locally`
- `operator verified`

Do not collapse them into "done".
