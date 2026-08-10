# Takeover state — Runtime Reliability Closeout 01

Verified mechanically at closeout start, not assumed.

## Canonical numbers

```text
PRE_FIX_FIRST_ATTEMPT_RELIABILITY  = 32/38 =  84.21%
POST_FIX_FIRST_ATTEMPT_RELIABILITY = 38/38 = 100.00%
```

Confirmed at takeover by re-running the verifier and re-reading the ledger:

```text
PRE_FIX_BASELINE_LOCK: PASS
  PRE_FIX_FIRST_ATTEMPT_RELIABILITY = 32/38 = 84.21%
  failed cases                      = INT-05, NEW-04, FU-06, SVC-04, CTX-01, NEW-01
  preserved files verified          = 26
  volatile capture files hashed     = 116

POST ledger : 38/38 = 100.00% | failures: 0
              experiment_manifest_hash 661d75f16b4fd621…
              provenance problems: none
```

## Conditions that held for the POST-FIX proof

| condition | status |
|---|---|
| two separate frozen SUTs | yes — `fresh38-canonical-clean-20260810T011858Z` vs `fresh38-postfix-20260810T064731Z` |
| separate OutDirs | yes |
| zero artifact reuse between PRE and POST | yes — enforced by `-NoReuse` plus the manifest-hash gate, not by convention |
| zero external benchmark retry-to-green | yes — every case one `FIRST_ATTEMPT`, no retry pass |
| POST full 38 first attempts valid | yes — 38/38, all bound to one experiment manifest |
| PRE baseline lock preserved | yes — re-verified after the POST run, all 26 files byte-unchanged |

## Terminology, restated because it matters

```text
"no external retry"  !=  "no internal runtime retry"
```

The 38/38 figure means no *benchmark-level* retry was used to reach it: each case was captured
once and counted once. Production retry and provider fallback **inside** the LLM runtime are part
of the repaired SUT and are expected to fire — the entire FIX-RT01 repair exists to make them
reachable. `NEW-05` in the POST-FIX run is the clearest illustration: its `reply_drafter` stage
burned through four provider attempts and still produced a valid capture.

## Accepted as fixed — not reopened here

`RT01` intake timeout collision · stage-level deadline ownership · router remaining-budget
propagation · provider quota allocation · bounded cooldown/backoff · `terminal_failure_reason`
telemetry · `RT02` Daszek optional-dependency crash-loop · worker degraded/recovered behaviour ·
preclassifier bare-`prawnik` over-breadth · `FIRST_ATTEMPT`/`RECOVERY` artifact separation ·
Fresh38 manifest fingerprint · stale-artifact reuse rejection · `-NoReuse` · runner hash pinning.

These were re-run as regressions (they are inside Gate A and the targeted suites) but not
re-designed.

## Governance

The Runtime Reliability task `AIOS-RUNTIME-RELIABILITY-01` was still active
(`READY_TO_CLOSE`) and carried the provider-pool blocker that is literally CL-05, so it was
**resumed and adopted** rather than superseded by a new task, per the closeout instruction. Its
scope was extended with `knowledge:eval/runtime-reliability-closeout-20260810`; the six prior
commits were re-recorded on the checkpoint so the audit trail survived the re-declaration.

The Capability task `CAPABILITY-QUALIFICATION-20260809` remains `BLOCKED` with an open blocker and
was not touched. No second Capability task was created.

Foreign dirty state was not adopted and is unchanged: root (`CLAUDE.md`, two `rag_v2` scripts),
gmail-agent (`intake_shared_downstream.py`, five test files, `tests/test_preclassifier.py`),
knowledge (unrelated `eval/` directories).

## What this closeout set out to settle

```text
CL-01  openai_agent_client timeout semantics — verify, do not assume
CL-02  remaining Anthropic orphan-work defect
CL-03  canonical Fresh38 runner reproducibility
CL-04  Fresh38 SUT dependency/fingerprint completeness
CL-05  degraded live provider pool triage
CL-06  PRE_FIX lock count: 26 vs 116
```
