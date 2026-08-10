# Provider architecture — before the bridge

Established mechanically before any code was written.

## Tier structure in `run_central_structured_stage`

```text
tier 0  cache (temperature==0 + output_model + DB configured)     -- cold in practice
tier 1  DeepSeek          if deepseek_configured(settings)
tier 2  Anthropic         elif anthropic_configured(settings)     -- UNSET, skipped
tier 3  router chain      else  ->  LLMRouter(_structured_providers(...))
```

The DeepSeek tier is **not** part of the router. It is a separate priority-1 attempt whose
provider attempts never appear in `llm_provider_attempts` — the fact that caused an earlier
report to misread `openai_chat` as "first in the chain".

## How the DeepSeek tier reaches its provider

`_deepseek_providers` builds a single `LLMProvider` whose call goes through
`_post_openai_chat_structured(..., base_url=<deepseek>, api_key=<deepseek>, extra_payload=<thinking>)`.

That adapter is **generic OpenAI-compatible**: structured output (`response_format=json_object`),
the JSON-schema contract folded into the system prompt, temperature, and `extra_payload` for
DeepSeek's thinking toggle. Everything below it — per-attempt timeout from the stage deadline,
retry, provider telemetry, empty-content classification — is shared.

## Was NVIDIA already supported?

Yes, as a **router-tier** provider: `nvidia_base_url`, `nvidia_api_key(s)`, `nvidia_model` in
`Settings`, an `nvidia` branch in `_structured_providers`, and model mapping in
`_structured_model_for_provider`. It uses the same `_post_openai_chat_structured` adapter.

**Conclusion: no new adapter is required.** NVIDIA NIM is an OpenAI-compatible endpoint and the
existing adapter already speaks that protocol. Creating a second LLM runtime would have been
redundant.

But the existing `nvidia` slot is the *generic fallback* identity with
`NVIDIA_MODEL=gpt-oss-120b` — not a DeepSeek host. Reusing it would have changed the logical
model while pretending only the host changed.

## `LLM_BACKEND` coupling — proven irrelevant here

`LLM_BACKEND` drives `openai_chat_completions_url` and `groq_model` resolution. The DeepSeek tier
passes an **explicit** `base_url`, `api_key` and `model` to the adapter:

```python
_post_openai_chat_payload(... base_url=deepseek_base_url ...)
url = _openai_chat_completions_url(base_url) if base_url is not None else settings.openai_chat_completions_url
```

so the branch that consults `LLM_BACKEND` is never taken for this tier. Host selection is
therefore independent of `LLM_BACKEND`, and it was left untouched. A test pins this
(`test_host_selection_is_independent_of_llm_backend`).

## Credential state at takeover

```text
DEEPSEEK_API_KEY        configured, account HTTP 402 Insufficient Balance
NVIDIA_API_KEY          present but EMPTY in both env files
NVIDIA_MODEL            gpt-oss-120b   (generic router slot, not DeepSeek)
GROQ pool               3 healthy slots
```
