# Six-Case Live First-Attempt Proof — did the failure class disappear?

Purpose, and its limit: this is **not** the canonical post-fix score. It answers exactly one
question before spending a full 38-case run — *did the runtime class that produced the six
pre-fix failures disappear?*

## Method

The six cases that failed in the pre-fix run, run once each on the repaired SUT.

```powershell
scripts/run_fresh38_case_batch.ps1 `
  -CaseIds "INT-05,NEW-04,FU-06,SVC-04,CTX-01,NEW-01" `
  -OutDir  "C:\top-code-session-scratch\rt01-sixcase-proof-20260810T060646Z" `
  -AttemptType FIRST_ATTEMPT `
  -NoReuse
```

- **One first attempt each.** No external retry-to-green.
- `-NoReuse` refuses every cached artifact, so nothing could be inherited from an earlier run.
- Runner provenance verified against the tracked pin before the first case started.

## Result

```text
[08:06:59] START INT-05   [08:09:29] OK INT-05
[08:09:29] START NEW-04   [08:11:59] OK NEW-04
[08:11:59] START FU-06    [08:13:21] OK FU-06
[08:13:21] START SVC-04   [08:14:56] OK SVC-04
[08:14:56] START CTX-01   [08:16:45] OK CTX-01
[08:16:45] START NEW-01   [08:18:21] OK NEW-01
DONE ok=6 failed=0 attempt=FIRST_ATTEMPT#1
```

| case | first-attempt valid | parity_error | attempt_type | experiment_manifest_hash |
|---|---|---|---|---|
| INT-05 | yes | — | FIRST_ATTEMPT | `62a05a7b8c4c6019` |
| NEW-04 | yes | — | FIRST_ATTEMPT | `62a05a7b8c4c6019` |
| FU-06 | yes | — | FIRST_ATTEMPT | `62a05a7b8c4c6019` |
| SVC-04 | yes | — | FIRST_ATTEMPT | `62a05a7b8c4c6019` |
| CTX-01 | yes | — | FIRST_ATTEMPT | `62a05a7b8c4c6019` |
| NEW-01 | yes | — | FIRST_ATTEMPT | `62a05a7b8c4c6019` |

**6/6 first-attempt valid.** Zero `parity_error`. Zero `INTAKE_LLM_TIMEOUT` across all six
stderr streams — the log key that appeared in every one of these cases before the repair.

Every artifact is bound to the same experiment manifest hash, so all six describe one SUT.

## Reading this honestly

Six cases passing once does not establish a reliability rate; the sample is far too small and
these are not independent of the failure they were selected for. What it does establish is
negative and specific: the mechanism that made these six fail — an outer envelope expiring before
the provider chain's own retry and fallback could act — did not recur under conditions that
previously triggered it in 6 of 38 attempts.

That was the gate for proceeding to a full post-fix Fresh38. It passed, so the full run went
ahead. The canonical number is `POST_FIX_FIRST_ATTEMPT_RELIABILITY` in
`POST_FIX_FIRST_ATTEMPT_RESULT.md`, from a separate 38-case run under a new out-dir.

## Note on a prior aborted attempt

An earlier invocation of this proof failed with `ok=0 failed=6` in under one second. That was not
a product failure: `docker` was absent from the PATH of that shell, so nothing was provisioned or
executed. It did expose a genuine wrapper weakness — the script logged `synced <file>` for every
product file whose `docker cp` had actually failed, and still wrote an experiment manifest. That
is the same contamination class FIX-MEAS01 addresses, so the wrapper now aborts when docker is
unavailable, when any hot-sync `docker cp` returns non-zero, or when the container image id
cannot be resolved. The run above was executed after that fix.
