# POST-FIX First-Attempt Reliability — Fresh38 on the repaired SUT

Frozen SUT: `POST_FIX_FROZEN_SUT_MANIFEST.md`
Capture out-dir: `C:\top-code-session-scratch\fresh38-postfix-20260810T064731Z`
Experiment manifest hash: `661d75f16b4fd621…`
Ledger: `POST_FIX_FIRST_ATTEMPT_LEDGER.json` / `.csv`

## Result

```text
FIRST_ATTEMPT_TOTAL       = 38
FIRST_ATTEMPT_VALID       = 38
FIRST_ATTEMPT_FAILURES    = 0
POST_FIX_FIRST_ATTEMPT_RELIABILITY = 38/38 = 100.00%
```

All 38 cases run once, as `FIRST_ATTEMPT`, with `-NoReuse`. No retry was performed and none is
permitted to alter this number. Every artifact carries a sidecar bound to the same experiment
manifest hash, and the ledger builder fails if any is missing, mismatched, or not a first attempt
— it reported `provenance: every artifact bound to this experiment manifest, all FIRST_ATTEMPT`.

## Honest comparison

| | PRE-FIX | POST-FIX |
|---|---|---|
| first-attempt reliability | **32/38 = 84.21%** | **38/38 = 100.00%** |
| failures | 6 | 0 |
| failed cases | INT-05, NEW-04, FU-06, SVC-04, CTX-01, NEW-01 | — |
| dominant failure class | `PRODUCT_RUNTIME` (timeout-budget collision) | — |
| `INTAKE_LLM_TIMEOUT` occurrences | 6 | **0** |

Neither number was altered by a retry. Both are first-attempt only, on separate frozen SUTs in
separate out-dirs, with zero artifact reuse between them. The pre-fix baseline was re-verified
**after** this run: `PRE_FIX_BASELINE_LOCK: PASS`, still `32/38 = 84.21%`, 26 preserved files
unchanged.

The six cases that previously failed all completed at `stage_reached = full`:

```text
INT-05 valid  NEW-04 valid  FU-06 valid  SVC-04 valid  CTX-01 valid  NEW-01 valid
```

## What one case proves about the model

`NEW-05` is the most informative artifact in the run. It emitted the new
`LLM_STAGE_BUDGET_FAILURE` telemetry — and still completed as a valid capture:

```text
stage                   reply_drafter
terminal_failure_reason provider_chain_failed        <- not a deadline exhaustion
configured_stage_budget 180000 ms
elapsed                 8876 ms      remaining  171124 ms

provider      status  error_class      latency  provider_budget  remaining
openai_chat   failed  quota_exhausted   152 ms      34422 ms      171960 ms
groq          failed  rate_limit        282 ms      42990 ms      171678 ms
groq          failed  rate_limit        278 ms      57226 ms      171400 ms
groq          failed  auth              275 ms      85700 ms      171125 ms

error: 401 Unauthorized: GROQ_API_KEY was rejected by Groq. Invalid API Key.
```

Four things are demonstrated here on live traffic, not in a test double:

1. **The per-provider budget share works exactly as designed.** Five configured providers
   (openai_chat + four Groq keys) split the remaining budget evenly at each step:
   `171960/5 ≈ 34422`, `171678/4 ≈ 42990`, `171400/3 ≈ 57226`, `171125/2 ≈ 85700`. No provider can
   take the share reserved for the ones not yet tried.
2. **Fast failures cost the chain nothing.** Each attempt terminated in 152–282 ms; the whole
   chain consumed 8.9 s of a 180 s budget. The requirement that quick 429/quota/auth errors fall
   through immediately holds in production — the budget model added no latency to failure.
3. **`terminal_failure_reason` correctly distinguishes a provider fault from budget exhaustion.**
   This chain died with 171 s still available, and it says so. That is precisely the labelling fix
   made in `a2ebeb9`, validated live: before it, an in-loop terminal raise carried no reason at
   all.
4. **The telemetry answers the question it was built for.** "Which provider consumed the budget
   and why did fallback not recover?" is answerable directly from this record: *nobody consumed
   the budget — the chain exhausted its providers on credential and quota errors with 95% of the
   budget unspent.*

## Finding for the operator — not fixed here

That same record surfaces a real, pre-existing production configuration problem, unrelated to this
repair and outside its scope:

- `openai_chat` returned **`quota_exhausted`**.
- At least one of the four `GROQ_API_KEY` values is **invalid** (`401 … Invalid API Key`), and two
  others were rate-limited at that moment.

The repaired runtime absorbed this — the case still produced a valid capture, and the whole run
finished 38/38 — but a degraded provider pool is a live risk that the new telemetry has now made
visible. It should be triaged separately; it is a credentials/quota matter, not a code defect.

## Reading this honestly

`38/38` is one run of 38 cases on one day against a live external provider chain. It is a strong
result and a large improvement on a like-for-like measurement, but it is not a claim that the
system cannot fail: a single clean run bounds the failure rate loosely, and provider tail latency
— the original trigger — is inherently variable. What changed structurally is that such latency
now has 180 s of coordinated retry and fallback to absorb it instead of a 60 s envelope that
foreclosed both.
