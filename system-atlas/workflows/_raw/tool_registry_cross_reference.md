# Raw inventory — gmail-agent agent-tool registry cross-reference

Generated during the mechanical reverse-audit pass (2026-07-30). Source of truth for tool
dispatch: `gmail-agent/tools/gmail_audit/agent_runtime/tools/handlers.py`, `HANDLERS` dict
(lines 1086-1116).

## Registered tool names (HANDLERS dict keys, verbatim)

1. `search_gmail_thread` → `search_gmail_thread` (legacy read tool)
2. `list_drive_folder` → `list_drive_folder` (legacy read tool)
3. `generate_draft_reply` → `generate_draft_reply` (legacy read tool)
4. `query_anything` → `query_anything` (Generic Hands — CONFIRMED BROKEN on 2/4 sub-branches,
   `WORKFLOW_GAPS.md` item 1)
5. `propose_mutation` → `propose_mutation` (Generic Hands — the mutation-proposal gateway,
   includes the `case_coherence` validation gate, `EV-00126`)
6. `propose_plan` → `propose_plan` (Generic Hands)
7. `read_google_drive_file` → `read_google_drive_file`
8. `extract_facts_from_text` → `extract_facts_from_text`
9. `check_cp2025_eligibility` → `check_cp2025_eligibility_tool`
10. `call_kalk_top_quote` → `call_kalk_top_quote` (confirms D2, `EV-00099`-adjacent)
11. `request_operator_clarification` → `request_operator_clarification`
12. `report_gaps_and_stop` → `report_gaps_and_stop`
13. `request_human_handoff` → `request_human_handoff`
14. `retry_hard_parse` → `retry_hard_parse`
15. `search_rag_knowledge` → `search_rag_knowledge` (CONFIRMED CORRECT sibling of `query_anything`'s
    broken RAG branch, `EV-00077`)
16. `get_pipeline_summary` → `_bp_dispatch(..., "get_pipeline_summary")` (Business Pulse)
17. `get_client_health` → `_bp_dispatch(..., "get_client_health")` (Business Pulse)
18. `get_daily_delta` → `_bp_dispatch(..., "get_daily_delta")` (Business Pulse)
19. `get_win_rate` → `_bp_dispatch(..., "get_win_rate")` (Business Pulse — **CONFIRMED
    CONTRACT_DRIFT, `EV-00136`**: queries `status='won'`, real vocabulary uses `status='completed'`)
20. `get_top_clients` → `_bp_dispatch(..., "get_top_clients")` (Business Pulse)
21. `get_revenue_forecast` → `_bp_dispatch(..., "get_revenue_forecast")` (Business Pulse —
    depends on `get_win_rate`'s `rate_pct`, so inherits the same contract-drift distortion)
22. `get_system_health_snapshot` → `_bp_dispatch(..., "get_system_health_snapshot")` (Business Pulse)
23. `get_business_signals` → `_bp_dispatch(..., "get_business_signals")` (Business Pulse)
24. `get_agent_activity_summary` → `_bp_dispatch(..., "get_agent_activity_summary")` (Business Pulse)

## Cross-reference method

For each tool name, confirmed: (a) a handler function/lambda exists in `HANDLERS` (all 24 do —
no orphaned tool declarations found), (b) the handler's implementation was opened for the
security/business-critical subset (`query_anything`, `propose_mutation`, `call_kalk_top_quote`,
`search_rag_knowledge`, `get_win_rate`, `get_revenue_forecast`) rather than all 24 exhaustively,
given time budget — the remaining Business Pulse tools (`get_pipeline_summary`, `get_client_health`,
`get_daily_delta`, `get_top_clients`, `get_system_health_snapshot`, `get_business_signals`,
`get_agent_activity_summary`) and legacy read tools were NOT individually opened this pass —
flagged as still open for a deeper reverse-audit pass, not silently claimed as verified.

## Result classification

- 24/24 tool names have a registered handler — no `MISSING_EXECUTOR` found for tool registration
  itself.
- 1 confirmed `CONTRACT_DRIFT` (`get_win_rate`, cascades into `get_revenue_forecast`'s `rate_pct`
  input).
- 0 confirmed `MISSING_PRODUCER` at the tool-registration layer (all registered tools have code
  behind them) — the `MISSING_PRODUCER` findings this session (calendar proposal, sale outcome)
  are at a different layer (the data/state the tool or executor depends on), not the tool
  registration layer itself.
- Not yet done: cross-referencing tool names AGAINST `tool_schemas.py`'s planner-facing schema
  declarations (i.e., is every `HANDLERS` key also declared to the LLM planner, and vice versa?)
  — this specific sub-check was not completed this pass, flagged as an open item for a future
  reverse-audit continuation.
