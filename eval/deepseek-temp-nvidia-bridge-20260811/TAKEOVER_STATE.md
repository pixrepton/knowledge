# Takeover state — DEEPSEEK-TEMP-BRIDGE-01

## What this task is, and is not

A **temporary, operator-controlled host bridge** so AI-OS can keep working while the DeepSeek
Direct account is unfunded. It is not a migration, not a change of target architecture, not a new
Capability Program, and not a final qualification.

```text
deepseek_direct  = CANONICAL_TARGET     (unchanged, still the intended primary SUT provider)
deepseek_nvidia  = TEMPORARY_BRIDGE
groq             = FALLBACK
cerebras         = OPTIONAL_FALLBACK
```

## Accepted state carried in

```text
PRE_FIX_FIRST_ATTEMPT_RELIABILITY  = 32/38 =  84.21%
POST_FIX_FIRST_ATTEMPT_RELIABILITY = 38/38 = 100.00%
POST_CLOSEOUT (closeout SUT)       = 38/38 = 100.00%
```

Topology before this task: DeepSeek Direct Tier 1 -> Anthropic (unconfigured, skipped) ->
router `groq -> cerebras`. `openai_chat` was removed from the active chain on 2026-08-10 and the
known-invalid Groq credential was removed.

Blocker carried in: **DeepSeek Direct returns HTTP 402 "Insufficient Balance"** — the balance was
exhausted during the previous DEEPSEEK-EMPTY-CONTENT-01 reproduction.

## Governance

`AIOS-RUNTIME-RELIABILITY-01` was still active and is the runtime/provider task, so it was
resumed and its scope extended with
`knowledge:eval/deepseek-temp-nvidia-bridge-20260811` rather than opening a second active task
(which would trip the workspace write guard). The work is tracked under the
`DEEPSEEK-TEMP-BRIDGE-01` name inside it.

`CAPABILITY-QUALIFICATION-20260809` remains BLOCKED and untouched. Foreign dirty state was not
adopted. Nothing was pushed.
