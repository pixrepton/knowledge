# CAPABILITY-FIX-04 Status

Status: CLOSED

Scope:
- NEW-01: DRAFT_CONTEXT_BUDGET_OVERFLOW
- SVC-02: UNSUPPORTED_SERVICE_SCHEDULING_PROMISE
- SVC-05: SAFE_BOUNDED_REPLY_BLOCKED_BY_DRAFT_OR_BUSINESS_GATE

Current result:
- Focused Fresh38 post-2 batch captured all 3 cases.
- NEW-01 no longer returns reply_drafter HTTP 413; top-level reply_drafter draft_enabled=true.
- SVC-02 and SVC-05 produce enabled bounded service clarification drafts in planner path.
- No unsupported visit promise, invented diagnosis, invented price, or unsupported scheduling wording found in generated service draft bodies.
- Canonical Gate A passed with 0 failures.

Gate A:

```text
python -m pytest tools/gmail_audit/tests -q
2396 passed, 15 skipped, 24 subtests passed in 302.88s
```

Runtime proof:

```text
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_fresh38_case_batch.ps1 -CaseIds NEW-01,SVC-02,SVC-05 -OutDir C:\top-code-session-scratch\capability-closeout-20260809\fix04-post2
DONE ok=3 failed=0
```

Focused proof JSON:

```text
focused-proof.json
SHA256 0163DB9886DC6B46E83905781C6703835B416789892AB0B4403179B43757CF97
```
