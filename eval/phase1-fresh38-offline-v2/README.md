# Phase 1.1 Fresh 38 — status

Status: **PARTIAL** (2026-08-04). Task: `AIOS-PHASE1-FRESH38-01`.

## Done when (roadmap)

- `scoring_complete: true`
- v2 rubric primary
- run artifact

## What shipped this slice

| Deliverable                                             | Path                                        |
| ------------------------------------------------------- | ------------------------------------------- |
| Offline v2 rescore wrapper                              | `scripts/run_fresh38_offline_v2.ps1`        |
| Case-by-case SUT capture (anti-OOM)                     | `scripts/run_fresh38_case_batch.ps1`        |
| Offline artifact (frozen Exit2 capture + REJUDGE judge) | `knowledge/eval/phase1-fresh38-offline-v2/` |

## Offline v2 result (reproducible)

Source capture: `C:\top-code-session-scratch\exit2-fresh38-20260803T185704\fresh-full38-results.json`  
Judge: `fresh-understanding-judge.REJUDGE.json`

| Metric           | Value                                     |
| ---------------- | ----------------------------------------- |
| clean_pass       | **13**                                    |
| CAPABILITY       | 20                                        |
| HARNESS          | 5 (capture gaps only; **0** judge errors) |
| scoring_complete | **false**                                 |
| verdict          | `NOT QUALIFIED — CAPTURE GAP`             |

Capture-gap cases: `NEW-03`, `FU-05`, `SVC-01`, `SVC-02`, `CTX-01` (`understanding` missing; SVC also draft).

Roadmap rule: **do not chase 34/38**. Qualification threshold remains documented but Phase 1.1 accepts honest PARTIAL until gaps are re-captured.

## Live gap re-capture

Command:

```powershell
powershell -File scripts/run_fresh38_case_batch.ps1 `
  -OutDir C:\top-code-session-scratch\phase1-fresh38-gap-recapture-20260804 `
  -CaseIds NEW-03,FU-05,SVC-01,SVC-02,CTX-01
```

After success: merge into full38 JSON → re-judge → `run_fresh38_offline_v2.ps1` again.

## Commands

```powershell
# Offline only (no LLM)
powershell -File scripts/run_fresh38_offline_v2.ps1

# Gap re-capture (LLM + Docker nodeb-api)
powershell -File scripts/run_fresh38_case_batch.ps1
```

## Anti-claims

- Do not treat Exit2 `clean_pass=7` (pre-rejudge) as current.
- Do not treat 13/38 as Fresh 38 PASS.
- Do not claim `scoring_complete:true` while HARNESS capture gaps remain.
