# CL-04 — SUT fingerprint: the manual blind spot, removed by construction

## The class of problem

The fingerprint only covered a hand-maintained list of ~25 files:

```text
file on the list changes         -> manifest hash changes   -> stale artifact rejected   GOOD
dependency NOT on the list changes -> manifest hash unchanged -> stale artifact ACCEPTED   BLIND SPOT
```

Adding "a few more files" does not close this — it moves the edge and leaves the same failure
mode. Only mechanical enumeration removes the class.

## Why the image-identity approach (Preferred A) does not suffice here

Container image digest + repo SHA would be enough **if** the container ran only what the image
contains. It does not: `run_fresh38_case_batch.ps1` deliberately hot-syncs host source into the
running container so a capture can test uncommitted work without a rebuild. The image digest
therefore describes what the container was *built* from, not what it is *running*.

The operator's condition for Preferred A was to prove hot-sync changes nothing beyond the
fingerprint. That cannot be proven, because changing the container is precisely what hot-sync is
for. So **Preferred B** — dependency closure over the source subtree — is the correct route.

## What is fingerprinted now

```text
SUT source root : gmail-agent/tools/gmail_audit
included        : every **/*.py under that root
excluded dirs   : tests, __pycache__, runs, data, .pytest_cache, scripts, .venv
count           : 361 files  (versus 25 curated)
```

The **same derived set** is both fingerprinted and hot-synced, so what is measured and what runs
cannot diverge — the two were previously independent, which is how they drifted.

Also in the fingerprint, unchanged from FIX-MEAS01: wrapper hash, runner hash, scoring hash,
corpus hash, container image id, mode.

### Determinism

- ordinal-sorted, forward-slash relative paths;
- content hashes only;
- no timestamps, no temp paths, no filesystem enumeration order, no generated files.

Asserted directly: two runs over an unchanged tree produce an identical hash, and the fingerprint
contains no temp path and no timestamp.

### Transfer

361 files are staged and copied in a **single** `docker cp`. Per-file copying would be slow, and a
partial failure mid-list is exactly the silent-drift failure this section removes. The wrapper
aborts if the copy returns non-zero.

## Proof

`scripts/tests/test_fresh38_sut_fingerprint.ps1` (docker stubbed, controlled source tree,
`-SutSourceRoot` override). Gate `FRESH38_SUT_FINGERPRINT`: **PASS**.

| # | requirement | assertion | result |
|---|---|---|---|
| 1 | deterministic | two runs, unchanged tree → identical hash | PASS |
| 1 | scope | top-level and nested product files fingerprinted, forward-slash paths | PASS |
| 1 | scope | `tests/` and `__pycache__/` excluded | PASS |
| 2 | known file | changing a file that was on the old curated list → hash changes | PASS |
| **3** | **blind spot** | **changing `obscure_runtime_dependency.py`, which no curated list ever mentioned → hash changes** | **PASS** |
| 4 | no over-invalidation | changing tests / bytecode / a `.txt` → hash unchanged | PASS |
| 5 | growth | adding a brand-new product module → hash changes, automatically | PASS |
| 6 | determinism | no temp paths, no timestamps in the fingerprint | PASS |

Row 3 is the one the curated list could never satisfy. Row 4 is its necessary counterpart: a
fingerprint that invalidates on everything would be useless in a different way.

Artifact reuse rejection on fingerprint mismatch remains covered by
`scripts/tests/test_fresh38_reuse_gate.ps1` (`REUSE_REJECT_SUT_MISMATCH`), gate
`FRESH38_REUSE_GATE`: **PASS**.

## Honest limits

- The boundary is *directory-based*, not an import-graph closure. A product module living outside
  `tools/gmail_audit` and imported at runtime would still be missed. Nothing in the current
  capture path does that, and a true import closure would be less deterministic (dynamic imports,
  conditional loading) than enumerating the owned subtree.
- Non-`.py` runtime inputs inside the tree — YAML configs such as `config/agent_goals.yaml` —
  are not fingerprinted. They are not hot-synced either, so they cannot drift between host and
  container mid-run; they change only via an image rebuild, which changes the container image id
  that *is* in the fingerprint. Recorded as a known boundary rather than an unnoticed gap.
