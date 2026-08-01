# Gap Migration Map

Scope: Wave 1 / Subagent C atomic preview only for `WORKFLOW_GAPS.md` -> stable machine-tractable gap IDs. Canonical workflow files remained read-only.

Files inspected: `knowledge/system-atlas/workflows/WORKFLOW_GAPS.md`, `knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml`, `knowledge/system-atlas/workflows/WORKFLOW_EVIDENCE.jsonl`, `knowledge/system-atlas/workflows/normalize_workflow_gaps.py`, `knowledge/system-atlas/workflows/_raw/gap_registry_preview.generated.yaml`, `knowledge/system-atlas/workflows/_raw/gap_registry_preview.generated.md`, `knowledge/system-atlas/workflows/_raw/gap_registry_normalization_report.json`.

Assumptions: current working tree is the source of truth; numbered items `38-40` are canonical even though they are not bolded; stable IDs are workflow-anchored instead of legacy-number-anchored; MCP not used.

Proposed changes: replace legacy one-item-per-markdown-entry normalization with an atomic registry; split merged legacy items into one gap per independent producer-consumer break; keep one stable gap ID reusable across future renumbering; preserve legacy-to-atomic mapping explicitly.

Unresolved: item `35` remains a documentation-adjudication gap rather than a code-proven defect; item `15` confirms shared mailbox coupling but the narrower duplicate-case residual was not promoted into a separate atomic gap because it is still unproven; several architecture-risk items remain intentionally broad because the canonical evidence proves fragmentation, not yet the final target state.

Validation commands: `git rev-parse HEAD`; `python -X utf8 -c "from pathlib import Path; import re; text=Path(r'knowledge/system-atlas/workflows/WORKFLOW_GAPS.md').read_text(encoding='utf-8'); print(len(re.findall(r'(?m)^\\d+\\. ', text)))"`; `python -X utf8 -c "import yaml, pathlib; yaml.safe_load(pathlib.Path(r'knowledge/system-atlas/workflows/_raw/subagents/gaps/gap_registry_preview.yaml').read_text(encoding='utf-8')); print('yaml_ok')"`.

Repo SHA: `beb8309f52576df181c04e965e1353aedeba9de1`

Timestamp: `2026-07-30T22:22:44.7551660+02:00`

## Summary

- Canonical legacy items counted: `48`
- Proposed atomic gaps: `78`
- Legacy items split into more than one atomic gap: `19`
- One-to-one legacy items: `29`

## Merged Legacy Items

- `1` -> 4 atomic gaps
- `2` -> 3 atomic gaps
- `3` -> 2 atomic gaps
- `4` -> 2 atomic gaps
- `5` -> 3 atomic gaps
- `6` -> 3 atomic gaps
- `7` -> 3 atomic gaps
- `8` -> 2 atomic gaps
- `9` -> 3 atomic gaps
- `10` -> 3 atomic gaps
- `11` -> 2 atomic gaps
- `19` -> 2 atomic gaps
- `20` -> 2 atomic gaps
- `22` -> 3 atomic gaps
- `28` -> 2 atomic gaps
- `32` -> 4 atomic gaps
- `36` -> 2 atomic gaps
- `40` -> 2 atomic gaps
- `46` -> 2 atomic gaps

## Migration

