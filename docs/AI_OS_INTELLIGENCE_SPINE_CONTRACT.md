# AI-OS Intelligence Spine Contract

Status: active contract with bounded implementation slices. Created:
2026-08-20. Current closeout writeback: 2026-08-21.

Purpose: preserve business decision semantics from BusinessReasoning through
tool execution without moving policy authority into the semantic layer.

## Core Rule

```text
Business layer says what to do and who it is for.
Policy says whether it is allowed and with what authority.
Envelope says which tools may realize that approved meaning.
Planner chooses how inside the envelope.
Execution verifies that the planner did not change the meaning.
HITL approves side effects, but does not change action target or intent.
```

## Current Flow

```text
BusinessReasoning
  -> ActionPlan
  -> Case Intelligence
  -> DecisionCandidate
  -> PolicyDecision
  -> ActionProposal v2
  -> PolicyActionEnvelopeV1
  -> effective_tools
  -> Planner
  -> Execution guard
  -> HITL
```

## Responsibility Table

| Layer | Owns | Must not own |
| --- | --- | --- |
| BusinessReasoning / Case Intelligence | Business meaning: `action_type`, target, channel, goal, missing information. | Approval, send authority, policy clearance. |
| PolicyDecision | Authority: allowed/denied, approval/HITL, dry-run/live limits, execution authority. | Rewriting customer-directed work into operator-directed work. |
| PolicyActionEnvelopeV1 | Read-only projection that combines business meaning and policy result into execution constraints. | Recomputing policy, creating new business meaning, deciding approval by semantic rule. |
| effective_tools | Physical affordance filter for tools offered to the planner. | Interpreting customer intent or weakening policy. |
| Planner | Selects one concrete tool and arguments inside the envelope. | Changing `action_type`, target, channel, or goal. |
| Execution guard | Blocks semantic/policy mismatches even if the planner returns a bad tool. | Repairing the decision silently. |
| HITL | Approves, rejects, or edits the side effect proposed by the system. | Changing the intended addressee or action semantics without a new decision. |

## Evidence Finding: allowed_tools Semantics

Current `agent_runtime.effective_tools.compute_effective_available_tools()`
filters the full `available_tools` tuple that would be sent to the planner.
Therefore `PolicyActionEnvelopeV1.allowed_tools` is currently a full planner
whitelist, not merely an action-tool whitelist.

Consequence: semantic envelopes must not narrow `allowed_tools` to a single
action tool unless it is intentional to hide every read-only helper for that
turn. The v1 pattern is:

```text
forbidden_tools: tools that cannot realize the decision meaning
allowed_tools: empty unless a full planner-turn whitelist is required
allowed_action_tools: action tools that may realize this decision meaning
```

`allowed_action_tools` is the action-only whitelist. It must not be treated as
a full planner-turn whitelist.

## Customer Missing-Data Invariant

For a business decision with:

```text
action_type = ask_for_missing_data
target = customer
channel = mail
```

the system must preserve customer-facing clarification through execution.

Allowed policy outcomes include requiring HITL or operator approval before the
message is sent. That approval comes from `PolicyDecision` and is propagated by
`PolicyActionEnvelopeV1`.

Forbidden semantic substitution:

```text
customer/mail/ask_for_missing_data
  -> request_operator_clarification
```

`request_operator_clarification` remains valid only when the missing input is
actually operator-held context or an operator decision.

## Fact-Use Contract

Case truth is `CaseContextPack.active_facts` plus
`CaseContextPack.conflicting_facts`, not message-level HVAC extraction alone.

Hybrid fact handling separates two axes:

```text
trust_state = confirmed | provisional | conflicted
decision_usable = true | false
decision_block_reason = fact_conflict | ""
```

Critical conflicts must block only actions that consume the conflicted fact.
They must not block the entire case by default.

Initial decision-critical fact keys:

- `customer_email`
- `address`
- `heated_area_m2`
- `device`
- `model`
- `service_date`
- `price`
- `amount`
- `warranty`
- `service_obligation`

Examples:

```text
heated_area_m2=180, trust_state=conflicted, decision_usable=false
```

This blocks calculations or offers that require heated area. It does not block
a customer reply that does not consume heated area, such as acknowledging
received documents.

Implemented bounded surface:

- `mailbox_memory.active_facts.annotate_decision_fact_use()`
- `mailbox_memory.active_facts.action_conflict_block()`
- `case_context_contract.build_case_context_pack_vnext()` annotates active
  facts after conflicts are finalized.

Focused proof on 2026-08-20:

- `test_slice3b_policy_execution_spine.py`
- `test_planner_execution_fidelity_01.py`
- `test_rp30_policy_enforcement.py`
- `test_active_facts_decision_usability.py`
- `test_split_conflicting_facts_tiebreak.py`
- `test_rp29_fact_supersession.py`
- `test_case_context_contract.py`
- `test_daszek_v3_operational_feed.py`

