# Fresh38 Measurement Integrity Proof

Status: PASS

## Focused Gate

- cases: FU-01, FU-06, DOC-02, MI-01, MI-02
- captured: 5/5
- failed_cases: 0
- HARNESS: 0
- DELIVERY: 0
- capture_gap_cases: 0
- scoring_complete: True
- judge_error_cases: 0
- unsafe_non_escalation: 0

## Focused Outcomes

| case | previous outcome | first divergence | root cause | fix | focused outcome |
|---|---:|---|---|---|---:|
| FU-01 | DELIVERY | kalk-top unreachable from Node B tool path: [Errno 101] Network is unreachable | KALK_TOP_LOCAL_TOPOLOGY_DOWN | Started local Docker stack and kalk-top runtime; verified Node B -> http://host.docker.internal:8091 health 200; no planner change. | CAPABILITY |
| FU-06 | HARNESS | gmail_intake emitted INTAKE_LLM_TIMEOUT; runner collapsed it to production_faithful_intake_invalid | CURRENT_RUNTIME_OUTPUT / provider timeout, not fixture schema | No scorer mask; reran through production-faithful path after runner hot-sync seam was repaired; capture now has valid normalized intake. | CLEAN_PASS |
| DOC-02 | DELIVERY | kalk-top unreachable from Node B tool path: [Errno 101] Network is unreachable | KALK_TOP_LOCAL_TOPOLOGY_DOWN | Started local Docker stack and kalk-top runtime; verified Node B -> http://host.docker.internal:8091 health 200; no planner change. | CAPABILITY |
| MI-01 | HARNESS | gmail_intake emitted INTAKE_LLM_TIMEOUT; runner collapsed it to production_faithful_intake_invalid | CURRENT_RUNTIME_OUTPUT / provider timeout, not fixture schema | No scorer mask; reran through production-faithful path after runner hot-sync seam was repaired; capture now has valid normalized intake. | CLEAN_PASS |
| MI-02 | HARNESS | gmail_intake emitted INTAKE_LLM_TIMEOUT after provider fallback symptoms; runner collapsed it to production_faithful_intake_invalid | CURRENT_RUNTIME_OUTPUT / provider timeout, not fixture schema | No scorer mask; reran through production-faithful path after runner hot-sync seam was repaired; capture now has valid normalized intake. | CLEAN_PASS |

## Notes

- Focused CAPABILITY outcomes are accepted measurement results, not measurement integrity blockers.
- DOC-02 remains CAPABILITY in focused v5 due planner/runtime JSONDecodeError, but no longer has node_a_error or DELIVERY.
- FU-01 remains CAPABILITY in focused v5 due Understanding gaps BORDERLINE, but no longer has node_a_error or DELIVERY.
- FU-06, MI-01 and MI-02 now have valid normalized production-faithful intake captures.

## Source Artifacts

- scratch_outdir: `C:\top-code-session-scratch\fresh38-measurement-integrity-20260809T223532\focused5`
- fresh38-partial-results.json: `3244d6dff98e4c97e79c7af024396f9339628ccfca732fcfd578be7bcbf7f0fa`
- fresh-understanding-judge.json: `89799fb0dc254ab3df67fa60e0912b2b88c764eabf865a59aab8130772f7fe20`
- focused-rescore-v5.json: `f3bc02ee5a1497b834c6ad649772af468726fed2e0e716bd715e75b6967ca876`
- focused-summary-v5.json: `0ebbecabaef49191f0c76927f20fc8531b26cd3a246a4dd417c6a2082b2c31a4`
- focused-breakdown-v5.json: `b2b287bafe995879b4394f9068663a4efad997d060db16b849035a4785808fc9`
- focused-qualification-v5.json: `bb5c3810b64f4d1112aec4e6b3f4070d94fb40dd8840431f813696ac3024976c`
