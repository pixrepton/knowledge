# Active Workspace

Status: current direction only. Last updated: 2026-08-21 (Intelligence Spine closeout writeback).

## Current program (canonical)

**Plan kanoniczny:** `knowledge/docs/AI_OS_ROADMAP.md`.

**Strategic posture:** infrastructure cleanup remains `COMPLETE_LOCAL`. The one current full
Fresh38 has been **executed and requalified** (measurement). Product capability remains
**below threshold** (27/38 CLEAN_PASS vs 34 required) and is the current product-quality program.

```text
AI_OS_INFRASTRUCTURE_CLEANUP = COMPLETE_LOCAL
CAPABILITY_PROGRAM_READINESS = GO
REQUIRED_OPEN = 0
UNKNOWN_NEEDS_PROOF = 0
FRESH38_MEASUREMENT_QUALIFICATION = REQUALIFIED
FULL FRESH38 AGAINST CURRENT CODE = RUN (attempt fresh38_full_current_20260816T124100)
CURRENT CAPABILITY BASELINE = 27 CLEAN_PASS / 11 CAPABILITY (contract v5, threshold 34) → NOT QUALIFIED — CAPABILITY
P2_CAPABILITY_CAUSAL_OBSERVABILITY = PASS / CLOSED
P2_PRODUCT_SHA = ae59750565d2a0e334f646a4d5f7bc94bd92f602
P2_RUNNER_SHA = 800318a7a2a34cfd0865889a0daacdcf530d9cda
CAPABILITY-OBSERVABILITY-01 = CLOSED
INT-01 = HISTORICAL_ONLY / REGRESSION_WATCH (current reproduction NO)
SVC-05 = CLOSED (PRODUCT_FIX PASS; DOWNSTREAM_FIX PASS; FINAL_PROVIDER_LIVE_PROOF PASS; gmail-agent 0a407cb3/78603fb/70c3d94)
P3A_FROZEN_K3_ADJUDICATION = COMPLETE (INT-04/NEW-05/FU-01/MI-01 = EVALUATOR_WRONG)
P4_VS_P3B_FORK = CLOSED (all P4 steps complete; P3B deferred; no full Fresh38)
11-CAPABILITY = CLOSED (all 11 fixed or explicitly classified)
NEXT = STOP
```

### Intelligence Spine closeout (2026-08-21)

```text
INTELLIGENCE_SPINE_1_2_3_END_TO_END_PROVEN = PASS
SCOPE = bounded invariants only
PRODUCT_AUTONOMY_READINESS = NOT_CLAIMED
FULL_FRESH38 = NOT_RUN
```

Proof owner: `gmail-agent` commits `3469dbd`, `7fc257b`, `c80be17`; contract
owner: `knowledge/docs/AI_OS_INTELLIGENCE_SPINE_CONTRACT.md` commits `7d2fa39`,
`cbf0cda`.

Proven bounded invariants:

- `allowed_action_tools` is an action-tool whitelist and execution rejects
  mismatches even when a tool is not globally forbidden.
- customer/mail/ask-for-missing-data cannot silently become
  `request_operator_clarification`.
- `trust_state`, `decision_usable` and `decision_block_reason` survive the
  normalization boundaries needed by the real dependent consumer.
- a consumer depending on conflicted `heated_area_m2` cannot execute the
  dependent kalk/offer action, while independent customer acknowledgement
  remains legal.

Current operator-authorized execution order:

1. Write back and publish current Intelligence Spine state.
2. Close procedural/tooling residuals to professional `PASS` where bounded:
   `TASK-ENGINE-SCOPE-UPDATE`, `GOV-06`, and a concrete disposition for
   `IQ-01-ADJUDICATED`.
3. Implement `UNTRUSTED-INPUT-EXECUTION-BOUNDARY-01`.
4. Run `REAL-MAIL INTELLIGENCE DISCOVERY` on 10-15 historical cases without
   side effects.
5. Use the resulting gap map to prioritize RAG/facts/attachments/reasoning/tools
   work before larger historical qualification and shadow-live.

### AI-OS truth sync — current workspace posture (2026-08-20)

```text
AI_OS_FULL_WORKSPACE_TRUTH_SYNC = CLOSED_PASS
11-CAPABILITY_PRODUCT_RESIDUALS_OPEN = 0
SVC-05 = CLOSED / PRODUCT_FIX PASS / DOWNSTREAM_FIX PASS / FINAL_PROVIDER_LIVE_PROOF PASS
FULL_FRESH38_RERUN_FOR_CLOSEOUT = NO
```

Current runtime/tooling facts from the 2026-08-20 sync:

- `gmail-agent` HEAD is `70c3d94efa41f6b46a87fbd4b1c07d96ca3e6d66`; worktree clean.
- Local Node B API is running and healthy on `127.0.0.1:8766`; mailbox memory container is healthy.
- RAG backend is not currently healthy on `127.0.0.1:8000`; canonical `rag-chat-asystent`
  Docker compose start attempted but hung in build/compose without creating RAG containers.
  Treat full core preflight as **not current PASS** until RAG is started and health is proven.
