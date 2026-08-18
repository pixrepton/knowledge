# Last Session

Updated: 2026-08-18 — **P2 causal observability closeout PASS**.

## Headline

```text
P2_CAPABILITY_CAUSAL_OBSERVABILITY = PASS / CLOSED
P2_PRODUCT_SHA = ae59750565d2a0e334f646a4d5f7bc94bd92f602
P2_RUNNER_SHA = 800318a7a2a34cfd0865889a0daacdcf530d9cda
CAPABILITY-OBSERVABILITY-01 = CLOSED
INT-01 = HISTORICAL_ONLY / REGRESSION_WATCH (current reproduction NO)
SVC-05 = CURRENT_PRODUCT_DIAGNOSIS_PENDING (observability blocker REMOVED)
NEXT = P3A frozen K3 adjudication (INT-04, NEW-05, FU-01, MI-01)
NO_RECAPTURE_FOR_P3A = YES
OPERATOR_DECISIONS_UPDATED = NO
```

## What this closeout proved

- Additive Brain1 draft-path evidence (`draft_path_observability.v1`) without product
  draft/gate/case-state semantics change.
- Current INT-01 draft-absent symptom is **not** reproduced (`DRAFT_ACCEPTED`).
- Current SVC-05 draft-absent **is** reproduced and classifiable (`SKIPPED_PRE_DRAFTER` /
  `BR_ACTION_AND_REPLY_FLAG_NOT_ELIGIBLE`).
- GitNexus gmail-agent reindexed at `ae59750`; module is on the live call path.
  Missing reverse CALLS and BR-as-data are index limitations, not code defects.
- Canonical residual owner: `eval/mail-agent-intelligence-current/`.

## Stop / next

P2 CLOSED. P3A must adjudicate frozen Fresh38 27/38 captures only.
Do not run INT-04/NEW-05/FU-01/MI-01 again as the reason those cases failed in 27/38.
Do not treat INT-01 as fixed forever.

## Previous headline (2026-08-16, preserved)

```text
FRESH38_MEASUREMENT_QUALIFICATION = REQUALIFIED
FULL FRESH38 AGAINST CURRENT CODE = RUN (38/38 capture QUALIFIED, FIRST_ATTEMPT#1)
CURRENT CAPABILITY BASELINE (contract v5) = 27 CLEAN_PASS / 11 CAPABILITY → NOT QUALIFIED — CAPABILITY
```

The 2026-08-16 measurement requalification and consolidation notes below remain
historical/current measurement truth. They are not rewritten.


## What happened this session

- **RCA closed** — pełny kontrakt L0 + tożsamość harnessa (`PROVEN_FULL_RUN_HARNESS=3b3041e5`,
  `COMMITTED_HARNESS=035534a7…`, `IMPLEMENTATION_HARDENING_AFTER_FULL_PROOF=YES`) w
  `docs/MEASUREMENT_INTEGRITY_V3.md` (canonical owner); tutaj tylko synteza: attach EOF /
  docker client EOF ≠ completion authority; authenticated callback EOF = process-exit edge.
- **FU-07 17/38 abort:** `HOST_SLEEP_ABORT_CAUSE = PROVEN_ENVIRONMENTAL` (host sleep, battery
  critical → kernel-power 42/107; runner finished 90 s after wake; harness fail-closed correct)
  — **not** an L0 channel root cause. `DOCKER_INTERNAL_PREMATURE_ATTACH_EOF_TRIGGER =
  NOT_PROVEN_AND_NOT_REQUIRED`.
- **Deterministic gates:** 6/6 PASS (lifecycle channel, exec instrumentation, capture contract,
  reuse gate, SUT fingerprint, runner contract) — fresh logs
  `C:\top-code-session-scratch\fresh38-deterministic-gates-20260816`.
