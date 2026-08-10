# NVIDIA NIM qualification — BLOCKED_OPERATOR_ACTION

```text
TEMP_BRIDGE_QUALIFICATION = BLOCKED_OPERATOR_ACTION
```

No qualification call was made, because there is no credential to make it with.

## Why

`NVIDIA_API_KEY` is **present but empty** in both env files:

```text
.env.local-vps   line 57  NVIDIA_API_KEY configured=False
.env             line 43  NVIDIA_API_KEY configured=False
```

The harness therefore stopped before its connectivity smoke:

```text
BLOCKED_OPERATOR_ACTION: DEEPSEEK_NVIDIA_API_KEY is not configured for deepseek_nvidia
No provider call was made; nothing was spent.
```

`§9` requires exactly one tiny smoke call first and a stop if it fails. Here even the smoke was
impossible, so the six representative qualification calls were never attempted. Nothing about
NVIDIA NIM's compatibility with the AI-OS contracts has been demonstrated — that is honestly
unknown, not assumed-good.

## Canonical host health, for contrast

The same harness was pointed at the canonical host, which spends exactly one smoke call:

```text
deepseek_direct  smoke  http=402  error_class=quota_exhausted  "Insufficient Balance"
VERDICT=FAIL  (stopped before qualification)
cost: calls=1  completion_tokens=0  reasoning_tokens=0  guard_triggered=True
```

That is the carried-in blocker, reproduced cheaply.

## What the operator needs to do

```text
variable   DEEPSEEK_NVIDIA_API_KEY      (falls back to NVIDIA_API_KEY if you prefer to reuse it)
where      gmail-agent/.env.local-vps   -- the deployment env file the container mounts
model      DEEPSEEK_NVIDIA_MODEL        defaults to deepseek-ai/deepseek-r1
           set it explicitly if your NIM deployment exposes a different DeepSeek model id
```

Then verify without spending anything beyond one smoke call:

```bash
python scripts/qualify_deepseek_host.py --host deepseek_nvidia --out /tmp/nvidia_qual.json
```

Expected on success: `smoke OK http=200`, then up to six qualification calls, then a verdict.

**Do not** set `AI_OS_PRIMARY_PROVIDER=deepseek_nvidia` before that qualification passes. The
bridge is implemented and inert; activating an unqualified host would put an unverified provider
in front of every stage.

## What the six qualification calls will measure, when they can run

| # | stage | contract |
|---|---|---|
| 1 | `signal_extraction` | `SignalExtractionResult` |
| 2 | `intake_reasoning` | `IntakeReasoningResult` |
| 3 | `business_reasoning` | `BusinessReasoningResult`, normal context |
| 4 | `business_reasoning_large_context` | same contract, larger realistic payload |
| 5 | `reply_drafter` | `ReplyDraftResult` |
| 6 | `schema_stress` | largest schema (`IntakeReasoningResult`, 8,782 chars) |

Recorded per call: HTTP status, latency, `finish_reason`, `content_len`, `content_type`,
`structured_output_valid`, `schema_valid` (real Pydantic validation), `reasoning_present`,
reasoning/completion tokens, `has_tool_calls`, `failure_class`, and an explicit `outcome` of
`PRIMARY_SUCCESS` or `PRIMARY_FAILED:<class>`.

Synthetic fixtures only — no real customer data. No reasoning/chain-of-thought text is stored.

## Primary vs fallback will not be blurred

Per `§14`, the harness probes the host **directly**, so a Groq rescue cannot be misreported as an
NVIDIA success. `fallback_triggered` is `false` by construction and every row states whether
NVIDIA itself produced the answer.
