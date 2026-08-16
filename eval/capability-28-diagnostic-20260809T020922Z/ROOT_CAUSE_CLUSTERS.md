# CAPABILITY-28 Root Cause Clusters

Status: read-only diagnostic. Counts below are FIRST_DIVERGENCE counts, not every downstream symptom.

## CLUSTER-01 - BRAIN1_POLICY_APV2_HANDOFF_MISSING

root cause: DecisionCandidate exists, but frozen planner signal did not carry/persist PolicyDecision and ActionProposal v2 envelope before Brain2. Policy guard correctly failed closed.
affected cases: INT-05, INT-06, NEW-02, NEW-04, NEW-05, SVC-03, CTX-02, CTX-03, MI-03
count: 9
first divergence: BRAIN1 -> BRAIN2 HANDOFF / POLICY DECISION / ACTION PROPOSAL
type: BRAIN1_BRAIN2_HANDOFF
shared code path: Frozen artifact: planner.envelope_presence=wiring_failure + canonical_action_proposal_v2_not_found. Current code: eval_planner_spine_handoff.py:24-95 and :138-159; envelope_presence.py:88-98; graph.py:769-803.
likely leverage: Focused proof that current recovery/Fresh38 path uses the handoff should recover the cases with no earlier product failure.
confidence: high

## CLUSTER-02 - CASE_LINK_CONTEXT_SIGNAL_NOT_TRUSTED

root cause: CaseContextPack carries prior facts/case_id, but case_link_decision is empty/weak in the intelligence/Understanding projection, so follow-ups are treated as weakly linked and over-reviewed.
affected cases: FU-01, FU-02, FU-05, FU-06, FU-07, DOC-03, MI-02, DEC-02
count: 8
first divergence: CORRELATION / CONTEXT SELECTION / BUSINESS REASONING
type: CORRELATION
shared code path: gmail_intake.link_case_context -> case_linker; intake_shared_downstream passes case_link_result before mailbox pack refresh; understanding_output exposes case_link_decision from case_link_result only.
likely leverage: Teach/route case link from verified CaseContextPack or entity link into Brain1 projection before Business/Understanding gap generation.
confidence: medium-high

## CLUSTER-03 - OVERSTRICT_GAP_AND_REVIEW_GUIDANCE

root cause: Business/Understanding converts answerable sales/service/technical messages into blocking missing-data/review checklists, even when expected behavior allows answer, service triage, or bounded clarification.
affected cases: INT-01, INT-04, NEW-03, SVC-01, SVC-04, DOC-02, MI-01
count: 7
first divergence: BUSINESS REASONING / CASE GUIDANCE / UNDERSTANDING SYNTHESIS
type: UNDERSTANDING_SYNTHESIS
shared code path: business_reasoner output -> case_intelligence.missing_info -> understanding_output.missing_critical_fields and risks.
likely leverage: Separate actionable answer/triage from quote-ready data collection; demote helpful facts from critical gaps where ground truth says the current message is already actionable.
confidence: medium

## CLUSTER-05 - DRAFT_REPLY_GATE_AND_PROMISE_SEMANTICS

root cause: Draft path either disables a safe clarification due review gating or emits a service draft with unsupported scheduling promise wording.
affected cases: SVC-02, SVC-05
count: 2
first divergence: DRAFT / BUSINESS DECISION GATE
type: DRAFT_REASONING
shared code path: reply_drafter.should_draft_reply/fallback_reply_drafter plus draft commitment/sanity gates.
likely leverage: Tight focused tests for ambiguous service clarification and third-person scheduling promises.
confidence: medium

## CLUSTER-04 - DRAFT_CONTEXT_BUDGET_OVERFLOW

root cause: Reply drafter input exceeded provider TPM/request budget and fell back to non-draft output.
affected cases: NEW-01
count: 1
first divergence: DRAFT INPUT / DRAFT GENERATION
type: DRAFT_INPUT
shared code path: reply_drafter.run_reply_drafter -> central_llm_stage; fallback_reply_drafter returns draft_enabled=false on GroqClientError.
likely leverage: Add focused draft prompt budget proof and reduce assembled context for reply_drafter before full rerun.
confidence: high

## CLUSTER-06 - EVAL_EXPECTATION_FALSE_NEGATIVE

root cause: Frozen judge/scorer marks a case failed although the captured Understanding contains the required budget context; NEW-03 also has a secondary extraction scoring-spec false positive, but its first product divergence is over-gap Understanding.
affected cases: CTX-04
count: 1
first divergence: SCORING / EXPECTATION INTERPRETATION
type: EVAL_EXPECTATION_ISSUE
shared code path: fresh-understanding-judge.json semantic verdict vs captured Understanding fields; eval_measurement_scoring field spec parser for NEW-03 secondary extraction issue.
likely leverage: Do not change product for this one before adjudicating expectation/scorer evidence with a frozen-contract-compatible micro-proof.
confidence: high

## Cross-Cutting Observation

Missing policy/action envelope appears in 25 CAPABILITY cases, but it is first divergence only in CLUSTER-01. In the other cases, earlier product or expectation divergence already polluted the downstream planner/draft path.
