# WAVE_02_PROBLEM_ANALYSIS.md

Status: `ANALYZED`

Wave: `WAVE-02 - JIT Decision Proofs`

Execution state:

- `WAVE_01_COMPLETE`
- `WAVE_02_ANALYSIS_COMPLETE`
- `WAVE_02_CLOSED`
- `CODE_MUTATION_COMPLETE_LOCAL`

Current package snapshot:

- `RP-14`: `CLOSED`
- `RP-15`: `CLOSED`
- `RP-06`: `CLOSED`
- `RP-12`: `CLOSED`
- `RP-01`: `CLOSED`
- `RP-20`: `CLOSED`
- `RP-07`: `CLOSED`

## Scope

Wave 2 covers the decision-dependent packages:

- `RP-01` Knowledge aggregator replacement
- `RP-06` Durable Daszek transport
- `RP-07` Calendar canonical lifecycle
- `RP-12` Mailbox intake ownership
- `RP-14` Document readiness contract
- `RP-15` Temporal trigger ownership
- `RP-20` GraphRAG enrichment decision

Wave 2 is not a documentation-only wave. Its default job is:

`prove -> decide -> implement -> test -> runtime proof -> close`

Only if proof exposes a large migration, risky cutover or non-local data repair may a package stop at `prove -> decide` and be promoted into a later implementation wave.

## Immutable Constraints

- Workflow Registry v1 remains immutable.
- Gmail API is read-only.
- Google Calendar is read-only.
- Node B does not send Gmail, create Gmail drafts, or create/update/delete Google Calendar events.
- `proposed_visit` is a proposal state only.
- `scheduled_visit` requires an ingested real `calendar_event_id`.
- Wave 2 may produce proof artifacts, decisions and package execution records, but it must not create a new planning layer unless proof forces that split.

## Cross-Package Problems

### 1. Stale planning assumptions still exist

The current repair overlay still contained three stale assumptions before this update:

- `DQ-04` still assumed a write-capable Calendar lifecycle.
- `DQ-06` was biased toward replacing the transport before runtime proof of the existing DB outbox and JSONL bridge.
- `DQ-11` preselected "one authoritative poller" before proving the actual current ownership model.

These assumptions would have pushed Wave 2 into premature architecture choices instead of proof-driven closure.

### 2. Proof readiness is lowest exactly where the blast radius is highest

The Wave 2 clusters with the largest cross-repo or state blast radius have low proof readiness:

| Cluster | Package | Proof readiness | Why this is a problem |
| --- | --- | --- | --- |
| `RC-06` | `RP-06` | `LOW` | transport failure semantics are live-path relevant, but producer/consumer/retry state is not yet frozen with current proof |
| `RC-07` | `RP-07` | `LOW` | calendar semantics were historically split across shadow paths and older write assumptions |
| `RC-11` | `RP-12`, `RP-15` | `LOW` | current pollers, retries and temporal callers are ambiguous, so ownership decisions would otherwise be guesses |

Wave 2 therefore has to start with runtime-read-only discovery, not with code edits.

### 3. Some Wave 2 packages overlap on the same operational decision surface

The packages are not independent:

- `RP-06`, `RP-12` and `RP-15` all touch ownership, retry and trigger semantics.
- `RP-01` and `RP-20` both touch the RAG/retrieval surface and can easily duplicate work.
- `RP-07` and `RP-14` both require one truthful state vocabulary and can create downstream projection drift if decided separately.

Without a shared decision sequence, one package could invalidate another package's implementation plan.

### 4. Wave 1 changed the baseline for Wave 2

Wave 1 already closed the live Google write-shaped paths by making them fail-closed. That changes Wave 2 scope:

- `RP-07` does not reopen Calendar writes.
- `RP-07` now focuses on read-only event-linked lifecycle semantics, source-kind routing and removal/consolidation of remaining shadow branches.
- `RP-01` must not reopen the local-routing defects already fixed under `RP-19`.

### 5. Historical data impact is uneven and must remain hypothesis-first until proof

| Package | Historical data impact | Consequence |
| --- | --- | --- |
| `RP-01` | `LIKELY_NONE` | mostly contract and caller cleanup, unless proof finds a hidden live consumer |
| `RP-06` | `NO_ACTION_REQUIRED` | local proof showed no active recovery campaign, DB outbox was dormant, and feed push is projection-only best-effort telemetry/proof rather than an irreversible side-effect queue |
| `RP-07` | `NO_ACTION_REQUIRED` | code now rejects textual scheduled_visit without calendar_event_id; projections converge naturally from active read-only Calendar events without destructive data mutation |
| `RP-12` | `NO_ACTION_REQUIRED` | local proof showed Node B `signal-worker` as the active local intake owner and no proven duplicate-polling contamination |
| `RP-14` | `LIKELY_MANUAL_REVIEW` | document-readiness history may remain semantically ambiguous even after the contract is fixed |
| `RP-15` | `TBD_BY_PROOF` | scheduler-owned signals may need explicit quarantine, reclassification, or no data action at all |
| `RP-20` | `LIKELY_NONE` | remove-or-park decision only unless a real caller is found |

