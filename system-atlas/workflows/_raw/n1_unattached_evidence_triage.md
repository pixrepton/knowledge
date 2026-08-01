# N1 Unattached Evidence Triage

- timestamp: `2026-07-30 21:52:00 +02:00`
- working_directory: `C:\Users\compg\Desktop\top-code workspace`
- scope:
  - classify the 33 evidence rows still unattached after registry-only derivation
  - separate strong primary-workflow candidates from genuine cross-workflow / atlas-global items
- sources used:
  - `WORKFLOW_EVIDENCE.jsonl` summaries/claims for unattached IDs
  - `PROGRESS.md` domain status and evidence lists
  - `_raw/n1_evidence_workflow_attachment_seed.md`

## Classification Buckets

### A. Strong primary-workflow candidate

- `EV-00042` -> primary candidate `GMAIL-RECONCILE-MODE-DISPATCH`
  - note: case-id resolution priority chain belongs to the routing/dispatch split before handoff
- `EV-00043` -> primary candidate `GMAIL-RECONCILE-MODE-DISPATCH`
  - note: explicit orchestrator route decision (`defer` / `fast_link` / `deep_understand`)
- `EV-00071` -> primary candidate `AGENT-GRAPH-EXECUTE-RUN`
  - related: `AGENT-GRAPH-TURN-LOOP`
  - note: live `decision_pipeline_dry_run_only=False` proof is a run-level enablement fact
- `EV-00113` -> primary candidate `KALK-TOP-CALCULATE-OFFER-PIPELINE`
  - related: `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`, `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`
  - note: proves the agent kalk-top tool reaches the same calculate-offer backend
- `EV-00114` -> primary candidate `GMAIL-SIGNAL-WORKER-LOOP`
  - related: `GMAIL-RECONCILE-MODE-DISPATCH`
  - note: replay/rebuild entrypoints re-enter reconcile core
- `EV-00115` -> primary candidate `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
  - note: operator reject-same-case correction loop
- `EV-00121` -> primary candidate `GMAIL-SIGNAL-WORKER-LOOP`
- `EV-00122` -> primary candidate `GMAIL-SIGNAL-WORKER-LOOP`
- `EV-00123` -> primary candidate `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
  - related: `GMAIL-RECONCILE-MODE-DISPATCH`
- `EV-00124` -> primary candidate `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
  - related: `GMAIL-RECONCILE-MODE-DISPATCH`
- `EV-00125` -> primary candidate `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
- `EV-00126` -> primary candidate `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
- `EV-00127` -> primary candidate `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
- `EV-00133` -> primary candidate `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`
- `EV-00134` -> primary candidate `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`
- `EV-00135` -> primary candidate `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`
- `EV-00136` -> primary candidate `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
- `EV-00155` -> primary candidate `DASZEK-COMMAND-OUTBOX-DRAIN`
  - related: `DASZEK-FEED-PUSH-NO-RETRY`
- `EV-00156` -> primary candidate `DASZEK-FEED-PUSH-NO-RETRY`
- `EV-00163` -> primary candidate `DASZEK-FEED-PUSH-NO-RETRY`

### B. Workflow-specific but needs manual split between primary and related

- `EV-00066`
  - candidate set: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`, `AGENT-GRAPH-EXECUTE-RUN`
  - reason: shared downstream stage order starts before agent execution but feeds the run contract
- `EV-00067`
  - candidate set: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`, `AGENT-GRAPH-EXECUTE-RUN`
- `EV-00068`
  - candidate set: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`, `AGENT-GRAPH-EXECUTE-RUN`
- `EV-00069`
  - candidate set: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`, `AGENT-GRAPH-EXECUTE-RUN`
- `EV-00070`
  - candidate set: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`, `AGENT-GRAPH-EXECUTE-RUN`
- `EV-00105`
  - candidate set: `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`, `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`
  - reason: harness-only `wp-bridges` evidence informs Domain 8 boundaries but is not a product path by itself
- `EV-00132`
  - candidate set: `KALK-TOP-CALCULATE-OFFER-PIPELINE`, `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`, `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`, `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`
  - reason: cross-system missing producer for margin/sale outcome

### C. Genuine cross-workflow / atlas-global evidence

- `EV-00112`
  - route inventory closure for `api_app.py`
  - likely needs atlas-level attachment strategy rather than forcing one workflow
- `EV-00118`
  - tooling-methodology evidence about GitNexus limits on `kalk-top`
  - should likely remain atlas-global or tooling-only
- `EV-00173`
  - WordPress compose mount topology across multiple repos
  - cross-workflow infrastructure fact
- `EV-00174`
  - exhaustive PHP route enumeration across all four PHP repos
  - atlas-global inventory fact
- `EV-00175`
  - closes remaining one-sided cross-repo contracts to both-sided
  - spans multiple offer workflows and likely belongs in cross-repo normalized core
- `EV-00178`
  - reverse-audit category 4 event type <-> emitter <-> handler
  - cross-workflow by design

## Immediate Normalization Guidance

- Rows in bucket A can be normalized first with a concrete `workflow_id` and optional `related_workflow_ids`.
- Rows in bucket B need one explicit operator-grade decision on what counts as the primary workflow for shared subflow evidence.
- Rows in bucket C argue for an atlas-level normalization strategy:
  - either define a canonical cross-workflow attachment rule
  - or introduce a documented atlas-global evidence mode in the normalized schema before rewriting JSONL

## Exit Condition for This Triage Step

- achieved: every unattached evidence row now has a triage bucket
- remaining before JSONL rewrite:
  - decide the primary workflow policy for shared-subflow evidence
  - decide how atlas-global evidence is represented without falsifying workflow ownership
