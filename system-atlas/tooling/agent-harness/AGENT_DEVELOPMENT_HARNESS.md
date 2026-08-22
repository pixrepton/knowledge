# AGENT_DEVELOPMENT_HARNESS.md

Status: canonical control-plane map for `top-code workspace`.
Restored 2026-08-13 (`AIOS-CONTROL-PLANE-REPAIR-20260813`).

Referenced as "Control-plane map" from root `AGENTS.md`, root `CLAUDE.md`,
`.agents/AGENTS.md` and `.agents/skills/cursor-codex-harness/SKILL.md`.

A rewrite for the multi-repo workspace. The pre-2026-07 copy under
`archive-codex-and-claude/` describes the `gmail-agent` monolith and its paths no
longer resolve; do not restore it.

## What this document is

The map of **where agent behaviour is actually enforced**, so that a change to the
control plane can be made in the right layer instead of by adding another document.

It is not a constitution (root `AGENTS.md`), not a cold-start (owned by
`knowledge/INDEX.md`), and not a routing table for code intelligence (owned by
`../CODE_INTELLIGENCE_ROUTER.md`).

## The layers

Enforcement strength decreases downward. A rule stated only in a lower layer is a
suggestion; a rule implemented in an upper layer is binding.

| # | Layer | Where | Enforces |
| --- | --- | --- | --- |
| 1 | Permission allow/deny | `.claude/settings.local.json`, `.cursor/permissions.json` | Hard command blocks before any tool runs |
| 2 | Lifecycle hooks | `scripts/ai_os_claude_hook*.py`, `scripts/ai_os_codex_hook*.py`, `.claude/settings.json`, `.codex/hooks.json`, `.cursor/hooks.json` | Write guard, destructive-git guard, publication mode, checkpoint refresh |
| 3 | Declarative rules | `.codex/rules/git-change-control.rules` | Codex-side forbidden/prompt decisions with match/not_match examples |
| 4 | Task engine | `scripts/ai_os_task*.py` | Ownership, scope, gates, locks, scoped commits |
| 5 | Constitution and adapters | root `AGENTS.md` / `CLAUDE.md`, per-repo `AGENTS.md` | Invariants, SoT boundaries, completion standard |
| 6 | Procedural skills | `.agents/skills/`, mirrored to `.claude/skills/` where the client requires it | How to execute and prove a specific kind of work |
| 7 | Knowledge and memory | `knowledge/` | Routing, decisions, policies, durable operator memory |

**Design rule:** when an agent keeps violating something, do not add a seventh
paragraph to layer 5. Move the rule up. The reason raw `git commit` is genuinely
unavailable is `RAW_GIT_PATTERNS` in layer 2, not the prose in layer 5.

## Contracts in this directory

| File | Consumed by | Effect of editing |
| --- | --- | --- |
| `AGENT_HARNESS_MANIFEST.yaml` | `scripts/agent_harness_audit.py` | Changes which capabilities and core skills must exist |
| `AGENT_MAP_SCENARIOS.yaml` | `scripts/agent_map_audit.py` | Changes which routes, markers, rules, subagents and adapters are asserted |
| `AGENT_SKILLS_REGISTRY.md` | `agent_harness_audit.py`, skill authors | Registry of core skills; every core skill must be named here |

These are executable contracts, not prose. Editing them changes what the gates accept.

## Gates

```powershell
python scripts/agent_harness_audit.py      # manifest-driven: capabilities, core skills, L1/L2 adapters
python scripts/agent_map_audit.py          # scenario-driven: cold start, routes, MCP roles, skill contracts
python scripts/context_link_audit.py --scope workspace   # route integrity across control-plane documents
```

Run all three after any change to `.agents/`, `.claude/agents/`, `.cursor/rules/`,
`scripts/ai_os_task*`, the hook adapters, or this directory.

`context_link_audit.py` audits both markdown links and **backticked path citations**,
because this workspace expresses routes overwhelmingly in the latter form. It also
refuses to excuse a missing `knowledge/...` or `gmail-agent/...` target as
"cross_repo" when that repository is present in the working tree. Both behaviours
exist because their absence let six dead canonical routes pass as green.

## Adding a control-plane rule

1. Decide the lowest layer that can actually enforce it (see the table above).
2. If it is layer 1–3, implement it there and add a test under `scripts/dev-tooling/`.
3. If it is layer 4, extend the task engine and cover it in `test_ai_os_*`.
4. If it is layer 5–7, write it once, in the owning file, and route to it.
5. Never state the same rule in two layers without a test that keeps them in sync —
   root `AGENTS.md` and root `CLAUDE.md` already drifted this way.
6. Re-run the three gates.

## Known structural debts

Recorded here so they are not rediscovered as if new:

- Root `AGENTS.md` and root `CLAUDE.md` are near-duplicates with no generator and no
  sync test; the "answer in Polish" rule exists only in the `CLAUDE.md` copy, so
  Codex and Cursor never receive it.
- `.agents/skills/` and `.claude/skills/` mirror by hand because the two clients use
  different skill discovery roots.
- `AI_OS_TASK_ID` has been observed as a **persistent Windows user environment
  variable**, which silently overrides per-session task resolution for every agent on
  the machine. A task pointer belongs to a session, never to `HKCU\Environment`.
- `task-close` requires at least one commit and one gate, so a legitimate read-only
  task cannot be closed cleanly — only archived via `task-cleanup --archive`.
- `task-finalize` (2026-08-23) runs the deterministic close orchestration in one
  command: validate -> commit-plan -> commit -> optional post-commit gate
  (`--gate-id/--gate-repo/--gate-profile`) -> refresh stale PASSED gate
  fingerprints from recorded argv -> checkpoint READY_TO_CLOSE -> close.
  `task-gate --profile <name>` resolves deterministic pytest collections
  (repo-scoped, `scripts/ai_os_task_profiles.py`) and supports `--timeout` with
  owned-process cleanup + always-on UTF-8 gate logs.

## Anti-goals

- A second constitution, cold-start, backlog or memory store.
- Documenting a tool as available when Step 0 cannot confirm it in the session.
- Restoring monolith-era paths (`memory-bank/`, embedded `Daszek/`).
- Treating a passing gate as runtime proof.
