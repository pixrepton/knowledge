# CL-03 — Fresh38 runner provenance: final architecture

## Verdict

```text
REPRODUCIBLE_FROM_REPOSITORY_STATE = YES
ACCEPTED_BOUNDARY                  = not needed
```

## The three states this went through

| stage | canonical source | verified? | reconstructable from a fresh checkout? |
|---|---|---|---|
| original | `C:\top-code-session-scratch\exit2-fresh38-…\run_recovery_pf.PATCHED.py`, silently falling back to `.artifacts/…/harness/` | no — the two were never compared | **no** |
| after FIX-MEAS01 | `.artifacts/…/harness/run_recovery_pf.py`, SHA256 pinned in tracked `scripts/fresh38_runner_provenance.json` | yes — mismatch aborts the capture | **no** — `.artifacts/` is gitignored |
| now (CL-03) | **`scripts/fresh38/run_recovery_pf.py`**, tracked, same pin | yes | **yes** |

Hash pinning proved the runner had not *changed*. It could not make the runner *exist* in a
clean clone, which is what reproducibility actually requires.

## Final architecture

```text
scripts/fresh38/run_recovery_pf.py     tracked, canonical    8c2f3ddc…abf13
scripts/fresh38/scoring.py             tracked, canonical    68801d8f…9dc15
scripts/fresh38_runner_provenance.json tracked, pins both hashes
run_fresh38_case_batch.ps1             -HarnessDir defaults to scripts/fresh38
```

There is exactly **one** canonical source. The wrapper no longer reads `.artifacts/` or session
scratch for the runner. Both former locations are recorded in the provenance file under
`deprecated_copies` with `status: NOT_CANONICAL`.

Migration was byte-preserving — the tracked copies are identical to the harness that produced the
38/38 measurement, and to the pins that were already in place:

```text
scripts/fresh38/run_recovery_pf.py                                  8c2f3ddc…abf13
.artifacts/ai-os-post-stage6-fresh-baseline/harness/run_recovery_pf.py  8c2f3ddc…abf13   (identical)
pinned in scripts/fresh38_runner_provenance.json                    8c2f3ddc…abf13   (match)
```

## Guarding against a second canonical

The operator's constraint was explicit: do not maintain a tracked canonical *and* an ignored
second canonical. Two mechanisms enforce it:

1. The wrapper resolves the runner only from `-HarnessDir` (default `scripts/fresh38`). The
   `.artifacts` path is never consulted, so it cannot silently become authoritative again.
2. If a deprecated copy still exists **and its bytes differ** from the canonical, the capture logs
   `WARN DEPRECATED_RUNNER_COPY_DIVERGED path=… sha256=… (canonical=…)`. Divergence becomes
   visible instead of dormant. It is a warning rather than an abort because the file is inert —
   aborting a valid run over an unread leftover would be over-strict.

## Verification at capture time

Every capture, before anything is provisioned:

```text
runner_provenance=VERIFIED sha256=8c2f3ddc… path=…\scripts\fresh38\run_recovery_pf.py
```

and on mismatch:

```text
ABORT RUNNER_PROVENANCE_MISMATCH expected=… actual=… path=…
```

Proven in `scripts/tests/test_fresh38_reuse_gate.ps1` step `[0/5]`: a runner that fails its pin
aborts the run and produces no experiment manifest.

## Changing the harness deliberately

Edit `scripts/fresh38/`, update the hash in `scripts/fresh38_runner_provenance.json` in the same
commit, and say why. The pin exists to make an unintended change loud, not to make an intended one
hard. It must never be edited to make a failing capture pass.
