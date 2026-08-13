# AGENT_SKILLS_REGISTRY.md

Status: canonical registry of workspace procedural skills.
Restored 2026-08-13 (`AIOS-CONTROL-PLANE-REPAIR-20260813`).

Consumed by `scripts/agent_harness_audit.py` (`check_registry_lists_skills`): every
`core_skills` entry in `AGENT_HARNESS_MANIFEST.yaml` must be named here.

## What a skill is — and is not

A skill describes **how** to execute and prove a specific kind of work. A skill
never overrides:

- root `AGENTS.md` (L1 constitution),
- product-repo `AGENTS.md` (L2 adapter),
- Source of Truth boundaries,
- proof discipline and the evidence hierarchy.

Load **1–3** relevant skills per task. Loading the whole pack is an anti-goal:
it inflates the router and drowns the actual task.

## Discovery roots

| Client | Reads | Note |
| --- | --- | --- |
| Codex / Cursor | `.agents/skills/` | canonical pack |
| Claude Code | `.claude/skills/` | `Skill` cannot see `.agents/`; mirrors exist only where required |

When a skill is mirrored, `.agents/skills/` is the source and the mirror must not
diverge in rules — only in client-specific invocation notes.

## Core skills

| Skill | Path | Load when | Do not load when |
| --- | --- | --- | --- |
| `code-intelligence-routing` | `.agents/skills/code-intelligence-routing/` | Exploring an unknown area, symbol, workflow, dependency, contract or blast radius; before broad `Read`/`Grep`; before an edit that depends on unrouted structure | External library docs only (Context7); runtime or browser proof; operator gave an exact file and line range |
| `cursor-codex-harness` | `.agents/skills/cursor-codex-harness/` | Writing implementation prompts, task specs, handoff prompts, read order, Definition of Done, validation commands, anti-drift instructions | A domain skill already covers execution and no prompt design is needed |
| `agent-skill-quality-gate` | `.agents/skills/agent-skill-quality-gate/` | Creating, editing or reviewing any skill under `.agents/skills/` | Using an existing skill without changing it |
| `policy-action-gates` | `.agents/skills/policy-action-gates/` | `policy_engine`, `DecisionCandidate`, `PolicyDecision`, APv2 intent, `ToolPlan`, HITL, reply drafts, send/archive actions, cooldowns, execution permissions in `gmail-agent` | Passive classification or projection with no action or policy decision |
| `gmail-agent-proof-run` | `.agents/skills/gmail-agent-proof-run/` | Running and reporting a bounded proof inside `gmail-agent` | No runtime proof is required for the change |
| `topinstal-node-topology` | `.agents/skills/topinstal-node-topology/` | Reasoning about Node A / Node B topology and which node owns a datum or action | Work stays inside a single repo with no cross-node contract |

`code-intelligence-routing` is the workspace's default pre-`Read`/`Grep` activator.
Its **Step 0** — verifying which MCP servers are actually registered in the current
session — is mandatory every session, not once. Repo documentation describes GitNexus
MCP tools as always available; that text is not evidence.

## Client-only skill packs

`.claude/skills/gitnexus/` holds GitNexus usage skills (`gitnexus-exploring`,
`gitnexus-impact-analysis`, `gitnexus-debugging`, `gitnexus-refactoring`,
`gitnexus-guide`, `gitnexus-cli`, `gitnexus-pdg-query`, `gitnexus-taint-analysis`,
`gitnexus-pr-review`). These are **not** core skills: they are only usable when
Step 0 confirms the GitNexus MCP server is registered. When it is not, only
`gitnexus-cli` applies, because the on-disk index under `.gitnexus/` remains valid
even while the MCP surface is unavailable.

## Adding or changing a skill

1. Run `agent-skill-quality-gate` first.
2. Give the skill concrete **Use When** and **Do Not Use When** sections — a skill
   without exclusions bloats the router.
3. Keep `SKILL.md` short; deep material belongs in `references/`.
4. Add the skill to this registry.
5. Add it to `core_skills` in `AGENT_HARNESS_MANIFEST.yaml` only if it is genuinely
   cross-cutting.
6. Ensure at least one scenario in `AGENT_MAP_SCENARIOS.yaml` lists it under
   `must_load` — `agent_map_audit.py` fails on any core skill no scenario covers.
7. Re-run both gates:

```powershell
python scripts/agent_harness_audit.py
python scripts/agent_map_audit.py
```

## Anti-goals

- Using skills as an alternate constitution or a parallel memory bank.
- Duplicating full Cursor rules inside a skill.
- Registering a repo-local procedure as a workspace skill.
- Keeping a skill that documents a tool Step 0 cannot confirm.
