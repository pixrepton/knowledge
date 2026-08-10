# Frozen SUT Manifest — Fresh38 Canonical Clean Run

Frozen at: 2026-08-10T01:18:58Z
AI-OS task: `CAPABILITY-QUALIFICATION-20260809`

Full machine-readable manifest: `FROZEN_SUT_MANIFEST.json` in this directory.

## Why this run exists

The prior run `knowledge/eval/fresh38-clean-20260809T225941Z/` (`CLEAN_PASS=21/38`) is **not**
a valid canonical baseline. Mechanical proof from its own `capture.log`: the hot-sync file list
in `scripts/run_fresh38_case_batch.ps1` only started including `preclassifier.py` on the 5th of
6 sub-runs (`2026-08-10 00:29:39`). Every case except `DEC-01` was `REUSE`d from a cache captured
**before** that sync. 37/38 cases in that run reflect the pre-fix preclassifier; only `DEC-01`
reflects the post-fix one. The wrapper's resume logic checks for `parity_error` only, with no
SUT-fingerprint guard — so it silently mixed two different SUT states into one "clean" result.

## What is frozen for this run

| Component | Path | SHA256 (working tree) | Status |
|---|---|---|---|
| Capture wrapper | `scripts/run_fresh38_case_batch.ps1` | `8c6ba009bddc7f47912cf415318716d77f551945cd89cb6d4adb0b89df2f3af` | uncommitted, task-owned, verified general |
| Preclassifier | `gmail-agent/tools/gmail_audit/preclassifier.py` | `f6112142488b2d24dd9b69fcb3fc1fd1cd72090694184c5278d8ca7ba37537a` | uncommitted, task-owned, verified general |
| Preclassifier tests | `gmail-agent/tools/gmail_audit/tests/test_preclassifier.py` | `197c419fefbefbd61853bfd5b85b59e8a85ec650984c553d529b18dceda2ad9` | uncommitted, task-owned |
| Recovery runner (selected) | `C:\top-code-session-scratch\exit2-fresh38-20260803T185704\run_recovery_pf.PATCHED.py` | `8c2f3ddc8c5b31ecab5c0c9478485468a3945480f5c82bc0b4a65ef8f25abf1` | VALID_FROZEN_COMPAT, byte-identical to fallback |
| Rescorer (v1-v5) | `gmail-agent/tools/gmail_audit/eval_final_rescore_versioned.py` | committed at `146857f38c4a27f37922f03e9724c280bda3b8da` | CANONICAL, git-tracked, covered by Gate A |
| Judge driver | `.artifacts/ai-os-post-stage6-fresh-baseline/judge/run_rotating_judge.py` | n/a | VALID_FROZEN_COMPAT |
| Capture corpus | `corpus-v2.json` | `6550a075d5180d492a35b983a4cdc30624756d80cc3b398ae75fa310c470c04` | canonical fixture |
| Score-base corpus | `corpus-v1.json` | n/a | canonical fixture (v5 contract derives from this) |

Gate A (`python -m pytest tools/gmail_audit/tests -q`): **2401 passed, 15 skipped, 24 subtests
passed, 0 failed.**

Runner provenance: `VALID_FROZEN_COMPAT`.

Runtime: Node B (`gmail-agent-nodeb-api`) self-health 200; kalk-top (`kalk-top-runtime`) docker
health `healthy`; Node B -> kalk-top reachability confirmed live (HTTP 200 via
`http://host.docker.internal:8091`). Unrelated pre-existing issue: the async worker
`gmail-agent-vps-gmail-agent-worker-1` is crash-looping on a Daszek WordPress login endpoint
(`host.docker.internal:8090`) — not on the Fresh38 capture path, not fixed, flagged only.

## Freeze rules for the duration of this experiment

1. Zero reuse of any `one-CASE.json` from any prior run.
2. New, empty `OutDir` before case 1/38.
3. No product code, preclassifier, runner, wrapper, corpus, ground truth, judge, scorer,
   thresholds, provider configuration, or Docker image changes between case 1/38 and the
   completed judge + v5 rescore.
4. Retry permitted only for transient capture failures under this exact frozen manifest; any
   SUT/tooling change invalidates the run and requires a new manifest + new `OutDir` from 0/38.

`FROZEN_SUT_READY = YES`
