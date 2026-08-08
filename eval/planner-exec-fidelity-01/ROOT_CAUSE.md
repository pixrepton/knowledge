# ROOT_CAUSE

| Layer | Finding |
|---|---|
| harness fidelity | Fresh 38 / `run_recovery_pf` skips PolicyDecision→APv2→envelope spine → 36/36 `missing_policy_envelope` |
| production wiring | Envelope path exists (`agent_reconcile` + `policy_action_spine`); fail-closed added when Brain1/policy required but envelope missing |
| tool configuration | `call_kalk_top_quote` was allowlisted and offered despite empty `KALK_TOP_BASE_URL` |
| planner quality | Formal action-class PASS ≠ semantic quality; known-fact reasks and bad drafts |
| Understanding upstream | Weak `recommended_next_step` remains; out of scope for this slice |
| draft handler/template | Deterministic `missing_info` template asks metraż/OZC — blocked for service kinds by draft sanity gate |
| measurement coverage | Frozen v2 contract untouched; Fresh 38 does not measure Slice 3B fidelity |
