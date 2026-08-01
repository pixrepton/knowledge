# AI-OS Repair Program - Superplan

Status: `STRATEGIC_PLAN_READY / WAVE_02_CLOSED_LOCAL`

Date: `2026-07-31`

Scope: canonical synthesized repair plan for the immutable Workflow Registry v1 baseline in `knowledge/system-atlas/workflows/`.

This document synthesizes:

- the existing atlas-coupled repair plan in `knowledge/system-atlas/repairs/`;
- the external executable plan from `pasted-text`.

It does **not** start implementation, does **not** create a Capability Registry yet, and does **not** mutate Workflow Registry v1.

Current execution overlay status:

- Wave 1: `COMPLETE`
- Wave 2: `CLOSED_LOCAL`
- Workflow Registry v1: immutable baseline
- Workflow Registry v2: not created

## 1. Synthesis Outcome

The two input plans are compatible, but each is strongest in a different dimension.

What is retained from the atlas-coupled plan:

- exact `78/78` gap coverage;
- machine-readable `GAP_DISPOSITIONS.yaml`;
- machine-readable `ROOT_CAUSE_CLUSTERS.yaml`;
- machine-readable `REPAIR_DAG.yaml`;
- repair lanes already aligned to current atlas findings;
- completion rule tied to immutable Workflow Registry v1.

What is retained from the external executable plan:

- stronger multi-axis repair classification;
- richer capability decomposition by business journey, agent competency, platform capability and assurance;
- larger and more operational Early Decision Queue;
- sharper distinction between removable, dormant, local, live and runtime-unknown mechanisms;
- finer-grained execution packages under broad root-cause clusters.

What this superplan changes:

- `17` existing root-cause clusters remain the orchestration layer.
- Finer execution packages are introduced as a second layer for actual implementation waves.
- Capability contracts are expanded without creating a machine registry yet.
- The future Repair Registry schema is defined more strictly than in either input alone.
- "Phase" is demoted to a reporting view; it is not the primary control model.

## 2. Immutable Program Rules

- Workflow Registry v1 remains immutable on disk.
- `WORKFLOW_GAPS.yaml` and `WORKFLOW_GAPS.md` remain historical audit truth for the reconstruction wave.
- All repair execution state must live in an append-only overlay.
- Capability status is generated from repair records and proof, never handwritten.
- Workflow Registry v2 is a later snapshot, generated only after a repair wave closes.
- Node B (`gmail-agent`) remains the operational Source of Truth for case, engagement, proposal, mailbox and execution truth.
- Daszek remains projection-only and bounded HITL, not a write Source of Truth.
- `kalk-top` remains owner of HVAC logic and canonical `OfferDTO`.
- Runtime proof honesty remains mandatory: implemented, tested, runtime-enabled and runtime-proven remain separate claims.

Program model:

```text
Workflow Registry v1
        immutable baseline
               |
               v
Repair Registry
        append-only delta
               |
               v
Generated repair views
        capability status / lane status / closure status
               |
               v
Workflow Registry v2
        new validated snapshot after repair wave closure
```

## 3. Canonical Repair Data Model

Every baseline gap must carry independent execution dimensions. The existing `GAP_DISPOSITIONS.yaml` already covers part of this model. The full target schema for the future Repair Registry is:

| field | purpose |
| --- | --- |
| `gap_id` | immutable link to Workflow Registry v1 |
| `disposition` | `FIX | REMOVE | REPLACE | CONSOLIDATE | PROVE_AT_RUNTIME | ACCEPT_RISK | DEFER | NO_ACTION` |
| `change_type` | `DEFECT | CONTRACT_CHANGE | ARCHITECTURAL | TEST_GAP | OBSERVATION | DEAD_CODE | RUNTIME_UNKNOWN` |
| `decision_required` | whether execution is blocked by an early decision |
| `live_reachability` | `LIVE | REACHABLE | DORMANT | MISSING | LOCAL | OBSERVATION` |
| `mechanism_future` | whether the current mechanism survives, is removed, or is replaced |
| `blocks_capability` | whether this gap blocks a retained capability |
| `capability_refs` | business, agent, platform or assurance contracts affected |
| `macro_cluster_id` | orchestration cluster from current YAML |
| `repair_package_id` | finer execution package from this superplan |
| `lane` | `FAST | INTEGRITY | DECISION_DEPENDENT | ARCHITECTURAL | CONSOLIDATION` |
| `required_proof_level` | proof required before closure |
| `historical_data_impact` | `NONE | BACKFILL | QUARANTINE | MANUAL_REVIEW | REBUILD_PROJECTION` |
| `rollback_class` | blast-radius and rollback expectation |
| `owner_repo` | primary repo of repair |
| `owner_team` | future operating owner |
| `blocking_decisions` | list of `EDQ-*` packets |
| `proof_artifacts` | links to tests, runtime probes, logs and reports |

Canonical rule:

- "phase" may exist as a generated view, but it cannot replace the fields above.

## 4. Capability Contract Model

This is still not a Capability Registry. It is the canonical contract layer the future registry must reflect.

The plan uses four capability layers:

1. Business capabilities
2. Agent competencies
3. Platform capabilities
4. Assurances

Every capability contract must define:

- `trigger`
- `preconditions`
- `success_evidence`
- `failure_semantics`
- `non_goals`

### 4.1 Business Capabilities

| capability_id | capability | trigger | preconditions | success evidence | failure semantics | non-goals |
| --- | --- | --- | --- | --- | --- | --- |
| `BC-01` | Customer case intake and qualification | mail, phone, form, operator signal | source identified, signal durably stored, case resolution path available | signal attached to Case, state updated, next step or explicit missing data | analysis failure cannot look like successful processing | irreversible action without policy/HITL |
| `BC-02` | Customer email response | customer email, resend or operator send approval | case resolved, recipient confirmed, draft or clarification path available | durable execution receipt, provider receipt or explicit dry-run marker, projection updated | dry-run cannot look like send success, unknown side effect becomes explicit | autonomous negotiation or policy override |
| `BC-03` | Offer preparation and delivery | qualified offer request or operator decision | authoritative `kalk-top` path available, generator path chosen | canonical `OfferDTO`, truthful artifact format/readiness, dispatch result or draft | LLM cannot own price, DOCX fallback cannot look like `PDF_READY` | parallel pricing logic outside `kalk-top` |
| `BC-04` | Visit lifecycle management | customer date proposal, agent recommendation, operator decision | customer and Case resolved, calendar SoT chosen, timezone known | real `calendar_event_id`, Case linkage, correct projection | text fact cannot impersonate real event, unknown result must remain explicit | separate shadow truth for visits |
| `BC-05` | Operator decision to durable side effect | approve, reject, edit, clarification, note | active proposal, valid payload, permissions, idempotency key | durable decision record, durable effect receipt, preserved operator payload | no side effect before durable boundary, no replay after crash without receipt logic | executing effects before persistence safety |
| `BC-06` | Cieplo pipeline execution | qualifying intake or controlled retry | message mapped, calculator and generator reachable | truthful workflow state, truthful artifact state, review email or explicit blocked state | degraded format cannot be labeled `PDF_READY` | Cieplo becoming Case SoT |
| `BC-07` | Operator operational picture | case/execution/failure/SLA change | Node B remains operational SoT | Daszek shows current state, failures, warnings and pending actions | projection failure cannot be silent | Daszek owning canonical state |
| `BC-08` | Business outcome closure | win, loss, install complete, resignation, case close | case-offer-lead linkage exists | explicit outcome and value, or explicit missing data | `completed` cannot silently mean `won` | inferred revenue without business outcome record |

### 4.2 Agent Competencies

