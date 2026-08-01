# RP-01 EXECUTION

Package: `RP-01`

Status: `CLOSED`

Baseline overlay commit:

- `knowledge`: `bc91f3ad3f86f552dc20e3a871022cafce19cce5`

Code commits:

- `gmail-agent`: `1ccc39229df2ca2600bb2cb4bb5c89aa87457562`

Repositories and branches:

- `gmail-agent`: `handoff/20260719-1403-latest`

Proof timestamp anchor:

- `2026-07-31T07:55:04Z`

## Scope

Retire the over-claimed generic retrieval tool `query_anything`, keep `search_rag_knowledge` as the only retained case-scoped retrieval contract in Node B, and close the speculative company-knowledge adapter branch without mutating Workflow Registry v1.

## Proof Inventory

Repository state:

- `repo_state_before_commit.json`
- `repo_state_after_commit.json`
- `gmail_agent_post_commit_status.log`

GitNexus and static reachability:

- `gitnexus_query_anything_impact.log`
- `rp01_rp20_active_code_scan.log`

Patch and staging proof:

- `gmail_agent_patch.diff`
- `staged_diff_stat.log`
- `staged_paths.log`
- `gmail_agent_commit_scope.log`

Focused tests:

- `gmail_agent_retrieval_tests.log`
- `gmail_agent_retrieval_tests_post_commit.log`

## Findings

1. `query_anything` was still actively offered to the chat agent through the constitution, schema surface, budgets and runtime registration, so this was a live planner-facing path rather than harmless dead code.

2. The tool implementation was not a truthful retained contract.
   Its RAG branch still used the wrong call signature, its similar-cases branch depended on a broken import, and its top-level success wording counted source failures as positive answers.

3. GitNexus upstream impact for `query_anything` was `0`, and no focused runtime or planner proof established a separate business journey that truly required a generic multi-source aggregator.

4. The explicit Node B company-knowledge adapter path had no proven runtime consumer.
   Current company knowledge survives inside `rag-chat-asystent` prompt augmentation, not as a dedicated Node B retrieval capability.

## Frozen Contract Points

- Node B retains case-scoped retrieval only through `search_rag_knowledge`.
- No speculative `gmail-agent -> rag-chat-asystent` company-knowledge adapter is introduced without a real caller and truthful source contract.
- Workflow Registry v1 remains immutable.

## Decision

- `DQ-01`: resolved locally in favor of `CASE_SCOPED_RETRIEVAL_ONLY`.
  `search_rag_knowledge` remains the retained read tool for case-linked retrieval, while `query_anything` is retired from planner exposure, authz, runtime registration and operator guidance.

Rejected alternatives:

- patching each `query_anything` branch in place despite the lack of a proven retained capability;
- keeping a generic retrieval abstraction alive "for the future";
- adding a new dedicated Node B company-knowledge adapter without a real caller.

## Historical Data Impact

Classification: `NONE`

Notes:

- no historical rows, projections or traces were rewritten;
- this package only narrows the active retrieval contract and removes a planner-facing dead branch.

## Implementation Scope

Changed runtime and planner surface:

- `gmail-agent/tools/gmail_audit/agent_runtime/constitution_chat.py`
- `gmail-agent/tools/gmail_audit/agent_runtime/tool_budgets.py`
- `gmail-agent/tools/gmail_audit/agent_runtime/sub_agents.py`
- `gmail-agent/tools/gmail_audit/agent_runtime/authz.py`
- `gmail-agent/tools/gmail_audit/agent_runtime/tool_schemas.py`
- `gmail-agent/tools/gmail_audit/agent_runtime/tools/handlers.py`
- `gmail-agent/tools/gmail_audit/signal_reconciler.py`

Changed tests:

- `gmail-agent/tools/gmail_audit/tests/test_constitution.py`
- `gmail-agent/tools/gmail_audit/tests/test_search_rag_knowledge_tool.py`

## Tests And Runtime/Integration Proof

Commands executed:

```text
python -m pytest tools/gmail_audit/tests/test_constitution.py tools/gmail_audit/tests/test_search_rag_knowledge_tool.py tools/gmail_audit/tests/test_tool_reachability_contract.py -q
rg -n "query_anything|build_community_summary|community_summaries" gmail-agent\tools\gmail_audit\agent_runtime gmail-agent\tools\gmail_audit\signal_reconciler.py rag-chat-asystent\backend --glob '!**/tests/**'
npx gitnexus impact query_anything --repo gmail-agent
```

Observed results:

- focused gmail-agent retrieval surface tests: `54 passed`
- static active-code scan: `NO_ACTIVE_CODE_REFERENCES_FOUND`
- GitNexus upstream impact for `query_anything`: `LOW`, `impactedCount=0`

Proof limitations:

- proof is static plus integration-level planner/runtime contract validation, not a production-observed Node B runtime session;
- no external RAG HTTP call was needed because the retained change was retirement of the generic aggregator rather than introduction of a new adapter.

## Gap Outcome

Closed:

- `gap.case-scoped-rag-vs-global-rag.query-anything-rag-branch-call-signature-broken`
- `gap.case-scoped-rag-vs-global-rag.query-anything-similar-cases-import-broken`
- `gap.case-scoped-rag-vs-global-rag.query-anything-counts-source-errors-as-success`
- `gap.case-scoped-rag-vs-global-rag.query-anything-returns-ok-when-all-sources-fail`
- `gap.case-scoped-rag-vs-global-rag.gmail-agent-has-no-runtime-consumer-for-company-rag-service`

Residuals:

- none in the retained Node B retrieval contract for this package;
- any future explicit company-knowledge capability must re-open from a fresh proof-backed caller, not from this retired branch.

## Final Status

`CLOSED`
