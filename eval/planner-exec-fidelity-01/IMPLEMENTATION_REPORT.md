# IMPLEMENTATION_REPORT

## Modules added

| File | Role |
|---|---|
| `agent_runtime/effective_tools.py` | `compute_effective_available_tools` — config/freeze gates |
| `agent_runtime/planner_run_budget.py` | `PlannerRunBudget` / `build_planner_run_budget` |
| `agent_runtime/known_fact_guard.py` | known-fact reask detection |
| `agent_runtime/draft_sanity.py` | customer draft sanity gate |
| `agent_runtime/failure_taxonomy.py` | failure classes + attribution |
| `agent_runtime/envelope_presence.py` | expected_absence vs wiring_failure |

## Wired into

| File | Change |
|---|---|
| `openai_agent_client.py` | effective tool filter + unavailable notes in prompt |
| `graph.py` | effective tools before plan; budget loop; known-fact guard; envelope fail-closed; budget on `AgentGraphRunResult` |
| `tools/handlers.py` | draft sanity on `generate_draft_reply`; known-fact on clarification; kalk attribution |
| `tool_result.py` | optional `failure_class` / `failure_owner` / `retryable` |

## Tests

- `tests/test_planner_execution_fidelity_01.py`
- Gate A: `python -m pytest tools/gmail_audit/tests -q` → **2086 passed**, 10 skipped
