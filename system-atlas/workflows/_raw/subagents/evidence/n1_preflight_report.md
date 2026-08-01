# N1 Preflight Report

## Scope
- Build read-only normalization preview for `EV-00001..EV-00187` with `workflow_id`, `related_workflow_ids`, `evidence_type`, `confidence`, `raw_artifact`, `superseded_by`.
- Preserve original `claim`/`summary` payloads and do not mutate canonical `WORKFLOW_EVIDENCE.jsonl`, `WORKFLOW_REGISTRY.yaml`, `WORKFLOW_GAPS.md`, `PROGRESS.md`, or synthesis docs.
- Detect attachment/type/confidence/raw_artifact conflicts and ambiguities from current `knowledge/system-atlas/workflows` state plus existing `_raw` artifacts.

## Files Inspected
- `knowledge/system-atlas/workflows/WORKFLOW_EVIDENCE.jsonl`
- `knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml`
- `knowledge/system-atlas/workflows/PROGRESS.md`
- `knowledge/system-atlas/workflows/normalize_workflow_evidence.py`
- `knowledge/system-atlas/workflows/_raw/n1_attachment_policy.md`
- `knowledge/system-atlas/workflows/_raw/n1_evidence_workflow_attachment_seed.md`
- `knowledge/system-atlas/workflows/_raw/n1_unattached_evidence_triage.md`
- `knowledge/system-atlas/workflows/_raw/n1_unattached_preview_seed.json`
- `knowledge/system-atlas/workflows/_raw/test_evidence_mapping_cross_reference.md`
- `knowledge/system-atlas/workflows/_raw/wave1-preflight-20260730-220832/WORKFLOW_EVIDENCE.jsonl`

## Assumptions
- Source of truth for this preview is the current working tree under `knowledge/system-atlas/workflows` plus existing `_raw` artifacts; MCP was not used.
- `ATLAS-GLOBAL` is reserved for genuine cross-workflow inventory/cross-contract evidence and is always paired with non-empty `related_workflow_ids`.
- `superseded_by` is filled only for explicit, conservative whole-row corrections; partial refinements stay in the conflict list instead of being over-encoded as hard supersession.
- When no dedicated `_raw/*.md` artifact is cited or inferable, the preview falls back to `_raw/wave1-preflight-20260730-220832/WORKFLOW_EVIDENCE.jsonl#EV-xxxxx` rather than inventing a new raw artifact.

## Proposed Changes
- Wrote preview file `knowledge/system-atlas/workflows/_raw/subagents/evidence/n1_full_rewrite_preview.jsonl` with `187/187` normalized rows; ID sequence is contiguous and complete.
- Primary attachment sources used: `{'registry-single': 144, 'seed-unattached': 32, 'manual-multi': 11}`.
- Resulting `workflow_id: ATLAS-GLOBAL` count: `13`.
- Preserved payload split: `claim-only=162`, `summary-only=25`, `claim+summary=0` from current canonical input.
- `raw_artifact` precision split: `snapshot-fallback=175`, `dedicated-artifact-or-cited=12`.
- Conservative hard supersession recorded for `2` rows: `EV-00038 -> EV-00080`, `EV-00075 -> EV-00076`.

## Conflicts And Ambiguities
- Canonical inconsistency: current `WORKFLOW_EVIDENCE.jsonl` contains `187` rows (`EV-00001..EV-00187`), while current `PROGRESS.md` still reports `180` / `EV-00180` as the top of range.
- Attachment decisions requiring non-trivial resolution: `43` rows. High-signal cases are documented in `n1_multi_workflow_resolution.md`.
- Type decisions not purely preserved from canonical rows: `30` rows. Highest-risk manual/tooling classifications: `EV-00018`, `EV-00114`, `EV-00116`, `EV-00118`, `EV-00133`, `EV-00134`, `EV-00135`, `EV-00137`.
- Confidence decisions not purely preserved from canonical rows: `71` rows. The main medium-confidence family is tooling/synthesis evidence rather than direct runtime/test proof.
- Raw-artifact ambiguity remains high: `175` rows have no dedicated `_raw` artifact beyond the preflight snapshot copy of `WORKFLOW_EVIDENCE.jsonl`.
- Helper-script drift detected in `normalize_workflow_evidence.py` `KNOWN_RAW_ARTIFACTS`; confirmed stale mappings:
  - `EV-00177` helper points to `_raw/tool_registry_cross_reference.md` but current preview resolves to `_raw/planner_tool_chain_cross_reference.md`.
  - `EV-00179` helper points to `_raw/fact_key_producer_reader_supersession_invalidation_cross_reference.md` but current preview resolves to `_raw/proposal_type_creator_executor_cross_reference.md`.
  - `EV-00180` helper points to `_raw/signal_source_kind_cross_reference.md` but current preview resolves to `_raw/fact_key_producer_reader_supersession_cross_reference.md`.
- Partial corrections kept out of hard `superseded_by` because only part of the older row is revised:
  - `EV-00116` / `EV-00117`: DB outbox dormancy finding remains useful, but live-path ownership/retry framing was revised by EV-00117.
  - `EV-00117` / `EV-00165`: live JSONL drain path confirmed by EV-00117; retry/dead-letter semantics tightened by EV-00165.
  - `EV-00128` / `EV-00153`: Node B context mechanism remains real, but the presumed live caller was corrected by EV-00153.

## Unresolved
- `raw_artifact` fidelity is still shallow for snapshot-fallback rows; current preview favors completeness and non-invention over fabricated precision.
- `evidence_type` for non-normalized legacy rows is still heuristic preview output, not a canonicalized contract accepted elsewhere in the workspace.
- `superseded_by` remains conservative; additional partial-correction encoding would need an explicit contract for field-level supersession, not row-level replacement.

## Validation Commands
- `@'
import json
from pathlib import Path
p=Path(r'knowledge/system-atlas/workflows/_raw/subagents/evidence/n1_full_rewrite_preview.jsonl')
rows=[json.loads(line) for line in p.read_text(encoding='utf-8').splitlines() if line.strip()]
assert len(rows)==187
assert [r['id'] for r in rows]==[f'EV-{i:05d}' for i in range(1,188)]
assert all('workflow_id' in r and 'related_workflow_ids' in r and 'evidence_type' in r and 'confidence' in r and 'raw_artifact' in r and 'superseded_by' in r for r in rows)
print('OK')
'@ | python -`
- `rg -n "ATLAS-GLOBAL|EV-00112|EV-00182|EV-00183|EV-00184|EV-00185|EV-00186|EV-00187" knowledge/system-atlas/workflows/_raw/subagents/evidence/n1_full_rewrite_preview.jsonl`
- `rg -n "^## |^# " knowledge/system-atlas/workflows/_raw/subagents/evidence/n1_preflight_report.md knowledge/system-atlas/workflows/_raw/subagents/evidence/n1_multi_workflow_resolution.md`

## Repo SHA
- `beb8309f52576df181c04e965e1353aedeba9de1`

## Timestamp
- `2026-07-30 22:22:17 +0200`