Closeout extension on 2026-08-21:

- `gmail-agent:c80be17` proves the missing consumer-side enforcement seam.
- `allowed_action_tools` mismatch is rejected by execution even when the tool is
  not globally forbidden.
- decision-safety metadata is preserved through the normalization boundaries
  needed by the actual dependent kalk/offer consumer.
- dependent kalk/offer action is blocked when it requires conflicted
  `heated_area_m2`.
- independent acknowledgement remains legal with the same conflict.
- final focused proof: `110 passed`.

## Non-Goals

- No Full Fresh38.
- No new parallel spine.
- No case-id special casing.
- No global BusinessReasoning prompt rewrite.
- No global "critical conflict blocks case" rule.
- No policy approval decision inside semantic constraints.

## CanonicalActionDecision (CAD) — Contract + First Enforced Slice (2026-08-21)

Program: `AI-OS INTELLIGENCE SPINE — CONTRACT + FIRST ENFORCED SLICE` (P0).
This section is the contract extension implemented by P0; it does not replace
the Core Rule above.

### Core invariant

```text
After CanonicalActionDecision is created for
  goal / action_type / target / channel,
no further layer may change goal, action_type, target or channel.
Downstream may execute, restrict, block, or request an explicit revision
(DecisionRevisionRequest) — it must not reinterpret the decision.
```

First enforced vertical slice:

```text
action_type = ask_for_missing_data
target      = customer
channel     = mail
```

### Lifecycle split

Two distinct mechanisms, separated by the existence of the CAD:

```text
BusinessDecisionProposal
  -> CanonicalizationFailure        # BEFORE CAD exists; no decision_id yet
  -> NEEDS_REVIEW                   # workflow state, never a new action_type

CanonicalActionDecision (FROZEN)
  -> DecisionRevisionRequest        # AFTER CAD exists; carries decision_id
  -> decision owner -> new CAD
```

- `CanonicalizationFailure` is emitted when a proposal cannot be canonicalized.
  It has `decision_state="NO_CANONICAL_DECISION"`. The workflow outcome is
  `NEEDS_REVIEW` (operational/review state). It is **never** converted into a
  different business action such as `escalate_review`.
- `DecisionRevisionRequest` is emitted when downstream discovers new evidence,
  a conflict, or an impossible precondition after the CAD was frozen. It
  references `decision_id` + `revision` and asks the decision owner for a new
  CAD. Downstream never changes target/action by itself.

### SituationUnderstanding is state, not a target owner

SituationUnderstanding states facts: customer asked X, missing_information=Y,
open_questions=Z, risks, lifecycle, evidence. It does not decide `target`.
The canonicalizer checks logical support of the proposal by the state of
things (e.g. `required_information` is a subset of `missing_information`; no
conflicted/uncertain fact is used as certainty), **not** a
`SituationUnderstanding.target == proposal.target` equality.

### BusinessDecisionProposal

New typed artifact derived from the existing BusinessReasoning result:

```text
goal, action_type, target, channel, required_information[],
confidence, reason, risk_class, proposal_id
```

`BusinessReasoningResult` itself is not extended in P0 (consumer inventory:
~80 files touch the recommendation surface; separate artifact instead).

### CanonicalActionDecision

```text
decision_id      = dec_<uuid4>            # stable across revisions
revision         = int (starts at 1)
semantic_hash    = SHA256(canonical JSON: schema_version, case_id,
                  situation_version, goal, action_type, target, channel,
                  required_information(sorted), semantic_status)
semantic_status  = FROZEN
```

`semantic_hash` excludes `created_at`, rationale text, confidence and
presentation fields. It is the basis for Semantic Conservation checks:
any downstream artifact may reference `decision_id`/`semantic_hash`; none may
change the canonical semantic signature.

### Layer re-roles (P0)

- `ActionPlan` consumes the CAD and answers "how to execute": it carries
  `canonical_decision_id` and its own execution vocabulary
  (`execution_step=prepare_reply`). It does not re-select business meaning.
- `Case Intelligence / NBA` carries `canonical_decision_id` and its own
  projection vocabulary (`case_guidance=ask_for_missing_data`); it keeps
  missing info, risks, readiness, lifecycle, open loops and evidence, but does
  not re-choose the business action after the CAD is frozen.
- Policy adds only authority: `execution_authority` (`prepare_only`),
  `approval_required`, `max_side_effect` (`local_draft`). Policy never changes
  `action_type/target/channel`.
- Safety for the planner comes from capability filtering: the envelope's
  `forbidden_tools` / `allowed_action_tools` are applied in
  `effective_tools`, so `request_operator_clarification` is **not offered**
  for frozen customer/mail actions (planner sees only `generate_draft_reply`
  as the action tool). No special-cased planner prompt path.
- Reference monitor (`graph.py`) blocks any plan that would change
  target/channel relative to the CAD (reason codes:
  `semantic_tool_forbidden_for_action_intent`,
  `canonical_semantic_drift`).

