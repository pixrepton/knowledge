# RP-07 EXECUTION

Package: `RP-07`

Status: `CLOSED`

Baseline overlay commit:

- `knowledge`: `bc91f3ad3f86f552dc20e3a871022cafce19cce5`

Code commits:

- `gmail-agent`: `4b9d5b413dd39842555375c7bdfbe9def2717035`

Repositories and branches:

- `gmail-agent`: `handoff/20260719-1403-latest`
- `daszek`: inspected for projection-only UI; no code mutation required

Proof timestamp anchor:

- `2026-08-01T21:12:02Z`

## Scope

Close the residual Calendar lifecycle decision under the frozen read-only boundary:

- Google Calendar remains read-only;
- Node B never creates, updates or deletes Google Calendar events;
- `scheduled_visit` requires an ingested real `calendar_event_id`;
- `proposed_visit`, reschedule and cancel remain proposal/external-observation concepts, not proof of execution.

## Proof Inventory

Repository state and commit scope:

- `repo_state_after_code_commit.json`
- `gmail_agent_commit_scope.log`
- `gmail_agent_commit_full.log`

Focused and regression tests:

- `gmail_agent_rp07_focused_tests_post_commit.log`
- `gmail_agent_rp07_regression_tests_post_commit.log`

Static and runtime/integration proof:

- `static_calendar_write_scan.log`
- `runtime_read_only_calendar_proof.json`
- `runtime_read_only_calendar_proof.log`

## Current Topology

- Calendar ingest entrypoint: `CalendarRuntime.ingest_events`.
- Calendar signal producer: `calendar_signal_adapter.build_calendar_signal`.
- Calendar signal consumer: `signal_reconciler._reconcile_calendar_signal`, registered for `source_kind="calendar"`.
- Calendar event SoT in Node B: mailbox memory calendar event/link tables or in-memory equivalents.
- Daszek receives Calendar only as projection data from Node B feed/context; Daszek does not own the lifecycle.
- Existing Calendar write-shaped actions are forbidden by policy and cannot execute.

## Decision

`DQ-04`: `READ_ONLY_EVENT_LINKED_LIFECYCLE_PLUS_PROPOSAL_ONLY_RESCHEDULE_CANCEL`

Chosen model:

- observed external Calendar event with non-empty `calendar_event_id` creates/updates the event-linked visit lifecycle;
- cancelled external event removes the active scheduled-visit projection while retaining observed event history;
- proposed date text produces `customer_proposed_date` / `proposed_visit`, not `scheduled_visit`;
- reschedule/cancel survive only as proposal-only or externally observed states;
- Node B Calendar writes are fail-closed.

Rejected alternatives:

- reintroducing `create_calendar_event` or Calendar write wrappers;
- treating `scheduled_visit` text facts without `calendar_event_id` as confirmation;
- keeping `google_calendar` as the reconcile `source_kind` while the registry expects `calendar`;
- preserving separate Calendar risk implementations across context pack and feed.

## Historical Data Impact

Classification: `NO_ACTION_REQUIRED`

Notes:

- no production data mutation was performed;
- legacy textual `scheduled_visit` facts are no longer accepted as confirmation unless linked to a real `calendar_event_id`;
- existing projections may need natural rebuild/read refresh to stop presenting cancelled or unlinked visit text as confirmed, but no destructive migration is required for the code contract.

## Implementation Scope

Changed runtime contracts:

- `gmail-agent/tools/gmail_audit/calendar_models.py`
- `gmail-agent/tools/gmail_audit/calendar_runtime.py`
- `gmail-agent/tools/gmail_audit/calendar_signal_adapter.py`
- `gmail-agent/tools/gmail_audit/execution_runtime.py`
- `gmail-agent/tools/gmail_audit/mailbox_memory_runtime.py`
- `gmail-agent/tools/gmail_audit/daszek_v3_operational_feed.py`
- `gmail-agent/tools/gmail_audit/daszek_engagement_feed/day.py`
- `gmail-agent/tools/gmail_audit/reply_drafter.py`

Changed tests:

- `gmail-agent/tools/gmail_audit/tests/test_wave2_calendar_read_only_lifecycle.py`
- `gmail-agent/tools/gmail_audit/tests/test_signal_adapters.py`
- `gmail-agent/tools/gmail_audit/tests/test_rc_d2_commitment_gating.py`

## Tests And Runtime/Integration Proof

Commands executed on commit `4b9d5b413dd39842555375c7bdfbe9def2717035`:

```text
python -m pytest tools/gmail_audit/tests/test_wave2_calendar_read_only_lifecycle.py tools/gmail_audit/tests/test_signal_adapters.py tools/gmail_audit/tests/test_calendar_case_boundary.py tools/gmail_audit/tests/test_action_planner_contract.py tools/gmail_audit/tests/test_rc_d2_commitment_gating.py tools/gmail_audit/tests/test_x1_day_sections.py -q
python -m pytest tools/gmail_audit/tests/test_case_snapshot_manager.py tools/gmail_audit/tests/test_case_context_contract.py tools/gmail_audit/tests/test_context_tray_set.py tools/gmail_audit/tests/test_service_request_playbook.py tools/gmail_audit/tests/test_signal_reconciler_runtime.py tools/gmail_audit/tests/test_signal_worker.py -q
python -m compileall tools/gmail_audit/calendar_models.py tools/gmail_audit/calendar_runtime.py tools/gmail_audit/calendar_signal_adapter.py tools/gmail_audit/execution_runtime.py tools/gmail_audit/mailbox_memory_runtime.py tools/gmail_audit/daszek_v3_operational_feed.py tools/gmail_audit/daszek_engagement_feed/day.py tools/gmail_audit/reply_drafter.py -q
node --check public/app.js
npx gitnexus detect_changes --repo gmail-agent --scope staged
```

Observed results:

- RP-07 focused suite: `49 passed`
- related regression suite: `46 passed`
- additional context/snapshot/playbook suite before commit: `22 passed`
- signal worker/reconciler suite before commit: `24 passed`
- Google Calendar write API static scan: no `calendar.events.insert`, `calendar.events.update`, `calendar.events.delete` or active `.create_event(` call outside fail-closed code/tests
- staged GitNexus detect changes: `medium`, expected changed symbols and context/feed flows
- runtime/integration synthetic read-only proof: `PASS`

Proof limitations:

- runtime proof used a synthetic Calendar client and did not call external Google APIs;
- no production data or Calendar side effect was performed;
- local Docker image parity is handled at Wave 2 exit gate, not inside this package record.

## Gap Outcome

Closed:

- `gap.calendar-two-worlds-of-visits.customer-proposed-date-risk-is-cli-only`
- `gap.calendar-two-worlds-of-visits.visit-reschedule-flow-has-no-confirmed-implementation`
- `gap.calendar-two-worlds-of-visits.visit-cancel-flow-has-no-confirmed-implementation`
- `gap.calendar-two-worlds-of-visits.calendar-signal-source-kind-does-not-match-registered-handler`
- `gap.calendar-two-worlds-of-visits.calendar-risk-has-three-independent-implementations`

Already closed by `RP-07A` and retained as fail-closed:

- `gap.calendar-two-worlds-of-visits.schedule-visit-does-not-create-real-calendar-event`
- `gap.calendar-two-worlds-of-visits.create-calendar-event-action-proposal-has-no-producer`

Residuals:

- no retained Calendar write path;
- no live P0 left in the RP-07 scope;
- production-observed proof remains out of scope because production deployment and external Calendar mutation are forbidden.

## Final Status

`CLOSED`
