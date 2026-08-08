# Roadmap 1.3 — recommended_next_step quality

## Status: done (bounded product) — `confirmed by local tests`

Vague Brain1 NBA (`ręczna ocena` / `escalate_internal` / `escalate_review`) → concrete operator/planner next step.

### What changed

| Layer      | Change                                                                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source     | `understanding_output.build_understanding_output` + `validate_understanding_invariants` call `apply_nba_quality_to_understanding`                 |
| Module     | `agent_runtime/recommended_next_step_quality.py` — sales/service/admin/follow-up templates; empty NBA stays empty; `planner_action_hint`          |
| Projection | `build_case_understanding_projection` re-sharpens + emits `planner_action_hint`                                                                   |
| Contract   | `CaseUnderstandingProjection.planner_action_hint`                                                                                                 |
| Planner    | `_compact_view` surfaces `preferred_operator_next_step_pl` + `preferred_tool_class`; system prompt binds as DOMINUJĄCY cel + ZAKAZ vague escalate |

### Proof

```text
python -m pytest tools/gmail_audit/tests -q
# 2095 passed, 10 skipped, 24 subtests passed
```

Targeted: `test_planner_spine_handoff_closeout.py` (sharpen, apply, compact view, prompt binding).

### Intentionally not done

- Full Fresh 38 re-run
- Live LLM re-proof of INT-01/04 (covered by closeout-02)
- Inventing NBA when Brain1 left it empty
