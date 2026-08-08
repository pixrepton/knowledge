# DIFF_SCOPE

## gmail-agent (owned)

- `tools/gmail_audit/agent_runtime/effective_tools.py` (new)
- `tools/gmail_audit/agent_runtime/planner_run_budget.py` (new)
- `tools/gmail_audit/agent_runtime/known_fact_guard.py` (new)
- `tools/gmail_audit/agent_runtime/draft_sanity.py` (new)
- `tools/gmail_audit/agent_runtime/failure_taxonomy.py` (new)
- `tools/gmail_audit/agent_runtime/envelope_presence.py` (new)
- `tools/gmail_audit/agent_runtime/graph.py`
- `tools/gmail_audit/agent_runtime/openai_agent_client.py`
- `tools/gmail_audit/agent_runtime/tool_result.py`
- `tools/gmail_audit/agent_runtime/tools/handlers.py`
- `tools/gmail_audit/tests/test_planner_execution_fidelity_01.py` (new)

## knowledge (owned)

- `eval/planner-exec-fidelity-01/**`

## Untouched

- `knowledge/eval/phase1-fresh38-merged-v2/**` (frozen measurement)
- measurement contract v2 hashes / scorer / GT
- foreign dirty paths (e.g. root `scripts/__pycache__`, unrelated repos)