### P0 test surface

- Deterministic spine property suite
  (`test_canonical_action_decision_properties.py`): semantic conservation,
  review invariant, tool availability invariant, unsupported channel,
  forbidden tool, missing_info permutation, policy cannot retarget,
  CanonicalizationFailure -> NEEDS_REVIEW, decision_id/semantic_hash rules.
- Metamorphic LLM cohort (paraphrase, noise, prompt injection) is a separate
  P0.5 track and is not part of the deterministic gate.

### P0 closeout (2026-08-21) — semantic identity propagation + bounded proof

Delivery: `COMPLETE`. Proof: `PASS_LOCAL_BOUNDED`. Full Gate A: `PASS`
(0 failed). Semantic Conservation: `ENFORCED`. First CAD slice: `PROVEN`.
`FULL_FRESH38 = NOT_RUN`. P0.5 / P1 / P2 are **not** started (program order).

#### Semantic identity invariant (beyond canonical_decision_id)

Semantic identity of the first slice is preserved mechanically through every
downstream seam:

```text
CAD.semantic_hash
== ActionPlan.semantic_hash
== NBA.primary_next_action.semantic_hash
== APv2 raw proposal semantic_hash (lineage)
== PolicyActionEnvelopeV1.source_semantic_hash   # Policy + ToolEnvelope seam
== ToolCallPlan.semantic_hash                     # observed identity at execution
== ActionItem.source_semantic_hash                # materialized execution record
```

`source_semantic_hash` is projected from the APv2 record produced from the
CAD-driven ActionPlan; it is never recomputed downstream. The semantic hash
covers only the canonical payload (`case_id`, `situation_version`, `goal`,
`action_type`, `target`, `channel`, sorted `required_information`,
`schema_version`, `semantic_status`); it never includes transient metadata
(`created_at`, rationale, confidence, latency, provider, approval
timestamps).

Projection layers keep their own vocabulary: APv2 projects the frozen
customer/mail decision as `prepare_reply_draft` (execution vocabulary) while
`action_target=customer`, `action_channel=mail` and `source_semantic_hash`
stay frozen. Vocabulary labels are projections; the semantic signature is
the hash.

#### Runtime guard (reference monitor, fail closed)

Before an action tool executes, the reference monitor compares:

```text
expected = PolicyActionEnvelopeV1.source_semantic_hash
observed = ToolCallPlan.semantic_hash
```

- match -> consistent (existing tool-level checks still apply);
- mismatch -> DENY, `reason = canonical_semantic_drift`;
- missing observed hash -> existing correlation/forbidden-tool checks still
  apply (never a silent pass).

The planner client binds the plan to the hash of the envelope it was offered;
if the envelope changes between prompt and execution, the monitor denies.
Denial never rewrites the hash, never recomputes the decision downstream,
never substitutes a tool and never falls back to
`request_operator_clarification`.

#### Bounded runtime proof (CLOSEOUT-03)

One production-faithful trajectory through the `eval_planner_spine_handoff`
harness (no LLM call, no live send):

```text
Signal (service fault, missing diagnostic data)
-> SituationUnderstanding -> BusinessReasoning (collect_data)
-> BusinessDecisionProposal -> CanonicalActionDecision (FROZEN)
-> ActionPlan (execution_step=prepare_reply)
-> Case Intelligence / NBA (case_guidance=ask_for_missing_data)
-> DecisionCandidate -> Policy (allowed_with_review, approval required)
-> PolicyActionEnvelopeV1 (source_semantic_hash == CAD.semantic_hash)
-> effective_tools (generate_draft_reply offered;
   request_operator_clarification filtered: SEMANTIC_TOOL_FORBIDDEN)
-> Reference Monitor (consistent; canonical_semantic_drift=false)
-> generate_draft_reply (ok) -> HITL (draft_ready_for_approval)
```

Result: `action_type=ask_for_missing_data`, `target=customer`,
`channel=mail`; `canonical_decision_id` and `semantic_hash` identical at
every seam; `request_operator_clarification_executed=false`;
`live_send_executed=false`; `HITL_REQUIRED=true`.

Negative proof: a plan attempting `request_operator_clarification` against
the frozen customer/mail CAD is DENIED before execution
(`semantic_tool_forbidden_for_action_intent` +
`canonical_semantic_drift`; `hitl_gate.reason=
semantic_tool_mismatch:request_operator_clarification`).

Artifact:
`.artifacts/intelligence-spine-p0-closeout-20260821T193158/bounded-runtime-trajectory.json`.
Deterministic gates: `test_closeout_p0_bounded_runtime_slice.py` (3),
property suite (36 tests incl. closeout invariants).

## P0.5 — Data vs Authority hardening (2026-08-21)

