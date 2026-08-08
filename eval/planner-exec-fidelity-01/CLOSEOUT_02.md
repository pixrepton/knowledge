# CLOSEOUT_02 — harness fidelity + live proof + next-step quality

## Status: PASS (bounded) — `confirmed by local tests`

### Gaps closed

1. **Harness spine handoff** — `eval_planner_spine_handoff.py` + patched `run_recovery_pf.py`:
   - Understanding returns full `case_intelligence`
   - Planner receives `policy_action_envelope` + Brain1 projection
   - Fresh38 runner hot-syncs handoff module; PATCHED copy updated in session-scratch
2. **Live bounded proof** — INT-01 + INT-04 with real DeepSeek planner (`closeout_bounded_proof_live.json`)
3. **recommended_next_step quality** — `recommended_next_step_quality.sharpen_*` + projection + planner prompt

### Proof highlights

| Case        | Envelope          | Notes                                                           |
| ----------- | ----------------- | --------------------------------------------------------------- |
| INT-01 det  | `present_current` | draft enabled + parent refs complete; kalk filtered without URL |
| INT-04 det  | `present_current` | `DRAFT_SANITY_FAILED` on service missing_info                   |
| INT-01 live | `present_current` | LLM chose kalk then draft; HITL draft_ready                     |
| INT-04 live | `present_current` | LLM draft blocked by sanity gate                                |

### Intentionally not done

- Full Fresh 38 re-run (forbidden by Phase 1.1 closure)
- Real send
- Full Understanding LLM retrain / 34/38 chase
