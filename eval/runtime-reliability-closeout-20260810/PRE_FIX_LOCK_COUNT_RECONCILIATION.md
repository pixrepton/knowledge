# CL-06 — `26 files` vs `116 files`: reconciliation

## The apparent contradiction

The hardening report states both:

```text
PRE_FIX_BASELINE_LOCK: PASS, 26 files
SHA256 of all 116 files from the volatile capture directory plus every report file
```

## Resolution: neither is a typo, and neither is wrong

They count **two disjoint sets**. `PRE_FIX_BASELINE_LOCK.json` has two independent inventories,
and the verifier prints one of each:

| number | key in the lock | what it counts | where those bytes live |
|---|---|---|---|
| **26** | `preserved_in_repo.files` | files committed into the repository and re-hashed on every verification | `knowledge/eval/fresh38-canonical-clean-20260810T011858Z/**` |
| **116** | `volatile_capture_out_dir.files` | files that existed in the session-scratch capture out-dir, recorded as hashes only | `C:\top-code-session-scratch\fresh38-canonical-clean-20260810T011858Z\` |

Mechanically confirmed:

```text
preserved_in_repo.file_count    = 26   (actual keys: 26)
volatile_capture_out_dir.count  = 116  (actual keys: 116)
overlap between the two sets    = 0
```

### The 26 — durable, byte-verified

```text
 6  report files          FIRST_ATTEMPT_LEDGER.{json,csv}, FROZEN_SUT_MANIFEST.{json,md},
                          PHASE_A_B_REPORT.md, TIMEOUT_ENVELOPE_INVESTIGATION.md
19  raw failure evidence  raw-first-attempt-failures/: the six failed cases
                          (6 x .json + 6 x -stdout.txt + 6 x -stderr.txt) + capture.log
 1  verifier              verify_pre_fix_lock.py
──
26
```

### The 116 — volatile, hash-only

```text
38  one-CASE .json artifacts
38  one-CASE -stdout.txt
38  one-CASE -stderr.txt
 1  capture.log
 1  fresh38-partial-results.json
───
116
```

## Why they differ by design

Session scratch is not durable, and copying all 116 files (5.4 MB, including a 3.2 MB
`fresh38-partial-results.json`) into the repository would have been disproportionate. The
operator instruction asked to preserve *the six failed one-CASE artifacts, their stdout/stderr,
and `capture.log`* — which is exactly the 19 raw files inside the 26.

So the lock provides two different guarantees, deliberately:

- for the **26**: full byte-level immutability — the verifier re-hashes each file and fails on any
  drift;
- for the **116**: a tamper-evident record of what the volatile directory contained at freeze
  time. If that scratch directory still exists it can be checked against the lock; once it is
  cleaned, the hashes remain as the durable statement of what was there.

## Single unambiguous definition

From here on, in this and any later report:

```text
PRE_FIX_PRESERVED_FILES = 26    files committed to the repo and byte-verified on every run
PRE_FIX_CAPTURE_FILES   = 116   files recorded by hash from the volatile capture out-dir
```

Neither number is the reliability measurement. That remains, unchanged:

```text
PRE_FIX_FIRST_ATTEMPT_RELIABILITY = 32/38 = 84.21%
```

## No artifact was modified

This reconciliation is documentation only. `PRE_FIX_BASELINE_LOCK.json` and
`verify_pre_fix_lock.py` are themselves inside the 26 locked files: editing either would break
the very hash chain they exist to protect. Verified after writing this document:

```text
PRE_FIX_BASELINE_LOCK: PASS
  PRE_FIX_FIRST_ATTEMPT_RELIABILITY = 32/38 = 84.21%
  failed cases                      = INT-05, NEW-04, FU-06, SVC-04, CTX-01, NEW-01
  preserved files verified          = 26
  volatile capture files hashed     = 116
```

The verifier's own output already printed both numbers side by side with distinct labels; what
was missing was a statement that they describe different sets. That statement is this document.
