# Closeout Fresh38 — first-attempt reliability on the CL-01..CL-06 SUT

```text
CLOSEOUT_FIRST_ATTEMPT_RELIABILITY = 38/38 = 100.00%
FIRST_ATTEMPT_FAILURES             = 0
```

Ledger: `CLOSEOUT_FIRST_ATTEMPT_LEDGER.json` / `.csv`.
Out-dir: `C:\top-code-session-scratch\fresh38-closeout-20260810T175305Z`.
Experiment manifest: `9e1d641aede65104…`.

All 38 cases run once as `FIRST_ATTEMPT`, `-NoReuse`, new out-dir, no retry-to-green. The ledger
builder re-derived the result from the artifacts and reported
`provenance: every artifact bound to this experiment manifest, all FIRST_ATTEMPT`.

## The three measurements, side by side

| | SUT | first-attempt | failures |
|---|---|---|---|
| PRE-FIX | `fresh38-canonical-clean-20260810T011858Z` | **32/38 = 84.21%** | 6 |
| POST-FIX (hardening) | `fresh38-postfix-20260810T064731Z` | **38/38 = 100.00%** | 0 |
| POST-CLOSEOUT (this) | `fresh38-closeout-20260810T175305Z` | **38/38 = 100.00%** | 0 |

Three separate frozen SUTs, three separate out-dirs, zero artifact reuse between any of them,
and no external retry anywhere. The PRE-FIX lock was re-verified again after this run:
`PRE_FIX_BASELINE_LOCK: PASS`, still 32/38, all 26 repo-preserved files byte-unchanged.

`INTAKE_LLM_TIMEOUT` appears in **0** of the 38 stderr streams.

## The CL-05 fix, exercised live

`LLM_STAGE_BUDGET_FAILURE` fired in **7 of 38** cases, and every one of those cases still produced
a valid capture:

```text
DEC-01  DOC-03  MI-01  MI-02  MI-04  NEW-01  SVC-03      -> 7 cases, all valid_capture=True
```

Each of them hit the rejected Groq credential. `MI-01`, `business_reasoning` stage:

```text
openai_chat   failed  quota_exhausted   487 ms
groq          failed  rate_limit        286 ms
groq          failed  rate_limit        274 ms
groq          failed  rate_limit        ...
groq          failed  auth              <- the rejected key, at position 5
cerebras      skipped unconfigured (missing CEREBRAS_API_KEY)

terminal_failure_reason : provider_chain_exhausted
elapsed / budget        : 24048 ms of 180000 ms
```

Two things are visible here that were not possible before:

1. **The chain continued past the `auth` failure.** Under the previous semantics `auth` was
   chain-terminal, so the router would have raised at position 5 and `cerebras` would never have
   been recorded. This is the CL-05 fix running against a real rejected credential, not a stub.
2. **The failure is correctly attributed.** `provider_chain_exhausted`, with 156 s of the 180 s
   budget still unspent — so it is unambiguously *not* a timeout. The whole exhausted chain cost
   24 s, because every failure returned in 274–487 ms.

In this particular case the other three Groq keys happened to be rate-limited at that moment, so
the chain legitimately ran out of providers. Had any of them been healthy — the far more common
arrangement — the call would have recovered instead of aborting at the dead key, which is the
one-call-in-four loss the fix removes.

## What this run also says about the pool

Three Groq keys returning `rate_limit` inside one stage, plus a primary that is out of credits,
is a pool under real pressure. The runtime absorbed it and no case failed, but that is resilience
compensating for capacity, not capacity being adequate. It reinforces the two
`OPERATOR_ACTION_REQUIRED` items in `PROVIDER_POOL_TRIAGE.md` rather than softening them.

## Reading this honestly

`38/38` twice, on two different SUTs, is a stronger signal than one clean run — but it is still
two runs of 38 cases against a live external provider chain, and it bounds the failure rate
loosely. It does not prove the system cannot fail. What it does show is that the failure *class*
measured pre-fix (an envelope expiring before its own retry/fallback could act) did not reappear,
including on a SUT where the provider pool was actively degraded during the run.
