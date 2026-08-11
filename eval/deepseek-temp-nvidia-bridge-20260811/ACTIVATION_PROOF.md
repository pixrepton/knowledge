# Activation proof — DEEPSEEK-TEMP-BRIDGE-01

```text
TEMPORARY_ACTIVATION      = NOT_ACTIVE
TEMP_BRIDGE_QUALIFICATION = BLOCKED_OPERATOR_ACTION
CANONICAL_TARGET          = deepseek_direct   (unchanged)
```

There is no activation to prove. Qualification did not reach PASS, so under §8 of the activation
contract `AI_OS_PRIMARY_PROVIDER` was **not** set to `deepseek_nvidia`.

## What was deliberately not done

| step | state | why |
|---|---|---|
| `AI_OS_PRIMARY_PROVIDER=deepseek_nvidia` | not written | qualification != PASS |
| runtime restart / recreate | not performed | nothing to activate |
| production-path smoke through `run_central_structured_stage` | not run | would have proven nothing about an unqualified host |
| Fresh38 / judge / v5 | not run | out of scope by instruction, and doubly so now |
| trying a different model id | not done | substitution is an operator decision, not an automatic fallback |
| switching primary to Groq | not done | Groq is the fallback; promoting it would hide the problem |

## Current runtime state — unchanged by this task

```text
gmail-agent-nodeb-api                 Up 8 hours    restarts=0
gmail-agent-vps-gmail-agent-worker-1  Up 3 hours    restarts=0
```

Neither container was restarted, recreated or rebuilt. `.env.local-vps` was not modified by this
task; the operator's own edit (credential + model) is the only change to it.

`AI_OS_PRIMARY_PROVIDER` remains unset, so the resolver returns the canonical host by default.
The bridge remains inert — implemented, tested, and not in any request path.

## Two prerequisites before activation can be attempted again

1. **An explicit, host-offered model id.** `deepseek-ai/deepseek-v4-flash` was retired by NVIDIA
   on 2026-08-07. See `NVIDIA_QUALIFICATION.md`.
2. **An image rebuild.** `gmail-agent-runtime:local` predates the bridge code; `resolve_deepseek_host`
   is absent from the running container. A restart picks up env, not code. Rebuild from repo state
   — do not hand-copy files into the container.

Both are mechanically verified in `NVIDIA_QUALIFICATION.md`. Neither is a defect in the bridge.
