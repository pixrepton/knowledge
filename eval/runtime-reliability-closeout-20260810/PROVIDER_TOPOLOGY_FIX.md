# Provider topology correction — DeepSeek as intended Tier-1 SUT

## The question that started this: why was `openai_chat` attempted before DeepSeek?

**It was not.** DeepSeek was already Tier 1 on every Fresh38-relevant stage. The earlier report
misread `llm_provider_attempts` — that field records **only the router tier**. The DeepSeek
priority-1 tier runs *before* the router and never appears in it, so a list beginning with
`openai_chat` looked like "the chain" when it was actually "the fallback chain, after DeepSeek
had already failed".

Classification of that observation: **OTHER — telemetry-shape artifact, not provider drift.**

A separate, real inconsistency did exist:

**`CONFIG_DRIFT`** — `.env.local-vps` overrode the base config to put a dead credential first in
the *fallback* chain.

```text
tools/gmail_audit/.env   line 28  LLM_PRIMARY_PROVIDER=groq          <- base config, correct
.env.local-vps           line 41  LLM_PRIMARY_PROVIDER=openai_chat   <- deployment override, wins
```

The deployment file was written when OpenRouter was a funded endpoint. The credential later lost
its credits (`HTTP 402 — this account never purchased credits`) but the ordering was never
revisited, so every DeepSeek fallthrough spent a guaranteed-402 round-trip before reaching Groq.

## Changes applied

Authorized explicitly by the operator. `LLM_BACKEND` deliberately untouched — its coupling to
model/URL resolution is separate from Tier-1 selection, and changing it would widen the blast
radius for no benefit.

| file | key | before | after |
|---|---|---|---|
| `.env.local-vps` | `LLM_PRIMARY_PROVIDER` | `openai_chat` | `groq` |
| `.env.local-vps` | `LLM_FALLBACK_PROVIDERS` | `groq,cerebras` | `cerebras` |
| `.env.local-vps` | `AGENT_GROQ_API_KEY` | `<key d8c3ee154fce>` | *(emptied)* |
| `tools/gmail_audit/.env` | `AGENT_GROQ_API_KEY` | `<key d8c3ee154fce>` | *(emptied)* |
| `.env.local-vps` | `LLM_BACKEND` | `openai_chat` | **unchanged** |

Timestamped backups were written next to each file before editing. No secret value was printed,
logged or committed; both env files are gitignored.

### Where the invalid Groq key actually came from

It was **not** in either `GROQ_API_KEY` or `GROQ_API_KEYS`. `config.py` merges four sources:

```python
groq_api_keys = parse_api_key_pool(
    os.getenv("GROQ_API_KEYS"), os.getenv("GROQ_API_KEY"),
    os.getenv("GROQ_API_VL"), os.getenv("AGENT_GROQ_API_KEY"),
)
```

The rejected credential arrived through **`AGENT_GROQ_API_KEY`** — an *agent-runtime* variable
leaking into the structured-stage pool. Verified per-source:

```text
GROQ_API_KEYS       2 slots  6e6026d00870, 79294c09485e   healthy
GROQ_API_KEY        1 slot   e6c595459627                 healthy
GROQ_API_VL         0 slots
AGENT_GROQ_API_KEY  1 slot   d8c3ee154fce                 HTTP 401 invalid   <- the leak
```

The planner did **not** use it (its three Groq endpoints were the healthy fingerprints), so
emptying it removes the dead slot from the SUT pool without changing planner behaviour.

## Proven topology after the change

Read live from the running container:

```text
TIER 1   primary_llm_provider() = deepseek        deepseek_configured = True
TIER 2   anthropic_configured   = False           -> skipped
FALLBACK router chain           = ['groq', 'cerebras']

signal_extraction    router=['groq','cerebras']  resolved= groq, groq, groq, cerebras[UNCONF]
intake_reasoning     router=['groq','cerebras']  resolved= groq, groq, groq, cerebras[UNCONF]
business_reasoning   router=['groq','cerebras']  resolved= groq, groq, groq, cerebras[UNCONF]
reply_drafter        router=['groq','cerebras']  resolved= groq, groq, groq, cerebras[UNCONF]
case_guidance        router=['groq','cerebras']  resolved= groq, groq, groq, cerebras[UNCONF]
intake_second_pass   router=['groq','cerebras']  resolved= groq, groq, groq, cerebras[UNCONF]

groq pool slots                 = 6e6026d00870, 79294c09485e, e6c595459627   (exactly the valid ones)
openai_chat in active chain?    = False
```

Requirements check:

| requirement | state |
|---|---|
| DeepSeek primary | **proven** — `primary_llm_provider() == deepseek`, Tier 1 on all six stages |
| Groq healthy slots only | **proven** — pool is exactly the three 200-OK fingerprints |
| no knowingly-invalid active credential | **proven** — `d8c3ee154fce` no longer resolves into any pool |
| OpenRouter/`openai_chat` not an active hop | **proven** — absent from every stage's router chain |
| no secrets in artifacts | **proven** — fingerprints only; leak-scanned |

`openai_chat` still appears in the *triage inventory* because a credential is still configured for
it. That is inventory, not topology: it is no longer reachable as a fallback hop.

## Judge — deliberately not conflated

The judge uses `settings.groq_api_keys` with `judge.GROQ_PROVIDER` / `judge.GROQ_MODEL`, described
in its own runner as the *frozen historical judge provider*. It is intentionally Groq, is not part
of the SUT chain, and was not changed.

## Consequence recorded honestly

DeepSeek is now returning `HTTP 402 "Insufficient Balance"` — see
`DEEPSEEK_EMPTY_CONTENT_01.md`. The topology above is correct and proven, but Tier 1 is currently
unusable for reasons of account balance, not configuration.
