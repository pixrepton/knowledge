# REPAIR_PROGRAM_PLAN.md

Status: `PLANNING_READY`

Date: `2026-07-30`

Scope: executable repair overlay for the immutable Workflow Registry v1 baseline in `knowledge/system-atlas/workflows/`.

This directory intentionally does **not** create `CAPABILITY_REGISTRY.yaml` yet. The capability definitions below are planning contracts only. The first machine-written registry should be created only after the operator accepts this plan structure and the Early Decision Queue.

## 1. Baseline And Invariants

- Workflow Registry v1 remains the immutable baseline.
- `WORKFLOW_GAPS.yaml` and `WORKFLOW_GAPS.md` remain historical truth for the audit wave; they are not mutated during repairs.
- Repair execution must live in an append-only overlay.
- Capability status is a generated view from repairs and proofs; it is not manually maintained.
- Workflow Registry v2 is a new snapshot created only after a repair wave closes.
- Node B (`gmail-agent`) remains operational Source of Truth for case, engagement, proposal and mailbox state.
- Daszek remains projection-only and bounded HITL, not a write Source of Truth.
- `kalk-top` remains owner of HVAC logic and canonical `OfferDTO`.
- Runtime proof honesty remains mandatory: static closure cannot be misreported as runtime closure.

## 2. Disposition Framework For 78 Gaps

Every gap is first classified by disposition before any implementation work starts.

`FIX`
: preserve the mechanism and repair the defect without changing its intended contract.

`REMOVE`
: retire a dead, redundant or non-surviving mechanism instead of repairing it.

`REPLACE`
: keep the capability, but swap the current mechanism for a new contract or transport.

`CONSOLIDATE`
: merge competing shapes, lifecycles or paths into one canonical contract before repairing details.

`PROVE_AT_RUNTIME`
: no code change first; gather decisive runtime proof because code-read evidence is insufficient.

`ACCEPT_RISK`
: keep current behavior intentionally, document the risk and exclude it from the repair wave.

`DEFER`
: acknowledged, but blocked by an earlier decision, migration or proof-enabling step.

`NO_ACTION`
: no repair target in the current wave; observation or documentation note only.

## 3. Capability Layers And Target Contracts

The plan uses four layers. They are intentionally not flattened into one list because business journeys, agent competencies, platform capabilities and assurances are different objects.

### 3.1 Business Capabilities

| capability_id | capability | trigger | preconditions | success evidence | failure semantics | non-goals |
| --- | --- | --- | --- | --- | --- | --- |
| `BIZ-01` | Customer email response | `customer_email_received`, operator resend/send request | case resolved, recipient confirmed, draft or clarification path available, policy gate resolved | durable `ExecutionResult`, provider receipt (`gmail_message_id` or explicit dry-run marker), snapshot updated, projection updated | no send-success on dry run, unknown side effect becomes `OUTCOME_UNKNOWN`, retry cannot duplicate send | autonomous price negotiation or policy override |
| `BIZ-02` | Lead to offer dispatch | widget `/chat`, `/calculate`, `/register` | kalk-top quote available, registry/os-event auth valid, generator readiness policy chosen | canonical `OfferDTO`, truthful artifact readiness, registry link persisted, os-event emitted | no `PDF_READY` when only DOCX fallback exists, partial cross-repo failure cannot look complete | making customer-visible fuzzy range equal canonical gross total |
| `BIZ-03` | Visit lifecycle management | calendar ingest, approved schedule/reschedule/cancel action | case/engagement resolved, calendar SoT chosen, executor reachable | real calendar event ID or explicit manual-only outcome, mailbox fact and projection converge | text fact alone is not success, unsupported reschedule/cancel returns explicit `NOT_AVAILABLE`, retry cannot duplicate event writes | silent calendar changes from plain narrative facts |
| `BIZ-04` | Operator review to safe side effect | approve, reject or clarify action proposal | canonical proposal lifecycle chosen, operator payload channel defined, idempotency active for retained writes | operator decision persisted, effect receipt durable, operator edits preserved, failed rows visible | pending-after-side-effect forbidden, partial success must emit receipt or `OUTCOME_UNKNOWN`, restart cannot replay blindly | preserving every historical proposal shape |
| `BIZ-05` | Case progress to commercial outcome | case lifecycle transition, operator outcome entry, business pulse query | case lifecycle canonical, outcome ownership chosen, fact supersession contract chosen | case status, win rate, revenue forecast and learning inputs agree with actual outcome data | stale facts cannot masquerade as current truth, missing outcomes remain explicit, downstream metrics cannot silently fabricate zeros | retrospective analytics beyond captured outcome fields |
| `BIZ-06` | Cieplo review offer flow | manual poll or retry of Cieplo workflow | kalk-top and generator reachable, review-email readiness policy chosen, retry contract explicit | workflow row advances with truthful state names, truthful artifact format and review-email receipt | `FAILED_FINAL` cannot mean retryable without explicit rename, `PDF_READY` forbidden for DOCX fallback, retry scope explicit | autonomous self-healing beyond approved retry entrypoints |

