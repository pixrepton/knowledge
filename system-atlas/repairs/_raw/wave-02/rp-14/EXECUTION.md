# RP-14 EXECUTION

Package: `RP-14`

Status: `CLOSED`

Baseline overlay commit:

- `knowledge`: `bc91f3ad3f86f552dc20e3a871022cafce19cce5`

Code commits:

- `top-instal-generator`: `2afd4484b3c1372222b637ccd0cb1a41a573617d`
- `fast-kalk`: `40bdd7bc21d0c827ddcc919202ecc0ac278d0bda`
- `cieplo-orchestrator`: `8e2ad74b4a22a4c1f0567129c010cf2c4f82b067`

Repositories and branches:

- `top-instal-generator`: `handoff/20260719-1403-latest`
- `fast-kalk`: `handoff/20260719-1403-latest`
- `cieplo-orchestrator`: `handoff/20260719-1403-latest`

Proof timestamp anchor:

- `2026-07-31T07:36:01Z`

## Scope

Close the document-readiness contract without mutating Workflow Registry v1, without reopening any Google write path, and without pretending DOCX fallback is equivalent to verified PDF success.

## Proof Inventory

Repository state:

- `repo_state_before_close.json`
- `repo_state_after_code_commits.json`

GitNexus change mapping:

- `gitnexus_top_instal_generator_detect_changes.log`
- `gitnexus_fast_kalk_detect_changes.log`
- `gitnexus_cieplo_orchestrator_detect_changes.log`

Focused proofs:

- `generator_readiness_contract.log`
- `generator_smoke.log`
- `fast_kalk_readiness_contract.log`
- `fast_kalk_e2e_smoke.log`
- `cieplo_pytests.log`

## Findings

1. Producer truth was incomplete.
   `top-instal-generator` returned HTTP success with `document.format=docx` plus fallback warning, but did not expose one canonical readiness contract separating verified PDF from degraded DOCX.

2. `fast-kalk` consumer semantics were false-success prone.
   `class-offer-dispatch.php` only checked `downloadUrl`, then fetched bytes and treated the result as PDF success even when the generator had actually degraded to DOCX.

3. `cieplo-orchestrator` overstated both readiness and terminal semantics.
   `runner.py` unconditionally mapped `downloadUrl` to `PDF_READY`, and `FAILED_FINAL` still participated in retry-style flows despite its final naming.

4. `direct-config` is not dead.
   Proof showed a live legacy consumer through generator UI / `simple_generate`, so removal would have been a false closure. The real fix was to keep that path explicit and truthful under the same readiness contract.

## Frozen Contract Points

- `PDF_READY` means verified PDF only.
- DOCX fallback is explicit degradation, not PDF success.
- `FAILED_FINAL` is terminal and not a retryable API state.
- Workflow Registry v1 remains immutable.

## Decision

- `DQ-07`: resolved locally in favor of a typed readiness contract.
  Producer contract now distinguishes `READY` vs `DEGRADED`, requested format, actual format, artifact verification, degraded code, and retryability.
- `DQ-12`: resolved locally in favor of retaining `direct-config` as explicit legacy mode.
  The path remains live, but it now shares the same truthful readiness payload instead of shadow semantics.

Rejected alternatives:

- removing `direct-config` in Wave 2 despite a proven live legacy consumer;
- preserving `FAILED_FINAL` as retryable convenience;
- teaching consumers to guess readiness from `downloadUrl` alone.

## Historical Data Impact

Classification: `MANUAL_REVIEW`

Notes:

- historical generator success rows may include pre-fix DOCX fallback under success wording;
- historical `cieplo-orchestrator` rows in `PDF_READY` may need manual interpretation if audited;
- no replay, row rewrite, or projection rebuild was executed in this package.

## Implementation Scope

Changed producer:

- `top-instal-generator/core/application/GenerateOfferDocumentUseCase.php`
- `top-instal-generator/wp-adapter/ajax/GenerateOfferDocumentAjaxController.php`
- `top-instal-generator/core/application/harness/document-readiness.contract.php`

Changed consumers:

- `fast-kalk/wp-content/plugins/topinstal-lead-widget/includes/class-offer-dispatch.php`
- `fast-kalk/scripts/document-readiness-contract.php`
- `cieplo-orchestrator/src/topinstal_cieplo_worker/workflow/runner.py`
- `cieplo-orchestrator/src/topinstal_cieplo_worker/workflow/states.py`
- `cieplo-orchestrator/src/topinstal_cieplo_worker/workflow/row_updates.py`
- `cieplo-orchestrator/src/topinstal_cieplo_worker/api/routes.py`
- `cieplo-orchestrator/src/topinstal_cieplo_worker/api/workflow_context.py`
- `cieplo-orchestrator/src/topinstal_cieplo_worker/integrations/event_spine/workflow_events.py`
- `cieplo-orchestrator/tests/test_workflow_e2e_mocked.py`
- `cieplo-orchestrator/tests/test_cieplo_workflow_os_events.py`
- `cieplo-orchestrator/tests/test_workflow_row_updates.py`
- `cieplo-orchestrator/tests/test_ingress_integration.py`

## Tests And Runtime/Integration Proof

Commands executed:

```text
python -m pytest tests/test_workflow_e2e_mocked.py tests/test_cieplo_workflow_os_events.py tests/test_workflow_row_updates.py tests/test_ingress_integration.py -q
php core/application/harness/document-readiness.contract.php
php core/application/harness/generate-offer-document.smoke.php
php scripts/document-readiness-contract.php
php scripts/e2e-scenarios-smoke.php
```

Observed results:

- `cieplo-orchestrator`: `18 passed`
- `top-instal-generator`: contract harness `PASS`, smoke `PASS`
- `fast-kalk`: readiness contract `4/4 PASS`, local E2E smoke `39/39 PASS`

Proof limitations:

- no production runtime or external mail send was executed;
- Cieplo proof is integration-level and local, not production-observed;
- historical rows were not migrated.

## Gap Outcome

Closed:

- `gap.top-instal-generator-offer-document.legacy-direct-config-generation-path-remains-live`
- `gap.top-instal-generator-offer-document.document-converter-path-has-two-live-modes`
- `gap.top-instal-generator-offer-document.generator-success-status-masks-docx-fallback-degradation`
- `gap.fast-kalk-lead-widget-calculate-register-dispatch.fast-kalk-treats-docx-fallback-as-pdf-ready`
- `gap.cieplo-orchestrator-intake-to-review-email.cieplo-treats-docx-fallback-as-pdf-ready`
- `gap.cieplo-orchestrator-intake-to-review-email.failed-final-state-name-overstates-recoverability`

Residuals:

- historical readiness history remains ambiguous until separately reviewed;
- no new production-proof claim is made.

## Final Status

`CLOSED`
