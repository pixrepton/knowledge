# Tooling Policy

Status: active. Last updated: 2026-08-02.

## Tool Choice

- In Codex safe mode, default to direct Git, source reads and `rg` for known files, current diffs and final verification.
- Use graph or indexed tools only when they materially improve discovery, impact analysis or symbol tracing for an explicit repo.
- Before relying on an index, prove tool availability plus the freshness and coverage needed for the claim.
- Current code, tests, Git state and local runtime outrank indexes, generated reports and historical snapshots.

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
