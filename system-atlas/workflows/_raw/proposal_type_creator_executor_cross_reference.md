# Raw inventory — proposal type ↔ creator ↔ approver ↔ executor ↔ result writer (reverse-audit category 5)

Generated during the mechanical reverse-audit pass (2026-07-30), continuation session.

## Command used

```
rg -n "proposal_type" gmail-agent/tools/gmail_audit --type py -g '!*test*'
rg -n "MaterializeProposalItem\(|append_materialize_proposal\(" gmail-agent/tools/gmail_audit
rg -n "\"link_existing\"|'link_existing'|\"create_case\"|\"create_artifact\"|\"defer_operator\"" gmail-agent/tools/gmail_audit --type py -g '!*test*'
```

## Scope

The `MaterializeProposalItem.proposal_type` Literal (`llm_contracts/engagement_snapshot_v2.py:212-215`)
— the proposal shape with the richest, already-heavily-audited executor
(`execute_materialize_proposal`, `materialize.py:332-428`, `EV-00142`). Cross-referenced against
every confirmed creator site. `action_proposals_v2`'s `action_type`/decision-pipeline shape is a
separate, different mechanism, already covered extensively in Domains 1-4 (`policy_action_spine`,
`DecisionCandidate`/`PolicyDecision`) — not re-audited here as it uses a different field name and
different creation path (decision-pipeline driven, not a caller-supplied literal).

## The 5 defined `proposal_type` values and their executor + creator status

| proposal_type | executor branch (`materialize.py`) | confirmed creator(s) |
|---|---|---|
| `composite_plan` | `_execute_composite_step` over `WRITE_EXECUTORS`, real per-step audit | `agent_runtime/tools/handlers.py:713` (`propose_plan`) and `:1060` (`propose_mutation`'s `_proposal_result` call) — BOTH call sites hardcode this exact literal; `scripts/seed_materialize_ctfu5.py:58` (test/seed fixture) also only uses this literal |
| `link_existing` | registers an engagement→case link via `correlation_store` | **NONE FOUND** — appears only in the Literal type definition and the executor branch |
| `create_case` | full case-row creation + email-level dedup + correlation registration | **NONE FOUND** as a `MaterializeProposalItem.proposal_type` — the only other `"create_case"` hits in the codebase are a DIFFERENT concept (a `write_executors.py` operation key used inside `composite_plan` steps, and `intake_policy.py`/`case_intelligence`'s unrelated `action`/`intake_action` classification vocabulary) |
| `create_artifact` | deliberate no-op stub (`{"action": "artifact_deferred", ...}`) | **NONE FOUND** |
| `defer_operator` | deliberate no-op stub (`{"action": "deferred", ...}`) | **NONE FOUND** |

`append_materialize_proposal` (`materialize.py:134-150`) is the ONLY function anywhere that
constructs a `MaterializeProposalItem` outside `materialize.py`'s own module scope and the seed
script — it takes `proposal_type` as a generic caller-supplied string parameter, but its single
real caller (`agent_runtime/tools/handlers.py`'s `_proposal_result`, called from exactly 2 sites)
always passes the literal `"composite_plan"`.

## Classification

- `composite_plan`: fully closed loop — creator (2 sites) → approve route → executor → durable
  effect. Already extensively audited this session (`EV-00142`..`EV-00150`).
- `link_existing`, `create_case`, `create_artifact`, `defer_operator`: **`MISSING_PRODUCER`** —
  a real, working, schema-validated, downstream-reconcile-aware (`materialize_bridge.py:246`
  explicitly checks for `create_case`/`link_existing` to trigger `reconcile_linked_after_materialize`)
  executor exists for all 4, but NO code path anywhere creates a `MaterializeProposalItem` with
  any of these 4 types. They are structurally unreachable in production — not merely unused,
  genuinely uncreatable by any live mechanism found.

## Unresolved / not independently re-verified this pass

- Whether an operator-facing UI action (rather than an LLM tool) could construct one of these 4
  proposal types directly via a lower-level API not yet found — an exhaustive route-by-route
  check of every daszek/gmail-agent write endpoint for a raw `MaterializeProposalItem` constructor
  call was not performed beyond the greps above.
- Whether this is a deliberate "not yet wired" placeholder (matching the codebase's frequent
  pattern of building executor + schema ahead of the corresponding creator) or an oversight was
  not determined — no comment/docstring in `materialize.py` clarifies intent for these 4 branches
  the way `create_artifact`/`defer_operator`'s no-op bodies hint at "not yet implemented".

## Evidence

`EV-00179` (this category's summary record). New P1 gap filed, `WORKFLOW_GAPS.md` item 32.
