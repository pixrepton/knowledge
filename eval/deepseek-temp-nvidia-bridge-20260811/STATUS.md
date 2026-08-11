# DEEPSEEK-TEMP-BRIDGE-01 — status

```text
TEMP_BRIDGE_IMPLEMENTATION     = PASS
TEMP_BRIDGE_QUALIFICATION      = BLOCKED_OPERATOR_ACTION
TEMPORARY_ACTIVATION           = NOT_ACTIVE
TEMP_BRIDGE_RUNTIME_PROOF      = NOT_APPLICABLE   (nothing was activated)
CANONICAL_TARGET               = deepseek_direct  (unchanged)
FINAL_CAPABILITY_SUT_FREEZE    = HOLD
```

## Where things stand

The operator configured both required variables correctly. The bridge mechanism engaged exactly
as designed and resolved to `host=deepseek_nvidia role=TEMPORARY_BRIDGE
model=deepseek-ai/deepseek-v4-flash configured=True`.

Then the host answered the connectivity smoke with **HTTP 410**:

> The model `'deepseek-ai/deepseek-v4-flash'` has reached its end of life on
> 2026-08-07T09:00:00Z and is no longer available.

NVIDIA NIM retired that model id four days ago. Its catalog (101 models) offers
`deepseek-ai/deepseek-v4-flash-0731` — a dated snapshot of the same line — and nothing else in
the V4 Flash family.

Nothing was activated. `AI_OS_PRIMARY_PROVIDER` remains unset, so the resolver returns the
canonical host. Qualification did not reach PASS, so under §8 activation was not attempted.

## Why the obvious substitution was not made

`-0731` is very likely what the retired alias resolved to, and it is clearly the right candidate
to consider. But the canonical side is also an unversioned alias (`DEEPSEEK_MODEL=deepseek-v4-flash`),
and nothing observable here proves DeepSeek Direct still resolves it to `0731`. Pinning the bridge
to a snapshot the canonical target may have moved past would reintroduce this morning's defect —
provider and model changing together — with the difference invisible in the measurement.

That is an operator decision. Full reasoning in `NVIDIA_QUALIFICATION.md`.

## Provider state

```text
deepseek_direct   CANONICAL_TARGET    HTTP 402 Insufficient Balance    <- carried-in blocker
deepseek_nvidia   TEMPORARY_BRIDGE    configured; model retired upstream 2026-08-07 (HTTP 410)
groq              FALLBACK            3 healthy slots
cerebras          OPTIONAL_FALLBACK   unconfigured, skipped
openai_chat       NOT_IN_ACTIVE_CHAIN removed 2026-08-10
anthropic         UNCONFIGURED        skipped
```

## Second blocker on the activation path

The running `gmail-agent-runtime:local` image was built 2026-08-10T17:35Z and **does not contain
the bridge code** — `resolve_deepseek_host` is absent from the container's `groq_client.py`. Env
reaches the containers through a read-only bind mount, so a restart suffices for configuration,
but not for code. Activation needs an image rebuild from repo state.

Not a `docker cp`. Hand-syncing files into a running container is the blind spot CL-04 removed.

## Two qualifier defects found by this run, and fixed

1. **`error_message=""` for a response that explained itself.** The qualifier read only the
   OpenAI error envelope; NIM answers RFC 7807 `problem+json`. Now reads both.
2. **A retired model id cost a call to discover.** A free `GET /models` preflight now runs first
   and names the ids the host does offer. Proven at zero cost in `NVIDIA_CATALOG_PREFLIGHT.json`.

`410` and *end of life* / *no longer available* wording are now classified `model_unavailable`
and abort the run. 19 deterministic tests replay the captured body — no re-spend.

## Cost

```text
provider calls this task     : 2   (1 canonical 402 carried in, 1 bridge 410)
completion tokens            : 0
reasoning tokens             : 0
free listings (GET /models)  : 1   - no inference, no tokens
guard violated               : no
```

## Two operator actions, either of which unblocks work

1. **Fund DeepSeek Direct** — returns to canonical mode directly. `RETURN_TO_DEEPSEEK_DIRECT.md`.
2. **Authorize a pinned bridge model** — e.g. `DEEPSEEK_NVIDIA_MODEL=deepseek-ai/deepseek-v4-flash-0731`,
   then rebuild the runtime image and re-run qualification. Any result must then be read as
   *V4 Flash `0731` snapshot, NVIDIA-hosted*.

They are independent. (1) is the destination; (2) is a way to keep working on the way there.

## Capability rule, restated

`FINAL_CAPABILITY_SUT_FREEZE = HOLD` until `deepseek_direct` is restored and re-verified. If the
bridge is later activated, any benchmark produced during it is
`TEMP_PROVIDER_CAPABILITY_SIGNAL_ONLY = true` and is **not** a canonical Capability baseline.

`CAPABILITY-QUALIFICATION-20260809` remains BLOCKED. No Fresh38, judge or v5 rescore was run.
