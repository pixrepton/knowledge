# Session Memory Policy

Status: active. Last updated: 2026-07-13.

Persistent session memory has one owner: `knowledge/memory/`.

## Canonical Files

- `OPERATOR_DECISIONS.md` - durable operator decisions. Keep the stability-freeze entry.
- `BACKLOG.md` - only open work with status and next action.
- `ACTIVE_WORKSPACE.md` - current workspace direction and proven state.
- `LAST_SESSION.md` - short summary of the last meaningful session.

## Session Hooks

- Start runner: `scripts/run-session-start-hooks.ps1`.
- Stop runner: `scripts/run-session-stop-hooks.ps1`.
- Scratch output: `C:\top-code-session-scratch\` unless `TOP_CODE_SESSION_SCRATCH` overrides it.

Hook outputs are temporary operator context, not documentation and not persistent memory.

## Prohibited Persistent Stores

- `top-code-memory/`
- repo-local `memory-bank/`
- raw transcript archives
- reflection stores
- shadow backlogs
- generated DRIFT/session chronologies in repo

## Write Rules

- Record facts, decisions and open work only once.
- Do not store secrets, raw customer data, terminal dumps or full transcripts.
- Do not keep history for its own sake; Git and the operator's external copy are the history.
- If a session produces no durable decision or open task, do not update memory files just to create a log.
