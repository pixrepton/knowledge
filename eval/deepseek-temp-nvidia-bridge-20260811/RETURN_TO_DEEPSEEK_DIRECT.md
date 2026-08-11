# Return to DeepSeek Direct — runbook

`deepseek_direct` is the canonical target. This is the only sanctioned path back. Nothing here
was executed as part of DEEPSEEK-TEMP-BRIDGE-01.

## Preconditions

The bridge changed configuration only. DeepSeek Direct's credentials, base URL and model were
never modified or overwritten, so returning is a configuration switch, not a rebuild.

## Steps

**1. Fund the DeepSeek Direct account**

Operator action. Nothing in the repo can do this.

**2. Tiny health smoke — one call, cost-guarded**

```bash
python scripts/qualify_deepseek_host.py --host deepseek_direct --out /tmp/direct_health.json
```

Stops after a single smoke call if the account is still unfunded. Expect `http=200` and a
non-empty `content_len`. While unfunded it reports `error_class=quota_exhausted`,
`"Insufficient Balance"`.

**3. Switch the primary provider back**

In `gmail-agent/.env.local-vps`:

```diff
- AI_OS_PRIMARY_PROVIDER=deepseek_nvidia
+ AI_OS_PRIMARY_PROVIDER=deepseek_direct
```

Or simply remove the line — `deepseek_direct` is the default. Then restart the runtime
containers; the env file is mounted, so no image rebuild is needed:

```bash
docker restart gmail-agent-nodeb-api gmail-agent-vps-gmail-agent-worker-1
```

**4. Verify the topology**

```bash
docker exec gmail-agent-nodeb-api python -c "
import sys; sys.path.insert(0,'/app/tools/gmail_audit')
from config import load_settings
from groq_client import resolve_deepseek_host
from central_llm_stage import primary_llm_provider
s = load_settings(require_groq=False, require_google=False)
h = resolve_deepseek_host(s)
print('host', h.host, '| provider', h.provider, '| role', h.role, '| model', h.model)
print('primary_llm_provider', primary_llm_provider(s))
"
```

Expect `host deepseek_direct | provider deepseek | role CANONICAL_TARGET`. Also re-run the
provider pool triage and confirm no knowingly-invalid credential is in the active chain:

```bash
docker exec gmail-agent-nodeb-api python /tmp/provider_pool_triage.py
```

**5. Freeze a NEW SUT**

New manifest, new out-dir. Do not reuse any bridge-era artifact — a capture produced on
`deepseek_nvidia` describes a different provider and is marked `TEMP_PROVIDER_CAPABILITY_SIGNAL`.

**6. Run the final canonical Fresh38**

38 cases, one first attempt each, `-NoReuse`, new out-dir, no external retry-to-green.

**7. Understanding judge**

**8. v5 rescore**

**9. Establish the final Capability baseline**

Only now. `FINAL_CAPABILITY_SUT_FREEZE` stays `HOLD` until steps 1–6 are green on
`deepseek_direct`.

## What to remove afterwards

Once canonical mode is restored and verified, the bridge can be retired without code changes:

- drop `AI_OS_PRIMARY_PROVIDER` (or leave it at `deepseek_direct`);
- optionally clear `DEEPSEEK_NVIDIA_API_KEY`;
- optionally clear `DEEPSEEK_NVIDIA_MODEL`;
- update `gmail-agent/tools/gmail_audit/provider_roles.json` to mark `deepseek_nvidia` as
  retired, and note the date.

The bridge code can stay: it is inert unless explicitly selected, and it is the mechanism that
makes the next host outage a configuration switch rather than another runtime rebuild.

## Before activating the bridge (if that path is taken first)

```text
DEEPSEEK_NVIDIA_API_KEY = <key>
DEEPSEEK_NVIDIA_MODEL   = <exact NIM id for the intended DeepSeek model>   REQUIRED
```

then one smoke -> up to six qualification calls -> only on PASS set
`AI_OS_PRIMARY_PROVIDER=deepseek_nvidia`. The model id has no default: the bridge changes the
host, not the model.

## What must NOT happen

- Do not treat any bridge-era benchmark as a canonical Capability baseline.
- Do not make `deepseek_nvidia` the default.
- Do not "fix" a DeepSeek Direct billing failure by switching hosts automatically — the switch is
  operator-controlled by design, so that a measurement can never silently change provider.
- Do not let the bridge pick a model. Changing host *and* model together makes a bridge result
  impossible to compare with a canonical one.
