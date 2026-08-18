# P2 causal observability — derived proof

Status: `PROVEN` current recapture labels only. Not recovered historical proof
for Frozen Fresh38 27/38.

```text
P2_CAPABILITY_CAUSAL_OBSERVABILITY = PASS
P2_PRODUCT_SHA = ae59750565d2a0e334f646a4d5f7bc94bd92f602
P2_RUNNER_SHA = 800318a7a2a34cfd0865889a0daacdcf530d9cda
OBSERVABILITY_SEMANTICS_CHANGE = 0
LLM_CALL_COUNT_DELTA = 0
PROVIDER_SELECTION_CHANGE = 0
DRAFT_BODY_SEMANTICS_CHANGE = 0
DRAFT_GATE_SEMANTICS_CHANGE = 0
CASE_STATE_SEMANTICS_CHANGE = 0
NEW_CAPTURE_HIST_UNRECOVERABLE = 0
```

Product commit (gmail-agent `feature/aios-roadmap-1.4-2.4`):
`feat(observability): persist Brain1 draft-path causal chain without changing product draft semantics`

Runner commit (workspace `repair/root-mcp-json-fix`):
`feat(fresh38): project draft-path observability and disable fabricated draft eligibility`

## Tests

- focused observability: 14 passed (`tools/gmail_audit/tests/test_draft_path_observability.py`)
- runner contract: 8 passed (`scripts/tests/test_fresh38_runner_contract.py`)
- Gate A gmail-agent (during P2 implementation, before closeout commit): 2567 passed / 15 skipped / 0 failed

## Current recaptures (outside git)

These are **current** runs after P2 instrumentation. They do not replace
frozen 2026-08-16 captures.

| case | labels | gate | execution | postcheck | source sha256 | path |
| --- | --- | --- | --- | --- | --- | --- |
| INT-01 | `CURRENT_RECAPTURE_COMPLETE` `CURRENT_DECISION_CHAIN_RECOVERABLE` `NON_REPRODUCED_CURRENT` `DRAFT_ACCEPTED` | RUN / `BR_ACTION_COLLECT_DATA` | SUCCESS | ACCEPT | `9bd1ad39ab13f9d847a83a7920883afe870eb5ffbe06df4c2cea11138707fb59` | `C:\top-code-session-scratch\p2-causal-obs-recapture\one-INT-01.json` |
| SVC-05 | `CURRENT_RECAPTURE_COMPLETE` `CURRENT_DECISION_CHAIN_RECOVERABLE` `CURRENT_FIRST_DIVERGENCE_CLASSIFIABLE` `SKIPPED_PRE_DRAFTER` | SKIP / `BR_ACTION_AND_REPLY_FLAG_NOT_ELIGIBLE` | NOT_STARTED | NOT_APPLICABLE | `410fa68e624a4f7e4a63a9e31d24aa636b7e7a1b554c43af39e27a837619095a` | `C:\top-code-session-scratch\p2-causal-obs-recapture-svc\one-SVC-05.json` |
| SVC-01 | `CURRENT_RECAPTURE_COMPLETE` `CURRENT_DECISION_CHAIN_RECOVERABLE` `DRAFTER_FAILED` `PROVIDER_FAILURE` | RUN / `BR_ACTION_COLLECT_DATA` | PROVIDER_FAILURE / `GROQ_CLIENT_ERROR` | NOT_APPLICABLE | `e5ea000b2384ca7fadce3d5b63f2393f3b69ffc0291da0564cef24eab4a1b253` | `C:\top-code-session-scratch\p2-causal-obs-recapture-svc01\one-SVC-01.json` |

SVC-05 BR: `recommended_next_action=escalate_review`, `reply_recommended=false`.
INT-01 draft-absent **not** reproduced on current code.

## GitNexus (gmail-agent, indexed commit ae59750)

```text
analyze PASS
status = up-to-date (indexed commit == HEAD ae59750)
draft_path_observability.py is in the graph
run_reply_drafter CALLS evaluate_draft_gate
run_reply_drafter CALLS annotate_reply_causal_observability CALLS attach_causal_observability
run_reply_drafter CALLS evaluate_draft_postcheck
draft_reply CALLS run_reply_drafter and annotate_reply_causal_observability
run_shared_downstream_stages CALLS annotate_reply_causal_observability
```

Index limitation (not a product defect): `trace(evaluate_draft_gate → run_reply_drafter)`
is `no_path` because CALLS is caller→callee. BusinessReasoning is consumed as
structured data by `evaluate_draft_gate` / `bounded_business_reasoning_result`,
not as a CALLS edge from the BR stage function. Code was not changed for GitNexus.

`detect_changes` after a clean commit was not used as closeout proof.
