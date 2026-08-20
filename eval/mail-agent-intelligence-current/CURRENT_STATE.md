# Mail-agent intelligence — current program state

Owner: this directory. Last updated: 2026-08-20 (P4-A MI-02).

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
NEXT = P4-B SVC-05 BR/gate diagnosis + optional fix; P3B deferred to step 5
```

INT-01 is `HISTORICAL_ONLY / REGRESSION_WATCH`. SVC-05 is current-reproduced
with recoverable causal chain; product diagnosis remains pending.
K3 P3A is COMPLETE: INT-04, NEW-05, FU-01, MI-01 are `EVALUATOR_WRONG`
for the canonical 27/38 CAPABILITY label. See `P3A_FROZEN_K3_ADJUDICATION.md`.

Do not treat current Groq recapture as the reason the canonical 27/38 failed.
Do not write operator decisions from this technical closeout.

MI-02 current multi-intent collapse was adjudicated `PRODUCT_WRONG` and the
minimal fix is implemented in gmail-agent (see
`P4A_MI02_ADJUDICATION_AND_FIX.md`). Capability re-proof remains pending.
