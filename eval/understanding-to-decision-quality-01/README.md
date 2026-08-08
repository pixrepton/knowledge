# IQ-01 — Understanding → Decision quality (bounded)

Status: bounded eval harness for roadmap **IQ-01** (`UNDERSTANDING-TO-DECISION-QUALITY-01`).

See **[PROTOCOL.md](./PROTOCOL.md)** for frozen capture pin, dual-score rules, labeling honesty,
and scratch artifact policy.

## Done-when (bounded)

- `recommended_next_step` not vague after sharpen
- Follow-up delta handled (FU-06 / FU-07 style)
- Gaps vs risks separated
- Each synthetic cohort case lands in exactly one of:
  `execute` / `approve` / `reply` / `complete-info` / `wait` / `close` / `consciously-do-nothing`
- Frozen pre-run baseline: pinned `fresh-full38-results.json` + dual-score runner
- **No claim** of human-adjudicated Fresh38 labels for all 36 unless separately labeled

## Cohorts

| Cohort | File / source | Labels | Size |
| --- | --- | --- | --- |
| Synthetic | `cohort.json` | `synthetic_fixture` expectations | 13 |
| Frozen Fresh38 | fixture `fresh-full38-results.json` | `machine_proposed` only | 36 Understanding / 38 capture |

## Runtime owner

Sharpening + classifier live in:

`gmail-agent/tools/gmail_audit/agent_runtime/recommended_next_step_quality.py`

## Commands

```powershell
# Focused unit tests (Gate A subset)
cd gmail-agent
python -m pytest tools/gmail_audit/tests/test_understanding_to_decision_quality.py tools/gmail_audit/tests/test_iq01_frozen_dual_score.py -q

# Synthetic bounded eval → session scratch (default; does not dirty git)
python knowledge/eval/understanding-to-decision-quality-01/run_iq01_eval.py

# Frozen dual-score → session scratch
python knowledge/eval/understanding-to-decision-quality-01/run_iq01_frozen_dual_score.py

# Dry integrity check
python knowledge/eval/understanding-to-decision-quality-01/run_iq01_frozen_dual_score.py --dry-run
```

Default artifacts: `C:\top-code-session-scratch\iq01-eval\` (or `%TOP_CODE_SESSION_SCRATCH%\iq01-eval\`).