- Codebase Memory MCP query-plane is callable in Codex; CBM project heads match current active
  repo HEADs.
- GitNexus is configured as local CLI/index in this Codex session, not callable as MCP; active
  repo indexes were refreshed to current HEAD during this sync.
- CodeScene MCP is configured but current call returns missing access token; do not claim
  CodeScene API proof until authentication is restored.
- GitHub publication/parity completed for this closeout on active branches; previous root
  `LOCAL_ONLY/no remote` statement is superseded by `OPERATOR_DECISIONS.md` 2026-08-20.

Historical baselines (prior SUT / older contract, not comparable to the 2026-08-16 baseline):
13 Aug capture = 23 CLEAN_PASS / 15 CAPABILITY; 08 Aug capture = 10 CLEAN_PASS / 28 CAPABILITY.
Fresh38 measurement requalification proof: `.artifacts/fresh38-full-current-20260816T124100`
(38/38 QUALIFIED, four-case `fresh38_fourcase_repair2_20260816T123000` 4/4 QUALIFIED) — see
`LAST_SESSION.md` and `docs/MEASUREMENT_INTEGRITY_V3.md` for the L0 execution-channel contract.

Every other
historical program/residual checked (Fresh38 harness recapture, FACT read+write, RAG-widget P0-4/P0-5,
RAG-V2-FINAL-TECHNICAL-GATE-01, Calendar dispatch topology, desk membership, projection
seam, 4.4, credential history) came back clean/closed/intentional — **do not reopen those
without new regression evidence.** Full findings: `docs/AI_OS_ROADMAP.md` changelog
2026-08-08 and this session’s report.

**Current residual owner:** `knowledge/eval/mail-agent-intelligence-current/`.

**Next program:** frozen eight-step sequence in `eval/mail-agent-intelligence-current/P4_VS_P3B_FORK.md`.
**Now for 11-CAPABILITY:** STOP. P4-A MI-02, P4-B SVC-05 final provider-live closeout, bounded re-proof and P4-C CTX-03 are
complete. P3B remains deferred to step 5 only. INT-01 remains
`HISTORICAL_ONLY / REGRESSION_WATCH`. K3 canonical failures are `EVALUATOR_WRONG`, not a
product-fix queue. Do not recapture Frozen Fresh38 27/38. Do not open another residual wave. **Nie** otwieraj
kolejnych slice’ów 5.3–8.x „bo są na roadmapie”.

### Zamknięte programy (nie wracać)

| Program / ID                                 | Status                                                               |
| -------------------------------------------- | -------------------------------------------------------------------- |
| `AIOS-ROADMAP-32-ORCH-01`                    | `ROADMAP_32_RUN_CLOSED_LOCAL_VERIFIED`                               |
| `POST32-COMMIT-01` (4.3/5.1/5.2/6.1/6.2/6.3) | CLOSED in HEAD                                                       |
| `RESIDUALS-WAVE-01` / `RESIDUALS-WAVE-02`    | CLOSED                                                               |
| `GOV-09`                                     | CLOSED `COMPLETE_BOUNDED`                                            |
| `FRESH38-RECAPTURE-01`                       | CLOSED — measurement healthy; product **NOT QUALIFIED — CAPABILITY** |
| `FACT-4.1-HIGH-01` (read-side)               | CLOSED `COMPLETE / CONFIRMED_LOCAL`                                  |
| `FACT-SUPERSESSION-WRITE-01`                 | CLOSED `COMPLETE / CONFIRMED_LOCAL`                                  |
| `RAG-WIDGET-ADMIN-SECURITY-CLOSEOUT-01`      | CLOSED `COMPLETE / CONFIRMED_LOCAL` (P0-4/P0-5)                      |
| `RAG-V2-LIVE-CUTOVER-READINESS-01`           | CLOSED `PARTIAL` — superseded by final technical gate                |
| `RAG-V2-FINAL-TECHNICAL-GATE-01`             | CLOSED `COMPLETE / proven_local` — `STAGED_ACTIVATION_EXECUTED`      |
| `OPERATOR-COMMAND-RECONCILE-BYPASS-01`       | CLOSED — canonical Agent Chat reconcile path; REQUIRED_OPEN = 0      |

### RAG staged activation (binding)

```text
STAGED_ACTIVATION_EXECUTED
```

Allowlist: `technical_manual`, `price_list` via opt-in staged compose. **No** global
`RAG_CORE=v2`. Expanding allowlist / global flip = new operator decision.

### 4.4 Install-prep (binding)

```text
REJECTED_BY_OPERATOR / NO PRODUCT ACTIVATION
```

Scaffold may exist in code from WAVE-01; **do not** develop or product-activate. No auto-revert
without blast-radius review (`OPERATOR_DECISIONS.md`).

### Otwarte residuale

