# WAVE_02_IMPLEMENTATION_PLAN.md

Status: `WAVE_02_CLOSED`

Code mutation state: `CODE_MUTATION_COMPLETE_LOCAL`

Current package snapshot:

- `RP-14`: `CLOSED`
- `RP-15`: `CLOSED`
- `RP-06`: `CLOSED`
- `RP-12`: `CLOSED`
- `RP-01`: `CLOSED`
- `RP-20`: `CLOSED`
- `RP-07`: `CLOSED`

Wave objective:

Run `prove -> decide -> implement` package-by-package without changing Workflow Registry v1 or reintroducing forbidden Google write paths.

Final Wave 2 result:

- all scoped packages have execution records;
- all scoped packages have a decision, implementation or proof-backed defer result, tests and proof artifacts;
- exit gate proof logs are stored in `_raw/wave-02/exit-gate/`;
- Workflow Registry v1 validator and hash gate remain PASS;
- no production deployment or push was performed.

Default rule:

- if proof closes the decision and the required code change stays local, implement in the same wave;
- only a proven large migration, risky cutover or non-local data repair may defer implementation into a later wave.

## Scope

Wave 2 packages:

- `RP-01` Knowledge aggregator replacement
- `RP-06` Durable Daszek transport
- `RP-07` Calendar canonical lifecycle
- `RP-12` Mailbox intake ownership
- `RP-14` Document readiness contract
- `RP-15` Temporal trigger ownership
- `RP-20` GraphRAG enrichment decision

Non-goals:

- no production deployment;
- no Gmail send;
- no Gmail draft creation;
- no Calendar create/update/delete;
- no Workflow Registry v2 snapshot;
- no broad architectural rewrite beyond the package actually proven and selected to survive.

## Execution Model

Wave 2 uses one execution model:

`prove -> decide -> minimal implement -> test -> runtime proof -> close`

Exception:

- if proof shows a large migration, risky cutover or non-local data repair, the package may stop after `prove -> decide`, but only with an explicit defer reason and a named later-wave target.

Per-package outputs:

- one canonical execution record;
- raw proof artifacts;
- Repair Registry update.

## Canonical Execution Record

Each package gets one canonical execution record, not four planning documents.

Suggested path:

- `knowledge/system-atlas/repairs/_raw/wave-02/rp-xx/EXECUTION.md`

Required sections:

1. scope and baseline SHA or validator snapshot;
2. proof inventory;
3. findings;
4. open versus frozen contract points;
5. decision;
6. historical data impact;
7. implementation scope;
8. tests and runtime proof;
9. status and residuals.

## Package Matrix

| Package | Blocking decisions | Required proof | Main repos | Default Wave 2 expectation |
| --- | --- | --- | --- | --- |
| `RP-06` | `DQ-06`, `DQ-08`, `DQ-09` | `RUNTIME_READ_ONLY`, `STATIC` | `gmail-agent`, `daszek` | prove and decide first; implement in-wave only if the retained transport does not require a large migration |
| `RP-12` | `DQ-11`, `DQ-08` | `RUNTIME_READ_ONLY`, `STATIC` | `gmail-agent`, possibly `cieplo-orchestrator` | prove and decide first; implement in-wave if ownership and retry stay local |
| `RP-15` | `DQ-15`, `DQ-08` | `RUNTIME_READ_ONLY`, `STATIC` | `gmail-agent` | prove and decide first; implement in-wave if one owner can be established without a larger cutover |
| `RP-14` | `DQ-07`, `DQ-12` | `INTEGRATION`, `STATIC` | `top-instal-generator`, `fast-kalk`, `cieplo-orchestrator` | prove, decide and implement the retained readiness vocabulary in-wave unless proof forces a larger migration |
| `RP-01` | `DQ-01` | `STATIC`, `INTEGRATION` | `gmail-agent`, `rag-chat-asystent`, `rag-widget` | prove, decide and narrow or replace the retained retrieval contract in-wave unless proof shows a larger adapter project |
| `RP-20` | `DQ-16` | `STATIC`, `RUNTIME_READ_ONLY` | `rag-chat-asystent`, `gmail-agent` | prove and remove or park immediately if no caller exists |
| `RP-07` | `DQ-04` | `RUNTIME_READ_ONLY`, `INTEGRATION` | `gmail-agent`, `daszek` | prove, decide and implement the retained read-only lifecycle in-wave unless proof exposes a larger migration |

## Execution Order

### Stage 0 - Wave boundary confirmation

Before Wave 2 work starts:

- re-check that Workflow Registry v1 hashes still match the frozen baseline;
- confirm Wave 1 closed state remains unchanged;
- confirm the read-only Google boundary remains binding.

### Stage 1A - Ownership and transport proof

