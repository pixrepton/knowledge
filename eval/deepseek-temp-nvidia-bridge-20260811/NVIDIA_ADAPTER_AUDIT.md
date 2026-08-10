# NVIDIA adapter audit — no new adapter needed

## Question

Does hosting the DeepSeek tier on NVIDIA NIM require new adapter code?

## Answer: no

NVIDIA NIM exposes an OpenAI-compatible `/chat/completions` endpoint. The DeepSeek tier already
calls `_post_openai_chat_structured`, a generic OpenAI-compatible adapter that accepts an explicit
`base_url`, `api_key` and `model`. Pointing those three at NVIDIA NIM is sufficient.

What flows through unchanged, verified by reading the call path:

| concern | mechanism | changes for the bridge? |
|---|---|---|
| structured output | `response_format={"type":"json_object"}` | no |
| JSON schema contract | schema folded into the system prompt by the adapter | no |
| reasoning metadata | `extra_payload` thinking toggle; `reasoning_content` never promoted to business output | no |
| max_tokens | not sent (provider default) | no |
| timeout / deadline | `attempt_timeout_sec()` from the stage budget | no |
| provider telemetry | `llm_provider_attempts` + new host provenance fields | identity only |
| retry / fallback | `LLMRouter` + tier structure | no |

## What was added instead of an adapter

A **host resolver** — configuration, not protocol:

```python
DeepSeekHost(host, provider, base_url, model, api_keys, missing_config, role)
resolve_deepseek_host(settings)   # deepseek_direct | deepseek_nvidia
```

`_deepseek_providers` asks it for the endpoint/credential/model and the telemetry identity. That
is the entire mechanism.

## Identity, deliberately

```text
deepseek_direct -> telemetry label "deepseek"          role CANONICAL_TARGET
deepseek_nvidia -> telemetry label "deepseek_nvidia"   role TEMPORARY_BRIDGE
```

The canonical host keeps its long-standing `"deepseek"` label on purpose: renaming it would make
future canonical-mode measurements non-comparable with the 32/38 and 38/38 baselines recorded
under that label. Only the bridge takes a new identity — which is exactly what makes the two
distinguishable.

Every DeepSeek-tier response additionally carries:

```text
llm_logical_model_intent = "deepseek"
llm_deepseek_host        = deepseek_direct | deepseek_nvidia
llm_provider_role        = CANONICAL_TARGET | TEMPORARY_BRIDGE
llm_canonical_target     = "deepseek_direct"
```

## No hidden switching

There is no code path that selects a host from an error, a status code or a balance state. A test
asserts this structurally over the resolver's AST: `resolve_deepseek_host` must not reference
`status_code`, `error_class`, `quota_exhausted`, `exc`, `balance` or `insufficient`. The switch is
`AI_OS_PRIMARY_PROVIDER`, set by an operator.
