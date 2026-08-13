# Git And Change Control

Status: canonical shared Git procedure for Codex, Claude Code and human-led agent runs.
Qualified: 2026-08-02.

This document defines how agent work becomes durable local Git history without
absorbing unrelated workspace state. It extends the workspace `AGENTS.md` and
`CODEX_EXECUTION_MAP.md`; it does not create another task registry or project
memory layer.

## Core Decision

An accepted write task authorizes the agent to create a local task branch and
safe scoped local commits needed to complete that task.

It does not authorize push, pull request creation, merge, deployment, VPS work,
production mutation, destructive cleanup or history rewriting.

The default publication mode is `LOCAL_ONLY`.

## Required Flow

```text
task-start
  -> task-branch when current branch is protected/default
  -> implementation and task-gate
  -> task-commit-plan
  -> task-commit
  -> post-commit gates
  -> READY_TO_CLOSE
  -> task-close
```

All write routes (`SMALL`, `MEDIUM`, `CRITICAL`) use the Wave 01 checkpoint.
`READ` never creates a checkpoint solely to answer a question.

## Publication Modes

| Mode | Local branch/commit | Push and draft PR | Merge | Deploy/live mutation |
|---|---:|---:|---:|---:|
| `LOCAL_ONLY` | Allowed | Not allowed | Not allowed | Not allowed |
| `PUBLISH` | Allowed | Allowed within task scope | Not allowed | Not allowed |
| `SHIP` | Allowed | Allowed; prepare merge-ready proof | Separate approval | Separate approval |

Change mode explicitly in the checkpoint. Never infer publication permission
from a previous conversation or from the existence of a remote.

## Branch Rule

Before the first write, determine the exact repository root and current branch.
Do not edit on:

- the repository default branch;
- `main`, `master` or `trunk`;
- detached HEAD;
- a branch involved in merge, rebase, cherry-pick or revert.

Use:

```text
python scripts/ai_os_task.py task-branch --repo <repo> --name <branch>
```

Prefer work-based names, not tool-based names:

```text
repair/RP-22-runtime-proof
fix/DQ-17-runtime-ownership
docs/git-change-control
```

Do not name branches `codex/*` or `claude/*` by default. One agent may start the
work and another may resume it.

## Commit Readiness

`COMMIT_READY` requires all of the following:

- the repository belongs to the active checkpoint;
- the current branch is a non-protected task branch;
- no merge/rebase/cherry-pick/revert is in progress;
- the task is not blocked and has no open blocker;
- the current owned diff is inside declared `repo:path` scope;
- ownership conflicts are absent or can be mechanically isolated from the
  preserved task-start baseline;
- a current passing gate matches the exact current repo state;
- the planned commit contains no detected secret or sensitive path;
- the commit can be built without staging or absorbing unrelated changes.

`NO_COMMIT` means the repository has no task-owned change to record.

`BLOCKED` means the agent must resolve the stated issue and rerun the plan. The
agent must not bypass the wrapper with raw Git commands.

## Commands

Plan:

```text
python scripts/ai_os_task.py task-commit-plan --repo <repo> --json
```

Commit:

```text
python scripts/ai_os_task.py task-commit \
  --repo <repo> \
  --message "fix(scope): describe the completed result"
```

The commit wrapper:

1. refreshes the ownership model;
2. obtains a per-repository commit lock;
3. builds an isolated temporary Git index from `HEAD`;
4. includes only task-owned file states;
5. subtracts preserved pre-task dirty hunks when mechanically safe;
6. preserves unrelated staged files and same-file foreign staged hunks;
7. scans planned file states for high-confidence secrets;
8. runs normal Git commit hooks through the temporary index;
9. restores the real index to the expected preserved-user state;
10. verifies the actual paths in the new commit;
11. records `repo:SHA` in the Wave 01 checkpoint;
12. performs no push.

After a commit, rerun the applicable final gates. A gate fingerprint containing
the previous `HEAD` is intentionally stale after the commit.

## Dirty Tree Ownership

The task-start baseline distinguishes:

- foreign staged files;
- foreign unstaged files;
- foreign untracked files;
- explicitly adopted baseline paths;
- task-owned staged, unstaged and untracked changes.

Never treat an unfamiliar change as disposable. Do not stage, commit, restore,
clean or reset it.

A pre-existing dirty path may be adopted only through explicit task scope. An
adopted path becomes task-owned and must be committed or otherwise resolved
before closure.

If task and foreign changes touch non-overlapping text hunks in one tracked
file, the wrapper may isolate the task-only commit and leave the foreign hunk
staged or unstaged after the new `HEAD`.

If changes overlap, are binary, involve a foreign untracked file, or cannot be
reconstructed deterministically, commit planning returns `BLOCKED`.

## Multi-Repository Work

Each repository has its own:

- branch;
- baseline SHA;
- dirty state;
- gates;
- commit SHA;
- remote publication action.

There is no atomic workspace-wide commit. A cross-repo task creates one or more
commits in each owner repository and records every `repo:SHA` in the same task
checkpoint. Verify owner and consumer contracts before closure.

Do not use root Git status as evidence for nested repositories.

## Multiple Agents

In one shared working tree:

- subagents may inspect and edit only disjoint declared scopes;
- the main agent owns branch changes, staging, commit planning and commits;
- no two agents may manipulate the same Git index concurrently;
- the commit lock is a safety net, not a substitute for file ownership.

A subagent may commit only when it runs in a separate explicit worktree and
branch with its own checkpointed scope. It returns the branch and SHA to the
main agent for integration.

## Prohibited Operations

Agents must not run:

- raw `git add` or raw `git commit`;
- `git reset`;
- `git clean`;
- destructive `git restore`;
- `git checkout -- <path>`;
- force push;
- `git stash drop` or `git stash clear`;
- `git branch -D`;
- automatic amend, rebase or other history rewrite;
- hook/check bypasses.

Recovery possibility through reflog is not authorization.

## GitHub Handoff

GitHub is publication and collaboration, not the source of truth for the local
runtime or dirty working tree.

Before push or PR creation:

- publication mode must be `PUBLISH` or `SHIP`;
- inspect the complete branch diff against the intended base;
- run the repository checks that would block CI;
- confirm the branch and remote;
- ensure every commit belongs to the task;
- write PR text from the actual diff and evidence.

A claimed PR must be confirmed by its actual repository, number and head SHA.
Do not report a PR merely because a title/body was prepared.

Merge remains a separate operator-approved action. `SHIP` does not authorize
merge or deployment.

## Completion Report

Report per repository:

- branch and base;
- initial and final SHA;
- created commit SHA and subject;
- actual committed paths;
- preserved foreign staged/unstaged/untracked state;
- gates and exact outcomes;
- publication action, if any;
- remaining residue, blockers and risk.

Never report `PASS` while required post-commit gates or runtime proof are
missing.

## Regression Scenarios

The shared engine must keep automated tests for at least:

1. protected-branch write denial;
2. scoped local commit and automatic SHA recording;
3. foreign staged file not absorbed;
4. foreign staged hunk in the same file preserved;
5. task/foreign overlap blocked;
6. secret pattern blocked;
7. write outside declared scope blocked;
8. raw Git add/commit blocked in Claude and Codex adapters;
9. `LOCAL_ONLY` push/PR denial;
10. closure blocked when task-owned residue remains.
