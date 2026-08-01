# EARLY_DECISION_QUEUE.md

Status: `REQUIRED_BEFORE_DECISION_DEPENDENT_WORK`

These decisions are intentionally extracted ahead of implementation because they determine whether a mechanism is repaired, removed or replaced.

## Frozen Invariants

These are not open decisions anymore:

- Gmail API remains read-only.
- Google Calendar remains read-only.
- Node B does not send Gmail, create Gmail drafts, or create/update/delete Google Calendar events.
- `proposed_visit` is proposal-only.
- `scheduled_visit` requires an ingested real `calendar_event_id`.
- `PDF_READY` means a verified PDF only.
- DOCX fallback is an explicit degraded result, never a synonym for PDF success.

| decision_id | decision | default recommendation | blocks clusters | representative gaps |
| --- | --- | --- | --- | --- |
| `DQ-01` | Company knowledge contract | prove the live caller need first; default to case-scoped RAG only, and add a dedicated Node B -> `rag-chat-asystent` adapter only if a real capability requires explicit company knowledge with truthful per-source status | `RC-01`, `RC-15` | `gap.case-scoped-rag-vs-global-rag.*`, `gap.rag-chat-asystent-query-and-ingest-pipeline.graphrag-community-summary-enrichment-has-no-callers` |
| `DQ-02` | Canonical proposal/execution lifecycle | choose one canonical sequence: persist decision intent -> execute retained side effect -> persist durable receipt -> project state; all alternative paths become adapters or are removed | `RC-09`, `RC-10`, `RC-12` | `gap.hitl-proposal-approval-dual-path.*`, `gap.agent-graph-turn-loop.semantic-policy-divergence-is-observed-but-never-enforced` |
| `DQ-03` | Materialize scope by proposal type | retain only proposal types with a confirmed creator, confirmed business need and proofable side-effect contract; remove executor-only dead branches by default | `RC-09`, `RC-14` | `gap.hitl-proposal-approval-dual-path.materialize-*-has-no-confirmed-creator` |
| `DQ-04` | Residual calendar lifecycle under the frozen read-only contract | keep the read-only event-linked lifecycle invariant; decide only whether residual reschedule/cancel concepts stay as proposal-only operator states or are removed, and collapse source-kind plus risk handling to one live model | `RC-07` | `gap.calendar-two-worlds-of-visits.visit-*-flow-has-no-confirmed-implementation`, `gap.calendar-two-worlds-of-visits.calendar-risk-has-three-independent-implementations` |
| `DQ-05` | Learning scope | near-term wave keeps learning as operator-feedback correction plus truthful business-outcome capture; world-model and behavior steering stay disabled until they have producers and outcome data | `RC-08` | `gap.learning-loop-divergence-to-candidate-evidence-only.approved-learning-rules-affect-only-conditional-precedent-enrichment`, `gap.learning-loop-divergence-to-candidate-evidence-only.world-model-producer-pipeline-has-no-callers` |
| `DQ-06` | Projection transport architecture | first prove the live producer, consumer, drain, retry and failed-row visibility state of the DB outbox and JSONL bridge; only then choose whether to finish, replace, retain temporarily or remove a transport path | `RC-06`, `RC-11` | `gap.daszek-command-outbox-drain.db-command-outbox-has-no-confirmed-live-producer`, `gap.hitl-proposal-approval-dual-path.bridge-queue-failures-have-no-retry-or-dead-letter` |
| `DQ-07` | Degraded document readiness vocabulary and consumer alignment | keep the `PDF_READY` invariant; decide whether the retained degraded contract is a single explicit DOCX-degraded state or a broader typed multi-format readiness model, then align all consumers to it | `RC-13` | `gap.top-instal-generator-offer-document.generator-success-status-masks-docx-fallback-degradation`, `gap.fast-kalk-lead-widget-calculate-register-dispatch.fast-kalk-treats-docx-fallback-as-pdf-ready`, `gap.cieplo-orchestrator-intake-to-review-email.cieplo-treats-docx-fallback-as-pdf-ready` |
| `DQ-08` | Retry policy by side-effect class | irreversible side effects require durable receipt and replay semantics; projection-only pushes may stay best-effort only if failure is surfaced and recoverable; manual-only retry must be named honestly | `RC-06`, `RC-11` | `gap.daszek-feed-push-no-retry.feed-push-has-no-durable-retry`, `gap.gmail-signal-worker-loop.gmail-signal-stage-failures-have-no-per-signal-retry`, `gap.sla-watcher-decision-escalation.sla-watcher-has-no-confirmed-automatic-trigger` |
| `DQ-09` | Operator warning contract | define one typed warning model: operator-facing warnings must render in UI; telemetry-only warnings stay out of operator-facing contracts | `RC-10`, `RC-06` | `gap.hitl-proposal-approval-dual-path.reconcile-warnings-reach-rest-response-but-have-no-ui-consumer`, `gap.daszek-feed-push-no-retry.operational-feed-validation-warnings-have-no-ui-consumer`, `gap.daszek-feed-push-no-retry.feed-quality-readonly-has-no-ui-consumer` |
| `DQ-10` | Fact supersession model | mutable facts use supersession or versioning, not `ON CONFLICT DO NOTHING`; stale facts remain readable historically but not silently current | `RC-12` | `gap.agent-graph-turn-loop.extract-facts-from-text-cannot-update-existing-fact-value` |
| `DQ-11` | Mailbox ingest ownership | prove current pollers, labels, cursors, dedupe and recovery first; then choose between one authoritative poller, two pollers with explicit split scope and shared dedupe, or one raw ingress routing model | `RC-11` | `gap.gmail-signal-worker-loop.shared-mailbox-polled-by-two-independent-workers`, `gap.gmail-signal-worker-loop.gmail-signal-stage-failures-have-no-per-signal-retry` |
| `DQ-12` | Legacy generator `direct-config` survival | prove whether the legacy `direct-config` path has a live consumer; remove it by default if no retained capability requires it | `RC-13` | `gap.top-instal-generator-offer-document.legacy-direct-config-generation-path-remains-live` |
| `DQ-15` | Scheduler ownership | prove which process, if any, is the actual automatic caller for SLA, retry and temporal signals; choose one owner, a bounded hybrid, or explicitly keep manual-only semantics | `RC-11`, `RC-16` | `gap.sla-watcher-decision-escalation.sla-watcher-has-no-confirmed-automatic-trigger` |
| `DQ-16` | GraphRAG enrichment future | prove a real caller and a measurable outcome before keeping GraphRAG enrichment; otherwise park or remove the dormant path | `RC-01`, `RC-16` | `gap.rag-chat-asystent-query-and-ingest-pipeline.graphrag-community-summary-enrichment-has-no-callers` |

