# Runner Provenance

RUNNER_PROVENANCE = VALID_FROZEN_COMPAT

## Source

- wrapper: `C:\Users\compg\Desktop\top-code workspace\scripts\run_fresh38_case_batch.ps1`
- selected_runner: `C:\top-code-session-scratch\exit2-fresh38-20260803T185704\run_recovery_pf.PATCHED.py`
- fallback_runner: `C:\Users\compg\Desktop\top-code workspace\.artifacts\ai-os-post-stage6-fresh-baseline\harness\run_recovery_pf.py`
- scoring_helper: `C:\Users\compg\Desktop\top-code workspace\.artifacts\ai-os-post-stage6-fresh-baseline\harness\scoring.py`

## SHA256

- wrapper_after_fix: `8c6ba009bddc7f47912cf415318716d77f551945cd89cb6d4adb0b89df2f3afd`
- selected_runner_after_fix: `8c2f3ddc8c5b31ecab5c0c9478485468a3945480f5c82bc0b4a65ef8f25abf13`
- fallback_runner_after_fix: `8c2f3ddc8c5b31ecab5c0c9478485468a3945480f5c82bc0b4a65ef8f25abf13`
- scoring_helper: `68801d8fde54d0bf4c1c3d37e40f5602a975ff677c63ed1499263cc2f199dc15`

## Git Relationship

- wrapper: tracked in workspace root git; modified by this task.
- selected_runner: not tracked by git; frozen scratch runner patched only at measurement seam.
- fallback_runner: not tracked by git under `.artifacts`; patched to match selected runner seam.
- scoring_helper: not tracked by git under `.artifacts`; unchanged.

## Contract Reasoning

- Initial wrapper provenance was stale/untrusted because hot-sync omitted FIX-04/FIX-05 critical product files and resume logic reused parity-error one-case artifacts.
- This task repaired only measurement seams: hot-sync includes `preclassifier.py`, `context_assembler.py`, `intake_payload.py`; resume skips and reruns existing `parity_error` captures.
- Runner seam was repaired so production-faithful intake uses the real preclassifier lane instead of forcing `intake_llm`; `review_direct` now follows the production deterministic intake shortcut.
- Focused proof: 5/5 captured, HARNESS=0, DELIVERY=0, capture gaps=0.
- Clean full proof: 38/38 captured, 30/30 Understanding judged, scoring_complete=true, capture gaps=0, judge errors=0.
- Verdict remains VALID_FROZEN_COMPAT rather than CANONICAL because the Python recovery runner is not a tracked canonical source file.
