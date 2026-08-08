# Active Workspace

Status: current direction only. Last updated: 2026-08-08 (FACT-4.1-HIGH-01).

## Current program (canonical)

**Plan kanoniczny:** `knowledge/docs/AI_OS_ROADMAP.md`.

**Run `AIOS-ROADMAP-32-ORCH-01`:** `ROADMAP_32_RUN_CLOSED_LOCAL_VERIFIED` (2026-08-06).

**Post-closure `POST32-COMMIT-01`:** CLOSED — 4.3/5.1/5.2/6.1/6.2/6.3 in HEAD (`LOCAL_ONLY`).

**`RESIDUALS-WAVE-01`:** CLOSED locally — 4.2 UI+Drive, 4.4, FG-01B, FG-04, PF-01, IQ-01 frozen, RAG-02/04 ephemeral.

**`RESIDUALS-WAVE-02`:** CLOSED locally — RAG-05 worker live, RAG-12 compose profile + smoke, RAG-01 Docling live host, RAG-09 opt-in live_data_plane, X1 live PW, SPINE tick, HITL harness, GROQ dead-key disable.

**`FRESH38-RECAPTURE-01`:** CLOSED `COMPLETE / CONFIRMED_LOCAL` — empty-content DELIVERY fix + honest Fresh 38/38 (`knowledge/eval/fresh38-recapture-20260808/`).

**`FACT-4.1-HIGH-01`:** CLOSED `COMPLETE / CONFIRMED_LOCAL` — residual CURRENT_STATE consumers + canonical active-facts contract; Gate A **2357**/15; bounded Postgres proof.

Repair = `PROGRAM_COMPLETE_LOCAL`. Fazy 3 **nie** otwierać bez regresji.

### Otwarte residuale (operator wybiera)

```text
P2 Write:    FACT-SUPERSESSION-WRITE-01 (replace_message_facts / merge write path)
P3 Monitor:  GOV-06 .serena; IQ-01-ADJUDICATED (human labels)
```

**GOV-09:** CLOSED `COMPLETE_BOUNDED` — remotes in sync; knowledge via sanitized branch (not poison history).

**Nie startuj ponownie bez regresji:** FACT-01…05, FACT-4.1-HIGH-01, Faza 3, POST32 spine, RESIDUALS-WAVE-01/02 closed IDs, FRESH38-RECAPTURE-01, 1.7/1.8 scaffolding, RAG-13/14, GOV-02/07/08, PH3 harness.
