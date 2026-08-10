# Phase A + B — First-Attempt Reliability Ledger

Frozen SUT: `FROZEN_SUT_MANIFEST.json` (unchanged throughout Phase A). Capture out-dir:
`C:\top-code-session-scratch\fresh38-canonical-clean-20260810T011858Z`. Full per-case ledger:
`FIRST_ATTEMPT_LEDGER.json` / `.csv` in this directory.

## Methodology note

Fresh38 previously asked only "can we eventually get 38 scorable artifacts?", where a successful
retry silently erased a real first-attempt production failure. This run separates that question
into three dimensions per operator instruction; **only dimension 1 is reported here**:

1. `FIRST_ATTEMPT_RELIABILITY` — does the system get through a case correctly on real first
   contact? (this report)
2. `CAPABILITY` — among valid captures, is the reasoning/output actually good? (not evaluated yet)
3. `RECOVERY` — for a first-attempt failure, does an identical frozen system recover on retry?
   (not evaluated yet — awaiting authorization)

No `CLEAN_PASS`/`CAPABILITY` number is reported or implied here.

## Execution record

- First 17 cases (`INT-01`…`FU-07`) captured under background task `by6cmcob3`.
- `SVC-01`'s first execution under that task was operator-interrupted mid-flight (no artifact
  written) and is **excluded** — not a success, not a failure.
- Remaining 21 cases (`SVC-01`…`NEW-01`, i.e. every case without a completed artifact) captured
  in a single pass under background task `b180423nr`, using the exact same `OutDir` and frozen
  manifest, zero SUT/runner/provider/config changes between the two.
- Every case in the corpus now has **exactly one** completed first-attempt artifact.

## Result

```text
FIRST_ATTEMPT_TOTAL      = 38
FIRST_ATTEMPT_VALID      = 32
FIRST_ATTEMPT_FAILURES   = 6
FIRST_ATTEMPT_RELIABILITY = 32/38 = 84.21%
```

### Failure breakdown by mechanical class

**Revised after deep investigation — see `TIMEOUT_ENVELOPE_INVESTIGATION.md` for full proof.**
Initial pass classified all 6 as `PROVIDER_AVAILABILITY`; operator-requested investigation of the
timeout envelope and provider chain found a mechanical, code-level cause and corrected this to
`PRODUCT_RUNTIME`.

```text
HARNESS_ONLY          = 0
TRANSPORT_ONLY         = 0
PROVIDER_AVAILABILITY  = 0
PRODUCT_RUNTIME        = 6
MODEL_OUTPUT_INVALID   = 0
CONTRACT_VALIDATION    = 0
UNKNOWN                = 0
```

### Failed cases

| case_id | stage_reached | exact error | production_would_fail |
|---|---|---|---|
| INT-05 | intake_reasoning_error | `INTAKE_LLM_TIMEOUT` (timeout_sec=60) | true |
| NEW-04 | intake_reasoning_error | `INTAKE_LLM_TIMEOUT` (timeout_sec=60) | true |
| FU-06 | intake_reasoning_error | `INTAKE_LLM_TIMEOUT` (timeout_sec=60) | true |
| SVC-04 | intake_reasoning_error | `INTAKE_LLM_TIMEOUT` (timeout_sec=60) | true |
| CTX-01 | intake_reasoning_error | `INTAKE_LLM_TIMEOUT` (timeout_sec=60) | true |
| NEW-01 | intake_reasoning_error | `INTAKE_LLM_TIMEOUT` (timeout_sec=60) | true |

All six are byte-identical in mechanism: real production code
(`gmail_intake.run_intake_reasoning` -> `_run_llm_with_timeout`,
`gmail-agent/tools/gmail_audit/gmail_intake.py:2453-2496`), a hard
`ThreadPoolExecutor.submit(...).result(timeout=60)` ceiling around the real
`run_central_structured_stage` intake-reasoning LLM call, zero response received within the full
60-second window (not a slow-but-completing response — a complete non-response), then a correct,
honest `parity_error=production_faithful_intake_invalid` from the frozen runner's parity contract
(it refuses to substitute a placeholder). Producer: the LLM provider chain behind the
`intake_llm`-lane central structured stage (`llm_backend=openai_chat`, per the frozen manifest).
Consumer: `compute_real_intake_result()` in the frozen recovery runner.

Classified `PRODUCT_RUNTIME` for all six (revised from an initial `PROVIDER_AVAILABILITY` pass):
the outer 60-second hard-kill in `_run_llm_with_timeout` is numerically identical to, and starts
before, the inner per-HTTP-attempt timeout (`settings.http_timeout=60`) used by the very
retry/fallback mechanism it wraps (4 attempts x 60s per provider, across `openai_chat` -> `groq`
[4 keys] -> `cerebras`). That inner resilience is structurally unreachable within the outer
envelope — the kill fires at or before the first HTTP attempt's own timeout could ever surface,
so the fallback to `groq` (proven reliable elsewhere in this same run) never gets a chance.
`signal_extractor.run_signal_extraction`, which calls the identical provider chain with **no**
outer envelope at all, succeeded 38/38 times in this run, including on all 6 cases that failed at
the intake-reasoning step — strong evidence the provider chain itself is not systemically broken.
A live preflight smoke call through the same chain succeeded in 5.6s minutes before this run
started, and 32/38 other real calls this run completed normally — the trigger (occasional
first-attempt provider latency) is ordinary; the reason it became a hard, unrecoverable failure is
the product's own timeout-budget design. Full mechanical proof: `TIMEOUT_ENVELOPE_INVESTIGATION.md`.

Every failure would occur identically against real production traffic today: same function, same
hard-coded 60s constant, same provider chain, same live configuration.

## What happens next (not started)

Per operator instruction, Phase C (recovery experiment: one controlled recovery attempt per
first-attempt failure, under the identical frozen SUT) and Phase D (capability dataset + judge +
v5 rescore) are **not started**. Awaiting operator authorization.
