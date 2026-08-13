# CODE_INTELLIGENCE_ROUTER.md

Status: canonical route table for code intelligence in `top-code workspace`.
Restored 2026-08-13 (`AIOS-CONTROL-PLANE-REPAIR-20260813`).

Referenced by `.agents/skills/code-intelligence-routing/SKILL.md`,
`knowledge/TOOLING_POLICY.md` and root `AGENTS.md`. This document owns the routing
detail; those files point here rather than restating it.

## Rule zero — prove availability before routing

Repo documentation (root `AGENTS.md`, generated `<!-- gitnexus:start -->` blocks,
the `gitnexus-*` skills) describes GitNexus `query` / `context` / `impact` as MCP
tools and `gitnexus://...` as MCP resources. **That text is not evidence that the
server is registered in the current session.**

Every session, before the first structural query:

```
ToolSearch(query: "gitnexus", max_results: 15)
```

- Tools returned → GitNexus MCP is live; use the routes below as written.
- Nothing returned → GitNexus is CLI/index-only for this session. Do **not** fall
  back silently to plain `Read`/`Grep`. Route through Codebase Memory (CBM).

The same applies to Serena. `knowledge/TOOLING_POLICY.md` states the general form
of this rule: *"Before relying on an index, prove tool availability plus the
freshness and coverage needed for the claim"* and *"Do not use errored or stale
MCP servers as evidence."*

Observed on 2026-08-13: `gitnexus` and `serena` were declared in `.mcp.json`, their
binaries were on PATH, and `gitnexus mcp` answered a direct MCP handshake with 17
tools — yet neither server was registered in the Claude Code session. Availability
is a per-session fact, not a property of the config file.

## Tool roles

| Tool | Owns | Is not |
| --- | --- | --- |
| **Context7** | Current public documentation for external libraries, frameworks, SDKs, APIs | Aware of local architecture |
| **GitNexus** | Architecture, processes, clusters, dependencies, blast radius, routes, cross-repo contracts | An editor or runtime proof |
| **CBM** | Structural graph, call graph, types, routes, resources, custom Cypher | The default tool for every exploration |
| **Serena** | Symbols, declarations, implementations, references, semantic edits | A complete cross-repo architecture map |
| **CodeScene** | Maintainability, Code Health, change-quality gates | A dependency oracle or functional test |
| **Playwright** | Browser behavior, UI flows, console, network, browser→backend proof | A code architecture tool |
| **Tests and runtime** | Proof of actual system behavior | Optional |

Graphs do not prove runtime behavior. Do not run every tool when one canonical
route answers the question.

## Choose the route

Each row lists the first tool when its server is live, and the fallback that
applies when Step 0 says it is not.

| Need | First tool | Fallback when unavailable | Next step |
| --- | --- | --- | --- |
| External library or API documentation | Context7 | web docs | inspect local integration |
| Unknown local area or concept | GitNexus `query` | CBM `search_code` | process, cluster or context |
| Architecture or workflow | GitNexus resources/process | CBM `get_architecture` | key symbols |
| Concrete symbol | Serena `find_symbol` | CBM `search_graph` | references or implementations |
| Dependencies or blast radius | GitNexus `impact` | CBM `trace_path` (`direction=inbound`, `risk_labels=true`) | confirm callers |
| Exact call graph or custom relation | CBM `get_graph_schema` → `trace_path` / `query_graph` | — | implementation read |
| Public HTTP API | GitNexus `route_map` / `api_impact` | CBM `query_graph` over route nodes | `shape_check`, contract test |
| MCP, RPC or tool contract | GitNexus `tool_map` | CBM `search_graph` | implementation |
| Cross-repo contract | GitNexus group contracts | CBM per-repo `project=` + manual join | verify owners and runtime path |
| Type, interface or DTO | Serena | CBM `search_graph` | CBM confirmation at high risk |
| Refactor | CodeScene review + GitNexus impact | CodeScene review + CBM `trace_path` | semantic edit |
| Rename | Serena rename | manual + CBM `trace_path` to enumerate callers | never find-and-replace |
| Backend or workflow debugging | GitNexus query/trace | CBM `trace_path` | runtime |
| UI or browser debugging | Playwright | — | owning backend path |
| Before commit | tests → GitNexus `detect_changes` | tests → CBM `detect_changes` | CodeScene safeguard |
| Final UI proof | Playwright | — | confirm console and network |

## Standard change path

1. Resolve the owning repository and Source of Truth.
2. Context7 when correctness depends on an external library or API.
3. Structural pass for the local process, affected area and blast radius
   (GitNexus if live, otherwise CBM).
4. Symbol pass for exact references (Serena if live, otherwise CBM).
5. CBM when raw graph structure, exact paths or custom queries are needed.
6. CodeScene review before a refactor.
7. Edit semantically when the change is symbol-scoped.
8. Run the required deterministic tests.
9. Run runtime, integration or Playwright proof appropriate to the affected layer.
10. Run `detect_changes` on whichever structural tool is live.
11. Run CodeScene `pre_commit_code_health_safeguard`.
12. Do not declare success from a graph, snapshot or Code Health score alone.

## High-risk protocol

A change is high-risk when it affects a public API, DTO or payload shape, database
state, authorization, policy or HITL, a cross-repo contract, Source of Truth
boundaries, routing, side effects, or external communication.

Required for high-risk work:

- impact or contract analysis (GitNexus if live, else CBM `trace_path` inbound),
- references or implementations (Serena if live, else CBM `search_graph`),
- CBM as independent structural confirmation where applicable,
- tests,
- runtime, integration or Playwright proof.

Shortcut when only CBM is available:

```text
CBM trace_path (impact, direction=inbound, risk_labels=true) on every symbol you are
about to edit → confirm no CRITICAL/HIGH caller you have not accounted for → edit
```

## Index and freshness rules

| Tool | Scope | Freshness rule |
| --- | --- | --- |
| **CBM** | Per-repository projects, named `C-Users-<user>-Desktop-top-code-workspace-<repo>` | Always pass explicit `project=`. Run `list_projects` once per session rather than guessing. Compare the project's `head_sha` against `git rev-parse HEAD`. Never substitute the root project for a repo-specific graph. |
| **GitNexus** | True Git repos plus root shell; group `topinstal-workspace` for cross-repo | Reindex with `node .gitnexus/run.cjs analyze` from the project root |
| **Serena** | Per-repository project configuration | Root is only a workspace shell |
| **CodeScene** | On-demand analysis | No durable local graph |
| **Context7** | External documentation only | Always current by definition |
| **Playwright** | Current browser state only | No index |

Reindex only the affected repository. Do not auto-reindex broad workspaces.
Report stale, incomplete or unavailable tools explicitly instead of working around
them silently.

After substantial code, contract, topology or workflow changes, assess whether
GitNexus, CBM, Serena or maintained `knowledge/` artifacts require refresh.

## Boundaries

- Do not use Context7 for local Source of Truth discovery, local DTOs, workflows,
  policies, callers, runtime proof, secrets or internal payloads.
- Do not treat generated node counts, endpoint lists or line numbers as maintained
  documentation.
- When tools disagree, verify current source, configuration and runtime. Never
  silently reconcile conflicting evidence by guessing.
