# Active Workspace

Status: current direction only. Last updated: 2026-08-16 (Fresh38 measurement requalified; capability baseline 27/38).

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
NEXT = CAPABILITY analysis of the 11 residual cases (not a new residual wave)
```

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

**Next program:** capability analysis of the 11 CAPABILITY residual cases (INT-01, INT-04,
INT-05, NEW-03, NEW-05, FU-01, SVC-05, DOC-02, CTX-03, MI-01, MI-02) with focused proofs
before any product change. Do not open another residual wave. **Nie** otwieraj kolejnych
slice’ów 5.3–8.x „bo są na roadmapie”.

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
NEXT: 11-CAPABILITY focused analysis
P3 Optional: IQ-01-ADJUDICATED (human labels); GOV-06 .serena monitor (ignore by default)
L0 repair: COMMITTED (4210ed5, LOCAL_ONLY) — do not re-open without new regression
```

**Nie startuj ponownie bez regresji:** FACT-01…05, FACT-4.1-HIGH-01 (read), FACT-SUPERSESSION-WRITE-01,
RAG-WIDGET-ADMIN-SECURITY-CLOSEOUT-01, RAG-V2-FINAL-TECHNICAL-GATE-01 / TEMPORAL / IMAGE-BAKE,
Faza 3, POST32 spine, RESIDUALS-WAVE-01/02 closed IDs, FRESH38-RECAPTURE-01 (harness),
1.7/1.8 scaffolding, RAG-13/14, GOV-02/07/08/09, PH3 harness, X1 live PW, FG-01/04, PF-01,
IQ frozen machine baseline.
