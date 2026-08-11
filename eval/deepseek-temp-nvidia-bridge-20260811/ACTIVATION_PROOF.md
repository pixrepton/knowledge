# Activation proof — DEEPSEEK-TEMP-BRIDGE-01

```text
TEMP_BRIDGE_QUALIFICATION = PASS        (deepseek-ai/deepseek-v4-flash-0731, 5/5 executed calls)
TEMPORARY_ACTIVATION      = NOT_ACTIVE  (stopped by operator decision, not by a failure)
CANONICAL_TARGET          = deepseek_direct / deepseek-v4-flash   (unchanged)
```

There is no activation to prove, and this time it is not because anything failed.

Qualification passed and the runtime image was rebuilt to contain the bridge. Before the activation
env change was written, the operator reported that DeepSeek Direct had been funded and stood the
bridge down. Work stopped there.

## Activation sequence — how far it got

| step | state |
|---|---|
| governance semantics corrected (`TEMPORARY_OPERATIONAL_BRIDGE`, family/equivalence) | done |
| `DEEPSEEK_NVIDIA_MODEL=deepseek-ai/deepseek-v4-flash-0731` | done |
| generic `NVIDIA_MODEL` cleaned up | done |
| free catalog preflight — id present | done |
| cost-guarded qualification | **PASS**, 5/5 executed, `schema_stress` cut by the call cap |
| image rebuild from repo state (`gmail-agent-runtime:local` → `73fbac63f0b2`) | done |
| **`AI_OS_PRIMARY_PROVIDER=deepseek_nvidia`** | **NOT WRITTEN** — stood down here |
| container recreate onto the new image | not performed |
| host↔container parity proof | not performed (nothing recreated to prove) |
| production-path smoke | not run |
| Fresh38 / judge / v5 | not run, out of scope |

## Current runtime state

```text
gmail-agent-nodeb-api                 restarts=0   pre-bridge image
gmail-agent-vps-gmail-agent-worker-1  restarts=0   pre-bridge image
AI_OS_PRIMARY_PROVIDER                unset -> canonical host by default
```

No container was restarted, recreated or rebuilt into service. The rebuilt image sits under the
`gmail-agent-runtime:local` tag but nothing runs it yet: `restart: unless-stopped` restarts a
container on its own image id, so the new image is picked up only by an explicit recreate.

## Canonical target is still not available

The reported top-up is not visible to the configured credential — `GET /user/balance` returns
`is_available: false` with a zero balance for key fingerprint `72a31b22fa33`. Evidence in
`DEEPSEEK_DIRECT_BILLING_CHECK.json`.

So the system currently has **no working DeepSeek tier on either host**: canonical is unfunded,
and the qualified bridge is switched off by choice. Structured stages therefore fall through to
the Groq router tier, which is healthy — the same state as before this task.

## If the bridge is wanted after all

Two steps, both reversible:

```bash
# 1. gmail-agent/.env.local-vps
AI_OS_PRIMARY_PROVIDER=deepseek_nvidia

# 2. recreate onto the already-built image, then prove parity and topology
docker compose --env-file .env.vps -f docker-compose.local-vps.yml \
  --profile api --profile worker up -d --force-recreate --no-deps
```

Then the outstanding proofs from the activation contract still apply: host↔container source
parity, active topology from the running container, and exactly one production-path smoke that
must be served by `deepseek_nvidia` without Groq rescue.
