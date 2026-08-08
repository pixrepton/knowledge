# Engineering Policy

Status: active. Last updated: 2026-07-13.

## Defaults

- Diagnose with evidence before editing: health/status, logs, config, code, tests.
- Prefer the smallest root-cause fix. Do not add new layers to hide a local bug.
- Keep runtime, endpoint, schema and env contract changes explicit and proven.
- Production/VPS work is out of scope unless the operator explicitly reopens it.
- Do not claim `freshly proven locally` without a current local proof.

## Safety

- Never print, commit or document secrets, DSNs, tokens, private keys or raw customer data.
- Secret values belong in Bitwarden/local gitignored env files, not docs.
- If a secret is found in a tracked diff, stop and report a redacted warning.
- Legal/license/security publication docs are protected.

## Error Handling

- For service failures: check health, then logs, then env/config, then code.
- For test failures: identify whether the failing contract is business/runtime or documentation-only.
- Escalate only when a blocker cannot be resolved from local evidence or missing secrets/access.
- Record only live follow-up work in `knowledge/memory/BACKLOG.md`.

## Workspace Lifecycle

- Worktree may be dirty; separate your changes from pre-existing changes.
- Do not run `git reset`, `git clean`, commit, push or deploy unless explicitly requested.
- Do not stop containers or alter compose/env as part of documentation cleanup.
- Update `world-state.yaml` only when a stable endpoint/owner changes.