| capability_id | capability | trigger | preconditions | success evidence | failure semantics | non-goals |
| --- | --- | --- | --- | --- | --- | --- |
| `AC-01` | Identity, Case and Engagement resolution | canonical signal | correlation data accessible | unambiguous or explicitly unresolved linkage | no false certainty and no duplicate Case creation | solving commercial outcome in identity layer |
| `AC-02` | Case understanding | Case state change | context pack available | complete understanding or explicit degraded result | empty result cannot impersonate successful understanding | using missing understanding as silent success |
| `AC-03` | Case and company knowledge retrieval | planner or response needs knowledge | reachable retrieval contracts, source definitions | per-source status, evidence or citations, truthful consulted-source counts | one failed source cannot inflate success | preserving dead generic retrieval branches |
| `AC-04` | Action and tool selection | understanding plus operator goal | available tool contracts and policy controls | selected path maps to reachable capability/tool | unreachable tool path must be rejected explicitly | treating schema exposure as proof of runtime support |
| `AC-05` | Draft and clarification handling | communication need or clarification approval | canonical draft contract and payload channel exist | one canonical draft or explicit request for missing data | operator edit/clarification cannot be dropped | preserving every historical draft lineage equally |
| `AC-06` | Feedback interpretation and learning | operator decision or business outcome | learning scope chosen | correct approve/reject/divergence semantics and outcome linkage | missing outcome cannot be silently assumed | full intelligence redesign in first wave |

### 4.3 Platform Capabilities

| capability_id | capability | trigger | preconditions | success evidence | failure semantics | non-goals |
| --- | --- | --- | --- | --- | --- | --- |
| `PC-01` | Signal ingestion and reconcile | Gmail/calendar/other signal | one authoritative poller per source, canonical handler reachable | signal durably recorded, deduplicated, processed or retryable | dual pollers cannot silently race | parallel uncontrolled ingress |
| `PC-02` | Canonical state and facts | fact write, correction, readback | provenance model chosen | facts have provenance, version/supersession and truthful current projection | correction cannot no-op silently | ad hoc overwrite without semantics |
| `PC-03` | Proposal and approval persistence | proposal creation or approval | canonical lifecycle chosen | proposal has one identifiable lifecycle and full operator payload | no fragmented lifecycle pretending to be one | parallel unowned lifecycle shapes |
| `PC-04` | Durable execution | irreversible write or external side effect | idempotency key, receipt store and retry class chosen | receipt, status and recovery path durable | no post-crash ambiguity where avoidable | best-effort memory as idempotency |
| `PC-05` | Gmail execution | send or dry-run | Gmail executor reachable, mode explicit | dry-run and live send produce distinct truthful results | dry-run cannot look executed | semantic collapse of mode and outcome |
| `PC-06` | Calendar integration | ingest or approved visit action | one SoT, one write model, reachable executor | create/reschedule/cancel share one lifecycle and truth model | mailbox fact alone is not calendar truth | keeping CLI-only richer logic hidden |
| `PC-07` | Offer calculation | fast-kalk, Cieplo or generator request | authoritative `kalk-top` contract available | schema exposed to agent matches real runtime handler | no fake or partial OfferDTO path outside owner | duplicating HVAC logic |
| `PC-08` | Document generation | artifact request | explicit generator mode and converter contract | format, MIME, URL and degradation typed truthfully | consumer cannot overstate readiness | permanent coexistence of incompatible readiness semantics |
| `PC-09` | RAG service access | case/company retrieval request or ingest | auth, timeout and route defined | case-scoped and company-scoped retrieval have truthful contracts and source-level status | no dead generic branch kept by docs only | blindly preserving all historical entrypoints |
| `PC-10` | Daszek delivery | feed push, command, dashboard refresh | durable transport chosen, failure visibility path exists | durable enough queue/outbox and visible failures | failed/invisible rows cannot disappear silently | promoting projection to write SoT |
| `PC-11` | Temporal scheduling | SLA deadline, follow-up time, timed event | one scheduler owner and dedupe policy | canonical temporal signals produced automatically | CLI-only operation is not normal production mode | manual CLI as primary scheduler |
| `PC-12` | Runtime configuration | process start or branch selection | one canonical config plane and precedence model | same config yields same branch selection and local-safe routing | loader order cannot change behavior | indefinite support for conflicting loaders |
| `PC-13` | Business outcome capture | outcome change or closure event | structured outcome model chosen | durable business outcome record | generic case status cannot stand in for outcome | inferred revenue from generic lifecycle status |

