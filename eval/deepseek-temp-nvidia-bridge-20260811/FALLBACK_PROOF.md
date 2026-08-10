# Fallback proof — the bridge slots into the existing contract

Deterministic, no live provider. `tools/gmail_audit/tests/test_deepseek_bridge_fallback.py`,
proven at the tier boundary in `run_central_structured_stage` with the bridge selected as host.

| required behaviour | test | result |
|---|---|---|
| bridge success -> Groq NOT called | `test_bridge_success_means_groq_is_never_called` | PASS — router tier never invoked; `central_llm_provider == "deepseek_nvidia"` |
| bridge retryable failure -> Groq reachable | `test_bridge_retryable_failure_reaches_groq` | PASS — 503 falls through, Groq serves, provider recorded as `groq` |
| bridge quota/auth failure -> structured attribution, existing policy | `test_bridge_quota_failure_is_attributable_and_follows_existing_policy` | PASS — 402 recorded via `LLM_DEEPSEEK_FAILED` with `status_code`/`error_class`, then falls through |
| Groq failure, Cerebras absent -> bounded terminal | `test_groq_failure_without_cerebras_is_a_bounded_terminal_result` | PASS — `terminal_failure_reason=provider_chain_exhausted` |

No new retry system was introduced. This rides the repaired stage-deadline model: the bridge is
one more host for the existing tier, so per-attempt timeouts, budget sharing, retry and
fallback are unchanged.

## Identity is preserved through the fallback

The quota test also pins that a bridge failure is attributable rather than anonymous — the
`LLM_DEEPSEEK_FAILED` diagnostics added in DEEPSEEK-EMPTY-CONTENT-01 carry `status_code` and
`error_class`, so "the bridge ran out of quota" and "the bridge returned empty content" remain
distinguishable after the fact.