```text
AI_OS_INFRASTRUCTURE_CLEANUP: COMPLETE_LOCAL
CAPABILITY_PROGRAM_READINESS: GO
REQUIRED_OPEN: 0
UNKNOWN_NEEDS_PROOF: 0
FRESH38_MEASUREMENT_QUALIFICATION: REQUALIFIED
FULL FRESH38 AGAINST CURRENT CODE: RUN (2026-08-16)
CURRENT CAPABILITY BASELINE: 27/38 CLEAN_PASS (v5, threshold 34) — NOT QUALIFIED — CAPABILITY
P2_CAPABILITY_CAUSAL_OBSERVABILITY: PASS / CLOSED
P3A: COMPLETE (K3 EVALUATOR_WRONG)
P4_VS_P3B_FORK: CLOSED
SVC-05: CLOSED (PRODUCT_FIX PASS; DOWNSTREAM_FIX PASS; FINAL_PROVIDER_LIVE_PROOF PASS; no executed request_operator_clarification in final SVC-05 proof)
NEXT: STOP
P3 Optional: IQ-01-ADJUDICATED (human labels); GOV-06 .serena monitor (ignore by default)
L0 repair: COMMITTED (4210ed5, LOCAL_ONLY) — do not re-open without new regression
```

### Konsolidacja 2026-08-16 — final state (Pass 2)

```text
AI_OS_WORKSPACE_CONSOLIDATION = CLOSED_PASS
REOPEN_CONDITION = NEW_EVIDENCE_OF_DRIFT_OR_CONTRACT_BREAK
AIOS-WORKSPACE-CONSOLIDATION-20260813 = CLOSED
PROOF-ECONOMY-CONSOLIDATION-20260813 = CLOSED
AIOS-KALK-CANONICALIZE-20260811 = SUPERSEDED_AS_PUSH_BLOCKER_BY_2026-08-20_TRUTH_SYNC
ALL_ACTIVE_REPOS_CLEAN = YES before truth-sync documentation edits
FINAL_SNAPSHOT_SEMANTICS = SOUND (lock v2 + external final-acceptance-snapshot.json)
PUBLISHED_REPOS_LOCAL_==_REMOTE = YES (workspace, knowledge, gmail-agent, kalk-top, daszek,
  rag-chat-asystent, rag-widget, cieplo-orchestrator, top-instal-generator, fast-kalk)
ROOT_PUBLICATION = PUBLISH_AUTHORIZED_FOR_2026-08-20_TRUTH_SYNC (no force push, no PR auto-merge)
KALK_TOP_PUSH = AUTHORIZED_FOR_CURRENT_BRANCH_PARITY_IN_2026-08-20_TRUTH_SYNC
GITNEXUS = FRESH_ALL_ACTIVE_REPOS_TO_CURRENT_HEAD (CLI/index; MCP namespace not exposed in Codex)
CBM = FRESH_ALL_ACTIVE_REPOS_TO_CURRENT_HEAD (query-plane callable; no broad auto-watch)
CODESCENE = CONFIGURED_BUT_NO_ACCESS_TOKEN_PROVEN
LOCAL_RUNTIME = NODE_B_HEALTHY; RAG_BACKEND_NOT_HEALTHY; CORE_PREFLIGHT_NOT_CURRENT_PASS
POST_RUN_WRITEBACK_SKILL = REGISTERED (registry + AGENT_MAP_SCENARIOS; NOT core_skills)
```

Consolidation task: `AIOS-WORKSPACE-CONSOLIDATION-20260813` — committed + closed via task engine
(commits: workspace `089945ba`+`ff098137`, knowledge `e2436492`+`80a59278`, gmail-agent `a0a7ffa2`+`db809664`,
fast-kalk `79ba2454`+`82128e64`, daszek `2607af87`, cieplo `92c0e6b7`, rag-widget `46731422`,
top-instal-generator `380bf989`, rag-chat-asystent `0715ccc8`, kalk-top `ef5db272`).

Closeout commit: workspace lock v2 + knowledge post-closure writeback (closeout task) — see
`LAST_SESSION.md` for exact SHAs. Final acceptance snapshot:
`C:\top-code-session-scratch\pre-consolidation-20260816T204528\final-acceptance-snapshot.json`.

**Nie startuj ponownie bez regresji:** FACT-01…05, FACT-4.1-HIGH-01 (read), FACT-SUPERSESSION-WRITE-01,
RAG-WIDGET-ADMIN-SECURITY-CLOSEOUT-01, RAG-V2-FINAL-TECHNICAL-GATE-01 / TEMPORAL / IMAGE-BAKE,
Faza 3, POST32 spine, RESIDUALS-WAVE-01/02 closed IDs, FRESH38-RECAPTURE-01 (harness),
1.7/1.8 scaffolding, RAG-13/14, GOV-02/07/08/09, PH3 harness, X1 live PW, FG-01/04, PF-01,
IQ frozen machine baseline.
