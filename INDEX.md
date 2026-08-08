# Knowledge Index

Status: active entry point. Last updated: 2026-08-08 (KNOWLEDGE-SYNC-6CHAT-01).

Read this file first, then only the files needed for the current task.

**Current program posture (binding via memory):** do not open roadmap 5.3–8.x “from the list”.
Open residuals only: `FACT-SUPERSESSION-WRITE-01`, `RAG-TEMPORAL-COMPLETE-01`, `RAG-IMAGE-BAKE-01`
(+ optional IQ adjudication / GOV-06). RAG staged activation =
`STAGED_ACTIVATION_AUTHORIZED — BLOCKED_BY_TECHNICAL_GATE`. Slice 4.4 =
`REJECTED_BY_OPERATOR / NO PRODUCT ACTIVATION`. Details: `memory/OPERATOR_DECISIONS.md`,
`memory/ACTIVE_WORKSPACE.md`, `docs/AI_OS_ROADMAP.md`.

## Choose The Route

| Need | Open next | Authority and freshness rule |
| --- | --- | --- |
| Owner of data or business logic | `source-of-truth.md` | Canonical ownership contract; confirm behavior in current code/runtime. |
| Current implementation or runtime | Owning repo source, Git, tests and local runtime | Stronger than every document or generated view. |
| AI-OS program plan / residual registry | `docs/AI_OS_ROADMAP.md` | Plan + residual ledger; open tickets also mirrored in `memory/BACKLOG.md`. |
| Workflow, repair, tooling or cross-repo evidence | `system-atlas/INDEX.md` | Canonical router for System Atlas packages. |
| Codex execution route | `system-atlas/tooling/CODEX_EXECUTION_MAP.md` | Canonical task/domain/tool/gate router. |
| Durable operator decision or open work | `memory/OPERATOR_DECISIONS.md`, then `memory/BACKLOG.md` | Project memory, not runtime truth. |
| Interrupted-work continuity | `memory/ACTIVE_WORKSPACE.md` and `memory/LAST_SESSION.md` only when relevant | Continuity snapshots; verify against Git and current package records. |

## Qualified Entrypoints

| Entry | Authority | Open when | Freshness / fallback |
| --- | --- | --- | --- |
| `source-of-truth.md` | `CANONICAL_CONTRACT` | Resolving domain and data ownership | Current code/runtime wins if implementation diverges. |
| `CONTROL_PLANE.md` | `CANONICAL_CONTRACT` | Classifying evidence and claim strength | Use the root evidence hierarchy when runtime, code and docs disagree. |
| `ARCHITECTURE_DECISIONS.md` | `CANONICAL_CONTRACT / LIMITED_FRESHNESS` | A change touches an active architectural invariant | Verify named symbols and runtime claims in the owning repo before relying on them. |
| `DOCUMENTATION_POLICY.md`, `ENGINEERING_POLICY.md`, `SESSION_MEMORY_POLICY.md` | `CANONICAL_CONTRACT` | Documentation, engineering or memory rules apply | Higher `AGENTS.md` and explicit operator instructions retain precedence. |
| `TOOLING_POLICY.md` | `CANONICAL_CONTRACT` | Selecting or maintaining agent tooling | Prove current host availability and index freshness before relying on a tool. |
| `system-atlas/INDEX.md` | `CANONICAL_ROUTER` | Entering workflows, repairs, tooling or historical baselines | Follow its package-specific validator/fallback. |
| `system-atlas/tooling/CODEX_EXECUTION_MAP.md` | `CANONICAL_ROUTER` | Routing Codex implementation work | Correct a dead route from current Git/source evidence. |
| `docs/WORKSPACE_ONBOARDING.md` | `CANONICAL_ROUTER` | A human or agent needs the short workspace overview | It defers cold-start order back to this file. |
| `world-state.yaml` | `UNQUALIFIED_STATE_SNAPSHOT` | A topology hint is useful | Compiled 2026-07-13; verify endpoints, flags and runtime before use. |
| `SYSTEM_ATLAS.md` | `ADVISORY` | A short domain overview is sufficient | Use `system-atlas/INDEX.md` for package navigation and current repos for truth. |
| `TOPINSTAL-KERNEL-GRAPH.yaml` | `ADVISORY` | A curated cross-repo relationship hint is useful | Last qualified 2026-06-11; never use as live dependency/runtime proof. |

## Durable Decisions And State

| Entry | Authority | Rule |
| --- | --- | --- |
| `memory/OPERATOR_DECISIONS.md` | `CANONICAL_CONTRACT` | Durable operator decisions and the active stability freeze. |
| `memory/BACKLOG.md` | `CURRENT_OPERATIONAL_STATE / DIRTY_IN_PROGRESS` | Open work only; verify status against current package records and Git. |
| `memory/ACTIVE_WORKSPACE.md` | `CURRENT_OPERATIONAL_STATE / DIRTY_IN_PROGRESS` | Direction and proven-state continuity, not code/runtime truth. |
| `memory/LAST_SESSION.md` | `CONTINUITY_SNAPSHOT / DIRTY_IN_PROGRESS` | Resume aid only; it does not define the next step when a package ledger is newer. |

## On Demand

- `docs/AI_OS_ROADMAP.md` - active AI-OS program plan + residual registry (post-6-chat consolidation).
- `docs/AIOS_4_1_FACT_SUPERSESSION_CONSUMER_AUDIT.md` - fact supersession consumer audit (write residual separate).
- `eval/rag-v2-live-cutover-20260808/PROOF_SUMMARY.md` - RAG V2 live cutover readiness proof.
- `docs/daszek-system-diagrams.md` - retained because it is an active Daszek UI manifest source.
- `docs/entity-vs-correlation-registry.md` - active identity contract note.
- `docs/graphstore-schema.md` - active GraphStore contract note.
- `docs/deploy-token-tiers.md` - active token/deploy reference.
- `docs/operator-glossary.md` - active Case/Task and operational feed terminology note.
- `rfc/` - only RFCs that still describe active or future decisions.

## Cold-Start

1. `AGENTS.md`
2. this file
3. `memory/OPERATOR_DECISIONS.md`
4. `memory/BACKLOG.md` only when planning or package status matters
5. `memory/ACTIVE_WORKSPACE.md` and `memory/LAST_SESSION.md` only for continuity
6. target repo `AGENTS.md`
7. the route selected above and the target repo manual/runbook only when needed

History is in Git and in the operator's external copy, not in active documentation.