This means Wave 2 cannot define only code tasks; it must also define the expected data follow-up model.

## Package-by-Package Problem Analysis

### `RP-01` Knowledge aggregator replacement

Target gaps:

- `gap.case-scoped-rag-vs-global-rag.query-anything-rag-branch-call-signature-broken`
- `gap.case-scoped-rag-vs-global-rag.query-anything-similar-cases-import-broken`
- `gap.case-scoped-rag-vs-global-rag.query-anything-counts-source-errors-as-success`
- `gap.case-scoped-rag-vs-global-rag.query-anything-returns-ok-when-all-sources-fail`
- `gap.case-scoped-rag-vs-global-rag.gmail-agent-has-no-runtime-consumer-for-company-rag-service`

Current problem:

- the generic retrieval capability is over-claimed;
- its branches are partially broken;
- top-level success semantics are false-success prone;
- the explicit company-knowledge path has no proven live consumer.

Why it is still open:

- local routing safety was fixed in Wave 1, but that did not answer whether the generic retrieval capability should survive;
- current docs still mix case-scoped retrieval, company knowledge, and GraphRAG enrichment.

Wave 2 output required:

- prove whether there is a live caller that actually needs company knowledge beyond case-scoped retrieval;
- decide whether `query_anything` is removed, replaced with an explicit adapter, or narrowed to one retained source contract;
- implement the surviving contract in the same wave unless proof shows a larger migration than a narrow branch removal or adapter introduction.

### `RP-06` Durable Daszek transport

Target gaps:

- `gap.daszek-feed-push-no-retry.feed-push-has-no-durable-retry`
- `gap.daszek-command-outbox-drain.live-bridge-command-flow-still-depends-on-jsonl-queue`
- `gap.hitl-proposal-approval-dual-path.bridge-queue-failures-have-no-retry-or-dead-letter`
- `gap.daszek-command-outbox-drain.bridge-queue-failed-rows-become-operator-invisible`
- `gap.daszek-feed-push-no-retry.operational-feed-validation-warnings-have-no-ui-consumer`
- `gap.daszek-feed-push-no-retry.feed-quality-readonly-has-no-ui-consumer`

Current problem:

- the operator-facing projection contract promises convergence without proving durable retry or visible failure;
- JSONL remains live;
- the DB outbox is not yet proven live or dead;
- operator warning semantics are not yet typed.

Why it is still open:

- replacing transport before proving producer/drain reality could cause unnecessary migration work;
- warning UI work depends on `DQ-09`;
- retry and replay semantics depend on `DQ-08`.

Wave 2 output required:

- classify the DB outbox as viable, dormant, or removable;
- classify JSONL as temporary bridge, canonical path, or removal target;
- close `DQ-06`, `DQ-08` and `DQ-09`;
- implement the retained transport path in the same wave if proof stays local;
- defer only the parts that require a proven large migration, replay campaign or cross-repo cutover.

### `RP-07` Calendar canonical lifecycle

Target gaps still relevant after Wave 1:

- `gap.calendar-two-worlds-of-visits.customer-proposed-date-risk-is-cli-only`
- `gap.calendar-two-worlds-of-visits.visit-reschedule-flow-has-no-confirmed-implementation`
- `gap.calendar-two-worlds-of-visits.visit-cancel-flow-has-no-confirmed-implementation`
- `gap.calendar-two-worlds-of-visits.calendar-signal-source-kind-does-not-match-registered-handler`
- `gap.calendar-two-worlds-of-visits.calendar-risk-has-three-independent-implementations`

Wave 1 already closed the write-shaped live-path claims for:

- `gap.calendar-two-worlds-of-visits.schedule-visit-does-not-create-real-calendar-event`
- `gap.calendar-two-worlds-of-visits.create-calendar-event-action-proposal-has-no-producer`

Current problem:

- calendar semantics are still split between proposal-only text states, ingest routing, and multiple risk models;
- older planning artifacts still implied event creation from Node B, which is no longer allowed.

Why it is still open:

- the architectural boundary changed: Node B cannot write to Calendar;
- reschedule/cancel now require a read-only compatible interpretation, not a write-path completion.

Wave 2 output required:

- define one read-only visit lifecycle where `scheduled_visit` exists only after ingest of a real external event;
- decide which reschedule/cancel concepts survive as operator proposals and which are removed as dead write-shaped branches;
- normalize one risk model and one source-kind routing contract.
- implement the retained read-only lifecycle and dead-branch cleanup in the same wave unless proof exposes a larger migration.

### `RP-12` Mailbox intake ownership

Target gaps:

- `gap.gmail-signal-worker-loop.shared-mailbox-polled-by-two-independent-workers`
- `gap.gmail-signal-worker-loop.gmail-signal-stage-failures-have-no-per-signal-retry`

Current problem:

- intake ownership is ambiguous;
- the current number of active pollers is not frozen with runtime proof;
- retry semantics depend on the chosen ownership model.

