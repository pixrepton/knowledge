# TEST_RESULTS

## Gate A (gmail-agent)

```text
python -m pytest tools/gmail_audit/tests -q
2086 passed, 10 skipped, 24 subtests passed
```

Log: `C:\top-code-session-scratch\planner-exec-fidelity-01-gate-a.txt`

## Targeted

```text
python -m pytest tools/gmail_audit/tests/test_planner_execution_fidelity_01.py -q
15 passed
```

## Bounded proof

```text
python knowledge/eval/planner-exec-fidelity-01/run_bounded_proof.py
→ bounded_proof.json ok=true
fresh38_rerun=false
send_performed=false
```

## Failure set vs prior Gate A

- Prior intermediate failure set (before draft_sanity strip fix): 12 failures in `test_canonical_draft_identity` due to `draft_sanity` extra field on snapshot — **fixed**.
- Final suite: **0 failures**.
