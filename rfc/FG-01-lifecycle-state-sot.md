# RFC: FG-01 — Lifecycle state Source of Truth

Status: **RESOLVED — Option B (case-status-primary)**. Resolved: 2026-08-07.  
Related backlog: `FG-01`. Roadmap residual under Follow-up Guardian.

## Problem

Follow-up Guardian and related Case OS surfaces currently see **multiple overlapping lifecycle notions**:

1. Snapshot / operational feed codes (`operational_status.code`) — only a subset (~3 of 5) carry SLA budget logic.
2. Mailbox `case_status` / engagement lifecycle (closed / merged / cancelled) — not always joined at snapshot read time.
3. Proposed richer mapping (`lifecycle_state` + `lifecycle_state_since`) partially delivered in FG-02 (`lifecycle_state_since` COMPLETE_BOUNDED) without a single operator-approved SoT for transitions.

Without one SoT, Guardian ticks, X1 membership, and archive/outcome closure can disagree on „is this case still live?”.

## Non-goals

- Reopening Faza 3 journeys.
- Live Calendar write or live Gmail send.
- Redesigning X1 as a second dashboard.

## Decision options (operator picks one)

| Option                         | Summary                                                                                             | Implications                                                     |
| ------------------------------ | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **A — Snapshot-primary**       | `operational_status` (+ `lifecycle_state_since`) is SoT for Guardian SLA; case_status is audit only | Fast; risk of closed cases still ticking until snapshot refresh  |
| **B — Case-status-primary**    | Mailbox case_status is SoT; Guardian must join closed/merged/cancelled                              | Correcter stop conditions; requires FG-03-class joins everywhere |
| **C — Explicit lifecycle FSM** | New Node B lifecycle enum with transitions + since timestamps as SoT; feed projects it              | Cleanest long-term; largest contract change                      |

## Required accompanying rules

- Daszek remains projection-only — no lifecycle write SoT in WordPress.
- Any chosen SoT must be filterable with fact supersession / outcome closure consumers.
- Proof: focused RED/GREEN for Guardian tick stop on closed/merged + one live worker tick (FG-04).

## Resolution

**Chosen: Option B — case-status-primary.**

Implementation (2026-08-07):

- `evaluate_follow_up_candidate(..., case_status=)` prefers mailbox/pipeline `case_status` when it
  maps to a budgeted `CaseLifecycleState` (e.g. `waiting` → `WAITING_CLIENT` / 168h SLA).
- `run_follow_up_guardian_tick` joins mailbox status for both FG-03 closed skip **and** FG-01 SLA map.
- Fallback remains `map_operational_to_lifecycle(code, case_status=...)` when status is absent or unbudgeted.
- Daszek stays projection-only; no WP lifecycle write SoT.
- Proof: `tests/test_aios_3_1_follow_up_guardian.py` FG-01 Option B cases + FG-04 CLI oneshot against local Postgres.

Option C remains a future backlog if an explicit FSM is later required; it is **not** opened by this resolution.