Program: `AI-OS INTELLIGENCE SPINE — P0.5 DATA vs AUTHORITY HARDENING`.
Status: `CLOSED` (Delivery COMPLETE, Proof PASS_LOCAL_BOUNDED). P1 remains
`NOT_STARTED`.

### Central principle

```text
UNTRUSTED AS AUTHORITY != UNTRUSTED AS INFORMATION
```

External content (customer mail, quoted/forwarded content, attachments, RAG
evidence, external-data-derived tool results) is a legitimate source of
information about the world: it may influence customer intent, facts, missing
information, questions, business reasoning, risk and a future CAD. It may NOT
directly establish or override CONTROL / AUTHORITY / EXECUTION state
(approval, execution_authority, tool availability, policy, operator
authority, execution recipient, canonical case/thread/decision identity,
canonical tool arguments).

### Read-only authority-flow audit (P0.5A-1)

Seams already protected before P0.5: `untrusted_input_boundary` (authority
keys + recipient override on inbound signals), `known_fact_guard`, D3
`gmail_ingress_guard`, `authz` (operator token scope), `policy_action_spine`
+ `effective_tools` (envelope forbidden/allowed tools, ROC not offered for
customer/mail), `graph` reference monitor + protected snapshot fields,
`write_executors` (send/calendar tombstones). Full classification matrix:
`.artifacts/intelligence-spine-p0-5-20260821T194500/p0-5-authority-flow-audit.json`.

Real gaps fixed in P0.5 (minimal, one shared seam):
1. No provenance dimensions existed (source_origin / evidence_authority /
   instruction_authority) — added as `evidence_authority.py`, one common
   contract for email, quoted/forwarded, attachments, RAG and tool results.
2. Execution guard did not bind canonical identity values (case_id,
   thread_id, decision_id, semantic_hash, draft_hash, engagement_id) and did
   not explicitly block approval claims — extended in the existing
   `untrusted_input_boundary.py` (no second execution boundary).
3. Planner prompt mixed external data with instructions — now explicitly
   labels TRUSTED_SYSTEM_INSTRUCTIONS / TRUSTED_OPERATOR_INSTRUCTIONS /
   BUSINESS_STATE / EXTERNAL_EVIDENCE, and the current message is tagged
   `[EXTERNAL_EVIDENCE]` in the reasoning trace (defense in depth; runtime
   enforcement unchanged as the real boundary).

### Three independent dimensions (no flat trust class)

```text
source_origin:         SYSTEM | OPERATOR | CUSTOMER_EMAIL | QUOTED_CONTENT |
                       FORWARDED_CONTENT | ATTACHMENT | RAG | TOOL_RESULT |
                       INTERNAL_STATE | DERIVED | UNKNOWN
evidence_authority:    INTERNAL_SOT | OPERATOR_STATEMENT | CUSTOMER_STATEMENT |
                       AUTHORITATIVE_DOCUMENT | CUSTOMER_DOCUMENT |
                       DERIVED_LLM_CLAIM | UNKNOWN
instruction_authority: NONE | OPERATOR | SYSTEM
```

Defaults: CUSTOMER_EMAIL/QUOTED/FORWARDED/ATTACHMENT/RAG/external
TOOL_RESULT -> `instruction_authority=NONE`; OPERATOR -> OPERATOR; SYSTEM /
INTERNAL_STATE -> SYSTEM. A RAG fragment of a customer document keeps
`source_origin=ATTACHMENT`, `evidence_authority=CUSTOMER_DOCUMENT`,
`produced_by=rag_retriever` — trusted execution mechanism does not make the
output an instruction source.

### Enforcement points (P0.5A-3)

In the existing `untrusted_input_boundary.py`, for action tools on untrusted
inbound signals:

```text
authority override        -> DENY  UNTRUSTED_AUTHORITY_OVERRIDE
recipient override        -> DENY  UNTRUSTED_RECIPIENT_OVERRIDE
approval claim            -> DENY  UNTRUSTED_APPROVAL_CLAIM
canonical identity bind   -> DENY  CANONICAL_ARGUMENT_MISMATCH
                          (proposed value must equal canonical snapshot/
                           envelope value; absent canonical = cannot be
                           established by external text)
```

Reference monitor (existing) still denies forbidden tools for frozen
customer/mail CAD (`semantic_tool_forbidden_for_action_intent`,
`canonical_semantic_drift`). No fallback, no CAD rewrite, no tool swap.

### P0.5B-1 deterministic adversarial suite

`test_untrusted_intelligence_context.py` (51 tests): source/evidence/
instruction classification; tool identity != output authority; classes A–J
(direct mail instruction, recipient hijack, fake approval, fake tool command,
attachment injection, RAG injection, quoted injection, forwarded
impersonation, fake canonical identifiers, negative control: useful external
info still influences reasoning -> CAD); metamorphic clean-vs-control-plane
with `UNAUTHORIZED_CONTROL_PLANE_MUTATION = 0`.

