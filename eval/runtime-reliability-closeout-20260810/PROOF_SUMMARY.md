# Proof summary — Runtime Reliability Closeout 01

Every claim below is backed by a named artifact, gate, test, or captured log line. Nothing here
rests on inspection alone.

## Result

```text
RUNTIME_RELIABILITY_CLOSEOUT = BLOCKED_OPERATOR_ACTION
```

Engineering complete; two credential/billing items require the operator.

## Per-item evidence

| item | verdict | how it was proven |
|---|---|---|
| **CL-01** planner timeout semantics | `FIX_REQUIRED` → **FIXED** | SDK behaviour read from the running container (`openai 1.109.1`, `max_retries=2`, `for retries_taken in range(max_retries + 1)`, timeout per `_build_request`) → inner ~90s+ vs outer 45s. 10 tests incl. AST-level "no executor" and an orphan-work counter. `CL01_OPENAI_AGENT_TIMEOUT_PROOF.md` |
| **CL-02** Anthropic orphan work | **FIXED** | `Executor.__exit__` source shows `shutdown(wait=True)` — the hard timeout bounded nothing. 11 fault-injection tests (fast success, fast failure, timeout, deadline exhaustion, structured terminal, no orphan, semaphore not leaked). `CL02_ANTHROPIC_ORPHAN_FIX.md` |
| **CL-03** runner reproducibility | **REPRODUCIBLE** | Harness copied byte-identically to tracked `scripts/fresh38/`; hashes match the existing pins; wrapper defaults there; live run logged `runner_provenance=VERIFIED … path=…\scripts\fresh38\run_recovery_pf.py`. `FRESH38_RUNNER_PROVENANCE.md` |
| **CL-04** SUT fingerprint completeness | **BLIND SPOT CLOSED** | Derived 361-file subtree replaces a 25-file curated list. Gate `FRESH38_SUT_FINGERPRINT` PASS, including the decisive case: changing a dependency no curated list ever mentioned changes the manifest. `FRESH38_SUT_FINGERPRINT_PROOF.md` |
| **CL-05** provider pool | **UNDERSTOOD + product defect FIXED** | Read-only smoke call per slot, no secrets. Found a proven CODE_DEFECT: `auth` was chain-terminal, so a rotated dead key aborted ~1 call in 4 before any healthy key. 9 tests + live confirmation. `PROVIDER_POOL_TRIAGE.md/.json` |
| **CL-06** 26 vs 116 | **RECONCILED** | Two disjoint inventories in the same lock; overlap computed = 0. No artifact byte changed; verifier still PASS. `PRE_FIX_LOCK_COUNT_RECONCILIATION.md` |

## Tests and gates

```text
targeted closeout suites   124 passed, 0 failed        TARGETED_TESTS.log
Gate A                     2474 passed, 15 skipped,
                           24 subtests, 0 failed       GATE_A.log
FRESH38_SUT_FINGERPRINT    PASS
FRESH38_REUSE_GATE         PASS
PRE_FIX_BASELINE_LOCK      PASS  (re-verified after every run)
```

Gate A grew from 2444 → 2474 (+30 tests) with zero failures.

## Runtime

```text
image            sha256:a7d97907ee67d10696dd54f219efb42dae5832ff1294feb6375b787f4a23c2df
parity           12 changed files x 2 containers, 0 mismatches   HOST_CONTAINER_PARITY.json
worker           running, restart_count 0
```

## Live measurement

```text
focused proof   7/7 first-attempt valid   (6 former failures + NEW-05)
full Fresh38    38/38 = 100.00%           new frozen SUT, new OutDir, -NoReuse
```

```text
PRE_FIX        32/38 =  84.21%
POST_FIX       38/38 = 100.00%
POST_CLOSEOUT  38/38 = 100.00%
```

Three separate frozen SUTs, zero artifact reuse, no external retry-to-green anywhere.

### The strongest single piece of evidence

`MI-01`, `business_reasoning`, captured live during the closeout run:

```text
openai_chat  quota_exhausted  487 ms      <- primary out of credits
groq         rate_limit       286 ms
groq         rate_limit       274 ms
groq         rate_limit       ...
groq         auth             <- the rejected key, position 5
cerebras     skipped (unconfigured)       <- REACHED: the chain continued past auth

terminal_failure_reason  provider_chain_exhausted
elapsed                  24048 ms of a 180000 ms budget
```

Under the previous semantics the router would have raised at position 5 and never recorded
`cerebras`. This is the CL-05 fix running against a genuinely rejected credential in production
configuration — and the attribution is exact: chain exhaustion, not a timeout, with 87% of the
budget unspent.

Seven of the 38 cases hit that rejected credential. All seven still produced valid captures.

## What is deliberately *not* claimed

- Not proven: that the system cannot fail. Two clean 38-case runs bound the failure rate loosely.
- Not proven live: the Anthropic path (CL-02). `anthropic_api_key` is UNSET, so there is nothing to
  prove against; determinism plus the configuration check is the honest limit.
- Not measured here: capability or answer quality. No judge, no v5 scoring was run.
