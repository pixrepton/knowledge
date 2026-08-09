# CAPABILITY-FIX-05 Negative Proof

Verified negative properties:

- `PRODUCT_WRONG` was not selected: captured Understanding already contains budget context.
- Runtime AI-OS was not modified for CTX-04.
- The corpus, case definition, ground truth, judge config and capture output were not edited.
- Missing budget context is not rescued by v5; regression `test_v5_does_not_rescue_missing_budget_context` covers this.
- v5 only adjudicates failed dimensions with explicit false-negative patterns:
  - `missing_budget_context` / `no budget mention`;
  - `no_proposal_details` / `no proposal provided`, only when Understanding captures the final offer/proposal request.
- Judge errors remain infra outcomes; v5 does not turn unavailable or malformed judge rows into passes.

Result: no product tuning to satisfy scorer; only the proven eval false negative is corrected.

