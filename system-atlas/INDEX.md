# System Atlas Index

Status: `CANONICAL_ROUTER`. Last updated: 2026-08-14.

This file routes System Atlas packages. It does not replace `knowledge/INDEX.md`
(workspace cold-start), `source-of-truth.md` (ownership), or product-repo
constitutions. Case OS architecture lives in
`gmail-agent/docs/core/CONSTITUTION_V2_1.md`.

Open only the package needed for the current task.

## Packages

| Package | Authority | Open when | Entry |
| --- | --- | --- | --- |
| Tooling — code intelligence | `CANONICAL_ROUTER` | Choosing GitNexus / CBM / Serena / Context7 / Playwright | [tooling/CODE_INTELLIGENCE_ROUTER.md](tooling/CODE_INTELLIGENCE_ROUTER.md) |
| Tooling — Codex execution | `CANONICAL_ROUTER` | Routing READ / SMALL / MEDIUM / CRITICAL work | [tooling/CODEX_EXECUTION_MAP.md](tooling/CODEX_EXECUTION_MAP.md) |
| Tooling — Git and change control | `CANONICAL_ROUTER` | Branch, ownership, scoped commit, publication mode | [tooling/GIT_AND_CHANGE_CONTROL.md](tooling/GIT_AND_CHANGE_CONTROL.md) |
| Tooling — agent harness | `CANONICAL_CONTRACT` | Control-plane layers, where agent behaviour is enforced | [tooling/agent-harness/AGENT_DEVELOPMENT_HARNESS.md](tooling/agent-harness/AGENT_DEVELOPMENT_HARNESS.md) |
| Tooling — skills registry | `CANONICAL_CONTRACT` | Which procedural skills to load | [tooling/agent-harness/AGENT_SKILLS_REGISTRY.md](tooling/agent-harness/AGENT_SKILLS_REGISTRY.md) |
| Repairs | `WAVE_01_COMPLETE / WAVE_02_CLOSED` | Historical repair overlay; do not reopen as a live program | [repairs/README.md](repairs/README.md) |
| Workflows | Workflow Registry v1 | Cross-repo workflow records, gaps, contracts | [workflows/WORKFLOW_REGISTRY.yaml](workflows/WORKFLOW_REGISTRY.yaml) |

## Workflows

There is no README at `workflows/` root. Canonical records in that directory:

- `WORKFLOW_REGISTRY.yaml` — Workflow Registry v1
- `validate_workflow_atlas.py` — local validator
- `WORKFLOW_ATLAS.md`, `CROSS_REPO_CONTRACTS.md`, `STATE_OWNERSHIP_MATRIX.md` — derived/supporting maps

Validate with:

```powershell
python knowledge/system-atlas/workflows/validate_workflow_atlas.py
```

## Repairs

Status in [repairs/README.md](repairs/README.md): `WAVE_01_COMPLETE / WAVE_02_CLOSED`.
This overlay does not create a Capability Registry and is not the next program.

## Fallback

If a route here is dead, use current Git, owning-repo source, and
`knowledge/INDEX.md`. Do not invent a missing atlas file.