Packages:

- `RP-06`
- `RP-12`
- `RP-15`

Reason:

These packages share the same failure domain: who owns triggers, who retries, and where operator-visible failure must surface.

Required proof outputs:

- current producer/consumer/drain map for DB outbox and JSONL bridge;
- failed-row visibility map;
- retry-class map by side-effect type;
- active mailbox poller inventory, labels, cursors and dedupe behavior;
- active scheduler or temporal caller inventory;
- explicit classification of manual-only versus automatic paths.

Decision outputs:

- `DQ-06` transport decision;
- `DQ-08` retry policy decision;
- `DQ-09` operator warning scope decision;
- `DQ-11` mailbox intake ownership decision;
- `DQ-15` scheduler ownership decision.

Default implementation rule:

- if the retained ownership and transport solution stays local, implement it in Wave 2;
- if proof shows a large migration, replay campaign or cross-repo cutover, stop after decision capture and promote the package with an explicit defer reason.

### Stage 1B - Calendar read-only lifecycle proof

Package:

- `RP-07`

Reason:

The read-only boundary is already frozen as an invariant, so the calendar lane can run in parallel instead of waiting until the end.

Required proof outputs:

- current ingest path for real `calendar_event_id`;
- current source-kind routing behavior and mismatches;
- current surviving visit states that still imply write-shaped semantics;
- current risk-model implementations and their live reachability;
- classification of reschedule/cancel as retained proposal-only concepts, ingest-only concepts, or removed dead branches.

Decision output:

- `DQ-04` residual read-only lifecycle shape.

Default implementation rule:

- implement the retained routing, risk and dead-branch cleanup in Wave 2 unless proof exposes a larger migration.

### Stage 1C - Document readiness proof

Package:

- `RP-14`

Reason:

The document contract spans three repositories and cannot be fixed safely until the exact producer and consumer matrix is frozen.

Required proof outputs:

- current producer matrix for PDF success versus DOCX fallback;
- current consumers of `PDF_READY`-shaped statuses;
- live or dormant status of the legacy `direct-config` path;
- truthful terminal-state naming requirements for Cieplo.

Decision outputs:

- `DQ-07` degraded readiness vocabulary and consumer alignment;
- `DQ-12` legacy `direct-config` survival.

Default implementation rule:

- implement the retained readiness vocabulary and consumer alignment in Wave 2 unless proof shows a larger migration or a non-local data repair.

### Stage 2 - Retrieval and GraphRAG proof

Packages:

- `RP-01`
- `RP-20`

Reason:

Both packages sit on the same retrieval surface and must be decided together to avoid duplicate refactors.

Required proof outputs:

- current live callers of case-scoped retrieval;
- current or absent live callers of `query_anything`;
- current or absent live callers of GraphRAG enrichment;
- truthful per-source status expectations for a retained company-knowledge capability;
- local-versus-production routing assumptions after Wave 1 local safety fixes.

Decision outputs:

- `DQ-01` retained retrieval contract;
- `DQ-16` GraphRAG enrichment future.

Default implementation rule:

- if no caller exists, remove or park GraphRAG in Wave 2;
- if the retained retrieval fix stays local, narrow or replace it in Wave 2;
- only a proven larger adapter or migration effort may defer the implementation.

### Stage 3 - Package implementation and closure

After each package closes its proof and decision:

- implement immediately if the retained fix stays local;
- run package tests;
- run runtime proof if required;
- close the package or explicitly defer it with a proof-backed migration reason.

## Parallelism

Safe parallel lanes:

- `RP-06`, `RP-12`, `RP-15` can run as one coordinated proof lane with shared findings.
- `RP-07` can run in parallel in an isolated calendar lane because the read-only boundary is already frozen.
- `RP-14` can run in parallel with the ownership/transport lane because it does not share production files.
- `RP-01` and `RP-20` should run together, but after enough routing context is captured from Wave 1 and current local config.

Do not parallelize:

- `RP-01` and `RP-20` as separate uncoordinated tracks;
- any code mutation before its package-level decision output is frozen.

## Proof Qualification Contract

Every static, test or runtime proof recorded in Wave 2 must include:

- repository commit SHA or explicit dirty-worktree note;
- container digest, image id or service version when the proof is runtime-bound;
- environment;
- timestamp;
- command, endpoint or harness used;
- service identifier;
- proof type: `STATIC`, `TEST`, `RUNTIME_READ_ONLY`, `PRODUCTION_OBSERVED`;
- result;
- limitations and blind spots.

Recommended artifact layout:

