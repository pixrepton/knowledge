# Phase 1.1 Fresh 38 — merged result

Status: **MEASUREMENT COMPLETE** (2026-08-04). Task: `AIOS-PHASE1-FRESH38-01`.

## Done-when checklist

| Criterion | Result |
|-----------|--------|
| `scoring_complete: true` | **YES** |
| v2 rubric primary | **YES** (`measurement_contract_version=v2`) |
| Run artifact | **YES** (this directory) |

## Headline numbers (v2)

| Metric | Value |
|--------|-------|
| CLEAN_PASS | **13** |
| CAPABILITY | **25** |
| HARNESS / capture gaps | **0** |
| judge errors | **0** |
| scoring_complete | **true** |
| verdict | `NOT QUALIFIED — CAPABILITY` (threshold 34 not claimed) |

Roadmap: **do not chase 34/38**. Phase 1.1 is green on measurement integrity; product quality waves are 1.2–1.5.

## What changed vs Exit2 REJUDGE

| Item | Exit2 REJUDGE | Phase 1.1 merged |
|------|---------------|------------------|
| capture gaps | 5 (NEW-03, FU-05, SVC-01, SVC-02, CTX-01) | **0** (live re-capture) |
| scoring_complete | false | **true** |
| CLEAN_PASS | 13 | 13 |
| DeepSeek empty crash | container lacked host fix | synced `central_llm_stage.py` into API |

## Artifacts

| File | Role |
|------|------|
| `fresh-full38-results.MERGED.json` | Exit2 capture + 5 gap re-captures |
| `fresh-understanding-judge.json` | full 30/30 Understanding SCORED |
| `rescore-v2.json` / `summary-v2.json` / `breakdown-v2.json` / `qualification-v2.json` | offline v2 rescore |

Gap re-capture scratch: `C:\top-code-session-scratch\phase1-fresh38-gap-recapture-20260804c\`

## Runners added

- `scripts/run_fresh38_offline_v2.ps1`
- `scripts/run_fresh38_case_batch.ps1` (case-by-case + hotfile sync)

## Next (Phase 1.2+)

Tool-budget integrity → planner/draft/RAG quality — **not** another Fresh 38 until those levers land.