Why it is still open:

- the older plan jumped too early to a single authoritative poller;
- there is not yet a current proof set for labels, cursors, dedupe and recovery across the real live path.

Wave 2 output required:

- prove the actual current ownership model;
- close `DQ-11`;
- separate ownership choice from retry policy choice;
- implement the retained intake path in the same wave if the proof stays local;
- split retry and recovery into a later package only if the proof shows a larger migration or data repair.

### `RP-14` Document readiness contract

Target gaps:

- `gap.top-instal-generator-offer-document.legacy-direct-config-generation-path-remains-live`
- `gap.top-instal-generator-offer-document.document-converter-path-has-two-live-modes`
- `gap.cieplo-orchestrator-intake-to-review-email.failed-final-state-name-overstates-recoverability`
- `gap.top-instal-generator-offer-document.generator-success-status-masks-docx-fallback-degradation`
- `gap.fast-kalk-lead-widget-calculate-register-dispatch.fast-kalk-treats-docx-fallback-as-pdf-ready`
- `gap.cieplo-orchestrator-intake-to-review-email.cieplo-treats-docx-fallback-as-pdf-ready`

Current problem:

- producer and consumers do not share one truthful readiness vocabulary;
- legacy generator branches may still be live;
- terminal naming overstates recoverability in Cieplo.

Why it is still open:

- removing the wrong generation branch could break a still-used path;
- the correct contract must be chosen across three repositories, not within one file.

Wave 2 output required:

- close `DQ-07` and `DQ-12`;
- classify whether DOCX fallback stays as an explicit degraded contract or whether `PDF_REQUIRED` becomes the only success state;
- produce a single cross-repo readiness vocabulary and consumer matrix;
- implement the retained vocabulary and consumer alignment in the same wave unless proof shows a larger migration.

### `RP-15` Temporal trigger ownership

Target gaps:

- `gap.sla-watcher-decision-escalation.sla-watcher-has-no-confirmed-automatic-trigger`

Current problem:

- there is no current proof that an automatic trigger actually exists;
- the owner for SLA/retry/temporal signals is not yet canonical.

Why it is still open:

- this package is impossible to implement honestly before proving whether the capability is automatic at all;
- it overlaps with `RP-12` on ownership and with `RP-06` on retry semantics.

Wave 2 output required:

- close `DQ-15`;
- classify the capability as automatic, manual-only, or mixed;
- if automatic survives, define one owner and one trigger path;
- if not, record explicit manual-only semantics instead of pseudo-automation.
- implement the retained ownership path in the same wave if proof shows a local fix rather than a larger cutover.

### `RP-20` GraphRAG enrichment decision

Target gaps:

- `gap.rag-chat-asystent-query-and-ingest-pipeline.graphrag-community-summary-enrichment-has-no-callers`

Current problem:

- the enrichment path has no proven caller;
- keeping it alive without a user journey risks accidental architecture drag.

Why it is still open:

- it overlaps with `RP-01`, but it is not the same decision;
- removing it too early without proof could erase a future intended capability, while keeping it without proof preserves dead code.

Wave 2 output required:

- close `DQ-16`;
- classify the path as removed, parked, or promoted into an explicit measured capability;
- if promoted, bind it to one real caller and one proofable user journey.
- if no caller exists, remove or park it in the same wave instead of promoting it into a later planning package.

## Recommended Execution Order

1. Stage 0: freeze invariants and validate the overlay.
2. Stage 1A: `RP-06`, `RP-12`, `RP-15`
   - shared proof lane for transport, ownership, retry and temporal triggers.
3. Stage 1B: `RP-07`
   - isolated calendar read-only lane can run in parallel because the boundary is already frozen as an invariant.
4. Stage 1C: `RP-14`
   - document readiness lane can run in parallel because it does not share production files with the ownership lane.
5. Stage 2: `RP-01`, `RP-20`
   - retrieval and GraphRAG decisions must close together to avoid duplicate RAG redesign.
6. Stage 3: implement immediately where proof stays local; defer only proven large migrations.

## Wave 2 Success Contract

Wave 2 is ready to close only if all of the following are true:

- each scoped package has a current proof artifact;
- each blocking `DQ-*` decision above is resolved or explicitly waived with proof;
- each package either closes in-wave or has a proof-backed reason for deferring implementation;
- packages no longer contain stale write assumptions for Gmail or Calendar;
- historical-data impact is classified per package;
- no Wave 2 artifact creates a new planning layer without a proof-backed migration reason.

## Wave 2 Closeout Result

Wave 2 is closed locally.

- Closed packages: `RP-01`, `RP-06`, `RP-07`, `RP-12`, `RP-14`, `RP-15`, `RP-20`.
- Final exit gate artifacts: `_raw/wave-02/exit-gate/`.
- Workflow Registry v1 remains immutable and final-validator PASS.
- Deferred with proof: automatic per-signal replay for `RP-12`; it is intentionally held for later idempotency/recovery hardening rather than treated as an unresolved Wave 2 residual.
