# Engineering Policy

Status: active. Last updated: 2026-08-02.

## Defaults

- Diagnose with evidence before editing: health/status, logs, config, code, tests.
- Prefer the smallest root-cause fix. Do not add new layers to hide a local bug.
- Keep runtime, endpoint, schema and env contract changes explicit and proven.
- Production/VPS work is out of scope unless the operator explicitly reopens it.
- Do not claim `freshly proven locally` without a current local proof.

## Safety

- Never print, commit or document secrets, DSNs, tokens, private keys or raw customer data.
- Secret values belong in Bitwarden/local gitignored env files, not docs.
- If a secret is found in a planned or tracked diff, stop and report a redacted warning.
- Legal/license/security publication docs are protected.

## Error Handling

- For service failures: check health, then logs, then env/config, then code.
- For test failures: identify whether the failing contract is business/runtime or documentation-only.
- Escalate only when a blocker cannot be resolved from local evidence or missing secrets/access.
- Record only live follow-up work in `knowledge/memory/BACKLOG.md`.

## Workspace Lifecycle

- The workspace and nested repositories may already be dirty. Capture and preserve the pre-task staged, unstaged and untracked state per repository.
- Every write task uses the Wave 01 checkpoint, declared `repo:path` scope and a non-protected task branch.
- A request to fix, implement, configure, migrate, update or close a repair package authorizes safe local branch creation and scoped local commits required to finish that task.
- Local commit authorization never implies push, PR, merge, deployment, VPS or production mutation.
- Default publication mode is `LOCAL_ONLY`; use `PUBLISH` or `SHIP` only when the operator includes remote publication in scope.
- Do not use raw `git add` or `git commit` for agent work. Use the ownership-aware `task-commit-plan` and `task-commit` commands.
- Do not run `git reset`, `git clean`, destructive restore/checkout, force push, stash deletion, forced branch deletion or automatic history rewriting.
- Do not stop containers or alter compose/env as part of documentation cleanup.
- Update `world-state.yaml` only when a stable endpoint/owner changes.

Canonical Git procedure:

`knowledge/system-atlas/tooling/GIT_AND_CHANGE_CONTROL.md`
