# TOOL_BUDGET_CONTRACT

```text
PlannerRunBudget
  max_turns              ← min(AGENT_MAX_ROUNDS, steps_remaining)
  max_total_tool_calls   ← derived from constitution tool_budget sum (capped)
  max_research_calls     ← search_rag_knowledge constitution limit
  max_repeated_objective_calls = 1  (existing RAG duplicate guard)
  max_tokens             = 0 (reserved; not enforced)
  max_tool_failures      ← bounded from rounds
  deadline_seconds       = 0 (reserved)
```

Enforcement:

1. Computed at start of `AgentGraphEngine._run`
2. `check_before_turn()` before each planner call
3. `record_turn()` after each tool attempt
4. On exceed → HITL `planner_budget_exceeded:*`, no further LLM turn
5. Returned on `AgentGraphRunResult.planner_run_budget`

Coexists with existing per-tool `MAIL_AGENT_TOOL_BUDGET` in `AgentToolRegistry`.