1. `1` -> `gap.case-scoped-rag-vs-global-rag.query-anything-rag-branch-call-signature-broken`, `gap.case-scoped-rag-vs-global-rag.query-anything-similar-cases-import-broken`, `gap.case-scoped-rag-vs-global-rag.query-anything-counts-source-errors-as-success`, `gap.case-scoped-rag-vs-global-rag.query-anything-returns-ok-when-all-sources-fail`
2. `2` -> `gap.learning-loop-divergence-to-candidate-evidence-only.fetch-open-proposals-uses-tuple-rows`, `gap.learning-loop-divergence-to-candidate-evidence-only.row-to-proposal-drops-fields-on-tuple-rows`, `gap.learning-loop-divergence-to-candidate-evidence-only.classify-operator-response-misclassifies-approve-when-proposal-type-missing`
3. `3` -> `gap.hitl-proposal-approval-dual-path.hitl-gmail-dry-run-reports-executed-true`, `gap.hitl-proposal-approval-dual-path.hitl-gmail-decision-status-does-not-distinguish-dry-run-from-live`
4. `4` -> `gap.agent-graph-execute-run.agent-concurrency-error-swallowed-as-generic-failure`, `gap.agent-graph-execute-run.cas-conflict-mislabeled-as-agent-dry-run`
5. `5` -> `gap.case-engagement-resolve-and-agent-handoff.case-intelligence-stage-exceptions-are-swallowed`, `gap.case-engagement-resolve-and-agent-handoff.case-intelligence-failure-collapses-to-empty-agent-signal`, `gap.case-engagement-resolve-and-agent-handoff.case-intelligence-failure-preserves-reconciled-terminal-state-without-retry`
6. `6` -> `gap.daszek-feed-push-no-retry.feed-push-has-no-durable-retry`, `gap.calendar-two-worlds-of-visits.customer-proposed-date-risk-is-cli-only`, `gap.calendar-two-worlds-of-visits.schedule-visit-does-not-create-real-calendar-event`
7. `7` -> `gap.learning-loop-divergence-to-candidate-evidence-only.approved-learning-rules-affect-only-conditional-precedent-enrichment`, `gap.learning-loop-divergence-to-candidate-evidence-only.business-outcome-capture-missing`, `gap.learning-loop-divergence-to-candidate-evidence-only.auto-approve-bypasses-confidence-threshold-on-observation-volume`
8. `8` -> `gap.learning-loop-divergence-to-candidate-evidence-only.get-win-rate-uses-nonexistent-won-status`, `gap.learning-loop-divergence-to-candidate-evidence-only.revenue-forecast-consumes-broken-win-rate`
9. `9` -> `gap.hitl-proposal-approval-dual-path.materialize-side-effect-runs-before-approval-persistence`, `gap.hitl-proposal-approval-dual-path.materialize-post-effect-errors-leave-proposal-pending-and-rerunnable`, `gap.hitl-proposal-approval-dual-path.materialize-path-lacks-durable-effect-receipt-before-post-effect-failures`
10. `10` -> `gap.hitl-proposal-approval-dual-path.materialize-idempotency-enforced-only-for-composite-plan`, `gap.hitl-proposal-approval-dual-path.materialize-idempotency-wrapper-silently-noops-without-db-url`, `gap.hitl-proposal-approval-dual-path.materialize-idempotency-records-only-ok-results`
11. `11` -> `gap.hitl-proposal-approval-dual-path.hitl-approve-ignores-operator-draft-payload`, `gap.hitl-proposal-approval-dual-path.bridge-queue-send-ignores-operator-draft-payload`
12. `12` -> `gap.hitl-proposal-approval-dual-path.hitl-clarification-approval-contract-lacks-answer-payload-channel`
13. `13` -> `gap.hitl-proposal-approval-dual-path.proposal-execution-restart-recovery-is-inconsistent-across-lifecycles`
14. `14` -> `gap.case-scoped-rag-vs-global-rag.gmail-agent-has-no-runtime-consumer-for-company-rag-service`
15. `15` -> `gap.gmail-signal-worker-loop.shared-mailbox-polled-by-two-independent-workers`
16. `16` -> `gap.hitl-proposal-approval-dual-path.proposal-execution-lifecycle-fragmentation-persists`
17. `17` -> `gap.case-engagement-resolve-and-agent-handoff.threadpool-executor-is-serialized-by-immediate-result-awaits`
18. `18` -> `gap.case-engagement-resolve-and-agent-handoff.action-planning-precedes-full-understanding`
19. `19` -> `gap.top-instal-generator-offer-document.legacy-direct-config-generation-path-remains-live`, `gap.top-instal-generator-offer-document.document-converter-path-has-two-live-modes`
20. `20` -> `gap.daszek-command-outbox-drain.db-command-outbox-has-no-confirmed-live-producer`, `gap.daszek-command-outbox-drain.live-bridge-command-flow-still-depends-on-jsonl-queue`
21. `21` -> `gap.case-engagement-resolve-and-agent-handoff.finalize-case-persists-state-in-nontransactional-multiwrite-sequence`
22. `22` -> `gap.calendar-two-worlds-of-visits.create-calendar-event-action-proposal-has-no-producer`, `gap.calendar-two-worlds-of-visits.visit-reschedule-flow-has-no-confirmed-implementation`, `gap.calendar-two-worlds-of-visits.visit-cancel-flow-has-no-confirmed-implementation`
23. `23` -> `gap.sla-watcher-decision-escalation.sla-watcher-has-no-confirmed-automatic-trigger`
24. `24` -> `gap.calendar-two-worlds-of-visits.calendar-signal-source-kind-does-not-match-registered-handler`
25. `25` -> `gap.agent-graph-turn-loop.preplan-subagent-selection-cannot-activate-document-or-draft-scopes`
26. `26` -> `gap.agent-graph-turn-loop.semantic-policy-divergence-is-observed-but-never-enforced`
27. `27` -> `gap.hitl-proposal-approval-dual-path.reconcile-warnings-reach-rest-response-but-have-no-ui-consumer`
28. `28` -> `gap.hitl-proposal-approval-dual-path.bridge-queue-failures-have-no-retry-or-dead-letter`, `gap.daszek-command-outbox-drain.bridge-queue-failed-rows-become-operator-invisible`
29. `29` -> `gap.learning-loop-divergence-to-candidate-evidence-only.world-model-producer-pipeline-has-no-callers`
30. `30` -> `gap.agent-graph-turn-loop.request-human-handoff-handler-has-no-exposed-schema-or-caller`
31. `31` -> `gap.kalk-top-calculate-offer-pipeline.call-kalk-top-quote-schema-advertises-ignored-arguments`
32. `32` -> `gap.hitl-proposal-approval-dual-path.materialize-link-existing-has-no-confirmed-creator`, `gap.hitl-proposal-approval-dual-path.materialize-create-case-has-no-confirmed-creator`, `gap.hitl-proposal-approval-dual-path.materialize-create-artifact-has-no-confirmed-creator`, `gap.hitl-proposal-approval-dual-path.materialize-defer-operator-has-no-confirmed-creator`
33. `33` -> `gap.agent-graph-turn-loop.extract-facts-from-text-cannot-update-existing-fact-value`
34. `34` -> `gap.calendar-two-worlds-of-visits.calendar-risk-has-three-independent-implementations`
35. `35` -> `gap.agent-graph-turn-loop.action-dictionary-resolution-docs-conflict-and-adjudication-incomplete`
36. `36` -> `gap.rag-chat-asystent-query-and-ingest-pipeline.rag-widget-defaults-to-vps-api-url-in-local-docker`, `gap.rag-chat-asystent-query-and-ingest-pipeline.local-stack-has-no-automated-rag-api-url-override`
37. `37` -> `gap.rag-chat-asystent-query-and-ingest-pipeline.graphrag-community-summary-enrichment-has-no-callers`
38. `38` -> `gap.fast-kalk-lead-widget-calculate-register-dispatch.customer-visible-price-is-fuzzed-range-not-canonical-total`
39. `39` -> `gap.api-surface.deprecation-metadata-is-applied-inconsistently-across-legacy-routes`
40. `40` -> `gap.cross-cutting.best-effort-no-durable-retry-is-a-systemic-architecture-pattern`, `gap.gmail-signal-worker-loop.gmail-signal-stage-failures-have-no-per-signal-retry`
41. `41` -> `gap.cieplo-orchestrator-intake-to-review-email.failed-final-state-name-overstates-recoverability`
42. `42` -> `gap.top-instal-generator-offer-document.generator-success-status-masks-docx-fallback-degradation`
43. `43` -> `gap.daszek-feed-push-no-retry.operational-feed-validation-warnings-have-no-ui-consumer`
44. `44` -> `gap.daszek-feed-push-no-retry.feed-quality-readonly-has-no-ui-consumer`
45. `45` -> `gap.case-engagement-resolve-and-agent-handoff.agent-runtime-enabled-branch-depends-on-loader-order`
46. `46` -> `gap.fast-kalk-lead-widget-calculate-register-dispatch.fast-kalk-treats-docx-fallback-as-pdf-ready`, `gap.cieplo-orchestrator-intake-to-review-email.cieplo-treats-docx-fallback-as-pdf-ready`
47. `47` -> `gap.fast-kalk-lead-widget-calculate-register-dispatch.fast-kalk-lacks-direct-end-to-end-test-for-lead-to-dispatch`
48. `48` -> `gap.cieplo-orchestrator-intake-to-review-email.mocked-e2e-test-fails-at-collection`
