# N1 Attachment Policy Seed

- timestamp: `2026-07-30 21:56:00 +02:00`
- working_directory: `C:\Users\compg\Desktop\top-code workspace`
- purpose:
  - define the attachment policy to apply when rewriting `WORKFLOW_EVIDENCE.jsonl`
  - prevent silent distortion of shared-subflow and atlas-global evidence

## Proposed Policy

### 1. Workflow-specific evidence

- rule:
  - set `workflow_id` to the owning canonical workflow
  - set `related_workflow_ids` only when the evidence directly constrains another canonical workflow
- applies to:
  - bucket A from `_raw/n1_unattached_evidence_triage.md`
  - all single-attachment registry-derived evidence

### 2. Shared-subflow evidence

- rule:
  - set `workflow_id` to the earliest canonical workflow that owns the shared step in the real lifecycle
  - put downstream or sibling dependents into `related_workflow_ids`
- working interpretation for current backlog:
  - evidence about route choice before agent handoff -> primary `GMAIL-RECONCILE-MODE-DISPATCH`
  - evidence about case intelligence / stage_config / handoff assembly -> primary `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
  - evidence about active agent execution loop after handoff -> primary `AGENT-GRAPH-EXECUTE-RUN`

### 3. Atlas-global or cross-workflow evidence

- rule:
  - allow a sentinel primary `workflow_id: ATLAS-GLOBAL`
  - require non-empty `related_workflow_ids`
  - use this only when forcing a canonical workflow would misstate ownership
- candidate rows:
  - `EV-00112`
  - `EV-00118`
  - `EV-00173`
  - `EV-00174`
  - `EV-00175`
  - `EV-00178`
- rationale:
  - these rows are inventory/methodology/cross-contract findings spanning multiple workflows
  - selecting one business workflow as primary would be arbitrary and misleading

### 4. High-fanout evidence already attached to many workflows

- rule:
  - choose one primary workflow that most directly owns the described behavior
  - keep all other affected workflows in `related_workflow_ids`
  - never duplicate the evidence row to preserve ID stability
- examples:
  - `EV-00182` -> primary should be the workflow whose status contract is most directly analyzed in the row, with the rest related
  - `EV-00186` -> if no single owner is defensible, treat as `ATLAS-GLOBAL`
  - `EV-00187` -> `ATLAS-GLOBAL` by design, because it is a registry-wide test mapping artifact

## Preconditions Before JSONL Rewrite

- apply this policy consistently to:
  - the `33` currently unattached evidence rows
  - the `154` registry-attached rows
  - the high-fanout evidence rows with `2+` workflow associations
- update any downstream validator/gate to accept `ATLAS-GLOBAL` as a legal normalization sentinel

## Exact Next Mutation Target

- file: `WORKFLOW_EVIDENCE.jsonl`
- operation: add `workflow_id`, `related_workflow_ids`, and `raw_artifact` to every row; backfill `evidence_type` and `confidence` where still missing