### 4.4 Assurances

| capability_id | capability | trigger | preconditions | success evidence | failure semantics | non-goals |
| --- | --- | --- | --- | --- | --- | --- |
| `AS-01` | No false success | any visible or side-effecting action | canonical status vocabulary exists | top-level and nested status agree with actual effect | dry-run, degraded or partial failure cannot look like success | log-only mitigation without semantic change |
| `AS-02` | Idempotency | repeated irreversible action | receipt and dedupe strategy exist | duplicate recognized or blocked durably | no configuration-only silent downgrade | pretending receiptless write is safe |
| `AS-03` | Crash recovery | crash, restart, replay, retry | replay entrypoint and retry class known | state resolves to not done, done or `OUTCOME_UNKNOWN` | failed rows cannot disappear | universal auto-retry |
| `AS-04` | HITL integrity | operator review path | identity, payload and versioning retained | decision, text and version survive end-to-end | operator payload cannot be dropped | payload reconstruction from logs |
| `AS-05` | State atomicity and convergence | multi-write flow | transaction or explicit reconciliation strategy | related writes converge to one truthful state | finalize cannot mask partial failure | giant transaction by default |
| `AS-06` | Operator-visible failure | warning, queue failure, degraded output | failure surfaces exist | operator can see failures that matter operationally | silent failure is forbidden | telemetry-only for operator-critical failures |
| `AS-07` | Cross-repo contract integrity | producer-consumer boundary | field and status ownership defined | producers and consumers agree on schema and semantics | one side cannot silently reinterpret status or format | duplicating owner logic |
| `AS-08` | Runtime proof honesty | proof, test or runtime report | proof taxonomy defined | code, test, runtime-enabled and runtime-proven are kept distinct | no inflation of static proof into runtime proof | narrative confidence as evidence |

## 5. Early Decision Queue

The synthesized Early Decision Queue is the union of both plans. No blocked repair package may move from `REPRODUCED` to `READY` without its required decision being resolved or explicitly waived.

| decision_id | decision | default recommendation | blocks |
| --- | --- | --- | --- |
| `EDQ-01` | Future of generic knowledge aggregator `query_anything` | replace with typed per-source contract or retire in favor of specialist tools | gaps 1-4; macro `RC-01` |
| `EDQ-02` | Canonical Node B <-> Daszek transport | one durable outbox/queue, not JSONL plus dormant DB path forever | `RC-06`; parts of `RC-11` |
| `EDQ-03` | Canonical proposal/execution lifecycle | choose one retained lifecycle and migrate/remove the rest | `RC-09`; `RC-14` |
| `EDQ-04` | Operator response payload shape | one payload supporting approve/reject/edit/clarification/note/version | `RC-10` |
| `EDQ-05` | Node B access to company knowledge | explicit service client with auth, timeout, source status and citations | `RC-01`; company retrieval work |
| `EDQ-06` | Mailbox intake ownership | one authoritative poller per mailbox/source | `RC-11` |
| `EDQ-07` | Understanding vs planning sequence | understanding required before final planning/draft; provisional earlier outputs only | `RC-12` |
| `EDQ-08` | Visit Source of Truth | real Google Calendar event is truth; Case facts are projection | `RC-07` |
| `EDQ-09` | DOCX fallback semantics | typed degraded result; never `PDF_READY` for DOCX fallback | `RC-13`; Cieplo status semantics |
| `EDQ-10` | Fact correction model | append-only observations plus versioned active fact projection | `RC-12`; `RC-17` style work |
| `EDQ-11` | Scope of learning v1 | repair classification bugs now; outcome-backed learning as separate architectural track unless proven necessary | `RC-08` |
| `EDQ-12` | Legacy generator `direct-config` | prove consumers first, then keep, deprecate or remove | document readiness / generator branch |
| `EDQ-13` | Unreachable tool scopes and dormant executors | remove by default unless confirmed business usage exists | dead proposal branches; unreachable tools |
| `EDQ-14` | Policy divergence semantics | decide telemetry-only vs warning vs hard gate by action class | divergence controls |
| `EDQ-15` | Scheduler ownership | one owner for SLA, retry and temporal signals | temporal signals; scheduler paths |
| `EDQ-16` | GraphRAG enrichment future | remove dormant enrichment unless real runtime use and measurement are committed | GraphRAG gaps |
| `EDQ-17` | Canonical config loader | one loader, one precedence model, no `os.environ` mutation while reading | config-plane determinism |