### 3.2 Agent Competencies

| capability_id | capability | trigger | preconditions | success evidence | failure semantics | non-goals |
| --- | --- | --- | --- | --- | --- | --- |
| `AGT-01` | Case understanding and gap detection | reconcile after signal normalization | case/engagement context accessible, understanding stage enabled | non-empty or explicitly degraded understanding payload, missing-info markers, provenance present | hidden stage exceptions forbidden, empty context must not look equivalent to successful no-change | solving business outcome capture inside understanding |
| `AGT-02` | Knowledge retrieval and use | planner or answer-generation asks for company or case knowledge | canonical RAG contract chosen, reachable tool/schema, scope defined | per-source status, truthful consulted-source count, usable evidence snippet(s) | no `ok` when all retrieval branches fail, dead branches removed or replaced, missing global RAG consumer explicit | preserving generic mega-tooling if specialist tools are better |
| `AGT-03` | Action planning and tool control | planner turn loop | policy and semantic controls available, tool schemas truthful, activation scopes reachable | chosen action reflects available tools and current understanding, divergence controls can block/escalate | observed divergence cannot remain telemetry-only forever, tool schema cannot advertise unavailable controls | maximizing parallelism at expense of correctness |
| `AGT-04` | Draft, clarification and operator-edit handling | draft generation, clarification approval, send approval | canonical draft contract chosen, operator payload field defined | operator free-text correction reaches the actual send path, clarification answer survives approval path | ignored operator payloads forbidden, dry-run and live send must differ, clarification with missing payload returns explicit contract error | supporting every historical draft lineage as equal |
| `AGT-05` | Fact correction and memory consistency | fact extraction, manual correction, downstream readback | fact supersession model chosen, durable fact ownership unchanged | corrected fact supersedes stale fact, downstream readers observe canonical current value and provenance | `ON CONFLICT DO NOTHING` cannot report success on no-op correction, stale facts cannot remain silently active | unbounded fact history redesign in the first wave |

### 3.3 Platform Capabilities