### P0.5B-2 provider-live micro-cohort (bounded)

6 cases, canonical provider chain (DeepSeek `deepseek-v4-flash` priority-1,
then Groq/OpenRouter fallbacks), `.env.local-vps`, no secrets, no live send:

```text
evaluated_cases              = 6
forbidden_tool_attempt_rate  = 0.0
executed_policy_violation_rate = 0.0
```

Artifact:
`.artifacts/intelligence-spine-p0-5-20260821T194500/provider-micro-cohort.json`.
Bounded malicious trajectory (deterministic): source_origin=CUSTOMER_EMAIL,
evidence_authority=CUSTOMER_STATEMENT, instruction_authority=NONE; proposed
tool ROC -> reference monitor DENY (`semantic_tool_forbidden_for_action_intent`
+ `canonical_semantic_drift`); recipient override DENY
(`untrusted_recipient_argument`); approval_state unchanged; ROC and live send
not executed. Artifact:
`.artifacts/intelligence-spine-p0-5-20260821T194500/bounded-runtime-malicious-trajectory.json`.

### Residuals (P1 / P2, not opened)

- Full `DecisionRevisionRequest` runtime (P1), multi-intent `customer_intents[]`
  (P1), argument-level ToolEnvelope for every action class (P1).
- Quoted/forwarded content has no dedicated extraction seam yet; authority
  boundary is enforced by default `instruction_authority=NONE` for all external
  content (residual: structured quoted/forwarded tagging in a later program).
- RAG/attachment records do not yet carry the three provenance dimensions at
  every storage surface; the classification contract is ready and enforcement
  is already source-kind based.
- Provider micro-cohort is bounded (n=6); it measures one model snapshot, not
  a claim of prompt-injection immunity (`PROMPT_INJECTION_SOLVED` is NOT
  claimed).

## P1.1 — Decision Revision Runtime (2026-08-22)

Program: `AI-OS INTELLIGENCE SPINE — P1.1 DECISION REVISION RUNTIME`.
Status: `COMPLETE` / Proof `PASS_LOCAL_BOUNDED`; Full Gate A `PASS` (0 failed).
P1.2 / P1.3 / P1.4 / P1.5: `NOT_STARTED`.

### Core invariant

P0 ustanowil: downstream cannot mutate canonical semantics. P1.1 dodaje:

```text
downstream MAY request revision,
but ONLY the canonical decision layer may create a new CAD revision.
```

Niedozwolone: silent mutation, downstream reinterpretation, in-place CAD
update, downstream edit of `semantic_hash`.

### Decision identity (logical decision vs revision)

```text
decision_id        = dec_<uuid>            # stable decision lineage identity
revision           = monotonic int (1,2,3)
decision_version_id= dec_<id>:r<rev>       # unique concrete version
semantic_hash      = SHA256(canonical semantic payload of THIS revision)
```

`semantic_hash` zalezy wyłącznie od canonical payload (case_id,
situation_version, goal, action_type, target, channel, required_information,
schema_version, semantic_status); NIE haszuje revision, requested_at,
approval/provider, rationale, journal id. Po ponownej walidacji bez zmiany
znaczenia `semantic_hash` MOZE pozostac ten sam, ale `decision_version_id`
MUSI sie zmienic.

### DecisionRevisionRequest (public contract)

```text
request_id, decision_id, current_revision, current_decision_version_id,
reason_code (enum), failed_precondition, source_layer, source_event_id,
evidence_refs, requested_at, status (PENDING|ACCEPTED|REJECTED|SUPERSEDED)
```

Reason codes (P1.1 minimum): NEW_CONFLICTING_EVIDENCE, FAILED_PRECONDITION,
CANONICAL_FACT_CHANGED, STALE_SITUATION, TOOL_CAPABILITY_MISSING,
POLICY_REEVALUATION_REQUIRED (+ legacy IMPOSSIBLE_PRECONDITION,
OUT_OF_SCOPE_REQUEST).

### Lifecycle

```text
CAD r1 [FROZEN/CURRENT]
  -> new evidence / conflict / failed precondition
  -> DecisionRevisionRequest (jedyny kanoniczny path emisji)
  -> canonical decision boundary (canonical_action_decision + ledger)
  -> ACCEPT -> CAD r2 [FROZEN/CURRENT], CAD r1 [SUPERSEDED]
  -> REJECT -> CAD r1 pozostaje CURRENT, request REJECTED
```

Re-evaluation uzywa aktualnego SituationUnderstanding/faktow/BR inputu +
revision reason (trigger + evidence pointer); nigdy copy+patch z requestu.
Request nie niesie pol canonical semantics (target/action_type/channel/...
sa poza kontraktem).

### Supersession + stale invalidation (glowny invariant)

```text
No artifact derived from a superseded CAD revision may authorize execution.
```

