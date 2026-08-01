# Manifest Boundary

Target: `AI-OS-WORKFLOW-RECONSTRUCTION-FINAL-GATE-CLOSEOUT-01`

Status: active final-gate boundary for the workflow atlas closeout.

## Chosen Model

- `FINAL_MANIFEST.json` covers canonical workflow-atlas artifacts only.
- The manifest does **not** include a self-hash for `FINAL_MANIFEST.json`.
- The manifest does **not** include post-manifest verification proofs under `_raw/final-gate-closeout/`.
- Final verification proof stores the SHA-256 of both `FINAL_MANIFEST.json` and `validate_workflow_atlas.py`.
- After the final PASS, no file covered by the manifest may be mutated.

## Why

- A self-hash would force recursive regeneration or a synthetic placeholder mechanism.
- Post-manifest verification logs are intentionally written after the final PASS and therefore must stay outside the manifest boundary.
- Integrity truth for covered artifacts comes from `size + sha256`, not from mutable filesystem timestamps.

## Covered Artifact Classes

- Canonical normalized data:
  - `WORKFLOW_EVIDENCE.jsonl`
  - `WORKFLOW_REGISTRY.yaml`
  - `WORKFLOW_GAPS.yaml`
- Canonical rendered docs and synthesis:
  - `WORKFLOW_GAPS.md`
  - `WORKFLOW_ATLAS.md`
  - `ENTRYPOINT_INVENTORY.md`
  - `STATE_OWNERSHIP_MATRIX.md`
  - `CROSS_REPO_CONTRACTS.md`
  - `ARCHITECTURAL_RULES_AUDIT.md`
  - `RUNTIME_BASELINE.md`
  - `RUNTIME_PROOF_PLAN.md`
  - `EXECUTIVE_SUMMARY.md`
  - `PROGRESS.md`
  - `FINAL_CONSISTENCY_REPORT.md`
- Canonical atlas tooling used to generate/verify the closeout:
  - `workflow_tools_common.py`
  - `normalize_workflow_evidence.py`
  - `normalize_workflow_registry.py`
  - `normalize_workflow_gaps.py`
  - `generate_workflow_atlas_docs.py`
  - `generate_progress.py`
  - `validate_workflow_atlas.py`
  - `build_final_manifest.py`
  - `run_validator_negative_tests.py`

## Explicitly Out Of Scope

- `FINAL_MANIFEST.json` self-hash
- `_raw/final-gate-closeout/final_manifest_verification.json`
- `_raw/final-gate-closeout/final_manifest_verification.log`
- `_raw/final-gate-closeout/validator_negative_tests.md`
- `_raw/final-gate-closeout/validator_negative_tests.log`
- `_raw/final-gate-closeout/validator_negative_tests.json`
- reproduction fixtures and reproduction logs under `_raw/final-gate-closeout/`
