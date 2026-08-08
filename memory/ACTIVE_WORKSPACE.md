# Active Workspace

Status: current direction only. Last updated: 2026-08-08 (KNOWLEDGE-SYNC-6CHAT-01).

## Current program (canonical)

**Plan kanoniczny:** `knowledge/docs/AI_OS_ROADMAP.md`.

**Strategic posture (after Fresh38 + residuals waves):** infrastruktura pomiaru i Case OS
rdzeń są w dużej mierze zamknięte. **Nie** otwieraj kolejnych slice’ów 5.3–8.x „bo są na
roadmapie”. Następny rozwój produktu: (1) correctness residuals poniżej, (2) opcjonalnie
staged RAG V2 po gate’ach technicznych, (3) potem jakość capability na podstawie Fresh38
(`NOT QUALIFIED — CAPABILITY`, CLEAN_PASS=10 / CAPABILITY=28) i realnych spraw firmy.

### Zamknięte programy (nie wracać)

| Program / ID | Status |
| ------------ | ------ |
| `AIOS-ROADMAP-32-ORCH-01` | `ROADMAP_32_RUN_CLOSED_LOCAL_VERIFIED` |
| `POST32-COMMIT-01` (4.3/5.1/5.2/6.1/6.2/6.3) | CLOSED in HEAD |
| `RESIDUALS-WAVE-01` / `RESIDUALS-WAVE-02` | CLOSED |
| `GOV-09` | CLOSED `COMPLETE_BOUNDED` |
| `FRESH38-RECAPTURE-01` | CLOSED — measurement healthy; product **NOT QUALIFIED — CAPABILITY** |
| `FACT-4.1-HIGH-01` (read-side) | CLOSED `COMPLETE / CONFIRMED_LOCAL` |
| `RAG-V2-LIVE-CUTOVER-READINESS-01` | CLOSED `PARTIAL` — host Gate B + dual-read PASS |

### RAG staged activation (binding)

```text
STAGED_ACTIVATION_AUTHORIZED — BLOCKED_BY_TECHNICAL_GATE
```

Operator already authorized staged (`technical_manual`, `price_list`). **Do not** re-ask.
Blocked on `RAG-TEMPORAL-COMPLETE-01` + `RAG-IMAGE-BAKE-01`. **No** global `RAG_CORE=v2`.

### 4.4 Install-prep (binding)

```text
REJECTED_BY_OPERATOR / NO PRODUCT ACTIVATION
```

Scaffold may exist in code from WAVE-01; **do not** develop or product-activate. No auto-revert
without blast-radius review (`OPERATOR_DECISIONS.md`).

### Otwarte residuale (jedyne realne)

```text
P1 Correctness: FACT-SUPERSESSION-WRITE-01
P1 RAG gate:    RAG-TEMPORAL-COMPLETE-01
P2 RAG bake:    RAG-IMAGE-BAKE-01
P3 Optional:    IQ-01-ADJUDICATED (human labels); GOV-06 .serena monitor (ignore by default)
```

**Nie startuj ponownie bez regresji:** FACT-01…05, FACT-4.1-HIGH-01 (read), Faza 3, POST32
spine, RESIDUALS-WAVE-01/02 closed IDs, FRESH38-RECAPTURE-01 (harness), 1.7/1.8 scaffolding,
RAG-13/14, GOV-02/07/08/09, PH3 harness, X1 live PW, FG-01/04, PF-01, IQ frozen machine baseline.
