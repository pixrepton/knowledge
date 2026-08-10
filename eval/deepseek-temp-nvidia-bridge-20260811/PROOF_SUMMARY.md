# Proof summary — DEEPSEEK-TEMP-BRIDGE-01

Every claim is backed by a named test, artifact or captured output.

## Result

```text
TEMP_BRIDGE_QUALIFICATION = BLOCKED_OPERATOR_ACTION
```

Mechanism built and proven; host unqualifiable for lack of a credential.

## What was proven

| claim | evidence |
|---|---|
| No new adapter is needed — NVIDIA NIM is OpenAI-compatible and the DeepSeek tier already uses that adapter | `NVIDIA_ADAPTER_AUDIT.md`; the tier calls `_post_openai_chat_structured` with explicit base_url/key/model |
| Host selection is independent of `LLM_BACKEND` | `test_host_selection_is_independent_of_llm_backend` — bridge resolves identically under both backend values; `LLM_BACKEND` untouched |
| Canonical target is the default and keeps its identity | `test_default_host_is_the_canonical_target`, `test_canonical_host_keeps_the_historical_telemetry_label` |
| Bridge has a distinct identity and role | `test_bridge_has_a_distinct_identity_and_role` — label `deepseek_nvidia`, role `TEMPORARY_BRIDGE` |
| Switching hosts changes endpoint/credential/model only | `test_switching_host_changes_only_endpoint_credential_and_model` |
| Bridge does not borrow the generic `nvidia` router model | `test_bridge_model_does_not_default_to_the_generic_nvidia_model` — stays a DeepSeek model, never `gpt-oss-120b` |
| No hidden billing-triggered switch | `test_no_code_path_selects_the_bridge_from_a_billing_or_quota_error` — AST assertion over the resolver |
| A typo cannot silently reroute a measurement | `test_an_unknown_host_value_is_a_config_error_not_a_silent_default` |
| Telemetry distinguishes the hosts | `test_bridge_calls_carry_host_provenance`, `test_canonical_calls_are_labelled_canonical` |
| Governance registry cannot drift from the runtime | `test_provider_roles_registry_matches_the_runtime` |
| Fallback contract unchanged | `FALLBACK_PROOF.md` — 4 deterministic tier-boundary tests |
| Cost guard works | `COST_GUARD_REPORT.json` — 0 tokens spent; canonical probe stopped at call 1 on 402 |

## What was NOT proven

- **NVIDIA NIM compatibility with the AI-OS contracts.** No call was made. Schema fidelity,
  empty-content behaviour, structured-output handling and latency on that host are **unknown**.
- Nothing about equivalence to DeepSeek Direct. That was never in scope, and six calls could not
  establish it anyway.

## Tests

```text
targeted provider suites   112 passed, 0 failed
Gate A                     2501 passed, 15 skipped, 24 subtests, 0 failed
```

## Secrets

Leak scan over all artifacts: **PASS**. Credentials appear only as `configured=true/false` or as
one-way sha256 fingerprints. No key, prompt, customer text or reasoning content is recorded.