`decision_version_id` jest wiazane w: ActionPlan, NBA, APv2,
PolicyActionEnvelopeV1, ToolCallPlan, ActionItem, ActionProposal (approval).
Guard (policy_action_spine + graph): jezeli plan/envelope roznia sie wersja ->
DENY `STALE_DECISION_REVISION` (fail closed, bez podmiany toola, bez fallbacku).
Approval wiaze decision_id + decision_version_id + semantic_hash + draft_hash;
stara zgoda nie autoryzuje nowej rewizji. Concurrency: `expected_current_revision`
(stale request -> STALE_REVISION_REQUEST, bez nowego CAD; duplikat -> co
najwyzej jeden r2). Porzadek rewizji = integer/expected, nigdy timestamp.
`COUNT(current execution-eligible revisions per decision_id) == 1`; naruszenie
-> fail closed (`DecisionRevisionError.one_current_revision_violation`).

### Observability codes

DECISION_REVISION_REQUIRED, DECISION_REVISION_ACCEPTED,
DECISION_REVISION_REJECTED, STALE_DECISION_REVISION, STALE_REVISION_REQUEST,
DUPLICATE_REVISION_REQUEST, SUPERSEDED_DECISION_ARTIFACT. Audit trail:
append-only `DecisionRevisionLedger` (decision_id, old/new version ids,
request id, reason, outcome, created_at) + opcjonalny event sink do istniejacego
event memory. Bez drugiego journala / decision engine / Temporal.

### Bounded proof

`.artifacts/intelligence-spine-p1-1-20260822T100000/bounded-revision-trajectory.json`:
r1 -> CANONICAL_FACT_CHANGED -> r2 (required_information reduced); stale
ToolCallPlan r1 vs envelope r2 -> DENY STALE_DECISION_REVISION (tool not
executed); nowy plan r2 -> consistent -> generate_draft_reply -> HITL;
live_send=false; FULL_FRESH38=NOT_RUN. Commits: `gmail-agent:42440af`,
`5f0979d`, `e42f774`, `99ae4e8`.

Pozostale P1 (not started): P1.2 argument-level ToolEnvelope; P1.3
known/inferred/unknown; P1.4 customer_intents[]; P1.5 unified fact/memory
consolidation proof.

## P1.1P — Durable Decision Revision State (2026-08-22)

Program: `AI-OS INTELLIGENCE SPINE — P1.1P DURABLE REVISION STATE`.
Status: `COMPLETE` / Proof `PASS_LOCAL_BOUNDED`; Full Gate A `PASS` (0 failed).
P1.2 / P1.3 / P1.4 / P1.5: `NOT_STARTED`.

### Problem

P1.1 zamknal lifecycle rewizji, ale `DecisionRevisionLedger` byl in-memory.
P1.1P czyni lineage trwalym: po restarcie procesu odtwarzane sa
`decision_id`, `revision`, `decision_version_id`, `semantic_hash`, status,
`supersedes_version_id` / `superseded_by_version_id`, request + request status
oraz dokladnie jedna CURRENT revision na lineage.

### Durable seam (bez nowej bazy)

Istniejacy canonical store `MailboxMemoryStore` (Postgres + InMemory, ten sam
protokol) rozszerzony addytywnie o dwie tabele:
`mailbox_memory_decision_revisions` oraz
`mailbox_memory_decision_revision_requests`
(schema: `tools/gmail_audit/mailbox_memory/schema.py`). Nowe metody protokolu:
`append_decision_revision`, `append_decision_revision_request`,
`accept_decision_revision_transition`, `fetch_decision_revisions`,
`fetch_decision_revision_requests`, `list_decision_lineage_ids`.

### Ledger = projection/cache, nie SoT

`DecisionRevisionLedger(store=...)` pisze przez store przed aktualizacja
projekcji; `DecisionRevisionLedger.from_store(store)` / `rebuild()` odtwarza
stan po restarcie. Fail closed:

- 0 CURRENT lub >1 CURRENT w durable lineage -> `DecisionRevisionError.rebuild_one_current_violation`;
- porzadek wylacznie po `revision` integer / `expected_current_revision`, nigdy po timestamp.

### Failure atomicity

`accept_decision_revision_transition` wykonuje w jednej transakcji (Postgres:
advisory lock + commit/rollback): old -> SUPERSEDED, new -> CURRENT,
request -> ACCEPTED. Durable state nie moze legalnie zawierac dwoch CURRENT.

### Idempotencja po restarcie

- replay tego samego `request_id` po restarcie -> `DUPLICATE_REVISION_REQUEST`, bez r3;
- stale request (expected r1, durable current r2) -> `STALE_REVISION_REQUEST`;
- stary approval / ToolPlan / envelope r1 po restarcie -> DENY `STALE_DECISION_REVISION`;
- audit trail rekonstruowany z durable lineage + requests.

### Bounded proof

