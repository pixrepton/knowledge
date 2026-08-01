# Validator Test Report

- Status: `PASS`
- Scope: draft validator only for target `AI-OS-WORKFLOW-RECONSTRUCTION-AND-REGISTRY-01`; no canonical atlas artifacts or helper scripts outside `_raw/subagents/validator/` were modified
- Timestamp: `2026-07-30T22:41:04+02:00`
- Repo SHA:
  - `knowledge`: `597b1091a296930ed32afb379ec19b8ab425d4fa`
  - workspace root: `beb8309f52576df181c04e965e1353aedeba9de1`

## Scope

Prepared a standalone draft validator at:

- `knowledge/system-atlas/workflows/_raw/subagents/validator/validate_workflow_atlas.py`

Prepared negative fixtures at:

- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/broken_core/`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/`

The validator is designed to cover:

- JSONL evidence
- YAML registry
- evidence sequence
- evidence associations
- workflow IDs
- evidence scopes
- raw artifacts
- registry schema
- statuses
- test statuses
- gap IDs
- gap evidence
- route counters
- contracts
- ownership
- runtime claims
- syntheses
- stale markers
- manifest

## Files Inspected

- `knowledge/system-atlas/workflows/WORKFLOW_EVIDENCE.jsonl`
- `knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml`
- `knowledge/system-atlas/workflows/WORKFLOW_GAPS.yaml`
- `knowledge/system-atlas/workflows/WORKFLOW_ATLAS.md`
- `knowledge/system-atlas/workflows/ENTRYPOINT_INVENTORY.md`
- `knowledge/system-atlas/workflows/CROSS_REPO_CONTRACTS.md`
- `knowledge/system-atlas/workflows/STATE_OWNERSHIP_MATRIX.md`
- `knowledge/system-atlas/workflows/ARCHITECTURAL_RULES_AUDIT.md`
- `knowledge/system-atlas/workflows/RUNTIME_BASELINE.md`
- `knowledge/system-atlas/workflows/RUNTIME_PROOF_PLAN.md`
- `knowledge/system-atlas/workflows/EXECUTIVE_SUMMARY.md`
- `knowledge/system-atlas/workflows/PROGRESS.md`
- `knowledge/system-atlas/workflows/_raw/subagents/registry/registry_normalization_plan.yaml`
- `knowledge/system-atlas/workflows/_raw/subagents/supporting/supporting_registry_plan.md`

## Assumptions

- Canonical atlas root for validation is `knowledge/system-atlas/workflows`.
- `WORKFLOW_GAPS.yaml` is the machine-readable gap source, while `WORKFLOW_GAPS.md` is a rendered view.
- Final hard gate should be stricter than the current intermediate state, so the validator exposes:
  - `draft` mode: current atlas may pass with warnings.
  - `final` mode: manifest, normalized docs, and stale-marker cleanup are blocking requirements.
- Current working-tree content is the source of truth; fixtures are intentionally synthetic and negative-only.

## What The Draft Validator Currently Checks

1. `WORKFLOW_EVIDENCE.jsonl`
   - contiguous `EV-xxxxx` sequence
   - required row fields
   - allowed `evidence_type` and `confidence`
   - `ATLAS-GLOBAL` contract
   - `raw_artifact` existence under `_raw/`
   - `superseded_by` reference integrity
   - workflow/related-workflow references against the registry

2. `WORKFLOW_REGISTRY.yaml`
   - top-level schema keys
   - `evidence_scopes` and `ATLAS-GLOBAL`
   - taxonomy values
   - subflow evidence references
   - workflows in either current list shape or final mapping shape
   - `path_statuses`, `contract_statuses`, runtime decomposition
   - forbidden legacy `status`
   - forbidden `confidence` placement in registry/test nodes
   - `workflow_test_status` keys and allowed statuses

3. `WORKFLOW_GAPS.yaml`
   - top-level schema keys
   - `atomic_gap_count`
   - `gap_id` uniqueness/format
   - workflow/evidence references
   - allowed gap statuses
   - required producer/consumer/impact fields

4. Supporting docs and syntheses
   - presence checks
   - stale markers (`STALE`, `regeneration pending`, `next step is`)
   - normalized marker checks for:
     - `ENTRYPOINT_INVENTORY.md`
     - `CROSS_REPO_CONTRACTS.md`
     - `STATE_OWNERSHIP_MATRIX.md`
     - `ARCHITECTURAL_RULES_AUDIT.md`
   - `FINAL_CONSISTENCY_REPORT.md` required in `final` mode

5. Manifest
   - JSON shape
   - required fields per entry
   - relative paths only
   - existence, size, sha256, modified timestamp
   - coverage of required final artifacts in `final` mode

## Validation Runs

### 1. Real atlas smoke test

Command:

```powershell
python "knowledge/system-atlas/workflows/_raw/subagents/validator/validate_workflow_atlas.py" --root "knowledge/system-atlas/workflows" --mode draft
```

Observed result:

- Exit code: `0`
- Status: `PASS`
- Summary: `errors=0 warnings=102`

Meaning:

