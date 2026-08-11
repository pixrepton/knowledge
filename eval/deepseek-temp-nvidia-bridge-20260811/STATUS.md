# DEEPSEEK-TEMP-BRIDGE-01 — status

```text
TEMP_BRIDGE_IMPLEMENTATION     = PASS
TEMP_BRIDGE_QUALIFICATION      = PASS      (deepseek-ai/deepseek-v4-flash-0731)
TEMPORARY_ACTIVATION           = NOT_ACTIVE   <- operator stood down; bridge not needed
TEMP_BRIDGE_RUNTIME_PROOF      = NOT_APPLICABLE
CANONICAL_TARGET               = deepseek_direct / deepseek-v4-flash   (unchanged)
CANONICAL_AVAILABILITY         = UNAVAILABLE   (account balance zero; see below)
FINAL_CAPABILITY_SUT_FREEZE    = HOLD
```

## What happened

The operator authorized the `0731` snapshot, qualification ran and **passed**, the runtime image
was rebuilt to contain the bridge — and then the operator reported that DeepSeek Direct had been
funded, so the bridge was no longer needed. Activation was stopped before
`AI_OS_PRIMARY_PROVIDER` was ever written.

The bridge is therefore **qualified and ready, but inert**. Turning it on is one env line plus a
container recreate; nothing else is outstanding.

## Qualification result — deepseek-ai/deepseek-v4-flash-0731

Free catalog preflight first: id present in NVIDIA NIM's 101-model catalog, so no call was
risked on a retired id.

| stage | outcome | schema | completion tokens | latency |
|---|---|---|---|---|
| *connectivity smoke* | OK, http 200 | — | — | 13 875 ms |
| signal_extraction | NVIDIA_PRIMARY_SUCCESS | valid | 98 | 11 984 ms |
| intake_reasoning | NVIDIA_PRIMARY_SUCCESS | valid | 855 | 21 202 ms |
| business_reasoning | NVIDIA_PRIMARY_SUCCESS | valid | 862 | 18 500 ms |
| business_reasoning_large_context | NVIDIA_PRIMARY_SUCCESS | valid | 1 106 | 31 875 ms |
| reply_drafter | NVIDIA_PRIMARY_SUCCESS | valid | 592 | 57 625 ms |
| schema_stress | **SKIPPED** — `max_calls reached (6)` | — | — | — |

`5/5` executed calls succeeded on NVIDIA itself with valid schema, zero empty content, zero
fallback. **No Groq rescue: the qualifier is a direct host probe, so Groq is not in its path.**

**Read the coverage honestly.** Six representative stages were specified; five ran. The smoke
consumes one slot of `MAX_CALLS=6`, so `schema_stress` was cut by the cost guard rather than
passed. Raising the cap was explicitly out of contract, so it was not raised. `schema_stress`
reuses the `IntakeReasoningResult` contract that `intake_reasoning` already validated, so the
gap is small — but it is a gap, not a pass.

Latency is worth noting for planning: 12–58 s per structured call, notably slower than the
canonical host has historically been.

## Canonical DeepSeek Direct — still unavailable

The operator reported adding $2. The API disagrees, and the API is the authority here:

```text
POST /v1/chat/completions -> HTTP 402 "Insufficient Balance"
GET  /user/balance        -> HTTP 200   (free, no inference)
     {"is_available": false,
      "balance_infos": [{"currency":"USD","total_balance":"-0.00",
                         "granted_balance":"0.00","topped_up_balance":"-0.00"}]}
```

Exactly one `DEEPSEEK_API_KEY` is defined in `.env.local-vps` (line 157, sha256 fingerprint
`72a31b22fa33`), so this is not a duplicate-definition mix-up. The funds are not visible to this
credential: they went to a different account/org, or have not settled.

**Operator check:** confirm the funded DeepSeek account is the one that issued key `72a31b22fa33`.
If not, fund that account or replace `DEEPSEEK_API_KEY` with a key from the funded one.

## Config changes applied

```text
DEEPSEEK_NVIDIA_MODEL   deepseek-ai/deepseek-v4-flash -> deepseek-ai/deepseek-v4-flash-0731
                        (both duplicate blocks, lines 17 and 162)
NVIDIA_MODEL            deepseek-ai/deepseek-v4-flash -> cleared
LLM_BACKEND             untouched (openai_chat)
DEEPSEEK_API_KEY/MODEL  untouched
AI_OS_PRIMARY_PROVIDER  still unset -> canonical host by default
```

`NVIDIA_MODEL` feeds the *generic* nvidia router slot, not the bridge. It was left holding the
retired DeepSeek alias. The documented previous value `gpt-oss-120b` turns out not to be a valid
NIM id either (the catalog lists `openai/gpt-oss-120b`), so restoring it would have restored a
second broken id. Cleared instead, which under the config contract yields
`DEFAULT_NVIDIA_MODEL = meta/llama-3.3-70b-instruct` — catalog-verified present. The slot has no
credential (`NVIDIA_API_KEY=`) and is not in the active chain, so this is hygiene, not a fix.

## Governance semantics corrected

The bridge can no longer be described as "same model, different host", and no longer claims to be:

```text
role                                  TEMPORARY_OPERATIONAL_BRIDGE   (was TEMPORARY_BRIDGE)
logical_model_family                  DeepSeek V4 Flash              (preserved across hosts)
exact_model_equivalence_to_canonical  UNPROVEN on the bridge, PROVEN on canonical
temporary_model_snapshot              deepseek-ai/deepseek-v4-flash-0731
canonical_target                      deepseek_direct / deepseek-v4-flash
```

Carried in telemetry on every DeepSeek-tier call (`llm_logical_model_family`,
`llm_exact_model_equivalence`, `llm_canonical_target_model`), so a bridge-era result cannot be
mistaken for a canonical one by anyone reading only the provider label. A regression test asserts
the withdrawn wording does not reappear.

## Runtime state

```text
image gmail-agent-runtime:local   rebuilt 73fbac63f0b2 from repo state (contains the bridge)
containers                        NOT recreated - still on the pre-bridge image, restarts=0
AI_OS_PRIMARY_PROVIDER            unset -> canonical
```

Containers were deliberately left running. Activation was cancelled, so recreating them was not
required, and `restart: unless-stopped` keeps a container on its own image id — nothing will pick
up the new image until someone recreates it explicitly.

## Cost

```text
provider calls this task     8   (2 canonical 402, 1 bridge 410, 1 smoke + 5 stages on 0731)
completion tokens            3 521
reasoning tokens             0        (this snapshot returned no reasoning content)
free account/catalog queries 3        no inference, no tokens
guard violated               no       (stopped exactly at max_calls on the qualification run)
```

One earlier qualification attempt was killed by a harness timeout before writing its artifact;
its spend is included above. No budget was raised to compensate.

## Capability rule, restated

`FINAL_CAPABILITY_SUT_FREEZE = HOLD` until `deepseek_direct` is restored and re-verified. Any
benchmark produced on the bridge is `TEMP_PROVIDER_CAPABILITY_SIGNAL_ONLY = true` and is **not**
a canonical Capability baseline.

`CAPABILITY-QUALIFICATION-20260809` remains BLOCKED. No Fresh38, judge or v5 rescore was run.