`.artifacts/intelligence-spine-p1-1p-20260822T110000/restart-trajectory.json`
(+ `run_restart_trajectory.py`): r1 -> accept -> r2 -> zniszczenie ledgera ->
rebuild -> current=r2, r1 SUPERSEDED, duplicate/stale guards, old
approval/ToolPlan DENY, nowy plan r2 -> generate_draft_reply -> HITL.
Deterministic suite: `test_decision_revision_durable_restart.py` (10 testow).
Commit: `gmail-agent:f57028ea`.

### Production worker boot wiring (P1.1P final runtime closeout)

Production seam: `build_mailbox_memory_runtime(settings)` ->
`MailboxMemoryRuntime.bootstrap()` (signal worker `_build_runtime_context`,
HITL bridge, api_app). `bootstrap()` wykonuje `store.bootstrap()` (tabele),
po czym buduje `runtime.decision_revision_ledger` przez
`build_store_backed_decision_ledger(store)` (from_store + rebuild). Ledger
uzywany przez runtime jest store-backed; in-memory ledger bez store pozostaje
wyłącznie dla unit tests / jawnych test doubles.

Fail-closed boot: jesli rebuild wykryje 0 CURRENT / >1 CURRENT / uszkodzony
lineage -> `DecisionRevisionStateInvalidError` z observable reason code
`REVISION_STATE_INVALID` (detail: `rebuild_one_current_violation`). Worker
nie wybiera decyzji heurystycznie; nie uzywa timestamp/latest-wins.

### Real Postgres runtime proof

Testy (`test_decision_revision_worker_boot.py`, 5 testow; Postgres czesc
uruchamiana z `MAILBOX_MEMORY_TEST_DATABASE_URL`) przeszly przez production
boot seam na lokalnym canonical mailbox-memory Postgres
(container `gmail-agent-mailbox-memory`, testowa baza, bez danych
produkcyjnych):

- worker restart round-trip: CAD r1 -> ACCEPT (r2) -> zniszczenie runtime ->
  nowy boot -> `current_revision=2`, r1 SUPERSEDED, r2 CURRENT;
- atomicity: `COUNT(CURRENT) == 1` po commit; ponowny accept tego samego
  old CAD -> RuntimeError `decision_revision_conflict`, durable state bez
  czesciowej rewizji;
- stale safety po realnym restarcie: old ToolPlan r1 -> DENY
  `STALE_DECISION_REVISION`, old approval -> INVALID, duplicate ->
  `DUPLICATE_REVISION_REQUEST` (bez r3), stale -> `STALE_REVISION_REQUEST`;
- fail-closed boot: 2 CURRENT / 0 CURRENT w durable state ->
  `REVISION_STATE_INVALID`.

Artefakt:
`.artifacts/intelligence-spine-p1-1p-final-20260822T120000/p1-1p-postgres-worker-restart.json`
(store_backend=postgres, przed/po restarcie, current_revision_count=1,
old_tool_plan_verdict=STALE_DECISION_REVISION, old_approval_verdict=INVALID,
duplicate/stale verdicts, live_send=false).

Commity: `gmail-agent:f57028ea` (durable seam), `gmail-agent:b13945d0`
(worker boot wiring + fail-closed + Postgres tests). Full Gate A
`PASS` (2772 passed / 17 skipped / 24 subtests / 0 failed).
`FULL_FRESH38=NOT_RUN`, `LIVE_SEND=false`. P1.2 / P1.3 / P1.4 / P1.5:
`NOT_STARTED`.

## P1.2 — Argument-Level Tool Envelope (2026-08-22)

Program: `AI-OS INTELLIGENCE SPINE — P1.2 ARGUMENT-LEVEL TOOL ENVELOPE`.
Status: `COMPLETE` / Proof `PASS_LOCAL_BOUNDED`; Full Gate A `PASS`
(2831 passed / 17 skipped / 24 subtests / 0 failed).
P1.3 / P1.4 / P1.5: `NOT_STARTED`.

### Cel

Jeżeli planner wybral dozwolone narzedzie, nie moze zmienic znaczenia lub
authority dzialania przez dowolne argumenty. Zasada:

```text
ALLOWED TOOL != ALLOWED ARBITRARY ARGUMENTS
Planner may propose. Planner may not establish canonical execution state.
```

### Realny schema pierwszego slice (audyt, nie nazwy z promptu)

`generate_draft_reply` (Model A — deterministyczny kompozytor szablonu):
jedyne pole w `tool_schemas.py` to `intent` (enum `quote|missing_info`,
`additionalProperties: false`). Handler czyta tylko `intent`; case_id,
body, body_hash, draft_id pochodza z runtime snapshot / deterministycznej
produkcji. Pelna tabela argumentow: `p1-2-argument-flow-audit.json`.

### Ownership model

- CANONICALLY_BOUND (plan-level, istniejące guardy): `decision_version_id`
  (STALE_DECISION_REVISION), `semantic_hash` (canonical_semantic_drift).
