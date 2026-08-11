# NVIDIA NIM bridge — qualification record

```text
TEMP_BRIDGE_QUALIFICATION = PASS       (deepseek-ai/deepseek-v4-flash-0731)
TEMPORARY_ACTIVATION      = NOT_ACTIVE (operator stood the bridge down before activation)
```

Two attempts. The first was refused by the host; the second passed on the operator-authorized
snapshot.

## Attempt 1 — `deepseek-ai/deepseek-v4-flash` — refused upstream

Config was correct in form and the bridge engaged as designed. Then:

```text
POST /v1/chat/completions -> HTTP 410 Gone   (922 ms)
content-type: application/problem+json

{"detail":"The model 'deepseek-ai/deepseek-v4-flash' has reached its end of life
           on 2026-08-07T09:00:00Z and is no longer available."}
```

`GET /v1/models` (free) — 101 models; the entire DeepSeek family offered:

```text
deepseek-ai/deepseek-coder-6.7b-instruct
deepseek-ai/deepseek-v4-flash-0731
```

Stopped there rather than substituting a model, and escalated the choice. `NVIDIA_QUALIFICATION.json`
holds that run verbatim.

## Attempt 2 — `deepseek-ai/deepseek-v4-flash-0731` — PASS

Operator authorized the snapshot. Catalog preflight confirmed the id is present **before** any
inference, so nothing was risked on a second retired id.

| stage | outcome | http | finish | schema | content len | completion tokens | latency |
|---|---|---|---|---|---|---|---|
| *smoke* | OK | 200 | — | — | — | — | 13 875 ms |
| signal_extraction | NVIDIA_PRIMARY_SUCCESS | 200 | stop | valid | 298 | 98 | 11 984 ms |
| intake_reasoning | NVIDIA_PRIMARY_SUCCESS | 200 | stop | valid | 2 567 | 855 | 21 202 ms |
| business_reasoning | NVIDIA_PRIMARY_SUCCESS | 200 | stop | valid | 2 640 | 862 | 18 500 ms |
| business_reasoning_large_context | NVIDIA_PRIMARY_SUCCESS | 200 | stop | valid | 3 390 | 1 106 | 31 875 ms |
| reply_drafter | NVIDIA_PRIMARY_SUCCESS | 200 | stop | valid | 1 715 | 592 | 57 625 ms |
| schema_stress | **SKIPPED** | — | — | — | — | — | `max_calls reached (6)` |

```text
primary_success  5/5 executed
schema_valid     5/5 executed
empty_content    0
fallback         0   - and structurally impossible here: the qualifier posts directly to the
                      host, so Groq is not in its path and cannot rescue a result
```

`NVIDIA_PRIMARY_FAILED_FALLBACK_SUCCESS`: **zero**. `TERMINAL_FAILURE`: **zero**.

### The coverage gap, stated plainly

Six stages were specified; five ran. The connectivity smoke consumes one slot of `MAX_CALLS=6`,
so `schema_stress` was cut by the cost guard — **skipped, not passed**. Raising the call cap was
explicitly out of contract, so it was not raised, and the run was not repeated to buy one more
call. `schema_stress` exercises the `IntakeReasoningResult` contract that `intake_reasoning`
already validated, so the residual risk is small; it is nonetheless unproven.

### Observations worth carrying forward

- **No reasoning tokens at all** (`reasoning_tokens: 0` on every call). This snapshot returned
  plain content, unlike the canonical host's thinking-enabled behaviour. Any comparison of cost
  or latency between hosts must account for that difference.
- **Latency is materially higher**: 12–58 s per structured call, worst at `reply_drafter`.
- **No empty content** in 5/5 — notable given `DEEPSEEK-EMPTY-CONTENT-01` measured an 18.58 %
  empty-content rate on the canonical host. Five calls prove nothing statistically; recording it
  only as a signal to check if the bridge is ever activated for real work.

## Why this is not "the same model, different host"

The bridge's original claim has been withdrawn. NVIDIA retired the unversioned id; the canonical
side is itself an unversioned alias (`DEEPSEEK_MODEL=deepseek-v4-flash`) whose current resolution
cannot be observed from here. So `0731` may or may not be what canonical serves today.

Governance now states exactly that, and no more:

```text
logical_model_family                 DeepSeek V4 Flash      preserved across hosts
exact_model_equivalence_to_canonical UNPROVEN               on the bridge
role                                 TEMPORARY_OPERATIONAL_BRIDGE
```

Both values travel with every DeepSeek-tier call (`llm_logical_model_family`,
`llm_exact_model_equivalence`), so a bridge-era measurement cannot be mistaken for a canonical
one later.

## Qualifier hardening from attempt 1

1. **RFC 7807 error bodies are read.** The qualifier understood only the OpenAI
   `{"error": {"message": …}}` envelope, so NIM's `problem+json` 410 — which stated its own cause
   verbatim — was recorded as `error_message=""`. Fixed; the raw artifact keeps the empty value as
   evidence.
2. **Free catalog preflight before any inference.** A retired or mistyped id is now named, with
   the related ids the host does offer, at zero cost. It reports candidates; it never selects one.
3. **`model_unavailable`** is a distinct error class (410, or *end of life* / *no longer
   available* wording) and aborts the run instead of burning six calls.

19 deterministic tests replay the captured body — no re-spend.
