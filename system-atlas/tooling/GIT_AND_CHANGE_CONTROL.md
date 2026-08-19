# Git and change control (canonical)

Status: canonical procedure for agent Git workflow in `top-code workspace`.
Referenced from root `AGENTS.md`, `scripts/README.md`, `scripts/AGENTS.md`, harness skills.

## Principles

1. **Nested repos are separate Git units.** Root workspace meta-repo never commits product paths (`gmail-agent/`, `kalk-top/`, …) — use `task-commit --repo <nested>`.
2. **Agents never use raw `git add` / `git commit`** for task work. Use `scripts/ai_os_task.py`.
3. **Commit is a reasoned decision, not a checkbox and not an operator poll.** The agent analyzes, emits a verdict, then acts.
4. **Default publication is `LOCAL_ONLY`.** Local commit authorization does not authorize push, PR, merge or deploy.

## Task lifecycle

```text
task-start → task-branch (if needed) → writes → task-gate → task-commit-plan → decision → task-commit → task-close
```

Full command examples: `scripts/README.md` §Agent task and Git workflow.

## Commit decision discipline

Before every `task-commit`, run:

```powershell
python scripts/ai_os_task.py task-commit-plan --repo <repo> --json
```

The JSON payload includes a `decision` object. The agent **must** read it and include the same reasoning in the session report (section `## Decyzja commit`).

### Verdicts

| `decision.decision` | Meaning                                             | Agent action                                  |
| ------------------- | --------------------------------------------------- | --------------------------------------------- |
| `COMMIT_NOW`        | Slice complete; plan `COMMIT_READY`; scope coherent | Run `task-commit` without asking the operator |
| `COMMIT_LATER`      | Owned work exists but blockers remain               | Fix blockers; do **not** commit yet           |
| `NO_COMMIT`         | No owned paths in this repo                         | Continue work or close if no residue          |
| `DEFER_OPERATOR`    | Ownership conflict or policy ambiguity              | Stop; state conflict; wait for operator       |

### When `COMMIT_NOW`

All must hold:

1. `task-commit-plan.verdict` = `COMMIT_READY`
2. Every owned path is inside `declared_write_scope` (or adopted baseline)
3. Gate fingerprint matches current repo state (PASS recorded)
4. Logical slice is complete — no imminent edit to the same contract in the same turn
5. Task is not `CLOSED` / `ABORTED_WITH_EVIDENCE` (open micro-task first if follow-up)
6. `next_action` is empty when preparing `READY_TO_CLOSE`

### When `COMMIT_LATER`

Typical signals (engine surfaces these in `decision.blockers`):

- plan `BLOCKED` (stale gate, protected branch, secrets, nested path from root)
- `next_action` still describes unfinished slice work
- owned paths outside scope
- ownership conflicts
- task already closed while files remain dirty
- lock-file / topology snapshot must be regenerated **after** final harness edits (order: content → gates → lock → commit)

### When `NO_COMMIT`

- No task-owned dirty paths in the repo
- Review-only / Ask mode (no writes)

### Forbidden agent behavior

- Asking the operator "czy commit?" for routine scoped implementation
- Claiming `PASS` / `done` with uncommitted task-owned residue
- Closing a task before committing in-scope harness changes that are part of the same slice
- `git add -A` from workspace root

### Allowed operator ask

Only when `decision.ask_operator` is true or publication requires explicit push/merge/deploy authorization.

## Multi-repo tasks

Commit **per repository**, in dependency order when known:

1. Contracts / shared types owner first
2. Consumers second
3. Workspace harness / docs last (often includes `workspace-repos.lock.json` as final step)

Run `task-commit-plan` separately per repo; each plan carries its own `decision`.

## Agent report template

```markdown
## Decyzja commit

- Werdykt: COMMIT_NOW | COMMIT_LATER | NO_COMMIT | DEFER_OPERATOR
- Repo: <repo>
- Uzasadnienie: <1-3 zdania>
- Proof: <gate / test run>
- Następny krok: <task-commit | naprawa blockera | brak>
```

Copy from `decision.agent_report` when using `task-commit-plan --json`.

## Hooks and adapters

- Codex: `scripts/ai_os_codex_hook.py`
- Claude Code: `scripts/ai_os_claude_hook.py`
- Cursor: `.cursor/rules/95-commit-decision-discipline.mdc`

## Related

- Proof economy: root `AGENTS.md` §Change Discipline / Proof Economy
- Execution ladder: `.agents/skills/cursor-codex-harness/SKILL.md`
- Proof gates: `.cursor/rules/92-proof-gate-discipline.mdc`

## Control-plane gotchas

Short operational notes from consolidation sessions. Keep them concrete.

### Task-id resolution precedence

`resolve_task_id` resolves in this order:

1. explicit `--task-id`
2. `AI_OS_TASK_ID` environment variable
3. a single active task
4. otherwise error

A stale `AI_OS_TASK_ID` pointing to a closed/archived task can block writes or
raise "task is archived". Prefer passing `--task-id` explicitly; the env var set in
a parent process cannot be cleared from inside the session.

### Raw-git guard

The destructive/raw-git/publication regexes match newline-separated commands
(`(^|[;&|\n]\s*)` with `re.M`), so a bare `git add`/`commit`/`push` on its own
line is caught. Do not rely on this as an excuse to bypass `task-commit`; it is a
guard, not an authorization path.

### CRLF phantom detection

A "modified" file with an empty `--numstat` or `--ignore-cr-at-eol --numstat` is
usually a CRLF phantom. Confirm by comparing the `md5` of `HEAD:<file>` and the
working file **with and without** stripping `\r`; identical-after-strip means
CRLF-only. 18 of 22 dirty files in the consolidation pass were CRLF-only.

Prefer a `.gitattributes` LF policy per repository. Renormalize only after proving
content is identical, and never fold foreign dirty state into the same commit.

### Foreign ownership

Do not commit autoformat/whitespace changes to files owned by another active task
(e.g. a task that declares `knowledge:INDEX.md` or `knowledge:eval/...` in
`declared_write_scope`). Isolate your own owned paths and leave the rest untouched.