## 6. Root-Cause Model: Macro Clusters And Repair Packages

Two levels are now explicit.

### 6.1 Macro Clusters

The existing `17` entries in `ROOT_CAUSE_CLUSTERS.yaml` remain the orchestration layer for:

- DAG dependencies;
- lane allocation;
- proof-readiness grouping;
- historical-data remediation planning.

They should not be discarded.

### 6.2 Repair Packages

Execution should happen through finer packages nested under macro clusters. This resolves the main weakness of the earlier `17`-cluster-only approach: some clusters are still too broad for direct implementation planning.

| repair_package_id | package | primary macro cluster | main purpose |
| --- | --- | --- | --- |
| `RP-01` | Knowledge aggregator replacement | `RC-01` | retire/replace false-success generic retrieval |
| `RP-02` | Learning row-shape repair | `RC-02` | close tuple/dict learning-row defects |
| `RP-03` | Gmail dry-run/live truth split | `RC-03` | separate mode from effect truth |
| `RP-04` | Concurrency conflict semantics | `RC-04` | preserve real concurrency meaning |
| `RP-05` | Case-intelligence failure convergence | `RC-05` | stop finalize-from-degraded-empty behavior |
| `RP-06` | Durable Daszek transport | `RC-06` | one durable projection transport with visible failure |
| `RP-07` | Calendar canonical lifecycle | `RC-07` | one visit lifecycle with real event truth |
| `RP-08` | Learning v1 scope and outcome boundary | `RC-08` | separate evidence-only learning from outcome learning |
| `RP-09` | Proposal lifecycle consolidation | `RC-09` | reduce competing proposal/execution lifecycles |
| `RP-10` | Materialize integrity and restart safety | `RC-09` | receipt, idempotency and restart-safe effect order |
| `RP-11` | Node B company-knowledge client | `RC-01` / `RC-15` | explicit company retrieval contract |
| `RP-12` | Mailbox intake ownership | `RC-11` | one poller and one trigger model |
| `RP-13` | Downstream stage sequencing | `RC-05` / `RC-12` | make understanding/planning/finalize ordering truthful |
| `RP-14` | Document readiness contract | `RC-13` | typed artifact readiness and degradation semantics |
| `RP-15` | Temporal trigger ownership | `RC-11` / `RC-16` | one scheduler owner and canonical temporal signals |
| `RP-16` | Tool/planner contract cleanup | `RC-12` | truthful tool scopes and divergence controls |
| `RP-17` | Operator-visible failure surfaces | `RC-06` / `RC-10` | warnings and failed rows visible where operationally needed |
| `RP-18` | Fact supersession | `RC-12` | versioned active facts and truthful corrections |
| `RP-19` | Local RAG routing safety | `RC-15` | local-safe routing and production-protection |
| `RP-20` | GraphRAG enrichment decision | `RC-15` / `RC-16` | prove-or-remove dormant enrichment |
| `RP-21` | Observation-only triage | `RC-16` | classify observation-only gaps without accidental implementation |
| `RP-22` | Cieplo state semantics and test recovery | `RC-13` / `RC-17` | truthful Cieplo statuses and broken proof repair |
| `RP-23` | Fast-kalk end-to-end proof | `RC-17` | restore proof for lead-to-dispatch journey |
| `RP-24` | Config plane canonicalization | `RC-15` | one config loader and deterministic precedence |