## Current Decision Updates

- `DQ-01`: `RESOLVED_LOCAL`
  - selected path: `CASE_SCOPED_RETRIEVAL_ONLY`
  - retained Node B retrieval contract: `search_rag_knowledge`
  - `query_anything` is retired from planner/schema/runtime exposure
  - no dedicated Node B -> `rag-chat-asystent` company-knowledge adapter was kept in Wave 2
- `DQ-06`: `RESOLVED_LOCAL`
  - selected path: `REMOVE_DORMANT_DB_OUTBOX`
  - current live transport: JSONL `bridge_queue` only
- `DQ-08`: `RESOLVED_LOCAL`
  - bridge queue has retry / dead-letter / actionable semantics
  - SLA escalation is no longer manual-only
  - projection-only feed push remains best-effort with explicit telemetry/proof logging and heartbeat recovery
  - automatic per-signal Gmail replay is `DEFERRED_WITH_PROOF` because retrying irreversible stages requires later idempotency hardening
- `DQ-09`: `RESOLVED_LOCAL`
  - operator-facing failures in Wave 2 are the typed bridge/actionable failures and critical execution failures already exposed by the feed/API contract
  - feed validation and quality-readonly warnings are telemetry/proof-only in Wave 2 and do not require a UI consumer
- `DQ-11`: `RESOLVED_LOCAL`
  - current local owner: Node B `signal-worker`
  - Daszek mail-ingest cron is cleared when disabled
  - Cieplo poller remains disabled code path, not an active local owner
- `DQ-15`: `RESOLVED_LOCAL`
  - selected scheduler owner: `signal-worker` idle maintenance loop
- `DQ-07`: `RESOLVED_LOCAL`
  - selected path: typed readiness contract with `READY` versus `DEGRADED`
  - `PDF_READY` remains reserved for verified PDF only
  - `fast-kalk` now fails closed on degraded or unverified PDF responses
  - `cieplo-orchestrator` now uses `DOCUMENT_READY_DEGRADED` instead of overstating `PDF_READY`
- `DQ-12`: `RESOLVED_LOCAL`
  - current live consumer for `direct-config`: legacy generator UI / `simple_generate`
  - selected path: retain `direct-config` as explicit legacy mode under the same readiness contract
  - removal is deferred to a later retirement wave, not claimed in Wave 2
- `DQ-16`: `RESOLVED_LOCAL`
  - selected path: `REMOVE_DORMANT_ENRICHMENT`
  - `build_community_summary` had no proven caller, no route and zero GitNexus upstream impact
  - live `/chat` graph evidence and company-context prompt augmentation remain outside this removal
- `DQ-04`: `RESOLVED_LOCAL`
  - selected path: `READ_ONLY_EVENT_LINKED_LIFECYCLE_PLUS_PROPOSAL_ONLY_RESCHEDULE_CANCEL`
  - Calendar ingest emits `source_kind=calendar`, matching the registered handler
  - `scheduled_visit` requires an active ingested event with real `calendar_event_id`
  - proposed date, reschedule and cancel are proposal-only or externally observed states
  - Node B Calendar create/update/delete remains fail-closed

## Exit Criterion

No package or cluster referenced in the table above may move from `PROPOSED` to `READY` until its blocking decision is resolved or explicitly waived with current proof.

## Wave 2 Invariants

- Wave 2 may not reintroduce Gmail send, Gmail draft creation, Calendar create/update/delete, or shadow success semantics for those removed write paths.
- Decision closure must be based on current proof, not on historical intent or stale documentation.
- `prove -> decide -> implement` is the default package flow.
- Only a proven large migration, cross-repo cutover, or data-repair blast radius may defer implementation into a later wave.
