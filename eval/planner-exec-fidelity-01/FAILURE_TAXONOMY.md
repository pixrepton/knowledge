# FAILURE_TAXONOMY

| Class | Owner | Example |
|---|---|---|
| TOOL_UNAVAILABLE | infra | tool not offered / upstream down |
| TOOL_CONFIGURATION_MISSING | infra | `KALK_TOP_BASE_URL is not configured` |
| TOOL_EXECUTION_FAILED | capability | generic handler error |
| TOOL_TIMEOUT | infra | timeout text |
| TOOL_RATE_LIMITED | infra | 429 |
| TOOL_ARGUMENTS_INVALID | planner | missing required args |
| PLANNER_WRONG_TOOL_CLASS | planner | (reserved for semantic class checks) |
| PLANNER_KNOWN_FACT_REASK | planner | ask metraż when known |
| PLANNER_BUDGET_EXCEEDED | planner | max_turns / tool_calls |
| POLICY_ENVELOPE_MISSING | policy | wiring_failure fail-closed |
| POLICY_TOOL_MISMATCH | policy | `policy_blocks_actionable_tool` |
| DOWNSTREAM_RESULT_INVALID | quality | (reserved) |
| DRAFT_SANITY_FAILED | quality | service draft asks OZC |
| SAFE_ABSTENTION | planner | second known-fact reask → stop |

Attached via `ToolResult.failure_class` / `failure_owner` / `retryable` and `snapshot_delta.execution_attribution` (stripped before snapshot validate).