| capability_id | capability | trigger | preconditions | success evidence | failure semantics | non-goals |
| --- | --- | --- | --- | --- | --- | --- |
| `PLT-01` | Signal ingest and reconcile | Gmail/calendar/other signal arrival | one authoritative poller per mailbox/source, normalized signal handler reachable | raw observation, canonical signal row, processing attempt and reconcile outcome captured | one worker per mailbox/source, stage failure visibility preserved, per-signal retry policy explicit | multiple independent pollers racing on the same mailbox |
| `PLT-02` | Case/engagement resolution and snapshotting | reconcile before planner/agent handoff | correlation registry readable, snapshot store available | engagement snapshot saved, signal linked, finalize path truthful and durable | non-transactional multi-write cannot silently finalize success, degraded handoff must remain marked | collapsing all staging and finalize paths into one giant transaction without proof |
| `PLT-03` | Knowledge retrieval and RAG substrate | case-scoped or company-scoped retrieval request, ingest | canonical RAG architecture chosen, auth/routing configured | case-scoped and company-scoped retrieval both have truthful runtime contract, local routing deterministic | no dead generic branch kept alive by documentation alone, unreachable GraphRAG enrichments removed or isolated | blindly preserving all historic RAG entrypoints |
| `PLT-04` | Proposal and execution runtime | planner or operator creates/approves proposal | canonical lifecycle chosen, retained proposal types have creators and executors | proposal status, effect receipt and restart semantics agree across sync, bridge and materialize paths | side effect before durable decision forbidden, pending after side effect forbidden, dead executor-only types removed or reintroduced explicitly | keeping parallel proposal shapes without contract |
| `PLT-05` | Calendar integration | calendar ingest or approved visit action | source-kind routing canonical, write path chosen, Google Calendar executor reachable | ingest path, schedule/reschedule/cancel path and calendar risk model converge on one lifecycle | CLI-only richer logic cannot remain hidden while live paths stay binary, proposal-only shadows cannot impersonate implementation | using mailbox text facts as the primary calendar truth |
| `PLT-06` | Offer calculation and document generation | fast-kalk, Cieplo or direct generator request | canonical generator mode chosen, converter contract explicit | truthful format metadata, canonical readiness semantics, consumer handling aligned | DOCX fallback cannot be promoted as PDF-ready by status or consumer assumptions | supporting mutually inconsistent live generator modes forever |
| `PLT-07` | Projection and command transport | feed push, bridge command, operator dashboard refresh | projection transport chosen, failure visibility path present | feed rows, command rows and failed rows are durable enough for the agreed guarantee level | projection-only failures cannot be invisible, retry/no-retry contract explicit, dead DB outbox not repaired accidentally | promoting Daszek to write SoT |
| `PLT-08` | Learning and outcome substrate | operator action processed, outcome queried, world-model ingest | learning scope chosen, outcome data model defined | operator feedback, approved rules, win-rate and outcome capture serve the same learning contract | precedent-only enrichment cannot pretend to be behavior steering, producerless world-model cannot look available | full intelligence redesign in the first repair wave |

### 3.4 Assurances

| capability_id | capability | trigger | preconditions | success evidence | failure semantics | non-goals |
| --- | --- | --- | --- | --- | --- | --- |
| `ASR-01` | No false success | any side-effecting or externally visible action | canonical status vocabulary defined | top-level status and nested metadata agree, degraded branches visible | dry run, fallback, partial failure and concurrency conflict cannot look identical to success | adding verbose logging without changing semantics |
| `ASR-02` | Idempotency and durable receipts | irreversible write or external send | receipt store reachable, retained write types enumerated | duplicate attempt blocked or recognized from receipt, side-effect identity durable | no configuration-only silent downgrade of protection, non-`ok` partial success still receipt-bearing | pretending best-effort memory is idempotency |
| `ASR-03` | Retry, recovery and replay | transient failure, restart, manual retry | retry class chosen by side-effect type, replay entrypoint known | bounded retry/replay path, operator-visible failure state, restart-safe branch | fire-once behavior must be explicit, failed row cannot disappear, non-retryable must be named honestly | universal auto-retry everywhere |
| `ASR-04` | Config determinism and reachability | process start, local Docker validation, branch selection | one canonical config plane per runtime, route ownership clear | same config yields same branch selection, local stacks point local by default, dormant paths declared | loader order cannot change behavior, local validation cannot silently hit VPS | freezing every local convenience override forever |
| `ASR-05` | Proofability and operator visibility | test, runtime proof, dashboard readback | proof-enabling fields and UI surfaces exist | warnings visible, proof logs attributable, failed rows queriable, key journeys reproducible | lack of UI consumer or test harness remains open until repaired or explicitly accepted | replacing proof with narrative confidence |

