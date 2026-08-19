# Knowledge Index

Status: active entry point. Last updated: 2026-08-19 (P4 vs P3B fork freeze).

Read this file first, then only the files needed for the current task.

**Current program posture (binding via memory):** the one current full Fresh38 has been
**executed and requalified (measurement)**. Product capability remains below threshold.
P2 causal observability is **CLOSED**. P3A frozen K3 adjudication is **COMPLETE**.
Execution fork frozen: **P4 first** (next slice P4-A MI-02); P3B deferred to step 5.
Do not open another residual wave.
Do not open roadmap 5.3-8.x "from the list".

```text
HISTORICAL BASELINES (prior SUT / older contract, not comparable to current): 13 Aug = 23 CLEAN_PASS / 15 CAPABILITY; 08 Aug = 10 / 28
FRESH38_MEASUREMENT_QUALIFICATION = REQUALIFIED
FULL FRESH38 AGAINST CURRENT CODE = RUN (38/38 capture QUALIFIED, attempt fresh38_full_current_20260816T124100)
CURRENT CAPABILITY BASELINE = 27 CLEAN_PASS / 11 CAPABILITY (contract v5, threshold 34) → NOT QUALIFIED — CAPABILITY
P2_CAPABILITY_CAUSAL_OBSERVABILITY = PASS / CLOSED (gmail-agent ae597505, workspace 800318a7)
P3A_FROZEN_K3_ADJUDICATION = COMPLETE (INT-04/NEW-05/FU-01/MI-01 PRIMARY_CLASS=EVALUATOR_WRONG)
P4_VS_P3B_FORK = FROZEN (NEXT_EXECUTION=P4, NEXT_SLICE=P4-A_MI-02)
NEXT = P4-A MI-02; P3B deferred step 5; not a new recapture
```

Closed facts that remain binding: `OPERATOR-COMMAND-RECONCILE-BYPASS-01` is **CLOSED**;
registry `REQUIRED_OPEN = 0`, `UNKNOWN_NEEDS_PROOF = 0`. RAG technical gates
(`RAG-TEMPORAL-COMPLETE-01`, `RAG-IMAGE-BAKE-01`) are closed and re-verified clean.
RAG staged activation = `STAGED_ACTIVATION_EXECUTED` (allowlist `technical_manual,price_list`
only, no global `RAG_CORE=v2`). Slice 4.4 = `REJECTED_BY_OPERATOR / NO PRODUCT ACTIVATION`.
Details: `memory/OPERATOR_DECISIONS.md`, `memory/ACTIVE_WORKSPACE.md`, `memory/BACKLOG.md`,
`docs/AI_OS_ROADMAP.md`.

## Choose The Route

| Need | Open next | Authority and freshness rule |
| --- | --- | --- |
| Owner of data or business logic | `source-of-truth.md` | Canonical ownership contract; confirm behavior in current code/runtime. |
| Case OS architecture (runtime, memory, decision, execution, projection) | `gmail-agent/docs/core/CONSTITUTION_V2_1.md` | Authoritative Case OS constitution; do not duplicate it here. |
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
| `gmail-agent/docs/core/CONSTITUTION_V2_1.md` | `CANONICAL_CONTRACT` | Case OS architecture: intake, journal, policy, HITL, execution, projection | Owned by `gmail-agent`; this index only points there. |
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

- `eval/mail-agent-intelligence-current/` — current 11-CAPABILITY residual matrix, P2 proof, P3A reports, P4 vs P3B fork.
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

This is the only cold-start order in the workspace. Do not duplicate it elsewhere.
It has two entry modes, because `knowledge` is an independent Git repository and can
be opened on its own.

### Whole workspace session

Work started at `top-code workspace` root, targeting one or more product repos.

1. root `AGENTS.md`
2. this file
3. `memory/OPERATOR_DECISIONS.md`
4. `memory/BACKLOG.md` only when planning or package status matters
5. `memory/ACTIVE_WORKSPACE.md` and `memory/LAST_SESSION.md` only for continuity
6. target repo `AGENTS.md`
7. the route selected above and the target repo manual/runbook only when needed

### Work opened directly inside the `knowledge` Git repo

Only this repository is open; root `AGENTS.md` may not be loaded.

1. `knowledge/AGENTS.md` — the local Typ A adapter: role, owns/must-not, Gate A,
   cross-repo duties and the safety capsule
2. this file
3. `memory/OPERATOR_DECISIONS.md`
4. `DOCUMENTATION_POLICY.md` before adding or restructuring any document
5. root `AGENTS.md` as soon as the change touches anything outside `knowledge/`

Root `AGENTS.md` still governs whenever the work runs inside the workspace; the
local adapter narrows it, never replaces it.

History is in Git and in the operator's external copy, not in active documentation.
