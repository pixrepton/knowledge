# Tooling Policy

Status: active. Last updated: 2026-08-02.

## Tool Choice

- In Codex safe mode, default to direct Git, source reads and `rg` for known files, current diffs and final verification.
- Use graph or indexed tools only when they materially improve discovery, impact analysis or symbol tracing for an explicit repo.
- Before relying on an index, prove tool availability plus the freshness and coverage needed for the claim.
- Current code, tests, Git state and local runtime outrank indexes, generated reports and historical snapshots.

## Code Exploration

Reading a known file at a known path is a direct read. **Exploration** — an unknown
area, symbol, workflow, dependency, contract or blast radius — is different, and the
default of reaching for workspace-wide `Read`/`Grep` is wrong.

- Route through the appropriate MCP/graph tool first, then read narrowly only the
  files that tool identified.
- The route table, per-need first tools and fallbacks live in
  `system-atlas/tooling/CODE_INTELLIGENCE_ROUTER.md`. This policy does not restate them.
- The procedure an agent follows is `.agents/skills/code-intelligence-routing/SKILL.md`
  (Claude Code uses the `.claude/skills/` mirror, same rules).
- Availability is a per-session fact. Run the skill's Step 0 every session before the
  first structural query; a server declared in `.mcp.json` may not be registered.
- When the routing tool is unavailable, use the documented fallback and say so. Do not
  fall back silently to broad `Read`/`Grep` and present the result as a routed answer.

## MCP / Plugins

- Use one tool for one responsibility; do not chain tools without a concrete need.
- Do not use errored or stale MCP servers as evidence.
- Do not auto-reindex broad workspaces. Refresh only the one explicit repo when the task needs it and the route allows it.
- Plugins/skills are workflow aids, not source of truth.
- OpenMemory or similar semantic memory is optional L5 context, never canonical project memory.
- Project memory remains `knowledge/memory/*`; tooling state is not project memory.

## Generated Graphs and Reports

- Static graphs, Graphify outputs, GitNexus reports and code intelligence snapshots are generated views.
- Keep generators only when useful; write outputs on demand to gitignored scratch or output locations.
- Do not treat generated node counts, endpoint lists or line numbers as maintained documentation.

## Evidence Labels

- Runtime/proof artifact: strongest evidence for readiness claims.
- Source code/tests/migrations/schemas: strongest evidence for implementation claims.
- Maintained docs: routing and operational context.
- Historical exports, old audits and transcripts: not source of truth.