Execution rule:

- closure is tracked per gap;
- planning and implementation sequencing are performed per repair package;
- dependency management remains anchored at macro-cluster and `EDQ-*` level.

## 7. Repair Lanes

The synthesized lanes remain the same as the atlas plan, but their membership is refined by repair package.

### 7.1 Fast Lane

Criteria:

- reproducible from current code or tests;
- no early decision required;
- local blast radius;
- proof is available without cross-repo irreversible runtime mutation.

Typical packages:

- `RP-02`
- `RP-03`
- `RP-04`
- `RP-19`
- `RP-23`
- selected subparts of `RP-16`
- selected subparts of `RP-24`

### 7.2 Integrity Lane

Focus:

- no false success
- durable receipts
- idempotency
- crash recovery
- state convergence
- operator-visible failure

Typical packages:

- `RP-05`
- `RP-06`
- `RP-09`
- `RP-10`
- `RP-17`
- `RP-18`
- integrity-critical parts of `RP-14`

### 7.3 Decision-Dependent Lane

Focus:

- mechanisms that may be removed instead of repaired;
- SoT and ownership decisions;
- path survival decisions;
- dormant-vs-retained adjudication.

Typical packages:

- `RP-01`
- `RP-07`
- `RP-08`
- `RP-11`
- `RP-12`
- `RP-15`
- `RP-20`
- portions of `RP-16`

### 7.4 Architectural Lane

Focus:

- capability completion where minimal bugfix is insufficient;
- new contracts or durable transports;
- missing producers/consumers;
- outcome-backed state models.

Typical packages:

- `RP-06`
- `RP-07`
- `RP-08`
- `RP-11`
- `RP-14`
- `RP-15`
- `RP-24`

### 7.5 Consolidation Lane

Focus:

- remove or collapse competing implementations after retained contract is chosen;
- clean up dormant branches and observation-only items;
- simplify after repair, not before proof.

Typical packages:

- `RP-09`
- `RP-16`
- `RP-20`
- `RP-21`
- dormant-branch closures under `RP-10` and `RP-14`

## 8. Repair DAG And Execution Shape

The machine-readable graph remains `REPAIR_DAG.yaml`. The synthesized execution shape is:

1. `R0 Proof Enablement`
   - repair broken proof surfaces needed by the wave;
   - close proof blockers that would otherwise make downstream closure ambiguous.
2. `Fast Confirmed Fixes`
   - execute Fast Lane items not blocked by decisions.
3. `Early Decision Queue`
   - resolve `EDQ-01` through `EDQ-17`.
4. `Integrity Wave`
   - close false-success, receipt, retry, restart and operator-visibility gaps.
5. `Architectural Completion`
   - implement retained transport, SoT and cross-repo contract decisions.
6. `Consolidation`
   - remove dormant branches and collapse obsolete shapes after retained contracts are proven.
7. `Proof Closure`
   - run required tests, runtime proofs and observation periods.
8. `Snapshot Closure`
   - generate and validate Workflow Registry v2.

Execution constraints:

- do not start a blocked package before its `EDQ-*` decision resolves;
- do not close an integrity gap without its required proof level;
- do not mark a capability complete if only one scenario path is proven;
- do not repair a dormant path just because code exists.

## 9. Repair Lifecycle

Every repair item, package and gap uses the same lifecycle:

`PROPOSED -> REPRODUCED -> READY -> IMPLEMENTED -> TEST_VERIFIED -> DEPLOYED -> RUNTIME_VERIFIED -> OBSERVED_STABLE -> CLOSED`

Allowed non-happy-path statuses:

- `BLOCKED`
- `SUPERSEDED`
- `REJECTED`
- `REVERTED`
- `REOPENED`
- `ACCEPTED_RISK`

Lifecycle rules:

- `REPRODUCED` requires a current proof of the defect or explicit structural absence proof.
- `READY` requires dependencies, rollout scope, rollback boundary and proof contract to be explicit.
- `TEST_VERIFIED` means all non-runtime proof obligations are met.
- `RUNTIME_VERIFIED` is mandatory only when the required proof level includes runtime.
- `OBSERVED_STABLE` is mandatory for irreversible or high-blast-radius side effects.