- `knowledge/system-atlas/repairs/_raw/wave-02/rp-06/`
- `knowledge/system-atlas/repairs/_raw/wave-02/rp-12/`
- `knowledge/system-atlas/repairs/_raw/wave-02/rp-15/`
- `knowledge/system-atlas/repairs/_raw/wave-02/rp-14/`
- `knowledge/system-atlas/repairs/_raw/wave-02/rp-01/`
- `knowledge/system-atlas/repairs/_raw/wave-02/rp-20/`
- `knowledge/system-atlas/repairs/_raw/wave-02/rp-07/`

## Package-Specific Decision Outputs

### `RP-06`

The decision record must end in exactly one selected path:

- `FINISH_EXISTING_DB_OUTBOX`
- `REPLACE_WITH_NODE_B_OWNED_OUTBOX`
- `RETAIN_JSONL_TEMPORARILY_AND_MIGRATE`
- `REMOVE_DORMANT_DB_OUTBOX`
- `OTHER_PROVEN_MODEL_REQUIRING_PLAN_AMENDMENT`

### `RP-12`

The decision record must end in exactly one selected intake model:

- `GMAIL_AGENT_SOLE_POLLER_CIEPLO_VIA_HTTP_INGRESS`
- `TWO_POLLERS_EXPLICIT_SCOPE_SHARED_DEDUPE`
- `ONE_RAW_INGRESS_ROUTED_TO_TWO_WORKFLOWS`
- `OTHER_PROVEN_MODEL_REQUIRING_PLAN_AMENDMENT`

### `RP-14`

The decision record must end in exactly one retained readiness contract:

- `PDF_REQUIRED_WITH_EXPLICIT_DEGRADED_DOCX`
- `TYPED_MULTI_FORMAT_READINESS`
- `OTHER_PROVEN_MODEL_REQUIRING_PLAN_AMENDMENT`

### `RP-15`

The decision record must end in exactly one scheduler classification:

- `ONE_AUTOMATIC_OWNER`
- `MIXED_OWNER_WITH_EXPLICIT_BOUNDARY`
- `MANUAL_ONLY_EXPLICIT`
- `OTHER_PROVEN_MODEL_REQUIRING_PLAN_AMENDMENT`

### `RP-01`

The decision record must end in exactly one retained retrieval model:

- `CASE_SCOPED_ONLY_REMOVE_GENERIC`
- `CASE_SCOPED_PLUS_EXPLICIT_COMPANY_KNOWLEDGE_CLIENT`
- `OTHER_PROVEN_MODEL_REQUIRING_PLAN_AMENDMENT`

### `RP-20`

The decision record must end in exactly one GraphRAG classification:

- `REMOVE_DORMANT_ENRICHMENT`
- `PARK_UNTIL_MEASURED_CALLER_EXISTS`
- `PROMOTE_TO_EXPLICIT_CAPABILITY`
- `OTHER_PROVEN_MODEL_REQUIRING_PLAN_AMENDMENT`

### `RP-07`

The decision record must end in exactly one read-only lifecycle model:

- `READ_ONLY_EVENT_LINKED_VISIT_LIFECYCLE`
- `READ_ONLY_EVENT_LINKED_LIFECYCLE_PLUS_PROPOSAL_ONLY_RESCHEDULE_CANCEL`
- `OTHER_PROVEN_MODEL_REQUIRING_PLAN_AMENDMENT`

No `RP-07` decision may reintroduce Calendar write operations from Node B.

Wave 2 result:

- decision: `READ_ONLY_EVENT_LINKED_LIFECYCLE_PLUS_PROPOSAL_ONLY_RESCHEDULE_CANCEL`
- implementation commit: `gmail-agent:4b9d5b413dd39842555375c7bdfbe9def2717035`
- execution record: `_raw/wave-02/rp-07/EXECUTION.md`
- result: `CLOSED`

## Wave 2 Exit Criteria

Wave 2 may be declared complete only if:

- every scoped package has current proof;
- every scoped package has a frozen decision output;
- every scoped package either closes in Wave 2 or has a proof-backed defer reason tied to a later wave;
- package overlaps have been resolved explicitly;
- historical-data impact is classified per package;
- no package retains a stale Gmail or Calendar write assumption;
- Workflow Registry v1 remains unchanged;
- no package is deferred only for planning convenience.

## Handoff Into Later Waves

Wave 2 hands off only the packages that prove they need a later-wave migration:

- later integrity and architectural waves take only the explicitly deferred packages;
- completion is claimed only after code change, tests, runtime proof and any required observation period;
- if current proof invalidates a planned capability, the package is marked `REMOVE`, `PARK`, or `NO_ACTION` instead of forcing implementation.

Wave 2 final handoff:

- automatic per-signal replay for the Gmail signal worker is deferred with proof until irreversible-path idempotency and recovery are hardened;
- no other Wave 2 package is left open for planning convenience.
