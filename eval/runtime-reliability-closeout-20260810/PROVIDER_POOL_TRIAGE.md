# CL-05 — Live LLM provider pool triage

Read-only. One `max_tokens=1` smoke call per configured credential slot; nothing was mutated.
Machine-readable form: `PROVIDER_POOL_TRIAGE.json`. Tool: `scripts/provider_pool_triage.py`.

**No secret appears here or in the JSON.** Each slot is identified by position and a one-way
`sha256(key)[:12]` fingerprint — enough for an operator to know *which* credential is bad without
the value being disclosed. A leak scan over the artifact found no key material, bearer token, or
Authorization header (the single textual match is the disclaimer sentence itself).

## Inventory

| provider | slot | fingerprint | configured | HTTP | classification | detail |
|---|---|---|---|---|---|---|
| `openai_chat` (primary) | `OPENAI_COMPAT_API_KEY` | `a4459b8072da` | yes | **402** | **QUOTA_CAPACITY** | "Insufficient credits. This account never purchased credits." |
| `groq` | `GROQ_API_KEY_SLOT_1` | `6e6026d00870` | yes | 200 | HEALTHY | |
| `groq` | `GROQ_API_KEY_SLOT_2` | `79294c09485e` | yes | 200 | HEALTHY | |
| `groq` | `GROQ_API_KEY_SLOT_3` | `e6c595459627` | yes | 200 | HEALTHY | |
| `groq` | `GROQ_API_KEY_SLOT_4` | `d8c3ee154fce` | yes | **401** | **CREDENTIAL_DEFECT** | "Invalid API Key" |
| `cerebras` | `CEREBRAS_API_KEY` | — | no | — | EXPECTED_UNCONFIGURED | declared fallback, no credential |
| `nvidia` | `NVIDIA_API_KEY` | — | no | — | EXPECTED_UNCONFIGURED | |
| `openrouter` | `OPENROUTER_API_KEY` | — | no | — | EXPECTED_UNCONFIGURED | not a separate slot; the OpenRouter endpoint is reached through `openai_chat` |
| `deepseek` | `DEEPSEEK_API_KEY` | `72a31b22fa33` | yes | 200 | HEALTHY | priority-1 structured tier |
| `anthropic` | `ANTHROPIC_API_KEY` | — | no | — | EXPECTED_UNCONFIGURED | the CL-02 path; unreachable by configuration |

```text
summary: HEALTHY 4 | QUOTA_CAPACITY 1 | CREDENTIAL_DEFECT 1 | EXPECTED_UNCONFIGURED 4
active chain: openai_chat -> groq -> cerebras
healthy providers in the active chain: groq
```

## What this means

The declared active chain is `openai_chat → groq → cerebras`. Its **primary is dead** (no credits,
a permanent state until someone buys them) and its **last hop is unconfigured**. Everything the
system currently does therefore rests on the Groq pool, in which **one of four keys is rejected**.

That is why the 38/38 measurement still succeeded: three healthy Groq keys absorbed the whole run.
It is not a comfortable position — it is a single-provider dependency wearing a three-provider
chain's clothing, and it was invisible until the FIX-RT01 telemetry exposed it.

Note also that `openai_chat` is pointed at `https://openrouter.ai/api/v1`, not at OpenAI. The
`quota_exhausted` seen in the `NEW-05` artifact was an OpenRouter credits failure.

## A product defect this triage uncovered — fixed here

Not a credentials problem, and the more serious finding of the two.

`auth` was classified non-retryable, and the router treated "not retryable" as "stop the chain".
Because `_rotate_groq_key_pool` rotates the starting slot on every call, roughly **one call in
four** began on the dead key and aborted the whole chain **without ever trying the three healthy
keys**. Reproduced deterministically:

```text
providers = [groq#dead(401), groq#healthy]
before: chain ABORTED,  tried = ['dead']
after : recovered,      tried = ['dead(401)', 'healthy']   selected = groq#healthy
```

Fix: retryability and chain-termination are now distinct (`ProviderErrorInfo.chain_terminal` /
`.stops_chain`). A rejected credential disqualifies itself, never the entries behind it. It is
still not retried against itself, and it stays visible in `llm_provider_attempts`, so a bad key
remains attributable rather than silently absorbed. Request-scoped failures (`contract`) still
stop the chain, because they would fail identically on every provider.

Nine tests pin this in `tools/gmail_audit/tests/test_provider_pool_degradation.py`, including a
reproduction of the exact live pool shape and an assertion that degradation is per-call — nothing
is permanently disabled behind the operator's back.

## Provider-chain behaviour, verified against the section-10 checklist

| requirement | status |
|---|---|
| configured but credential absent → skipped intentionally | verified — unconfigured providers are recorded `status=skipped`, `error_class=config`, never invoked |
| credential invalid → structured degradation, not silent repeated waste | fixed — one attempt, recorded, chain continues |
| quota exhausted → structured classification | verified — `quota_exhausted`, fast fall-through (152 ms observed live) |
| all providers unavailable → bounded terminal failure | verified — every reason recorded, `terminal_failure_reason` set |
| healthy fallback remains reachable | **fixed** — this was the defect above |
| transient failures not cached forever | verified — degradation is per-call; the dead key is retried on the next call rather than persistently disabled |

## OPERATOR_ACTION_REQUIRED

Two items. Neither can be completed without operator-held secrets or billing access, so neither
was attempted. No configuration file was modified.

### 1. Primary provider has no credits

```text
provider   openai_chat (primary)
slot       OPENAI_COMPAT_API_KEY   (endpoint https://openrouter.ai/api/v1)
problem    HTTP 402 - "Insufficient credits. This account never purchased credits."
action     Either purchase OpenRouter credits for that account, or repoint the primary
           (OPENAI_COMPAT_BASE_URL / OPENAI_COMPAT_API_KEY, or LLM_PRIMARY_PROVIDER) at a
           funded provider. Until then every stage burns one round-trip on a guaranteed 402
           before falling back.
```

### 2. One Groq key is rejected

```text
provider   groq
slot       GROQ_API_KEY_SLOT_4     (fingerprint d8c3ee154fce)
problem    HTTP 401 - "Invalid API Key"
action     Remove that entry from the GROQ_API_KEY pool in .env.local-vps, or replace it with a
           valid key. Slots 1-3 are healthy and need no change.
note       Removing a dead slot needs no new secret, but it is a live credential-file edit, so
           it is left to the operator. The runtime now tolerates it either way.
```

### Not required

`cerebras`, `nvidia`, `anthropic` are unconfigured **by design** for this deployment and are
correctly skipped. Configuring `cerebras` would restore a genuine third hop to the active chain,
but that is a capacity decision, not a defect.

## Residual risk after operator action

With item 1 unresolved the chain is effectively `groq`-only. Three healthy keys is real
redundancy against rate limits, but not against a Groq-wide outage. That is a capacity/topology
observation for the operator, not a runtime defect, and it is outside this closeout's scope.
