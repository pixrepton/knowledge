# PF-01 — Exhaustive `enabled=True` + customer/operator draft inventory

Status: **COMPLETE_BOUNDED** (2026-08-07). Scope: `gmail-agent/tools/gmail_audit` production code
(excluding `tests/`, `scripts/` proof helpers, and non-draft feature flags).

## Method

1. Scan for `enabled=True` / `"enabled": True` in production modules.
2. Classify each hit: **draft ActionItem** vs **non-draft flag**.
3. For draft ActionItems: require `evaluate_draft_sanity` **before** durable `enabled=True`
   (fail-closed → `enabled=False` + `DRAFT_SANITY_FAILED`).

## Draft ActionItem producers (must be gated)

| Location            | Path                                                                              | Gate                                                     |
| ------------------- | --------------------------------------------------------------------------------- | -------------------------------------------------------- |
| HITL mint           | `agent_runtime/draft_identity.py` `mint_gap_only_draft_action`                    | PF-01 `evaluate_draft_sanity`                            |
| HITL edit           | `agent_runtime/draft_identity.py` `apply_operator_draft_edit`                     | PF-01 re-run                                             |
| Brain1 transfer     | `agent_runtime/draft_lineage_transport.py` `materialize_transferred_draft_action` | PF-01 re-run                                             |
| Brain2 draft tool   | `agent_runtime/tools/handlers.py` `generate_draft_reply`                          | gate before `enabled=True`                               |
| kalk-top quote body | `agent_runtime/tools/handlers.py` `call_kalk_top_quote`                           | gate before `enabled=True`                               |
| Follow-up Guardian  | `follow_up_guardian.py` `build_follow_up_action_item`                             | **added 2026-08-07** (operator prompt; defense-in-depth) |

## Non-draft / out of PF-01 customer-draft scope

| Location                                                                                    | Why out of scope               |
| ------------------------------------------------------------------------------------------- | ------------------------------ |
| `config.py` / feature flags (`deepseek_thinking_enabled`, OTEL mirrors, guidance flags)     | Not ActionItem drafts          |
| `mailbox_memory_runtime.py` / `drive_ingest_runtime.py` `enabled=True` on non-draft records | Not customer payload_pl drafts |
| `mcp_service.py` smoke fixtures                                                             | Test harness inside module     |
| `observation_triage.py` / `v2_runtime.py` capability flags                                  | Not draft bodies               |
| `kalk_top_client.py` HVAC request shape `heating.enabled`                                   | Kalk payload, not mail draft   |

## Residual policy

Any **new** production site that sets ActionItem `enabled=True` with `payload_pl` **must** call
`evaluate_draft_sanity` first. Gate A regression: `tests/test_pf01_draft_sanity_coverage.py`.

## Proof

```text
python -m pytest tools/gmail_audit/tests/test_pf01_draft_sanity_coverage.py -q
```