- **Four-case requalification:** `fresh38_fourcase_repair2_20260816T123000` — CTX-04 / MI-03 /
  MI-04 / DEC-02 all QUALIFIED (FIRST_ATTEMPT#1, parity PASS).
- **Full 38/38:** `fresh38_full_current_20260816T124100` — `COMPLETED ok=38 failed=0`,
  `measurement_failures=0`, 38/38 manifests QUALIFIED, 0 engine-api exceptions, 0 confirm
  re-inspects needed. SUT `gmail-agent@37d4b37` (clean worktree), corpus-v2 `6550a075`,
  container `sha256:142cba…`, mode `production_faithful`.
- **L3 (fresh, frozen contract):** judge `score-run` 30/30 SCORED (groq `llama-3.3-70b-versatile`,
  `understanding-semantic-judge.v1`), then offline rescore contract **v5**
  (corpus `04c561a4`, ground truth `ba144753`, scorer `6ac1761b`, threshold 34,
  capture `4541e76f`, judge `2387daf9`): CLEAN_PASS=27, CAPABILITY=11,
  `scoring_complete=true`, `judge_error_cases=[]`, `capture_gap_cases=[]`,
  `unsafe_non_escalation=0` → product **NOT QUALIFIED — CAPABILITY** (separate from measurement).

## Current state / next

- Measurement: requalified and green. Product: below capability threshold (27/38).
- Next real program: focused capability analysis of the 11 CAPABILITY cases (INT-01, INT-04,
  INT-05, NEW-03, NEW-05, FU-01, SVC-05, DOC-02, CTX-03, MI-01, MI-02) before any product change.
- L0 repair **committed** `4210ed5` (workspace, LOCAL_ONLY) as part of administrative closure.

## Still open

1. 11-CAPABILITY product analysis (next program).
2. Optional: IQ-01 human adjudication; GOV-06 `.serena` monitor.

## Stop

Do not re-run Fresh38 or re-investigate the L0 lifecycle anomaly without new regression
evidence. Previous session handoff (2026-08-09 infra cleanup) is preserved in
`docs/AI_OS_ROADMAP.md` changelog and closed-program tables in `ACTIVE_WORKSPACE.md`.

## Follow-up — AI-OS Workspace Consolidation & Canonical Sync (2026-08-16, PASS)

- **Committed (task engine):** root control-plane (`089945ba`+`ff098137`), knowledge writeback +
  terminology + skill registry/map + eval artifacts (`e2436492`+`80a59278`), per-repo `.gitattributes`
  LF policy, rag-widget chat-widget, kalk-top AGENTS.md adapter, GitNexus block refresh.
- **Published:** 8 repos pushed, `LOCAL == REMOTE` verified per repo. Root stays
  `INTENTIONAL_LOCAL_ONLY` (no remote). kalk-top push deferred to `AIOS-KALK-CANONICALIZE-20260811`.
- **Code intelligence:** GitNexus root/gmail-agent/fast-kalk reindexed (INDEXED==HEAD);
  CBM gmail-agent refreshed; others `FRESH_PER_ROUTING`. CodeScene `UNAVAILABLE_AUTH`.
- **Baseline unchanged:** 27 CLEAN_PASS / 11 CAPABILITY (v5). Next program: 11-CAPABILITY analysis.

## Closeout 2026-08-16 (final)

- **AI_OS_WORKSPACE_CONSOLIDATION = CLOSED_PASS** (bounded closeout): all 10 active repos CLEAN
  (3 phantom residues resolved via `git add --renormalize`, blobs unchanged, `CONTENT_CHANGE=0`);
  `workspace-repos.lock.json` → v2 (sound semantics: observed_before_snapshot_commit, no
  self-referential HEAD claim); external exact terminal proof in
  `pre-consolidation-20260816T204528\final-acceptance-snapshot.json`.
- **Tasks:** `AIOS-WORKSPACE-CONSOLIDATION-20260813` CLOSED, `PROOF-ECONOMY-CONSOLIDATION-20260813`
  CLOSED (harness audit credible); only `AIOS-KALK-CANONICALIZE-20260811` active (intentional).
- **Procedural debt recorded:** `TASK-ENGINE-SCOPE-UPDATE` (scope/adoption needed direct JSON
  mutation; future canonical op `task-scope-add`/`task-adopt-path`) — backlog, not a blocker.
