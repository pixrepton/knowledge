# IQ-01 Protocol — Understanding → Decision quality

Status: active measurement protocol for roadmap **IQ-01**
(`UNDERSTANDING-TO-DECISION-QUALITY-01`).

This protocol closes the residual **"no true frozen pre-run baseline"** with a
pinned capture + dual-score runner. It does **not** claim human-adjudicated
Fresh38 decision-state labels unless an explicit adjudicated label set is added
later.

## Frozen capture (pre-run baseline)

| Field | Value |
| --- | --- |
| Path | `gmail-agent/tools/gmail_audit/tests/fixtures/measurement_contract_v1/fresh-full38-results.json` |
| Manifest | `gmail-agent/tools/gmail_audit/tests/fixtures/measurement_contract_v1/fixture-manifest.json` |
| Expected sha256 | `c04f295293e750856548ac35b4a9126d5946da4e74b6b5df4efebaea33bf736c` |
| Bytes (manifest) | `670035` |
| Capture mode | `production_faithful` |
| Cases in file | 38 |
| Understanding blobs extractable | up to **36** (`INT-02`, `INT-03` lack `understanding`) |

Integrity rule: `run_iq01_frozen_dual_score.py` **must** recompute sha256 of the
capture and refuse to score if it diverges from `fixture-manifest.json`.

This capture is the **frozen pre-run baseline artifact**. Re-running live Gmail /
Fresh38 is out of scope for IQ-01 bounded closeout.

## Cohorts

### Synthetic cohort (self-confirming harness)

| Field | Value |
| --- | --- |
| Path | `cohort.json` (this directory) |
| Size | **13 / 13** |
| Labeling | designed fixture expectations (`expected_decision_state`) |
| Label class | **synthetic_fixture** — not Fresh38 human adjudication |
| Runner | `run_iq01_eval.py` |
| Purpose | prove classifier + sharpen metrics on PII-free fixtures |

Synthetic PASS does **not** prove Fresh38 accuracy. It proves the bounded
Decision-state contract on constructed Understanding blobs.

### Frozen cohort (Fresh38 capture)

| Field | Value |
| --- | --- |
| Source | pinned `fresh-full38-results.json` |
| Size | **36** Understanding rows (of 38 capture cases) |
| Labeling status | **`machine_proposed`** only |
| Adjudicated labels | **none** for the full 36 (do not claim otherwise) |
| Runner | `run_iq01_frozen_dual_score.py` |
| Purpose | dual-score baseline vs sharpened on real frozen Understanding |

Honest labeling rules:

1. **`adjudicated`** — human-approved expected decision state for a case.
   Required for claiming Fresh38 label accuracy. **Not available for all 36.**
2. **`machine_proposed`** — decision state emitted by the current classifier
   (sharpened path). Recorded for inspection / distribution only.
3. **`expected_decision_state`** on the frozen cohort stays **blank** unless an
   adjudicated label exists. Do not copy `machine_proposed` into `expected` and
   then declare PASS as gold accuracy.

If a future label pack lands, store it beside this protocol with explicit
`labeling_status: adjudicated` and a separate sha256; do not silently upgrade
machine proposals.

## Dual-score definition

Runtime owner:

`gmail-agent/tools/gmail_audit/agent_runtime/recommended_next_step_quality.py`

| Score | Input next-step text | Classifier / checks |
| --- | --- | --- |
| **baseline** | raw `next_best_action_recommendation.title_pl` / `reason_pl` (**pre-sharpen**) | `is_vague_next_step` on raw; `classify_decision_state(sharpened_pl=raw…)` + gaps/follow-up helpers |
| **sharpened** | output of `sharpen_recommended_next_step` via `evaluate_understanding_to_decision_quality` | full IQ-01 checks; still **without** gold expected unless adjudicated |

API note:

- Sharpened scoring is first-class (`evaluate_understanding_to_decision_quality`).
- Baseline scoring is composed from the same exported primitives
  (`is_vague_next_step`, `classify_decision_state`, `separate_gaps_vs_risks`,
  `is_meaningful_follow_up_delta`). There is no separate gold expected for frozen.
- If a future API change removes baseline composition, the frozen runner must
  score **sharpened only** and set `baseline_gap: true` in the dual-score summary
  (never invent a fake pre-sharpen score).

## Artifact write policy (no dirty git by default)

Default output root:

```text
C:\top-code-session-scratch\iq01-eval\
```

Override with env `TOP_CODE_SESSION_SCRATCH` →
`%TOP_CODE_SESSION_SCRATCH%\iq01-eval\`, or CLI `--out DIR`.

| Runner | Default write | Optional git-dir write |
| --- | --- | --- |
| `run_iq01_eval.py` | scratch `synthetic-summary.json` | `--write-repo-summary` only (legacy `summary.json` in this dir) |
| `run_iq01_frozen_dual_score.py` | scratch `cohort-manifest.json` + `dual-score-summary.json` | never writes into git tree |

Do **not** commit scratch artifacts. Tracked `summary.json` in this directory is
historical / optional and must not be overwritten by default runners.

## Commands

```powershell
# Synthetic 13/13 → scratch (default)
python knowledge/eval/understanding-to-decision-quality-01/run_iq01_eval.py

# Optional dirty write of repo summary.json (explicit only)
python knowledge/eval/understanding-to-decision-quality-01/run_iq01_eval.py --write-repo-summary

# Frozen dual-score (verifies sha256, writes scratch)
python knowledge/eval/understanding-to-decision-quality-01/run_iq01_frozen_dual_score.py

# Dry mode (sha256 + extract counts, no score files required beyond stdout)
python knowledge/eval/understanding-to-decision-quality-01/run_iq01_frozen_dual_score.py --dry-run
```

Gate A (gmail-agent): pins fixture sha256 and asserts protocol/runner presence
(or dry-run entrypoint). See
`tools/gmail_audit/tests/test_iq01_frozen_dual_score.py`.

## IQ-01 closeout wording

Closing the **frozen pre-run baseline residual** yields at most:

```text
Delivery: COMPLETE_BOUNDED
Proof: CONFIRMED_BY_LOCAL_TESTS (synthetic) + FOCUSED_LOCAL (frozen dual-score harness)
Fresh38 labels: machine_proposed only — NOT adjudicated for all 36
```

Do **not** mark IQ-01 `COMPLETE` (unbounded) or claim human Fresh38 adjudication
from this protocol alone.

## 2026-08-21 disposition

`IQ-01-ADJUDICATED` is closed as `CLOSED_NOT_REQUIRED`, not implemented by
synthetic labels. The existing IQ-01 bounded harness remains valid:

- synthetic cohort: 13/13 PASS;
- frozen capture integrity: sha256 verified;
- frozen dual-score labels: `machine_proposed` only, not gold.

Future human/business labels belong to `REAL-MAIL-INTELLIGENCE-DISCOVERY-01`,
where real historical cases are reviewed with no side effects. Do not backfill
`expected_decision_state` from the current classifier output.
