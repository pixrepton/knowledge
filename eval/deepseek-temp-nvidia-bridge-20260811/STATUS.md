# DEEPSEEK-TEMP-BRIDGE-01 — status

```text
TEMP_BRIDGE_QUALIFICATION      = BLOCKED_OPERATOR_ACTION
TEMPORARY_ACTIVATION           = NOT_ACTIVE
CANONICAL_TARGET               = deepseek_direct        (unchanged)
FINAL_CAPABILITY_SUT_FREEZE    = HOLD
```

## Where things stand

The bridge **mechanism** is implemented, tested and reversible. The bridge **host** could not be
qualified, because `NVIDIA_API_KEY` is present but empty in both env files, so not even a
one-call connectivity smoke was possible.

Nothing was activated. `AI_OS_PRIMARY_PROVIDER` is unset, so the resolver returns the canonical
host — the default. Activating an unqualified provider in front of every stage would have been
the wrong trade.

## Provider state

```text
deepseek_direct   CANONICAL_TARGET    HTTP 402 Insufficient Balance   <- carried-in blocker
deepseek_nvidia   TEMPORARY_BRIDGE    implemented, credential absent
groq              FALLBACK            3 healthy slots
cerebras          OPTIONAL_FALLBACK   unconfigured, skipped
openai_chat       NOT_IN_ACTIVE_CHAIN removed 2026-08-10
anthropic         UNCONFIGURED        skipped
```

## Two operator actions, either of which unblocks work

1. **Fund DeepSeek Direct** — returns the system to canonical mode directly.
   Runbook: `RETURN_TO_DEEPSEEK_DIRECT.md`.
2. **Set `DEEPSEEK_NVIDIA_API_KEY`** — enables qualification of the temporary bridge, after
   which it may be activated while DeepSeek Direct is restored.

They are independent. (1) is the destination; (2) is a way to keep working on the way there.

## Cost

```text
completion tokens spent this task : 0
reasoning tokens spent this task  : 0
provider calls                    : 1  (canonical health smoke, HTTP 402)
```

For contrast, the previous diagnostic that zeroed the DeepSeek balance spent 38,699 completion
tokens. The guard is not theoretical: it stopped this run at the first 402.

## Capability rule, restated

`FINAL_CAPABILITY_SUT_FREEZE = HOLD` until `deepseek_direct` is restored and re-verified. If the
bridge is later activated, any benchmark produced during it is
`TEMP_PROVIDER_CAPABILITY_SIGNAL_ONLY = true` and is **not** a canonical Capability baseline.

`CAPABILITY-QUALIFICATION-20260809` remains BLOCKED. No Fresh38, judge or v5 rescore was run.
