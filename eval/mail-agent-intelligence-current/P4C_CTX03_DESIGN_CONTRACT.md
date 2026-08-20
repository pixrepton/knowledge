# P4-C CTX-03 — fact-supersession design contract (adjudication)

Owner: this directory. Frozen evidence: `.artifacts/fresh38-full-current-20260816T124100`.

## Verdict

`PRIMARY_CLASS = PRODUCT_WRONG` (fact supersession hides a real contradiction).
The judge failed the `contradictions` dimension:
`contradiction_not_detected` — "brak odnotowania konfliktu miedzy 120m2 a 160m2".

## Frozen evidence

- Prior context: `heated_area_m2 = 120` (customer stated earlier).
- Current message: "Dom ma 160m2 powierzchni ogrzewanej." Extraction
  `heated_area_m2 = 160.0`.
- Ground truth `must`: detect contradiction 120 vs 160 in `conflicting_facts`;
  `must_not`: silently replace the old value without noting the conflict.
- Captured `understanding.conflicting_facts = []`,
  `thread_delta.new_conflicts = []`. The old 120 was silently replaced by 160.

## Mechanism

`mailbox_memory_runtime.split_conflicting_facts` intentionally filters out rows
with `status == "superseded"` before ranking. The fact write path
(`append_facts_with_supersession`, RP-29) marks the prior 120 row as
`superseded` as soon as a different value appears, so the 120 vs 160 pair never
reaches the conflict detector. Result: a genuine contradiction is presented as a
silent supersession, violating the GT `must_not`.

## Design contract (decision required before code)

The fix must distinguish three fact-change semantics instead of treating every
value change as RP-29 supersession:

1. **Explicit correction** — the customer/writer clearly says the earlier value
   was wrong and supplies a replacement. Supersession is correct; no conflict
   is required.
2. **Independent conflicting value** — a new message states a different value
   without correction framing (CTX-03). This must surface as a
   `conflicting_facts` entry with both values.
3. **Authoritative supersession** — a higher-trust source replaces a fact
   outside a live customer disagreement. Supersession is correct.

## Minimal fix surface (candidate)

- Keep active-fact selection live-only, but let `split_conflicting_facts`
  include differing `superseded` values as conflict evidence (CTX-03 safe),
  OR carry an explicit `supersession_basis`/`correction` flag on the write path
  and only suppress conflict for genuinely corrective supersessions.
- Affected modules: `mailbox_memory_runtime.split_conflicting_facts`,
  RP-29 write path, and all consumers of `conflicting_facts` /
  `facts_invalidated`.

## Blast radius

High: fact persistence semantics and every conflict projection. The current
RP-29 tests assert the superseded-row exclusion behavior, so this is a real
contract change requiring a positive cohort (conflicting value) and a negative
cohort (explicit correction stays superseded).

## Status

`DESIGN_CONTRACT_PENDING`. The semantic choice (which change counts as
correction vs conflict vs supersession) is an operator decision; no heuristic
fact-policy change is made here.
