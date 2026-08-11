# Proof summary — DEEPSEEK-TEMP-BRIDGE-01

Every claim is backed by a named test, artifact or captured output.

## Result

```text
TEMP_BRIDGE_IMPLEMENTATION = PASS
TEMP_BRIDGE_QUALIFICATION  = PASS        (deepseek-ai/deepseek-v4-flash-0731)
TEMPORARY_ACTIVATION       = NOT_ACTIVE  (operator stood down; not a failure)
```

Mechanism built and proven, then qualified on the operator-authorized snapshot: 5/5 executed
calls succeeded on NVIDIA itself with valid schema and no fallback. Activation stopped before the
env change when the operator reported DeepSeek Direct funding. The canonical host is nonetheless
still unfunded per its own balance endpoint — see `DEEPSEEK_DIRECT_BILLING_CHECK.json`.

## What was proven

| claim | evidence |
|---|---|
| No new adapter is needed — NVIDIA NIM is OpenAI-compatible and the DeepSeek tier already uses that adapter | `NVIDIA_ADAPTER_AUDIT.md`; the tier calls `_post_openai_chat_structured` with explicit base_url/key/model |
| Host selection is independent of `LLM_BACKEND` | `test_host_selection_is_independent_of_llm_backend` — bridge resolves identically under both backend values; `LLM_BACKEND` untouched |
| Canonical target is the default and keeps its identity | `test_default_host_is_the_canonical_target`, `test_canonical_host_keeps_the_historical_telemetry_label` |
| Bridge has a distinct identity and role | `test_bridge_has_a_distinct_identity_and_role` — label `deepseek_nvidia`, role `TEMPORARY_BRIDGE` |
| Switching hosts changes endpoint/credential/model only | `test_switching_host_changes_only_endpoint_credential_and_model` |
| Bridge model is explicit-only, fails closed | `test_bridge_has_no_default_model`, `test_selecting_the_bridge_without_a_model_is_a_config_error`, `test_missing_bridge_model_makes_the_host_unconfigured` |
| Bridge never borrows the generic `nvidia` model or substitutes the canonical one | `test_bridge_never_borrows_the_generic_nvidia_model`, `test_bridge_never_substitutes_the_canonical_model` |
| Canonical mode unaffected by unset bridge variables | `test_canonical_mode_is_unaffected_by_an_unset_bridge_model` |
| No hidden billing-triggered switch | `test_no_code_path_selects_the_bridge_from_a_billing_or_quota_error` — AST assertion over the resolver |
| A typo cannot silently reroute a measurement | `test_an_unknown_host_value_is_a_config_error_not_a_silent_default` |
| Telemetry distinguishes the hosts | `test_bridge_calls_carry_host_provenance`, `test_canonical_calls_are_labelled_canonical` |
| Governance registry cannot drift from the runtime | `test_provider_roles_registry_matches_the_runtime` |
| Fallback contract unchanged | `FALLBACK_PROOF.md` — 4 deterministic tier-boundary tests |
| Cost guard works | `COST_GUARD_REPORT.json` — 0 tokens spent across both hosts; each probe stopped at call 1 (402, then 410) |
| The bridge engaged correctly once configured | `NVIDIA_QUALIFICATION.json` — resolved `host=deepseek_nvidia role=TEMPORARY_BRIDGE model=deepseek-ai/deepseek-v4-flash configured=True` before the call |
| The configured model is retired upstream | `NVIDIA_QUALIFICATION.json` HTTP 410 + `NVIDIA_CATALOG_PREFLIGHT.json` — 101-model catalog, id absent |
| A retired model id now costs zero calls | `NVIDIA_CATALOG_PREFLIGHT.json` — free `GET /models` preflight blocks before inference |
| Host error bodies are read in both envelope shapes | `test_rfc7807_detail_is_read_not_dropped`, `test_openai_envelope_still_wins_when_present` |
| `410` / end-of-life aborts instead of burning 6 calls | `test_retired_model_is_classified_as_model_unavailable`, `test_model_unavailable_aborts_instead_of_burning_six_calls` |
| Nothing was activated | `ACTIVATION_PROOF.md`, `PROVIDER_TOPOLOGY_AFTER.json` — `AI_OS_PRIMARY_PROVIDER` unset, containers not recreated |
| The 0731 snapshot satisfies the AI-OS structured contracts | `NVIDIA_QUALIFICATION_0731.json` — 5/5 executed, schema valid, 0 empty content, 0 fallback |
| No result was rescued by Groq | qualifier posts directly to the host; Groq is structurally absent from its path |
| The bridge claims family, not proven identity | `test_bridge_does_not_claim_proven_model_equivalence`, `test_both_hosts_serve_the_same_declared_family` |
| The withdrawn "preserved model identity" claim cannot silently return | `test_registry_no_longer_claims_preserved_model_identity` |
| Registry and runtime agree on family and equivalence, not just role | `test_provider_roles_registry_matches_the_runtime` (extended) |
| The reported DeepSeek top-up is not visible to the configured key | `DEEPSEEK_DIRECT_BILLING_CHECK.json` — `GET /user/balance` `is_available:false`, `total_balance -0.00` |

## Correction made before operator config

`DEEPSEEK_NVIDIA_MODEL` originally defaulted to `deepseek-ai/deepseek-r1`. That would have changed
provider *and* model together, which defeats the bridge. It is now explicit-only and fails closed
in three independent places: config validation, the host resolver, and the provider builder.

## What was NOT proven

- **NVIDIA NIM compatibility with the AI-OS contracts.** Still unknown. One transport-level call
  was made and it was rejected before reaching a model. Schema fidelity, empty-content behaviour,
  structured-output handling and latency on that host remain **unmeasured**.
- **That `deepseek-ai/deepseek-v4-flash-0731` is the same weights as DeepSeek Direct's current
  `deepseek-v4-flash`.** Both sides are aliases/snapshots; nothing observable from here settles it.
  This is the reason the substitution was left to the operator.
- Nothing about equivalence to DeepSeek Direct. That was never in scope, and six calls could not
  establish it anyway.

## Tests

```text
targeted provider suites   112 passed, 0 failed
qualifier cost-guard suite  19 passed, 0 failed   (12 prior + 7 error-envelope regressions)
Gate A                     2507 passed, 15 skipped, 24 subtests, 0 failed
```

Gate A was re-run for the fail-closed correction earlier today. The qualifier changes since then
are confined to `scripts/qualify_deepseek_host.py`, which no runtime path imports; they are
covered by the 19-test suite above.

## Secrets

Leak scan over all artifacts: **PASS**. Credentials appear only as `configured=true/false` or as
one-way sha256 fingerprints. No key, prompt, customer text or reasoning content is recorded.