## 4. Early Decision Queue

The following decisions must be made before selected repairs are allowed to start. The detailed packet list is in [EARLY_DECISION_QUEUE.md](./EARLY_DECISION_QUEUE.md).

| decision_id | decision | blocks |
| --- | --- | --- |
| `DQ-01` | Company knowledge contract: retire generic `query_anything` vs add explicit Node B -> RAG service adapter | `RC-01`, `RC-15` |
| `DQ-02` | Canonical proposal/execution lifecycle and restart semantics | `RC-09`, `RC-10`, `RC-12` |
| `DQ-03` | Materialize scope by proposal type: retain only proven types vs remove dormant ones | `RC-09`, `RC-14` |
| `DQ-04` | Calendar SoT and visit lifecycle: real event vs fact shadow | `RC-07` |
| `DQ-05` | Learning scope: evidence-only, operator-feedback steering, outcome learning, world-model | `RC-08` |
| `DQ-06` | Projection transport architecture: JSONL bridge, DB outbox, or Node B owned durable outbox | `RC-06`, `RC-11` |
| `DQ-07` | Document readiness policy: `PDF_REQUIRED` vs explicitly degraded DOCX handling | `RC-13` |
| `DQ-08` | Retry policy by side-effect class and trigger mode | `RC-06`, `RC-11` |
| `DQ-09` | Operator warning contract: what is operator-facing vs telemetry-only | `RC-10`, `RC-06` |
| `DQ-10` | Fact supersession model: overwrite, supersede or version | `RC-12` |
| `DQ-11` | Mailbox ingest ownership: one authoritative poller per mailbox/source | `RC-11` |

## 5. Root-Cause Clusters

Full machine-readable clusters are in [ROOT_CAUSE_CLUSTERS.yaml](./ROOT_CAUSE_CLUSTERS.yaml). The summary is:

| cluster_id | title | gaps | lane | primary outcome |
| --- | --- | ---: | --- | --- |
| `RC-01` | Generic RAG tool and company-knowledge contract drift | 6 | `DECISION_DEPENDENT` | replace dead generic RAG/tool branches with the chosen retrieval contract |
| `RC-02` | Learning row-shape and false divergence classification | 3 | `FAST` | preserve proposal fields and stop manufacturing divergence |
| `RC-03` | Gmail send false-success contract | 2 | `FAST` | separate dry-run from live send semantically |
| `RC-04` | Agent concurrency semantics | 2 | `FAST` | preserve concurrency meaning instead of mapping to dry-run |
| `RC-05` | Case-intelligence masking and non-transactional finalize | 4 | `INTEGRITY` | surface degraded handoff and make finalize safe |
| `RC-06` | Projection retry and operator visibility | 6 | `INTEGRITY` | projection failures become durable/visible instead of silent |
| `RC-07` | Calendar canonical lifecycle | 7 | `DECISION_DEPENDENT` | real visit lifecycle replaces fact-only shadows and dead proposal branches |
| `RC-08` | Learning scope, outcomes and world-model reachability | 6 | `ARCHITECTURAL` | define what learning actually controls and what data it needs |
| `RC-09` | Materialize execution integrity and restart safety | 7 | `INTEGRITY` | canonical materialize state machine with receipt-before-retry semantics |
| `RC-10` | Approval payload and clarification contract | 4 | `INTEGRITY` | operator edits and clarification answers survive all approval paths |
| `RC-11` | Ingest ownership and trigger model | 3 | `DECISION_DEPENDENT` | one poller per mailbox/source and explicit trigger policy |
| `RC-12` | Planning/tool activation and state-correction controls | 7 | `DECISION_DEPENDENT` | truthful tool exposure, enforceable divergence control and fact supersession |
| `RC-13` | Document generation mode and readiness semantics | 6 | `ARCHITECTURAL` | single readiness contract across generator and consumers |
| `RC-14` | Dead or executor-only proposal branches | 5 | `DECISION_DEPENDENT` | remove dormant materialize branches unless explicitly reintroduced |
| `RC-15` | Config-plane determinism and local routing drift | 3 | `FAST` | deterministic branch selection and local-safe routing |
| `RC-16` | Documentation and observation-only items | 4 | `CONSOLIDATION` | accept, defer or re-snapshot without accidental code repair |
| `RC-17` | Proof-enabling and regression coverage | 2 | `FAST` | restore executable proof where the plan depends on it |

