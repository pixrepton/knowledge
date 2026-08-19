# AGENTS.md — knowledge

Status: **Typ A — independent Git repository**, canonical project knowledge.
Created 2026-08-13 (`AIOS-CONTROL-PLANE-REPAIR-20260813`): the repo was listed as
Typ A in root `AGENTS.md` §Repository Routing and required by
`agent_harness_audit.py`, but had no L2 adapter.

Root `AGENTS.md` (L1) applies whenever work runs inside `top-code workspace`.
This file is an adapter, not an alternate constitution and not a second memory system.

## Role

Owns canonical project knowledge: routing, decisions, policies, registries,
tooling guidance, evaluation artifacts and durable operator memory.

It is a **documentation and decision** Source of Truth. It is **not** a runtime
Source of Truth: `gmail-agent` / Node B owns cases, engagements, mailbox policy,
decisions and execution state. When a document here disagrees with current code,
tests or runtime, the runtime wins and the document is stale.

## Owns / Must not

| Owns | Must not |
| --- | --- |
| `INDEX.md` — the only cold-start order and need→file router | Duplicate the cold-start order anywhere else |
| `memory/` — the four durable memory files | Grow a fifth memory store, shadow backlog or parallel decision log |
| `source-of-truth.md` — ownership contract | Restate or fork domain logic owned by product repos |
| `CONTROL_PLANE.md`, `*_POLICY.md` — evidence, documentation, engineering, session-memory and tooling rules | Weaken root `AGENTS.md`, SoT boundaries or proof discipline |
| `system-atlas/` — workflows, repairs, tooling routers and the agent harness contract | Become a code index; graphs and generated views are not maintained documentation |
| `eval/`, `rfc/` — proof packs and active RFCs | Store secrets, tokens, customer data or mailbox dumps |

## Read first

1. Root `../AGENTS.md` — L1 constitution, Task and Git Control
2. `INDEX.md` — cold-start and routing (this repo owns it)
3. `memory/OPERATOR_DECISIONS.md` — active operator decisions and the stability freeze
4. `CONTROL_PLANE.md` — how to classify evidence and claim strength
5. `DOCUMENTATION_POLICY.md` before adding or restructuring any document

## Write / task scope

- Commit scope is `knowledge:<path>`. `knowledge` is its own Git unit — never infer
  its state from workspace-root Git.
- Use the shared task engine, never raw `git add` / `git commit`:

```powershell
python scripts/ai_os_task.py task-commit-plan --repo knowledge --json
python scripts/ai_os_task.py task-commit --repo knowledge --message "<message>"
```

- Do not write `memory/*` without an explicit operator instruction.
- New documents require a route: an unrouted document is invisible and becomes
  stale by default. Add it to `INDEX.md` §On Demand or to the owning
  `system-atlas` package, or do not add it.
- Prefer editing an existing canonical document over creating a parallel one.

## Gate A

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File knowledge/_gate_docs_sync_a.ps1
python scripts/context_link_audit.py --scope workspace
```

When `system-atlas/tooling/` or `system-atlas/tooling/agent-harness/` changed, the
harness gates are also part of Gate A, because both audits read their contracts
from this repo:

```powershell
python scripts/agent_harness_audit.py
python scripts/agent_map_audit.py
```

A documentation change that breaks a route is a failure even when every file it
touched is individually well written.

## Cross-repo

- `INDEX.md` and `source-of-truth.md` are consumed by every other repo's agent.
  Changing a route or an ownership statement here is a cross-repo change: verify
  the owning repo still matches the claim before editing.
- `system-atlas/tooling/GIT_AND_CHANGE_CONTROL.md` and `CODEX_EXECUTION_MAP.md` are
  the canonical procedures referenced from root `AGENTS.md`, `scripts/AGENTS.md`
  and `.agents/`. Keep the path stable — eight files point at it.
- `system-atlas/tooling/agent-harness/*.yaml` are executable contracts, not prose.
  Editing them changes what the workspace gates accept.
- Do not copy product-repo runbooks here. Link to the owning repo instead.

## Anti-goals

- A second cold-start procedure, or a copy of root `AGENTS.md`.
- Restoring `top-code-memory/`, repo-local `memory-bank/`, transcript or reflection
  stores, shadow backlogs, or parallel decision logs.
- Treating `world-state.yaml`, `TOPINSTAL-KERNEL-GRAPH.yaml` or any generated graph
  as live dependency or runtime proof.
- Documenting intent as if it were proven behavior.
- Keeping `payload/` copies of canonical documents — canonical lives here.

## Safety capsule

- Default operational scope is local Docker only. No VPS, SSH, production mutation
  or deployment from work in this repo.
- Publication default is `LOCAL_ONLY`. Local commit authorization never implies
  push, PR, merge or deploy.
- No secrets, tokens, credentials, customer data or mailbox content in any file.
- The active stability freeze in `memory/OPERATOR_DECISIONS.md` is binding.
- Never report `PASS` without the proof the affected layer requires; documentation
  changes prove routes, not runtime.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **knowledge** (2520 symbols, 3418 relationships, 98 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> Index stale? Run `node .gitnexus/run.cjs analyze` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? `npx gitnexus analyze` (npm 11 crash → `npm i -g gitnexus`; #1939).

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows. For regression review, compare against the default branch: `detect_changes({scope: "compare", base_ref: "main"})`.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `query({search_query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `context({name: "symbolName"})`.
- For security review, `explain({target: "fileOrSymbol"})` lists taint findings (source→sink flows; needs `analyze --pdg`).

## Never Do

- NEVER edit a function, class, or method without first running `impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit changes without running `detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/knowledge/context` | Codebase overview, check index freshness |
| `gitnexus://repo/knowledge/clusters` | All functional areas |
| `gitnexus://repo/knowledge/processes` | All execution flows |
| `gitnexus://repo/knowledge/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
