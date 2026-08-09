# CAPABILITY-FIX-04 Proof Summary

Verdict: CLOSED

## Current-HEAD Re-base

| Case | Re-based first divergence | Root cause | Downstream symptom |
| --- | --- | --- | --- |
| NEW-01 | `reply_drafter` prompt still exceeded provider TPM before post-2 fix | Drafter prompt serialized non-response context and stage telemetry, then combined it with default assembled context budget | HTTP 413 / `draft_enabled=false` in top-level reply drafter |
| SVC-02 | Service case reached deterministic `generate_draft_reply`, but missing-info template asked sales sizing fields | `generate_draft_reply(intent=missing_info)` had one sales template for all case kinds | Draft sanity blocked with service sales-field reasons; historical unsupported scheduling promise was already gone |
| SVC-05 | Service case reached deterministic `generate_draft_reply`, but missing-info template asked sales sizing fields | Same service-vs-sales template split missing | Safe bounded clarification could not become an enabled planner draft |

## Implemented Fix

Code changes:
- `tools/gmail_audit/intake_payload.py`
  - added reply-draft response-relevant CaseContextPack projection;
  - omitted upstream LLM telemetry (`prompt_input`, `assembled_context`, `input_variants`, raw stage output) from drafter prompt;
  - preserved critical business/safety facts such as budget, device, scheduled/proposed visit, deadline, customer contact and service issue facts.
- `tools/gmail_audit/context_assembler.py`
  - added stage-specific assembled context budget for `reply_drafter`.
- `tools/gmail_audit/agent_runtime/tools/handlers.py`
  - added service-aware missing-info draft template.
- `tools/gmail_audit/agent_runtime/draft_sanity.py`
  - allowed bounded service clarification;
  - retained blockers for sales asks, unsupported service promises and unsupported certainty diagnosis.
- Tests updated in:
  - `tools/gmail_audit/tests/test_aios_1_4_draft_content_contracts.py`
  - `tools/gmail_audit/tests/test_planner_execution_fidelity_01.py`

## Focused Proof

Focused tests:

```text
python -m pytest tools/gmail_audit/tests/test_aios_1_4_draft_content_contracts.py tools/gmail_audit/tests/test_planner_execution_fidelity_01.py::test_draft_sanity_blocks_service_metraz_ozc tools/gmail_audit/tests/test_planner_execution_fidelity_01.py::test_draft_sanity_allows_bounded_service_handler tools/gmail_audit/tests/test_planner_execution_fidelity_01.py::test_draft_sanity_allows_sales_quote tools/gmail_audit/tests/test_context_assembler.py -q
28 passed
```

Relevant prior-fix regressions:

```text
python -m pytest tools/gmail_audit/tests/test_capability_fix_02_trusted_case_context.py tools/gmail_audit/tests/test_capability_fix_03_response_readiness.py tools/gmail_audit/tests/test_planner_spine_handoff_closeout.py tools/gmail_audit/tests/test_generate_draft_reply_contract.py tools/gmail_audit/tests/test_aios_3_2_draft_lineage_residual.py -q
53 passed
```

Focused Fresh38 post-2:

```text
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_fresh38_case_batch.ps1 -CaseIds NEW-01,SVC-02,SVC-05 -OutDir C:\top-code-session-scratch\capability-closeout-20260809\fix04-post2
DONE ok=3 failed=0
```

Case-level result:

| Case | Stage | Planner classification | Top drafter | Planner draft | Safety |
| --- | --- | --- | --- | --- | --- |
| NEW-01 | full | CLEAN_PASS | `draft_enabled=true`, no 413 | `tool_status=ok`, final action enabled | safe deterministic floor |
| SVC-02 | full | CLEAN_PASS | `draft_enabled=true` | `tool_status=ok`, final action enabled | `unsafe_non_escalation=false`, safe deterministic floor |
| SVC-05 | full | CLEAN_PASS | `reply_not_recommended` fallback, but planner draft path enabled | `tool_status=ok`, final action enabled | safe deterministic floor |

## Gate A

```text
python -m pytest tools/gmail_audit/tests -q
2396 passed, 15 skipped, 24 subtests passed in 302.88s
```

