# Mail-agent intelligence — current program state

Owner: this directory. Last updated: 2026-08-20 (SVC-05 closed).

This is the tracked current overlay for the 11-CAPABILITY program.
It supersedes the gitignored working copy
`.artifacts/mail-agent-intelligence-20260817/` as current truth.
It does **not** rewrite frozen Fresh38 evidence.

```text
P2_CAPABILITY_CAUSAL_OBSERVABILITY = PASS / CLOSED
P2_PRODUCT_SHA = ae59750565d2a0e334f646a4d5f7bc94bd92f602
P2_RUNNER_SHA = 800318a7a2a34cfd0865889a0daacdcf530d9cda
OBSERVABILITY_SEMANTICS_CHANGE = 0
NEW_CAPTURE_HIST_UNRECOVERABLE = 0
CAPABILITY-OBSERVABILITY-01 = CLOSED
FRESH38_MEASUREMENT_QUALIFICATION = REQUALIFIED
CURRENT CAPABILITY BASELINE = 27 CLEAN_PASS / 11 CAPABILITY (v5, threshold 34)
FROZEN_EXPERIMENT = .artifacts/fresh38-full-current-20260816T124100
FROZEN_SUT = gmail-agent@37d4b37
P3A_FROZEN_K3_ADJUDICATION = COMPLETE (INT-04/NEW-05/FU-01/MI-01 PRIMARY_CLASS=EVALUATOR_WRONG)
P4_VS_P3B_FORK = FROZEN (NEXT_EXECUTION=P4, NEXT_SLICE=P4-A_MI-02, P3B=DEFERRED_TO_STEP_5)
P4A_MI02 = COMPLETE (PRIMARY_CLASS=PRODUCT_WRONG; minimal fix implemented)
P4A_PRODUCT_SHA = f6c3b6a0006c7185708c729d68b42ac14d3ceb79
P4B_BOUNDED_COHORT = COMPLETE (MI-02 re-proved; INT-01 no regression; SVC-05 diagnosed)
P4B_SVC05 = CLOSED
SVC-05_PRODUCT_FIX = PASS (gmail-agent 0a407cb3)
SVC-05_DOWNSTREAM_FIX = PASS (gmail-agent 78603fb; final planner-hint closeout 70c3d94)
SVC-05_FINAL_PROVIDER_LIVE_PROOF = PASS (.artifacts/svc05-final-live-proof-fix-20260820T113843/recovery-attempt-2)
P4C_CTX03 = FIXED_IN_CODE (replace_message_facts conflicts surfaced)
P3B = COMPLETE (INT-04/NEW-05/FU-01/MI-01 evaluator applicability fixed)
P1.4B = LIVE_PASS (INT-05/DOC-02/NEW-03 no call_kalk_top)
SVC-05 = CLOSED (collect_data -> DRAFT_ACCEPTED -> prepare_reply -> ask_for_missing_data/mail -> generate_draft_reply -> HITL; no executed request_operator_clarification)
FRESH38_RERUN = NO (focused/bounded proofs only)
NEXT = STOP (11 CAPABILITY closed; SVC-05 closed)
```

INT-01 is `HISTORICAL_ONLY / REGRESSION_WATCH`. SVC-05 was current-reproduced
with recoverable causal chain and is now fixed with a deterministic
BusinessReasoning normalization, not an LLM-prompt or case-id exception.
K3 P3A is COMPLETE: INT-04, NEW-05, FU-01, MI-01 are `EVALUATOR_WRONG`
for the canonical 27/38 CAPABILITY label. See `P3A_FROZEN_K3_ADJUDICATION.md`.

Do not treat current Groq recapture as the reason the canonical 27/38 failed.
Do not write operator decisions from this technical closeout.

MI-02 current multi-intent collapse was adjudicated `PRODUCT_WRONG` and the
minimal fix is implemented in gmail-agent (see
`P4A_MI02_ADJUDICATION_AND_FIX.md`). Capability re-proof remains pending.

SVC-05 was diagnosed `PRODUCT_WRONG` and is now closed. The product fix uses
`customer_clarification_possible`: when intake has already marked the service
signal `ambiguous_signal`, review is required only because customer data is
missing, and BusinessReasoning named concrete gaps, the validator normalizes
`escalate_review` to `collect_data`. The downstream fix preserves that customer
clarification through ActionPlan/Case Intelligence/planner instead of
substituting `request_operator_clarification`.

Bounded runtime re-proof is recorded in `P4B_BOUNDED_COHORT_PROOF.md` for the
first product fix. Final provider-live closeout is
`.artifacts/svc05-final-live-proof-fix-20260820T113843/recovery-attempt-2`:
SVC-05, SVC-02 and MI-03 are 3/3 `QUALIFIED`; SVC-05 keeps
`collect_data -> DRAFT_ACCEPTED -> prepare_reply -> ask_for_missing_data/mail
-> generate_draft_reply -> HITL` and
`operator_clarification_requested=false`.

CTX-03 was adjudicated `PRODUCT_WRONG`: fact supersession silently hides the
120 vs 160 contradiction. The design contract is pending an operator decision
(`P4C_CTX03_DESIGN_CONTRACT.md`).

Closeout: CTX-03 is fixed in code (customer-message value changes now surface
as conflicts). P3B fixed the four GT-unanchored evaluator dimensions. P1.4B
live check passed (no unexpected kalk-top tool use). SVC-05 is closed by the
general BusinessReasoning contract signal plus downstream customer-clarification
preservation. No full Fresh38 re-run. See `P4_FINAL_ACCOUNTING.md` for the
11-case resolution.
