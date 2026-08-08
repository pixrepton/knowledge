# DRAFT_SANITY_GATE

Entry: every `generate_draft_reply` body before enabled final action.

Checks (deterministic):

- empty body
- placeholders / internal tokens
- forbidden promises
- service case asking sales fields (metraż/OZC/wycena)
- asking known heated_area / location
- `missing_info` intent on service kinds
- policy_allows_draft=false when envelope current

On fail: `status=error`, `failure_class=DRAFT_SANITY_FAILED`, action `enabled=false`, HITL reason `draft_sanity_failed:*`.

Invariant proven: service/awaria draft requesting metraż+OZC is blocked.