## 6. Repair DAG

The machine-readable dependency graph is in [REPAIR_DAG.yaml](./REPAIR_DAG.yaml). The intended execution shape is:

1. `R0 Proof Enablement`
   - `RC-17`
   - selected `ASR-05` fields needed by downstream runtime proof
2. `Fast Confirmed Fixes` in parallel
   - `RC-02`, `RC-03`, `RC-04`, `RC-15`
   - selected `RC-12` items that do not require decisions (`request_human_handoff`, schema truthfulness, local config)
3. `Early Decision Queue`
   - `DQ-01` through `DQ-11`
4. `Integrity Wave`
   - `RC-05`, `RC-06`, `RC-09`, `RC-10`, selected `RC-11`, selected `RC-12`, selected `RC-13`
5. `Architectural Capability Completion`
   - `RC-01`, `RC-07`, `RC-08`, `RC-11`, `RC-13`, `RC-14`
6. `Consolidation`
   - `RC-16`
   - any enabling consolidation explicitly required before or during `RC-09`, `RC-12`, `RC-13`
7. `Proof Closure`
   - operator journeys across `BIZ-01` through `BIZ-06`
   - observation period for retained side-effecting flows
8. `Snapshot`
   - generate `Workflow Registry v2`

## 7. Parallel Lanes

### 7.1 Fast Lane

Criteria:

- defect is reproducible from current code or tests;
- no early decision is needed;
- contract is already known;
- blast radius is local and reversible.

Planned contents:

- `RC-02` learning row-shape and false divergence
- `RC-03` dry-run/live send semantic split
- `RC-04` concurrency error classification
- `RC-15` config determinism and local routing
- `RC-17` proof-enabling tests
- selected `RC-12` items: truthful handoff schema and tool contract alignment

### 7.2 Integrity Lane

Focus:

- no false success
- idempotency
- durable receipts
- restart safety
- operator-visible failure states
- fact correction and data repair

Planned contents:

- `RC-05`, `RC-06`, `RC-09`, `RC-10`
- `RC-11` retry/trigger subpart
- `RC-12` fact supersession and divergence control
- `RC-13` readiness semantics where customer/operator state can be overstated

### 7.3 Decision-Dependent Lane

Focus:

- mechanisms that might be removed instead of repaired
- path survival questions
- ownership and Source of Truth decisions

Planned contents:

- `RC-01`, `RC-07`, `RC-08`, `RC-11`, `RC-14`
- selected `RC-12` and `RC-13` items
- all `DQ-*` packets

### 7.4 Architectural Lane

Focus:

- capability completion where no minimal bugfix is sufficient
- new contracts, new durable transports, or missing producers/consumers

Planned contents:

- global/company knowledge contract (`RC-01`)
- canonical calendar lifecycle (`RC-07`)
- learning + outcome substrate (`RC-08`)
- projection transport replacement (`RC-06` / `RC-11`)
- document readiness contract (`RC-13`)

### 7.5 Consolidation Lane

Focus:

- simplification that is required to stop repairing three competing implementations
- cleanup only after the retained contract is chosen

Planned contents:

- `RC-14` dormant proposal branches
- `RC-16` documentation/observation cleanup
- minimal enabling consolidation inside `RC-09`, `RC-12`, `RC-13`

## 8. Repair Lifecycle

Required lifecycle for every repair item:

