# NVIDIA NIM bridge — qualification record

```text
TEMP_BRIDGE_QUALIFICATION = BLOCKED_OPERATOR_ACTION
TEMPORARY_ACTIVATION      = NOT_ACTIVE
```

The operator supplied both required variables and they are correct in form. Qualification still
could not proceed: **NVIDIA NIM retired the configured model id four days before this run.**

## Config verification (no secret values)

```text
DEEPSEEK_NVIDIA_API_KEY    configured=true   len=70   sha256_fp=4de5a91e46e1
DEEPSEEK_NVIDIA_MODEL      deepseek-ai/deepseek-v4-flash      <- exact match to the request
DEEPSEEK_NVIDIA_BASE_URL   https://integrate.api.nvidia.com/v1
AI_OS_PRIMARY_PROVIDER     <unset>  -> resolves to deepseek_direct (canonical, unchanged)
LLM_BACKEND                openai_chat                        <- untouched
```

Host resolution before any call: `host=deepseek_nvidia provider=deepseek_nvidia
role=TEMPORARY_BRIDGE model=deepseek-ai/deepseek-v4-flash configured=True`. The fail-closed
correction is satisfied — the bridge was fully configured and the mechanism engaged correctly.

## What the host answered

Connectivity smoke, one call, `max_tokens=8`:

```text
POST https://integrate.api.nvidia.com/v1/chat/completions   ->  HTTP 410 Gone   (922 ms)
content-type: application/problem+json

{"type":"about:blank","title":"Gone","status":410,
 "detail":"The model 'deepseek-ai/deepseek-v4-flash' has reached its end of life
           on 2026-08-07T09:00:00Z and is no longer available."}
```

The smoke gate stopped the run there. **No qualification call was attempted.** Zero completion
tokens, zero reasoning tokens.

## Catalog (free listing, no inference)

`GET /v1/models` -> HTTP 200, 101 models. Every DeepSeek entry NVIDIA NIM currently offers:

```text
deepseek-ai/deepseek-coder-6.7b-instruct
deepseek-ai/deepseek-v4-flash-0731
deepseek-ai/deepseek-v4-flash            <- NOT PRESENT (retired 2026-08-07)
```

## Why this is a stop, not a substitution

`deepseek-ai/deepseek-v4-flash-0731` is a dated snapshot of the same V4 Flash line, and it is
very likely what the retired unversioned alias used to resolve to. It is **not** R1, not Coder,
not GPT-OSS. So it is the obvious candidate — and it is still an operator decision, for a reason
worth stating precisely:

The canonical side is `DEEPSEEK_MODEL=deepseek-v4-flash` on DeepSeek Direct — also an
unversioned alias. Nothing observable from here proves that DeepSeek Direct's alias currently
resolves to the `0731` snapshot rather than a newer one. If it does not, pinning the bridge to
`0731` reintroduces exactly the defect corrected earlier today: provider and model changing
together, with the difference invisible in the resulting measurement.

Choosing it anyway may well be the right call. It is not mine to make silently.

## Two diagnostic defects found and fixed in the qualifier

Both were exposed by this run, and both are in the tooling, not the runtime.

**1. The failure looked unexplained when the host had explained it.** The qualifier read only the
OpenAI-style `{"error": {"message": ...}}` envelope, so a body that named its own cause verbatim
was recorded as `error_message=""` — the worst kind of diagnostic. `error_detail()` now reads
RFC 7807 `problem+json` (`detail`/`title`) as well. `NVIDIA_QUALIFICATION.json` is kept exactly as
first written, empty `error_message` included, as the evidence of that blind spot.

**2. A retired model id cost a call to discover.** A free `GET /models` preflight now runs before
any inference: if the configured id is absent from the catalog, the run stops with
`model_not_offered_by_host` and names the related ids the host does offer. Proven end-to-end in
`NVIDIA_CATALOG_PREFLIGHT.json` — same conclusion, zero calls, zero tokens.

`410`, and any body saying *end of life* / *no longer available*, is now classified
`model_unavailable` and added to the abort classes, so it can never consume six calls.

Replayed deterministically from the captured body in
`scripts/tests/test_deepseek_host_qualifier.py` (19 tests) — no re-spend.

## Operator decision required

Either:

**A. Fund DeepSeek Direct.** Returns to canonical mode; the bridge becomes unnecessary.
Runbook: `RETURN_TO_DEEPSEEK_DIRECT.md`.

**B. Authorize an explicit pinned bridge model.** If the `0731` snapshot is acceptable:

```text
DEEPSEEK_NVIDIA_MODEL=deepseek-ai/deepseek-v4-flash-0731
```

Then re-run qualification. Note that the result must then be read as *DeepSeek V4 Flash,
`0731` snapshot, NVIDIA-hosted* — not as an unqualified "same model, different host".

Do not set it to `deepseek-ai/deepseek-r1`, `deepseek-ai/deepseek-coder-6.7b-instruct`, or any
GPT-OSS id. The fail-closed design will accept whatever is configured; it cannot judge intent.

## Second blocker on the activation path

Independent of the model, activation is **not** a restart-only operation as the runbook assumed:

```text
image gmail-agent-runtime:local   built 2026-08-10T17:35:48Z
container /app/tools/gmail_audit/groq_client.py   sha256 026ec0b2ce3a…  70634 bytes
  resolve_deepseek_host present: False
repo      gmail-agent/tools/gmail_audit/groq_client.py  sha256 140684102d00…  77121 bytes
  resolve_deepseek_host present: True
```

The running image predates the bridge entirely. Env changes reach the containers through the
read-only `.env.local-vps` bind mount, so a restart suffices for *configuration* — but the bridge
**code** is baked into the image and is simply not there. Activation therefore requires rebuilding
`gmail-agent-runtime:local` from repo state first.

This must be a rebuild, not a `docker cp` of the changed files. Hand-syncing files into a running
container is precisely the measurement blind spot CL-04 removed; reintroducing it here would make
the activation unreproducible.