- The draft validator can traverse the real current atlas without mutating it.
- The current atlas is not final-gate clean yet.
- The warnings are concentrated in:
  - `EV-00163..EV-00187` using empty `repo/file/symbol/lines` locator fields in the current JSONL
  - one gap row with missing `workflow_ids`
  - missing `FINAL_MANIFEST.json`

### 2. Negative fixture: broken core

Command:

```powershell
python "knowledge/system-atlas/workflows/_raw/subagents/validator/validate_workflow_atlas.py" --root "knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/broken_core" --mode final
```

Observed result:

- Exit code: `1`
- Status: `FAIL`
- Summary: `errors=29 warnings=0`

Detected failures include:

- broken evidence sequence
- invalid `ATLAS-GLOBAL` row
- invalid `evidence_type` and `confidence`
- missing raw artifacts
- invalid runtime trigger mode
- impossible `CONFIRMED + STATIC_ONLY`
- mismatched `workflow_test_status`
- invalid gap count and gap references
- missing final docs and manifest

### 3. Negative fixture: bad manifest and docs

Command:

```powershell
python "knowledge/system-atlas/workflows/_raw/subagents/validator/validate_workflow_atlas.py" --root "knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs" --mode final
```

Observed result:

- Exit code: `1`
- Status: `FAIL`
- Summary: `errors=10 warnings=0`

Detected failures include:

- stale marker in `ENTRYPOINT_INVENTORY.md`
- missing normalization markers for entrypoints/contracts/ownership/rules docs
- manifest size mismatch
- manifest sha256 mismatch
- manifest missing required coverage

## Proposed Changes

- Keep this validator draft isolated until core normalization and doc regeneration stabilize.
- When Phase C final artifacts are ready, wire this script into the canonical validation pass and decide whether it should be copied or reimplemented outside `_raw/subagents/validator/`.
- Before `final` mode is used as a hard gate, close at least these current atlas warnings:
  - fill or intentionally redefine locator semantics for `EV-00163..EV-00187`
  - attach `workflow_ids` to the one gap currently left empty
  - generate `FINAL_MANIFEST.json`
  - regenerate supporting docs with explicit normalized markers or adjust marker policy if the canonical doc schema intentionally uses different labels

## Unresolved

- The validator currently treats empty evidence locator fields as warnings in `draft` and errors in `final`; operator/integrator still needs to decide whether some atlas-global or synthesis-style evidence rows should be allowed to stay locator-light permanently.
- Supporting-doc marker checks are intentionally pragmatic string checks, not a deep parser. If the canonical regenerated docs use different field labels, the marker rules will need one controlled update.
- Manifest schema is draft-level and assumes `path`, `size`, `sha256`, `modified_at`. If final manifest shape differs, the validator will need to be aligned before hard gating.
- Gap status taxonomy is based on the current normalized YAML and may need extension if Phase C introduces additional stable gap states.

## Validation Commands

```powershell
git -C "C:\Users\compg\Desktop\top-code workspace" rev-parse HEAD
git -C "C:\Users\compg\Desktop\top-code workspace\knowledge" rev-parse HEAD
Get-Date -Format 'yyyy-MM-ddTHH:mm:ssK'
Get-Content -Path "knowledge/system-atlas/workflows/WORKFLOW_EVIDENCE.jsonl" -TotalCount 6
Get-Content -Path "knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml" -TotalCount 120
Get-Content -Path "knowledge/system-atlas/workflows/WORKFLOW_GAPS.yaml" -TotalCount 120
python "knowledge/system-atlas/workflows/_raw/subagents/validator/validate_workflow_atlas.py" --root "knowledge/system-atlas/workflows" --mode draft
python "knowledge/system-atlas/workflows/_raw/subagents/validator/validate_workflow_atlas.py" --root "knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/broken_core" --mode final
python "knowledge/system-atlas/workflows/_raw/subagents/validator/validate_workflow_atlas.py" --root "knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs" --mode final
```

## Saved Files

- `knowledge/system-atlas/workflows/_raw/subagents/validator/validate_workflow_atlas.py`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/validator_test_report.md`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/broken_core/WORKFLOW_EVIDENCE.jsonl`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/broken_core/WORKFLOW_REGISTRY.yaml`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/broken_core/WORKFLOW_GAPS.yaml`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/WORKFLOW_EVIDENCE.jsonl`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/WORKFLOW_REGISTRY.yaml`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/WORKFLOW_GAPS.yaml`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/WORKFLOW_ATLAS.md`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/ENTRYPOINT_INVENTORY.md`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/CROSS_REPO_CONTRACTS.md`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/STATE_OWNERSHIP_MATRIX.md`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/ARCHITECTURAL_RULES_AUDIT.md`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/RUNTIME_BASELINE.md`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/RUNTIME_PROOF_PLAN.md`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/EXECUTIVE_SUMMARY.md`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/PROGRESS.md`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/FINAL_CONSISTENCY_REPORT.md`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/FINAL_MANIFEST.json`
- `knowledge/system-atlas/workflows/_raw/subagents/validator/fixtures/bad_manifest_and_docs/_raw/source.md`