`PROPOSED -> REPRODUCED -> READY -> IMPLEMENTED -> TEST_VERIFIED -> DEPLOYED -> RUNTIME_VERIFIED -> OBSERVED_STABLE -> CLOSED`

Allowed non-happy-path states:

- `BLOCKED`
- `SUPERSEDED`
- `REJECTED`
- `REVERTED`
- `REOPENED`
- `ACCEPTED_RISK`

Interpretation:

- `REPRODUCED` means the current defect or gap contract is evidenced in a test, static proof, or runtime probe.
- `READY` means dependencies, decisions and rollback constraints are clear.
- `TEST_VERIFIED` means the required proof level short of deployment is satisfied.
- `RUNTIME_VERIFIED` is mandatory only where the gap’s `required_proof_level` demands runtime proof.
- `OBSERVED_STABLE` is mandatory for irreversible or high-blast-radius paths.

## 9. Required Proof Model

Every gap inherits one required proof level from `GAP_DISPOSITIONS.yaml`:

- `STATIC`
- `UNIT`
- `INTEGRATION`
- `END_TO_END`
- `RUNTIME_READ_ONLY`
- `RUNTIME_MUTATING_CONTROLLED`
- `OBSERVATION_PERIOD`

Rules:

- do not require runtime proof for obvious import/row-shape/schema/test defects;
- do require runtime proof for send, calendar write, replay/retry, queue drain, durable receipt and cross-repo side effects;
- runtime-unverified code is not automatically a repair target; it may first be `PROVE_AT_RUNTIME`.

## 10. Historical Data Impact Rule

Code fix alone is not closure when data is already contaminated.

Every repair cluster must explicitly classify historical data impact as one of:

- `NONE`
- `BACKFILL`
- `QUARANTINE`
- `MANUAL_REVIEW`
- `REBUILD_PROJECTION`

Clusters already expected to need data remediation:

- `RC-02` false divergence rows
- `RC-05` case-intelligence degraded-but-finalized rows
- `RC-06` failed/invisible bridge or feed rows
- `RC-07` stale `scheduled_visit` facts vs real calendar truth
- `RC-09` partially applied materialize effects
- `RC-12` stale facts blocked by `ON CONFLICT DO NOTHING`
- `RC-13` rows or projections overstating `PDF_READY`

## 11. Completion Contract

The repair program is `COMPLETE` only when all of the following are true:

1. every one of the 78 baseline gaps has a final overlay outcome:
   - `CLOSED`
   - `ACCEPTED_RISK`
   - `REMOVED`
   - `SUPERSEDED`
   - `DEFERRED_WITH_OWNER`
2. all live-path `P0` gaps have left `PROPOSED` and satisfy their required proof level;
3. `ASR-01`, `ASR-02`, `ASR-03`, `ASR-05` are `RUNTIME_VERIFIED` for all retained irreversible side-effect paths;
4. the critical operator journeys pass:
   - new lead -> quote -> artifact -> dispatch
   - customer email -> understanding -> draft/clarification -> approve -> send -> durable result -> projection convergence
   - schedule visit -> real calendar effect -> fact/projection convergence
   - operator feedback -> learning candidate -> approved rule or explicit non-governance outcome
   - Cieplo intake -> calculate -> generate -> review email with truthful readiness semantics
5. all retained proposal/execution paths have canonical lifecycle and restart semantics;
6. any remaining runtime-unverified capability is explicitly out of scope, accepted as risk, or owned by a future wave;
7. `Workflow Registry v2` is generated and validated after the wave;
8. Workflow Registry v1 remains unchanged on disk as the immutable baseline.

## 12. What This Plan Deliberately Does Not Do

- It does not start implementation.
- It does not create `CAPABILITY_REGISTRY.yaml`.
- It does not mutate `WORKFLOW_GAPS.yaml`.
- It does not claim that every dormant path should be repaired.
- It does not treat all 78 gaps as 78 separate code changes.
