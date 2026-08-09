# CAPABILITY-FIX-05 - CTX-04

Status: CLOSED

Verdict: EVAL_EXPECTATION_WRONG

Scope:
- Runtime AI-OS: unchanged.
- Corpus and ground truth: unchanged.
- Capture semantics: unchanged.
- Judge config: unchanged.
- Change seam: versioned offline measurement adjudication, `measurement_contract_version=v5`.

Mechanic:
- Frozen capture already contains CTX-04 budget context in Understanding.
- Frozen judge result claimed `missing_budget_context` and `no_proposal_details`.
- v5 corrects only this proven contradiction when captured Understanding carries the required budget context and proposal/offering request semantics.
- If budget context is absent, v5 does not rescue the case.

Focused proof:
- `focused-proof-ctx04.json`
- `focused-rescore-v5.json`
- `focused-summary-v5.json`
- `focused-breakdown-v5.json`
- `focused-qualification-v5.json`
- `effective-corpus-v5.json`

Focused regression:

```powershell
python -m pytest tools/gmail_audit/tests/test_measurement_integrity_v5.py tools/gmail_audit/tests/test_measurement_integrity_v4.py tools/gmail_audit/tests/test_measurement_integrity_v3.py tools/gmail_audit/tests/test_eval_measurement_contract_v2.py tools/gmail_audit/tests/test_eval_understanding_judge.py -q
```

Result:

```text
64 passed
```

Gate A:

```powershell
python -m pytest tools/gmail_audit/tests -q
```

Result:

```text
2400 passed, 15 skipped, 24 subtests passed in 301.99s
```

