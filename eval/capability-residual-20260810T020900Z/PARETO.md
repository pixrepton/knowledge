# Residual Pareto

Generated: 2026-08-10T00:11:20.553127+00:00

| cluster | cases | count | FIRST_DIVERGENCE | root cause | classification | business impact | systemic leverage | recommended disposition |
|---|---|---:|---|---|---|---|---|---|
| UNDERSTANDING_GAPS_NEXT_STEP_BORDERLINE | INT-01, INT-04, NEW-02, NEW-03, FU-01, FU-02, FU-06, FU-07, DOC-01, CTX-04, MI-02, MI-03 | 12 | understanding semantic judge: first non-PASS dimension is gaps and/or recommended_next_step BORDERLINE | Understanding gaps/next step BORDERLINE; secondary draft missing thank-you token. | NEEDS_ADJUDICATION:12 | medium | high | operator/eval adjudication before product change |
| KALK_TOP_NON_JSON_RESPONSE | FU-05, DOC-02 | 2 | agent_runtime.kalk_top_client.call_calculate_offer: configured kalk-top route reached response.json() and raised JSONDecodeError | call_kalk_top_quote reached kalk-top but response.json() raised JSONDecodeError. | ACTIONABLE_PRODUCT:2 | medium-high | medium | focused repair candidate |
| DRAFT_REQUIRED_CONTENT_MISS | SVC-05 | 1 | draft_quality deterministic check: factual_correctness.missing contains required clarification content | Draft lacks required clarification request. | ACTIONABLE_PRODUCT:1 | medium-high | medium | focused repair candidate |
| DRAFT_SURFACE_REPLY_NOT_RECOMMENDED | DEC-02 | 1 | reply_drafter output: draft_enabled=false, do_not_send_reasons=[reply_not_recommended] despite planner request_operator_clarification text | Planner produced clarification; reply_drafter surface remains reply_not_recommended/no draft. | ACTIONABLE_PRODUCT:1 | medium-high | low-medium | focused repair candidate |
| KNOWN_FACT_REASK_EVAL_NO_QUALITY_GT | INT-05 | 1 | eval_final_rescore_versioned: score_status=no_quality_ground_truth while planner abstained after known_fact_reask_blocked | Known-fact re-ask blocked; scorer leaves CAPABILITY with no quality ground truth/failing component. | ACTIONABLE_EVAL:1 | medium-high | low-medium | focused repair candidate |