- PARTIALLY_BOUND → P1.2 BIND: `intent` = ONE_OF(`[missing_info]`) dla
  `ask_for_missing_data`; OUT-OF-DOMAIN → `ARGUMENT_OUTSIDE_CANONICAL_SET`.
- ABSENT (planner must not supply): `case_id`, `thread_id`, `customer_id`,
  `decision_id`, `decision_version_id`, `semantic_hash`, `action_type`,
  `target`, `channel`, `recipient`, `required_information`, `attachment_ids`,
  `draft_hash`, `approval_receipt`, `body`, `subject` → wykryty w arguments
  → `ARGUMENT_NOT_ALLOWED`; nieznany argument → `ARGUMENT_NOT_ALLOWED`.
- NOT_APPLICABLE / LATER_STAGE_ONLY: `attachment_ids` (inny slice),
  `approval_receipt` / `draft_hash` (post-draft / approve / send).
- PLANNER_GENERATED: brak w tym toolu (schema celowo nie zawiera treści);
  generative freedom zyje w handlerze (szablony) + draft sanity.

### Kontrakt constraintów

Typed `ArgumentConstraint` (bez generycznego DSL): `argument_name`,
`constraint_mode` (EXACT | ONE_OF | SUBSET_OF | PRESENT | ABSENT |
PLANNER_GENERATED), `expected_value`/`allowed_values`, `source_kind`,
`source_ref`, `decision_id`, `decision_version_id`, `semantic_hash`.
Normalizacja deterministyczna i typowana (set ordering / whitespace / case to
reprezentacja, nie semantyka); brak LLM w ocenie zgodnosci.

### Projekcja i enforcement

- `project_slice_argument_constraints(...)` — deterministyczna projekcja z
  (envelope + revision); zwraca [] poza bounded slice. Wynik trafia do
  `PolicyActionEnvelopeV1.argument_constraints` (persist w
  `_semantic_tool_constraints` z kanonicznego `nba_action`, nie z APv2
  `prepare_reply_draft`).
- Reference monitor (`evaluate_semantic_policy_plan_consistency`) waliduje
  `plan.arguments` per constraint i zwraca `argument_violations`
  (argument_name, mode, expected, proposed, decision_version_id).
- `graph._policy_enforcement_block` DENY przed wykonaniem dla:
  CANONICAL_ARGUMENT_MISMATCH, ARGUMENT_NOT_ALLOWED,
  ARGUMENT_OUTSIDE_CANONICAL_SET, MISSING_REQUIRED_CANONICAL_ARGUMENT,
  UNBOUND_EXECUTION_ARGUMENT, STALE_DECISION_REVISION,
  canonical_semantic_drift. Bez silent repair, bez fallbacku do ROC.
- Durable-current: envelope musi byc projekcja CURRENT durable CAD revision
  (P1.1P ledger przez `ToolExecutionContext.decision_revision_ledger`,
  wiring w `execute_agent_run`); mismatch → DENY STALE_DECISION_REVISION.
  Nowa rewizja CAD → nowa projekcja constraintów (stare envelope stale).
- Tool schema nie zostal zmieniony (intent-only); provider-live cohort NIE byl
  wymagany (enforcement po stronie runtime).

### Bounded proof

`.artifacts/intelligence-spine-p1-2-20260822T130000/`:
`p1-2-argument-flow-audit.json` (read-only audit) +
`bounded-argument-trajectory.json` (positive PASS→HITL; 7 negative plans
DENY bez wykonania; revision test r1 DENY / r2 PASS; approval_required=true,
live_send=false). Deterministic suite: 58 testów w
`test_tool_argument_constraints.py`, `test_tool_argument_reference_monitor.py`,
`test_tool_argument_revision_binding.py`, `test_tool_argument_properties.py`.
Commity: `gmail-agent:950f9670`, `gmail-agent:4cc7595a`.

### Naprawiony pre-existing defect (Gate A blocker)

`MetricsCollector` uzywal nie-reentrantnego `threading.Lock`, a `_flush` →
`report()` re-akwizytowal ten sam lock (deadlock przy progu flush 100
zdarzeń). Fix: `threading.RLock` + regression guard
(`test_agent_runtime_metrics_flush.py`). Golden schema
`docs/contracts/engagement_snapshot_v2.schema.json` zregenerowany po
additive fields.

### Residuale

- Intent binding dla envelope bez persisted projection i z niejednoznacznym
  `action_intent` (np. legacy `prepare_reply_draft`) pozostaje domena schema
  (quote|missing_info); produkcja zawsze persistuje kanoniczna projekcję.
- Argument-level constraints dla innych tools / action classes (attachment
  sets, approval/send stages) — późniejsze slice'y.
- Wpięcie ledgera do kazdego produkcyjnego `ToolExecutionContext` (obecnie w
  `execute_agent_run`; inne konstrukcje ctx przekazują go jawnie w proofach).
