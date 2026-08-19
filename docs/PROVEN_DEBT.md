# Proven debt register

Status: durable register of problems that were observed and consciously **not**
fixed during P1/P2/P3A. Do not treat these as hidden fixes; they are separate
work when the operator authorizes it.

Source: P1 KALK-TOP CLOSEOUT, P2 causal observability, P3A frozen K3
(2026-08-16 .. 2026-08-19). Re-verify current state before acting.

| Debt | Owner | Status | Note |
| ---- | ----- | ------ | ---- |
| OfferDTO / `offer_snapshot` convergence | kalk-top + gmail-agent | `PROVEN_DEBT` / `NOT_CURRENT_FIRST_DIVERGENCE` | Canonical offer path is `fast-kalk/kalk-top -> OfferDTO -> event -> Case`; the `call_kalk_top_quote` path currently consumes totals text into a draft/tool result. |
| EV-00140 / `select_sub_agent` scope | gmail-agent | `PROVEN_DEBT` / `NOT_CURRENT_FIRST_DIVERGENCE` | Do not open broad sub-agent architecture unless an eligibility fix is mechanically impossible without it. |
| `QUOTE_INTENT_MODEL_LIMITATION` (scenario C) | gmail-agent / kalk-top | limitation | The only authoritative quote-intent signal is `CaseKindLiteral`; `zapytanie_klienta` + BR `reply` cannot be safely unlocked without a new intent ontology. |
| `kalk-top/docker/entrypoint-local.sh` fallback | kalk-top | owned by `AIOS-KALK-CANONICALIZE-20260811` | Generates a weaker local `_router.php` when the workspace overlay volume is not mounted. |
| NBA title "klient zgłosił zmianę" (INT-04/NEW-05) | evaluator / GT | parked secondary | Contaminated template title; not a PRIMARY defect. |
| FU-01 BR `escalate_review` vs GT `escalation_expectation=none` | evaluator / GT | parked secondary | P3A classified the PRIMARY as `EVALUATOR_WRONG`; this is a secondary signal. |

## Rules

- Do not silently "fix" these while doing unrelated scoped work.
- Do not reopen a historical Fresh38 capture and relabel it as recovered;
  `HIST_UNRECOVERABLE` remains a historical fact.
- Promote an item to an active task only with an explicit operator decision and a
  focused proof plan (cheapest discriminating experiment first).
