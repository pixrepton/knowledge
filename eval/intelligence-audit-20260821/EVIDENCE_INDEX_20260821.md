# EVIDENCE INDEX — AUDYT INTELIGENCJI 2026-08-21

Indeks dowodów źródłowych użytych w `INTELLIGENCE_AUDIT_FULL_20260821.md`.
Wszystkie ścieżki względem `gmail-agent/tools/gmail_audit/` (HEAD `a3d3ae6`).

| Moduł | Rola w audycie | Kluczowe linie |
| --- | --- | --- |
| `understanding_output.py` | A1 projection-safe kontrakt | 1, 42, 97-103, 236, 254, 421 |
| `case_intelligence/understanding.py` | A1 operator snapshot | 93 |
| `mailbox_memory/active_facts.py` | A2 active vs superseded | 64, 100, 134 |
| `mailbox_memory/facts.py` | A2 fact model (confidence/observed_at) | 65 |
| `llm_contracts/business_reasoning.py` | A3 Pydantic contract | 7 |
| `intake_schema.py` | A3/A12 normalizacje + second-pass | 321-445 |
| `business_reasoner.py` | A3 prompt + fallback | 76, 264, 333 |
| `action_planner.py` | A4/A17 ActionPlan | 37, 45, 66-97 |
| `case_intelligence/next_best_action.py` | A4/A17 NBA | 10, 18, 47-113 |
| `case_intelligence/orchestrator.py` | A4 spine assembly | 112 |
| `decision_candidate.py` | A4/A18 candidate | 101-207 |
| `policy_action_proposal.py` | A4 policy mapping | 118-160 |
| `policy_decision.py` | A4/A6 P0 gate | 30-90 |
| `action_proposal_v2.py` | A4/A17 v2 bundle | 28-123 |
| `agent_runtime/policy_action_spine.py` | A4/A7/A14 envelope + guard | 29, 47-77, 299-330 |
| `agent_runtime/graph.py` | A4/A5 runtime loop | 305-350, 759-885 |
| `agent_runtime/recommended_next_step_quality.py` | A5 planner hint | 144-178 |
| `agent_runtime/openai_agent_client.py` | A5/A11 system prompt | 400-455 |
| `agent_runtime/effective_tools.py` | A5/A23 tool availability | 47-59, 159 |
| `agent_runtime/policy_guardrails.py` | A5/A6 allowlist | 19-28 |
| `policy_engine.py` | A6 reguły policy | 27, 240-575 |
| `agent_runtime/authz.py` | A6/A13 token scope | 146-156 |
| `agent_runtime/materialize.py` | A7/A14 executor po approval | 159-183, 376 |
| `hitl_gmail_send.py` | A7 send manual operator | 95-141 |
| `agent_hitl_bridge.py` | A7 approval binding | 39 |
| `reply_drafter.py` | A8 draft contract | 61-67, 128, 233, 355-407, 434 |
| `agent_runtime/draft_sanity.py` | A8/A9 draft sanity | 48-94 |
| `llm_contracts/reply_draft.py` | A8 Pydantic draft | 8-20 |
| `follow_up_guardian.py` | A9 guardian | 7-42, 169, 208, 283 |
| `case_intelligence/lifecycle.py` | A9 lifecycle | 109 |
| `case_intelligence/constants.py` | A9/A4 słowniki | 37, 51-60 |
| `operator_learning_hooks.py` | A10 hooks | 9, 37, 63 |
| `correction_ledger.py` | A10 ledger | 15 |
| `agent_runtime/memory_consolidation/__init__.py` | A10/A2 konsolidacja | 19-61 |
| `agent_runtime/untrusted_input_boundary.py` | A13 fail-closed boundary | 70-114 |
| `agent_runtime/known_fact_guard.py` | A13 known-fact guard | 107 |
| `gmail_ingress_guard.py` | A13 ingress guard | 12 |
| `execution_runtime.py` | A14 lifecycle akcji | 141-261 |
| `agent_runtime/tools/write_executors.py` | A14 idempotency wrap | 873-921 |
| `agent_runtime/idempotency.py` | A14 idempotency_log | 46-105 |
| `agent_runtime/turn_journal.py` | A19 append-only journal | 27-131 |
| `event_memory.py` | A19 replay | 32-104 |
| `agent_runtime/snapshot_delta.py` | A19 wersjonowane delty | 21 |
| `llm_provider_router.py` | A15 fallback + klasyfikacja | 60-203, 262-302 |
| `agent_runtime/failure_taxonomy.py` | A15 failure classes | 57-115 |
| `llm_deadline.py` | A15 deadline | — |
| `_case_intelligence_legacy.py` | A16 dormant legacy | całość |
| `_mailbox_memory_legacy.py` | A16 re-export shim | 1-40 |
| `case_intelligence.py` | A16 compat shim | 1-30 |
| `case_context_contract.py` | A18 provenance | 453-512, 658-697, 1005-1090 |
| `tests/` | A20 357 plików / 2529 testów | kluczowe: test_svc05_customer_clarification, test_fact01_snapshot_supersession, test_rp29_fact_supersession, test_rp31_learning_integrity, test_untrusted_input_execution_boundary, test_planner_spine_handoff_closeout, test_hitl_no_send_without_approve, test_outbound_receipt |
| `docs/runbooks/LAST_PROVEN_STATE.md` | A21 ostatni live proof | 21 |

Stan indeksów: GitNexus `gitnexus://repos` zgodny z HEAD (root 7696a26,
gmail-agent a3d3ae6, knowledge ab3b1e5, pozostałe zgodne).