## 10. Proof Model

The synthesized proof taxonomy is the union of both plans:

- `STATIC`
- `UNIT`
- `INTEGRATION`
- `END_TO_END`
- `CONCURRENCY`
- `CRASH_RECOVERY`
- `RUNTIME_READ_ONLY`
- `RUNTIME_CONTROLLED_MUTATION`
- `DATA_MIGRATION`
- `OBSERVATION_PERIOD`

Proof rules:

- obvious import, row-shape, schema or dead-code defects do not require runtime proof;
- send, calendar write, retry, replay, durable receipt, cross-repo dispatch and scheduler changes usually require runtime proof;
- data contamination requires both code closure and data-remediation closure;
- a runtime-unverified retained path cannot be reported as fully closed;
- a dormant path may be `REMOVE` or `ACCEPT_RISK`; it does not automatically become a repair target.

## 11. Historical Data And Remediation

Code repair alone is insufficient where historical data is already contaminated.

Every repair package must classify data impact as one of:

- `NONE`
- `BACKFILL`
- `QUARANTINE`
- `MANUAL_REVIEW`
- `REBUILD_PROJECTION`

Expected remediation-heavy areas:

- learning misclassification and malformed learning rows;
- case-intelligence degraded-but-finalized rows;
- invisible or failed projection transport rows;
- stale `scheduled_visit` facts vs real calendar truth;
- partially applied materialize effects;
- stale facts blocked by no-op correction semantics;
- overstated document readiness states, especially `PDF_READY`.

## 12. Completion Contract

The repair program is `COMPLETE` only when all of the following are true:

1. all `78` baseline gaps have a final overlay outcome:
   - `CLOSED`
   - `ACCEPTED_RISK`
   - `REMOVED`
   - `SUPERSEDED`
   - `DEFERRED_WITH_OWNER`
2. every live-path `P0` gap has left `PROPOSED` and satisfied its required proof level;
3. all retained irreversible side-effect paths satisfy runtime proof for:
   - `AS-01` no false success
   - `AS-02` idempotency
   - `AS-03` crash recovery / retry truth
   - `AS-06` operator-visible failure where operationally required
   - `AS-08` proof honesty
4. critical operator journeys pass end-to-end:
   - new lead -> quote -> artifact -> dispatch
   - customer email -> understanding -> draft or clarification -> approve -> send -> durable result -> projection convergence
   - schedule visit -> real calendar effect -> fact/projection convergence
   - operator feedback -> learning candidate -> approved rule or explicit evidence-only outcome
   - Cieplo intake -> calculate -> generate -> review email with truthful readiness semantics
5. all retained proposal/execution paths share canonical lifecycle and restart semantics;
6. any remaining runtime-unverified retained capability is explicitly out of scope, accepted as risk or assigned to a named future wave;
7. Workflow Registry v2 is generated and validated after the wave;
8. Workflow Registry v1 remains unchanged on disk.

## 13. Immediate Planning Consequences

This synthesized plan implies the following before implementation begins:

1. `REPAIR_PROGRAM_SUPERPLAN.md` becomes the canonical textual entrypoint.
2. Existing YAML artifacts remain valid as execution backbone; they are not discarded.
3. The future Repair Registry must adopt the expanded data model from section 3.
4. Execution should be planned per `repair_package_id`, not only per macro cluster.
5. `EDQ-*` packets must be resolved before decision-dependent packages move to `READY`.
6. Capability completion must be measured by scenario contract fulfillment, not by "gap count closed".

## 14. What This Superplan Deliberately Does Not Do

- It does not start implementation.
- It does not create `CAPABILITY_REGISTRY.yaml`.
- It does not mutate Workflow Registry v1.
- It does not assume every dormant path should survive.
- It does not reduce the program to one flat phase list.
- It does not treat all `78` gaps as `78` independent code changes.
