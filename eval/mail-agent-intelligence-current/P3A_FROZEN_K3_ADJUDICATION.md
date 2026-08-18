# P3A — Frozen K3 adjudication

Question answered: why canonical Fresh38 `fresh38_full_current_20260816T124100`
classified these four cases as CAPABILITY, and whether that failure belonged
to the product or the measurement chain.

```text
P3A = ADJUDICATION ONLY
PRODUCT_CODE_CHANGE = 0
EVALUATOR_CHANGE = 0
GT_CHANGE = 0
SCORER_CHANGE = 0
JUDGE_CHANGE = 0
NO_RECAPTURE = YES
NO_MIXED_EXPERIMENT = YES
```

Current tree SHAs are context only. Adjudication target is frozen SUT
`gmail-agent@37d4b37`, attempt `fresh38_full_current_20260816T124100`.

Frozen identities (unchanged, used as-is):

- capture OutDir: `.artifacts/fresh38-full-current-20260816T124100`
- GT `ba144753…` (`ground_truth_changed_from_v4=false`)
- judge file `fresh-understanding-judge.json` sha256 `2387daf90b1f9017…`
- scorer identity `6ac1761b…` — **current modules still hash to the same identity**
- v5 qualification: 27 CLEAN_PASS / 11 CAPABILITY

No new LLM judge. No rescore. Frozen `rescore-v5.json` is the mechanical SoT
because scorer identity still matches.

## Method

For each case, four comparisons then `FIRST_DIVERGENCE_IN_EVALUATION_CHAIN`:

1. INPUT vs PRODUCT OUTPUT
2. PRODUCT OUTPUT vs GROUND TRUTH
3. PRODUCT OUTPUT vs JUDGE VERDICT
4. GT + JUDGE vs deterministic V5 SCORER

Do not start from the label CAPABILITY.

## Cohort verdicts

| case | FIRST_DIVERGENCE | PRIMARY_CLASS | ADJUDICATION_STATUS |
| --- | --- | --- | --- |
| INT-04 | 3 PRODUCT vs JUDGE (`recommended_next_step` BORDERLINE) | `EVALUATOR_WRONG` | COMPLETE |
| NEW-05 | 3 PRODUCT vs JUDGE (`recommended_next_step` BORDERLINE) | `EVALUATOR_WRONG` | COMPLETE |
| FU-01 | 3 PRODUCT vs JUDGE (`gaps` BORDERLINE) | `EVALUATOR_WRONG` | COMPLETE |
| MI-01 | 3 PRODUCT vs JUDGE (`gaps`+`risks` BORDERLINE) | `EVALUATOR_WRONG` | COMPLETE |

V5 step 4 is faithful in all four: `base_primary_outcome=CLEAN_PASS`,
understanding `quality_passed=false` → `primary_outcome=CAPABILITY`.
That is not `MEASUREMENT_WRONG` for this experiment. The scorer applied the
frozen contract to a judge fail.

Shared mechanism (P3B candidate, not executed here):

```text
GT-UNANCHORED_JUDGE_DIMENSION
A case can meet its case-level GT must/must_not and still fail the
understanding judge on a rubric dimension that GT does not require.
v5 then promotes CLEAN_PASS → CAPABILITY.
```

P3B, if opened later, must prove that general class on a positive+negative
cohort. Never `if case_id == FU-01`.

## INT-04

Input: service complaint, outdoor unit knocking since about a week, March install.
No address/phone in the message.

Product: service complaint recognized; missing address/phone; BR `escalate_review`;
`next_best_action_recommendation.action_type=escalate_internal`. Title is a generic
follow-up template (“klient zgłosił zmianę / źródło ciepła: pompa ciepła”).

GT understanding must: service problem + high importance. must_not: marketing.
Product meets GT. Intake GT (not reklama/noise) is outside this K3 quality fail.

Judge: essence/intent/gaps PASS. Only `recommended_next_step` BORDERLINE
(“zalecany krok nie jest wyraźnie określony”), evidence = NBA title.

PRIMARY_CLASS = `EVALUATOR_WRONG` for the canonical CAPABILITY label:
GT was met; the failing dimension is not a GT must.

SECONDARY_FINDINGS: NBA title looks template-contaminated. That is a real
product weakness, but it is not the GT miss that v5 scored.

## NEW-05

Input: asks whether TOP-INSTAL services heat pumps installed by others.

Product intent recognizes third-party / non-TOP-INSTAL install. BR `collect_data`.
NBA title is the same generic “klient zgłosił zmianę / istniejąca instalacja”
template, which is a poorer next-step than the intent text.

GT must: recognize third-party ambiguity. must_not: assume existing TOP-INSTAL
client without evidence. Intent meets GT. Judge essence/intent PASS.

Judge fails only `recommended_next_step` (“escalate_internal but lacks specificity”).
Evidence cites the collect-data reason_pl, not a GT miss.

PRIMARY_CLASS = `EVALUATOR_WRONG` for the canonical failure.

SECONDARY_FINDINGS: NBA title independently misframes the case as an existing
install change. Eligible as a later product fix, not as the 27/38 score cause.

## FU-01

Input: “thanks, I will check the offer and reply next week.” Neutral follow-up.

Product keeps 120 m² / Kraków / 9 kW offer context. GT understanding must is met.
GT planner: no fabricated SITE_VISIT; acceptable `report_gaps_and_stop` or no action.
GT `escalation_expectation=none`.

Judge essence/intent/next_step PASS. Fail = `gaps` BORDERLINE, reason
“lists gaps but does not affect overall understanding”.

PRIMARY_CLASS = `EVALUATOR_WRONG`. The judge itself says the listed gaps are
non-material, then fails the case on them. That is how CLEAN_PASS became
CAPABILITY.

SECONDARY_FINDINGS: BR `escalate_review` vs GT `escalation_expectation=none`.
Product over-escalation signal, not the scored understanding failure.

## MI-01

Input: two intents — Aquarea vs radiators question, plus CWU failure at
ul. Kwiatowa 5 (existing TOP-INSTAL install).

Product intent names both threads. GT must (two distinct intents) is met.
Judge essence/intent PASS.

Judge fails `gaps` and `risks` with “Some … identified, but not all”.
GT does not enumerate required gaps or risks.

PRIMARY_CLASS = `EVALUATOR_WRONG`. Completeness of gap/risk lists is not a
GT must; the stated GT (two intents, do not drop one / do not merge addresses)
was satisfied.

SECONDARY_FINDINGS: none that overturn the GT match. Helpful-only gaps are
verbose, not a missed second intent.

## What this does not authorize

- product fix
- GT edit
- scorer edit
- judge prompt edit
- case-id evaluator exception
- a new Fresh38 run
- treating K3 as “5 remaining product defects”

Current residual inventory after P3A: see `CURRENT_RESIDUAL_MATRIX.md`.
