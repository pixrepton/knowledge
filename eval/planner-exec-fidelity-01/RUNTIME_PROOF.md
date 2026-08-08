# RUNTIME_PROOF

Deterministic bounded proof (no LLM, no Fresh 38, no send). See `bounded_proof.json`.

| Case | Proven |
|---|---|
| INT-01 | kalk filtered without URL; offered with URL; known city reask blocked; envelope correlated |
| NEW-03 | known area/city; kalk miss → TOOL_CONFIGURATION_MISSING/infra; reask blocked |
| INT-04 | service draft → DRAFT_SANITY_FAILED; draft not enabled |
| FU-06/07 | brain1_context + what_changed_pl + heated_area reach planner view; change owner=Brain1 |
| budget/envelope | budget exhaust reason; harness expected_absence vs wiring_failure; fail-closed class; kalk not offered |

Unsafe execution: none. HITL/send freeze preserved.
