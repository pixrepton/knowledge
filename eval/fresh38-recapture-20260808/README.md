# Fresh 38 recapture — empty-content DELIVERY fix

Status: **COMPLETE / CONFIRMED_LOCAL** (2026-08-08). Residual: `FRESH38-RECAPTURE-01`.

## Closeout checklist

| Criterion | Result |
|-----------|--------|
| 38/38 capture, unique IDs | **YES** |
| capture_gap_cases | **[]** |
| judge_error_cases | **[]** |
| Understanding judged | **30/30 SCORED** |
| `scoring_complete` | **true** |
| MI-02 captured | **YES** (`stage=full`) |
| empty-content semantics | **proven** (unit + live DeepSeek fallback) |
| frozen SUT | `gmail-agent` `fea458f` + rebuilt `gmail-agent-runtime:local` |

## Decision F

**VARIANT 2 — full Fresh 38** (SUT changed: `llm_provider_router.py` + `groq_client.py`). No merge of old 37 + new MI-02.

## Headline (measurement contract v2)

| Metric | Value |
|--------|-------|
| CLEAN_PASS | **10** |
| CAPABILITY | **28** |
| HARNESS / DELIVERY / CAPACITY | **0** |
| unsafe_non_escalation | **0** |
| verdict | `NOT QUALIFIED — CAPABILITY` (threshold 34 not claimed) |

Do **not** optimize product quality to raise CLEAN_PASS. Roadmap: do not chase 34/38.

## Root cause (MI-02 residual)

DeepSeek returned HTTP 200 with empty `message.content` (reasoning may be present). Extractor correctly raised, but:

1. `classify_provider_error` mapped it to `contract` / non-retryable → router aborted.
2. `deepseek_error_allows_fallback` looked for substring `empty content`, which does **not** match `empty \`message.content\``.

Net: no fallback → harness crash → missing MI-02 capture. Classified as **DELIVERY**, not product CAPABILITY.

## Fix

- Classify empty/`None`/whitespace `message.content` (and empty Responses assistant text) as retryable `empty_content`.
- Enrich extract diagnostics (`finish_reason`, `has_tool_calls`, `has_reasoning_content`); never promote `reasoning_content`.
- Fail empty Responses text **inside** the provider call so `LLMRouter` can fallback.
- Planner path unchanged: empty content + `tool_calls` remains legal.

## Artifacts

| File | Role |
|------|------|
| `fresh-full38-results.json` | 38-case production_faithful capture |
| `fresh-understanding-judge.json` | 30/30 Understanding SCORED |
| `rescore-v2.json` / `summary-v2.json` / `breakdown-v2.json` / `qualification-v2.json` | contract v2 |
| `frozen_sut_manifest.json` | HEAD / hashes / image |
| `mi02-before-after-proof.json` | MI-02 before/after |
| `artifact_hashes.json` | SHA256 inventory |

Scratch runtime logs: `C:\top-code-session-scratch\fresh38-recapture-20260808T045859\`.

## Product commit

`gmail-agent:fea458f` on `feature/aios-roadmap-1.4-2.4` — Gate A **2352 passed, 14 skipped**.
