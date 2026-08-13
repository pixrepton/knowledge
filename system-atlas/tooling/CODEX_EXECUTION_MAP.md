# Codex Execution Map

Status: canonical workspace navigation for Codex. Qualified: 2026-08-02.

This document routes work. It does not replace `AGENTS.md`, project memory,
repository manuals, test harnesses, runtime proof, or the Wave 01 tooling. Git
branch, commit and publication behavior is defined by
[Git And Change Control](GIT_AND_CHANGE_CONTROL.md).

## Route In 15 Seconds

1. Find the owner in [Domain Router](#domain-router).
2. Read the applicable instruction chain in [Instruction Route](#instruction-route).
3. Choose the smallest sufficient route below.
4. Open the named source of truth and use the existing gate for that repository.
5. Finish with the proof required by the route, not with narrative confidence.

| Route | Use when | Wave 01 state | Minimum finish |
|---|---|---|---|
| `READ` | Question, review, diagnosis, status, or navigation with no writes | Do not start a checkpoint | Cite current source/evidence and state unknowns |
| `SMALL` | One repository, one bounded concern, no contract/data/security/runtime risk | Required when files will be written; no checkpoint for read-only SMALL work | Focused gate, scoped local commit when a change exists, post-commit proof and closure `PASS` |
| `MEDIUM` | Several related files, normal implementation, limited contract impact, or useful package proof | Required: start/resume, ledger, close | Focused gates, package gate where present, scoped commit, closure `PASS` |
| `CRITICAL` | Cross-repo contract, ownership, data, security, idempotency, recovery, migration, or runtime parity | Required; checkpoint before every risky boundary | Contract and focused tests, cross-repo/runtime proof as applicable, scoped commits, closure `PASS` |

`DISCOVERY` is a temporary phase, not a fifth route. End it as soon as owner,
repository, source, write scope, and proof route are known. Then select one route
above or report a concrete blocker.

Route-to-tooling mapping: `SMALL -> SMALL`, `MEDIUM -> MEDIUM`, and
`CRITICAL -> CRITICAL` when invoking [Wave 01](#wave-01-execution-state).

## Domain Router

Open the workspace [AGENTS.md](../../../AGENTS.md) first, then the row for the
owning repository. A consumer does not become the owner of a contract merely
because it validates, renders, or displays it.

| Domain / repository | Owns | Must not own or duplicate | Open next |
|---|---|---|---|
| `gmail-agent` / Node B | Mailbox intake, cases, engagements, policy, execution, operational runtime truth | HVAC pricing/sizing or `OfferDTO`; Daszek presentation | [AGENTS](../../../gmail-agent/AGENTS.md), [project manual](../../../gmail-agent/docs/core/PROJECT_README.md), [last proven runtime](../../../gmail-agent/docs/runbooks/LAST_PROVEN_STATE.md) only for runtime claims |
| `daszek` / Node A | Operator projection UI and bounded HITL | Case, decision, or execution SoT; Node B reconcile semantics | [AGENTS](../../../daszek/AGENTS.md), [project manual](../../../daszek/docs/core/PROJECT_README.md), then the Node B contract when feed semantics change |
| `kalk-top` | HVAC calculation, pricing/data rules, `OfferDTO` | Document rendering, mailbox/case semantics | [AGENTS](../../../kalk-top/AGENTS.md), [architecture](../../../kalk-top/docs/architecture/APPLICATION_WORKFLOW_AND_ENGINES_README.md), protected contract named by the repo router; also load a nested `AGENTS.md` under `core/`, `kalkulator/`, `konfigurator/`, or `wp-adapter/` when applicable |
| `top-instal-generator` | DOCX/PDF rendering from `OfferDTO` | HVAC decisions or pricing | [AGENTS](../../../top-instal-generator/AGENTS.md), [API contract](../../../top-instal-generator/docs/API_GENERATE_OFFER_DOCUMENT.md) |
| `cieplo-orchestrator` | Separate Cieplo ingress/pipeline and its own DB | A second case SoT; duplicated kalk-top/generator behavior | [AGENTS](../../../cieplo-orchestrator/AGENTS.md), [README](../../../cieplo-orchestrator/README.md); open owner contracts in kalk-top/generator for boundary changes |
| `rag-chat-asystent` | RAG ingest, retrieval, chat API, grounding | Case SoT, `OfferDTO`, Gmail pipeline | [AGENTS](../../../rag-chat-asystent/AGENTS.md), [START_HERE](../../../rag-chat-asystent/docs/START_HERE.md), [local runtime](../../../rag-chat-asystent/docs/LOCAL_RUNTIME.md); see the dead-link warning below |
| `fast-kalk` | Lead widget and its integration flow | HVAC engine, PDF mapping, Node B registry semantics | [AGENTS](../../../fast-kalk/AGENTS.md), [README](../../../fast-kalk/README.md), then kalk-top/generator/Node B owner contracts as needed |
| `rag-widget` | WordPress RAG client/proxy surface | Retrieval, embeddings, backend chat semantics | [AGENTS](../../../rag-widget/AGENTS.md), [README](../../../rag-widget/README.md), [response DTO](../../../rag-widget/hvac-rag-chat/README-DTO.md) |
| `knowledge` | Cross-repo routing, policies, operator decisions, active state, workflow/repair records | Product runtime truth or a parallel execution memory | [Knowledge router](../../INDEX.md); for workflow, repairs, tooling or cross-repo evidence use the [System Atlas router](../INDEX.md), then the narrow record |

Cross-repo rule: name the owner of every changed contract before editing a
consumer. Verify both the owning contract and the consuming flow.

## Instruction Route

Observed effective order for Codex in this workspace:

```text
Codex host system/developer policy
  -> current user task
  -> C:\Users\compg\.codex\AGENTS.md
  -> workspace AGENTS.md
  -> target repository AGENTS.md
  -> nested directory AGENTS.md
  -> triggered task Skill
  -> only the maintained documents routed by the layers above
```

[knowledge/INDEX.md](../../INDEX.md) is the required cold-start router, not a
Codex-native override. Load its memory files according to task relevance and
its cold-start order. `CLAUDE.md`, `.claude/*`, and `.cursor/*` are adapters for
other clients. Codex may inspect them as evidence, but they do not outrank the
chain above. No active `AGENTS.override.md` was found in the qualified scope.

If instructions conflict, follow the higher layer and record the conflict. In
the current Codex safe mode, direct Git/`rg`/file reads precede Codebase Memory;
this overrides the older RAG repo text requiring CBM before grep.

## Source-Of-Truth Router

| Need | Open or inspect | Freshness test | Fallback / limit |
|---|---|---|---|
| Current implementation | Target source, tests, schemas, migrations, config | Read current working tree and relevant diff | Documentation cannot prove implementation |
| Repository state | `git status`, `git diff`, `git log`, `git rev-parse HEAD` in each independent repo | Run per repo immediately before action | Never infer nested repo state from workspace-root Git |
| Test result | Existing repository command surface and current exit/output | Same code/config/runtime fingerprint as the claim | Old PASS reports are historical |
| Runtime behavior | Local Docker/host process, health, logs, and owner runbook | Current container/image identity plus fresh request/proof | A running container is not correctness or parity proof |
| Operator decisions | [OPERATOR_DECISIONS](../../memory/OPERATOR_DECISIONS.md) | Read current file; check dirty state | Do not create a parallel decision log |
| Open work / next project action | [BACKLOG](../../memory/BACKLOG.md), then [ACTIVE_WORKSPACE](../../memory/ACTIVE_WORKSPACE.md) when continuity matters | Current content and Git state | `LAST_SESSION` is a short handoff, not stronger than current state |
| Last session | [LAST_SESSION](../../memory/LAST_SESSION.md) | Compare with Git and live state | Session transcript/history is supporting context only |
| Architecture and ownership | [source-of-truth](../../source-of-truth.md), [SYSTEM_ATLAS](../../SYSTEM_ATLAS.md), [ARCHITECTURE_DECISIONS](../../ARCHITECTURE_DECISIONS.md), [world-state](../../world-state.yaml) | Verify disputed claims in source/tests/runtime; note dirty docs | Generated graphs and reports are advisory views |
| Workflow baseline | [WORKFLOW_REGISTRY](../workflows/WORKFLOW_REGISTRY.yaml), [WORKFLOW_EVIDENCE](../workflows/WORKFLOW_EVIDENCE.jsonl), [PROGRESS](../workflows/PROGRESS.md) | Run the workflow validator when this surface changes | Registry v1 is frozen; do not mutate it for normal repairs |
| Repair program | [repairs README](../repairs/README.md), [REPAIR_REGISTRY](../repairs/REPAIR_REGISTRY.yaml), package execution record | Run the repair-overlay validator; compare package proof | Repair overlay does not rewrite Workflow Registry v1 |
| Machine task state | `C:\top-code-session-scratch\ai-os-execution\top-code-workspace\current-task.json` | `task-status` / `task-resume` plus Git-state validation | Execution state only; never project memory |
| Proof artifacts | Existing repo proof location or bounded `.artifacts` output | Match command, SHA, config, scope, and runtime identity | Keep only evidence needed for the claim; not cold-start input |
| Historical report/audit | Named report, archive, Git history | Check date, SHA, scope, and verdict strength | Never promote historical proof to current runtime truth |

## Tool Router

| Need | Preferred tool | Use condition and freshness | Fallback |
|---|---|---|---|
| Known file, config, doc, exact contract | Direct file read | Path is known | `rg --files`, then read source |
| Text, filename, config key, test location | `rg` / `rg --files` | Default discovery in AI-OS safe mode | PowerShell file search if `rg` cannot cross a nested Git boundary |
| Changes, ownership, provenance, SHA | Git in the exact repository | Always before edits/staging/closure | Direct files for content; no workspace-wide Git inference |
| Unknown code flow or shared-symbol impact | GitNexus CLI/MCP | Use only when the graph materially helps; prove tool availability, explicit repo target, live index freshness, and language coverage, then verify the result in source | Git + `rg` + direct source/tests; zero graph hits do not prove absence |
| Cross-repo search/graph support | Codebase Memory | Only after project-name, ownership, resource, and query-only proof; never assume dirty changes are indexed | Git/`rg`/source in each owner repo; no broad auto-reindex |
| Maintainability/change-set risk | CodeScene | Non-trivial risky/hot files; prove installation/tool call and analyze the bounded change set | Source review, tests, linters; CodeScene is not architecture or runtime proof |
| Local service behavior/parity | Docker/Compose and repository runtime helpers | Local only; inspect compose source, container/image identity, health and host/container code parity | Host-level focused proof with limitation; never production fallback |
| Browser/UI behavior | Existing Playwright config or `webapp-testing` | UI behavior is in scope and local runtime is ready | Focused DOM/API/source proof, explicitly `RUNTIME_NOT_PROVEN` |
| Deterministic verification | Repository command surface below | Command exists and matches changed layer | Run the smallest direct test command; do not invent a wrapper |
| Parallel read-only discovery/review | Existing Codex profile such as `code-mapper`, `search-specialist`, `qa-expert`, `docker-expert`, or `reviewer` | Only when isolation saves material context; give explicit no-write scope | Main agent performs bounded work; read-only is not mechanically enforced |

Do not repair, restart, reindex, or replace a tool merely because it is stale or
unavailable. Follow global tool-maintenance safety and use the source fallback.

## Repository Gate Entrypoints

Choose a focused gate matching the changed layer. Use package/runtime proof only
when the route and claim require it. Commands below are entrypoints, not a test
catalogue.

| Repository | Focused verification | Package verification | Runtime / closure status |
|---|---|---|---|
| `gmail-agent` | Targeted `python -m pytest <test-path> -q --tb=line`; syntax via `just compile` | `just package-verify` | `just doctor-skip-gmail` is environment-dependent; rebuild/parity/health are required only for baked runtime claims; no universal repo closure |
| `daszek` | From workspace root: `node --check daszek/public/app.js`, `php -l daszek/includes/api-v3-handlers.php`, targeted pytest/Node test | `powershell -File scripts\verify-local-gates.ps1` when cross-repo local gates are relevant | [daszek-smoke.ps1](../../../scripts/daszek-smoke.ps1) is a local cross-repo runtime smoke that writes a probe task; run it only when that mutation and runtime scope are explicitly relevant |
| `kalk-top` | The narrow `npm run verify:*` or `npm run test:*` script matching the layer | `npm run verify` | `npm run proof` adds critical Playwright/soft proof; runtime start/sync alone is not proof |
| `top-instal-generator` | `php -l top-instal-generator.php`, `php validate-json.php`, or `php core/application/harness/generate-offer-document.smoke.php` | No single current aggregate package gate | Converter test is environment/network-dependent; Wave 01 closure can close a declared cycle but not document correctness |
| `cieplo-orchestrator` | `python -m pytest <test-path> -q` with `PYTHONPATH=src` when needed | `python -m pytest tests -q` | `cieplo-worker preflight` and `/healthz` are environment/runtime gates; no repo closure command |
| `rag-chat-asystent` | `pytest -q <target>` | `pytest -q backend/tests`; local bash surface also exposes `./scripts/run.sh gate-priority` and `release-gate` | Use [LOCAL_RUNTIME](../../../rag-chat-asystent/docs/LOCAL_RUNTIME.md); deployment/SSH commands in script docs are out of default scope |
| `fast-kalk` | The matching PHP harness under `scripts/` | No single non-runtime package gate | After local `:8091` setup, `php scripts/e2e-scenarios-smoke.php` is the canonical local flow proof; never add `--live-mail` without explicit scope |
| `rag-widget` | `npm test -- --runTestsByPath <test>` when useful | `npm test` | Backend contract/runtime proof belongs to `rag-chat-asystent`; no repo closure command |
| `knowledge` | Link/format/schema check for the changed document or generator | Workflow only: `python system-atlas/workflows/validate_workflow_atlas.py --final`; repairs only: `python system-atlas/repairs/validate_repairs_overlay.py` | No universal knowledge gate; use Wave 01 closure for a checkpointed package |

Workspace helpers such as [preflight-workspace](../../../scripts/preflight-workspace.ps1),
[preflight-local-stack](../../../scripts/preflight-local-stack.ps1), and
[verify-local-gates](../../../scripts/verify-local-gates.ps1) compose broader
checks. Run them only when their surface overlaps the task.

## Wave 01 Execution State

Use [scripts/ai-os-task.ps1](../../../scripts/ai-os-task.ps1) or
[scripts/ai_os_task.py](../../../scripts/ai_os_task.py); inspect `--help` for
arguments. The canonical operations are:

```text
task-start -> task-branch -> task-checkpoint/task-resume -> task-gate -> task-commit-plan/task-commit -> post-commit task-gate -> task-close
```

- `READ`: never start a checkpoint solely to answer a question.
- `SMALL`: use no checkpoint for read-only work; start one before any write.
- `MEDIUM` and `CRITICAL`: start or resume before implementation; declare exact
  `repo:path` write scope; record repeatable gates in the ledger.
- For every write route, create a task branch before the first edit when the
  current branch is protected/default.
- Checkpoint before a long test/rebuild, repository boundary, context boundary,
  blocker, and after a commit.
- Use `task-commit-plan` and `task-commit`; do not use raw `git add` or raw
  `git commit` for agent work. The wrapper preserves foreign staged state and
  records the resulting `repo:SHA`.
- Rerun applicable final gates after each commit because the previous gate
  fingerprint contains the previous `HEAD`.
- Dedupe only a previous `PASS` with the identical Wave 01 fingerprint. Never
  dedupe a gate that requires fresh security, migration, recovery,
  concurrency/idempotency, or runtime-observed evidence.
- `task-close` validates the declared execution cycle. It does not prove
  business correctness, contract semantics, runtime parity, or deployment.

## State And Memory Boundaries

| State | Canonical owner | Lifetime / rule |
|---|---|---|
| Durable project decisions and open work | `knowledge/memory/*` | Update only with explicit operator instruction; one project memory system |
| Current machine task checkpoint | Wave 01 scratch JSON | Local, uncommitted execution state; no secrets, logs, business data, or project history |
| Package progress | Existing package ledger such as workflow `PROGRESS.md` or repair execution record | Package-specific; do not generalize into a second registry |
| Session transcript/compaction state | Codex host | Supporting context, not a project source of truth |
| Proof artifact | Existing repo or bounded `.artifacts` location | Evidence for a named claim and fingerprint; keep the minimum useful artifact |
| Durable implementation history | Git commits in each independent repo | Accepted write tasks authorize ownership-aware scoped local commits through `task-commit`; default publication is `LOCAL_ONLY` |

## Delegation Route

- Do not delegate `READ` or a trivial `SMALL` task by default.
- For a larger `MEDIUM`/`CRITICAL` task, delegate only a bounded read-only result:
  discovery (`code-mapper`/`search-specialist`), test classification
  (`qa-expert`), local runtime inspection (`docker-expert`), or staged review
  (`reviewer`).
- The main Codex agent owns decisions, writes, branch changes, commit planning,
  commits, checkpoint, and closeout. Raw staging is replaced by the shared
  ownership-aware commit wrapper.
- Profiles share no proven hard read-only sandbox or worktree isolation. State
  the no-write boundary explicitly and verify the working tree afterward.
- Return a short evidence summary, not full logs, to the main context.

## Completion By Risk

| Route | Completion means |
|---|---|
| `READ` | Current sources were inspected, evidence strength and unknowns are explicit, and no write workflow was implied |
| `SMALL` | Declared local scope is reviewed, focused and post-commit gates pass, no task-owned residue remains, and a scoped local commit exists when files changed |
| `MEDIUM` | Focused plus available package proof pass on final committed state, checkpoint matches Git, scoped local commits exist, and `task-close` passes |
| `CRITICAL` | Owner/consumer contracts, failure semantics and relevant invariant tests pass; local runtime/cross-repo proof is fresh where claimed; closure passes without upgrading missing production/operator evidence |

If required runtime is unavailable, finish as `PARTIAL` with the exact missing
proof. Do not weaken the route to obtain a green label.

## Failure And Freshness Routes

| Signal | Reaction |
|---|---|
| Dirty repository | Separate baseline, staged, unstaged, and untracked state per repo; declare only owned files |
| Stale/missing index | Use Git/`rg`/source/tests; report graph limitation; refresh only the one explicit repo when authorized and necessary |
| Missing/dead link | Use the nearest current source, mark the route incomplete, and correct this map in the same bounded scope when safe |
| Gate fails | Classify product, test/harness, environment, or stale-fingerprint failure; fix only a blocker in declared scope |
| Runtime differs from source | Verify compose/build context, image/container identity, mounts, and host/container code before claiming a product defect |
| MCP transport closes after maintenance | Stop the tool-maintenance stage with `RESTART_REQUIRED`; do not create an alternate client in-session |
| Proof is historical or generated | Reproduce the narrow claim or label it historical/advisory |

## Harness Improvement Loop

| Friction | Change location |
|---|---|
| One-time ambiguity | Resolve the current task; do not persist a mechanism |
| Wrong owner, link, entrypoint, or gate route | Correct this map with source evidence |
| Existing script/validator is incomplete | Repair that canonical mechanism in a separate bounded scope |
| Stable repeated gap with a clear trigger | Open a bounded harness improvement after proving repetition and ownership |
| Repeated procedure cannot be expressed by map + existing command | Consider one Skill change only after the simpler forms fail |

Do not encode repo commands into the global Skill. Do not create a new registry,
memory store, wrapper, validator, profile, or hook to solve a navigation defect.

## Qualified Gaps And Stale Routes

These are navigation warnings, not implementation plans:

- GitNexus availability, repo rooting, and index freshness must be proved live
  for the explicit target repo. Do not store version numbers, index counts, or
  current SHA snapshots here, and do not auto-reindex the workspace.
- Codebase Memory is query-only by active policy; completeness and dirty-tree
  coverage are not proven. The current host must expose and prove the canonical
  project before use, and a known symbol should resolve before any result is
  trusted.
- CodeScene is configured but has no live call proof from this wave.
- `rag-chat-asystent/AGENTS.md` references missing
  `knowledge/ARCHITECTURE_DISCOVERY_POLICY.md`, `knowledge/agent-os/*`, and
  `rag-chat-asystent/docs/EVAL_GATE.md`. Use the live repo router,
  `docs/START_HERE.md`, source and tests until a separate owner fixes routing.
- `gmail-agent/justfile` says `package-verify` matches a missing
  `docs/core/PACKAGE_VALIDATION.md`; the recipe itself exists and is the usable
  entrypoint.
- Generated repo GitNexus instruction blocks use mixed historical tool names.
  The current host tool list and this execution map win.
- Codex command rules and Claude lifecycle hooks mechanically block raw agent
  staging/commits and destructive Git. Subagent file ownership remains primarily
  instruction/checkpoint enforced unless a separate worktree is used.
- Several repositories have focused/package tests but no aggregate closure;
  Wave 01 closes only the declared task cycle.

Baseline detail and evidence statuses: [Codex Execution Stack Current State](CODEX_EXECUTION_STACK_CURRENT_STATE.md).

## Route Acceptance Scenarios

| Scenario | Route selected from the first screen | Sources/tools/gates | Finish |
|---|---|---|---|
| Correct one isolated `rag-widget` Jest regression | `SMALL` | root + repo AGENTS, task checkpoint before writes, task branch, target test/source, Git, `npm test -- --runTestsByPath ...` | Focused PASS, scoped local commit, post-commit PASS and closure `PASS` |
| Implement a bounded Node B behavior across related Python modules | `MEDIUM` | Gmail AGENTS/manual, owner source/tests, GitNexus only after freshness proof, targeted pytest then `just package-verify`, Wave 01 ledger | Final-state gates, scoped commit, closure `PASS`; runtime proof only if baked behavior is claimed |
| Change `OfferDTO` consumed by generator and fast-kalk | `CRITICAL` | kalk-top owner contracts first, all consumer AGENTS, per-repo Git, impact/source verification, owner and consumer contract gates, local `:8091` flow where relevant | Cross-repo commits and contract/runtime proof on final state, closure `PASS`, no production claim |

Each scenario is routable from the opening table plus one domain row; the rest
of this document is consulted only for the selected tool, gate, or failure path.
