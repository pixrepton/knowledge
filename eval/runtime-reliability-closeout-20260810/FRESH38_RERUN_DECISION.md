# Fresh38 rerun decision

```text
DECISION = REQUIRED
```

Not a precaution — a classification result.

## Classifying the closeout changes

| change | file(s) | class |
|---|---|---|
| CL-01 planner deadline model | `agent_runtime/openai_agent_client.py` | **A — ACTIVE_FRESH38_PRODUCT_SUT_CHANGE** |
| CL-05 router auth chain-termination | `llm_provider_router.py` | **A — ACTIVE_FRESH38_PRODUCT_SUT_CHANGE** |
| CL-02 Anthropic path | `central_llm_stage.py` | B — INACTIVE_CONFIG_GATED (plus one active-path edge, below) |
| CL-03 tracked canonical runner | `scripts/fresh38/**`, provenance json | C — MEASUREMENT_ONLY (byte-identical runner) |
| CL-04 derived SUT fingerprint + single staged sync | `run_fresh38_case_batch.ps1` | C — MEASUREMENT_ONLY |
| CL-06 reconciliation, closeout artifacts | `knowledge/**` | D — DOCS/PROVENANCE_ONLY |

Two changes are class **A**, so `NO_NEW_FULL_FRESH38_REQUIRED` cannot be claimed.

## Why those two are genuinely on the capture path

Not assumed — read from the runner:

```text
scripts/fresh38/run_recovery_pf.py imports:
    from agent_runtime.graph import AgentGraphEngine
    from agent_runtime.openai_agent_client import OpenAIToolPlanner
    ...13 references to the agent runtime in total
```

So the capture drives the agent planner directly. `openai_agent_client` is executed, not merely
linked.

The router change is chain-wide: every structured stage goes through `LLMRouter.run()`, and the
live pool contains a credential that returns `401`. The POST-FIX run's own `NEW-05` artifact
records a `groq` `auth` failure, so this is not a hypothetical path — the old code would have
aborted that chain, the new code continues it. Behaviour on the measured path genuinely differs.

## Why CL-02 is class B but not purely so

`_call_with_retry` and `_anthropic_client` are reachable only when `anthropic_configured(settings)`
is true, and `anthropic_api_key` is UNSET in this deployment — so that code cannot execute during
a capture. However the edit touched `central_llm_stage.py`, which *is* on the active path, so the
file's identity changed even though the executed behaviour did not. The derived SUT fingerprint
(CL-04) correctly treats that as a new SUT, which is the conservative and correct outcome: a
changed file invalidates the manifest whether or not the changed branch runs.

## Sequence actually performed

```text
1. Gate A on the final code            2474 passed, 15 skipped, 24 subtests, 0 failed
2. Root gates                          FRESH38_SUT_FINGERPRINT PASS, FRESH38_REUSE_GATE PASS
3. Commit                              gmail-agent 4b9bb7c, root f436499
4. Rebuild + recreate both containers   image a7d97907…
5. Host<->container parity              12 changed files x 2 containers, 0 mismatches
6. FOCUSED LIVE PROOF                   7 cases, one first attempt each, -NoReuse
7. Full Fresh38                         38 cases, one first attempt each, -NoReuse, new OutDir
```

### Step 6 — focused live proof

Chosen to hit the changed paths: the six cases that failed pre-fix (full pipeline, agent planner)
plus `NEW-05`, the case whose POST-FIX artifact recorded the live `quota_exhausted` + `auth`
provider sequence that the CL-05 fix changes.

```text
INT-05 OK   NEW-04 OK   FU-06 OK   SVC-04 OK   CTX-01 OK   NEW-01 OK   NEW-05 OK
DONE ok=7 failed=0 attempt=FIRST_ATTEMPT#1
out: C:\top-code-session-scratch\closeout-focused-proof-20260810T173717Z
```

Green, so the full run proceeded. No retry-to-green: each case ran once.

### Step 7 — the canonical rerun

New frozen SUT, new OutDir, `-NoReuse`, all 38 as `FIRST_ATTEMPT`. No judge, no v5 scoring — this
run measures runtime reliability only.

```text
out_dir                   C:\top-code-session-scratch\fresh38-closeout-20260810T175305Z
experiment_manifest_hash  9e1d641aede65104f1a3f2bafa4f89dba63ec475fb6694e3a7b8fff97502d86c
runner_provenance         VERIFIED  8c2f3ddc…  from scripts/fresh38/run_recovery_pf.py  (tracked)
sut_source_files          361  (root tools/gmail_audit; excluded tests,__pycache__,runs,data,
                                .pytest_cache,scripts,.venv)
root_head                 f436499fa45237c730bdf10e6bdc9f962989b9bf
gmail_agent_head          4b9bb7c72205c269ee12dfa95d8ea55cb2b81efc
node_b_image              sha256:a7d97907ee67d10696dd54f219efb42dae5832ff1294feb6375b787f4a23c2df
```

Result: see `CLOSEOUT_FRESH38_RESULT.md`.

## Standing rule for next time

The earlier POST-FIX number is not discarded — `32/38 → 38/38` remains the proven improvement of
the hardening phase, on its own frozen SUT. This rerun measures a *different* SUT. Both are
first-attempt-only, neither was reached by retry, and neither may be edited to match the other.
