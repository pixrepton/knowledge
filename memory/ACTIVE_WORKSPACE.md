# Active Workspace

Status: current direction only. Last updated: 2026-08-08 (RAG-V2-FINAL-TECHNICAL-GATE-01).

## Current program (canonical)

**Plan kanoniczny:** `knowledge/docs/AI_OS_ROADMAP.md`.

**Strategic posture:** infrastruktura pomiaru, Case OS rdzeń i RAG V2 staged path są
zamknięte lokalnie. **Nie** otwieraj kolejnych slice’ów 5.3–8.x „bo są na roadmapie”.
Następny rozwój produktu: jakość capability na podstawie Fresh38
(`NOT QUALIFIED — CAPABILITY`, CLEAN_PASS=10 / CAPABILITY=28) i realnych spraw firmy.

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

### Otwarte residuale (jedyne realne)

```text
P3 Optional:    IQ-01-ADJUDICATED (human labels); GOV-06 .serena monitor (ignore by default)
```

**Nie startuj ponownie bez regresji:** FACT-01…05, FACT-4.1-HIGH-01 (read), FACT-SUPERSESSION-WRITE-01,
RAG-WIDGET-ADMIN-SECURITY-CLOSEOUT-01, RAG-V2-FINAL-TECHNICAL-GATE-01 / TEMPORAL / IMAGE-BAKE,
Faza 3, POST32 spine, RESIDUALS-WAVE-01/02 closed IDs, FRESH38-RECAPTURE-01 (harness),
1.7/1.8 scaffolding, RAG-13/14, GOV-02/07/08/09, PH3 harness, X1 live PW, FG-01/04, PF-01,
IQ frozen machine baseline.
