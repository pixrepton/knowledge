# RP-15 EXECUTION

Package ID: `RP-15`

Status: `CLOSED`

Baseline:

- Wave 2 overlay baseline commit: `bc91f3ad3f86f552dc20e3a871022cafce19cce5`
- gmail-agent package commit: `fb8b42e4ed3adffd96bb41d7d22264046002c696`

Scope:

- automatic versus manual ownership of SLA escalation
- scheduler location for temporal escalation signals in the local runtime

Proof inventory:

- `STATIC`
  - `rg -n "sla_watcher" C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit -g '!**/__pycache__/**'`
- `UNIT`
  - `python -m pytest tools/gmail_audit/tests/test_sla_watcher.py tools/gmail_audit/tests/test_signal_worker.py -q`
- `RUNTIME_READ_ONLY`
  - `docker top gmail-agent-vps-gmail-agent-worker-1`
  - `docker exec gmail-agent-vps-gmail-agent-worker-1 python tools/gmail_audit/gmail_intake.py sla-watcher --oneshot --verbose`

Findings:

1. Before repair, only a manual CLI caller was confirmed for `sla_watcher`.
2. The local worker process already owned idle maintenance and bridge draining, so it was the smallest correct automatic owner for SLA checks.
3. `_emit_sla_escalation()` was using the wrong keyword (`db_url` instead of `database_url`) and could fail even during manual oneshot execution.

Decision:

- `DQ-15`: `RESOLVED_LOCAL`
  - selected path: `ONE_AUTOMATIC_OWNER`
  - owner: `signal-worker` idle maintenance loop
- `DQ-08`: locally resolved for this package
  - SLA escalation is no longer manual-only in the active local runtime

Historical data impact:

- Classification: `NONE`
- Notes:
  - the change affects only forward scheduling and event emission;
  - no historical signal rewrite or quarantine is needed.

Implementation scope:

- `gmail-agent/tools/gmail_audit/sla_watcher.py`
- `gmail-agent/tools/gmail_audit/signal_worker.py`
- `gmail-agent/tools/gmail_audit/tests/test_sla_watcher.py`
- `gmail-agent/tools/gmail_audit/tests/test_signal_worker.py`

Changed behavior:

- `signal-worker` now runs `sla_watcher_oneshot()` during idle maintenance on a bounded interval
- watcher results and failures are recorded in `run_state["summary"]`
- SLA os_event emission now uses the correct publisher contract and returns explicit success/failure

Tests and runtime proof:

- Focused tests:
  - `python -m pytest tools/gmail_audit/tests/test_sla_watcher.py tools/gmail_audit/tests/test_signal_worker.py -q`
- Runtime proof artifacts:
  - `.artifacts/wave2-rp06-rp12-rp15/sla_watcher_runtime_post_commit.log`
  - `.artifacts/wave2-rp06-rp12-rp15/post_commit_repo_state.json`

Runtime details:

- Worker container: `b16d1a748d8354e540902f165748f40877d935cedf0b3a21737f765e47ea613c`
- Proof result from `sla_watcher_runtime_post_commit.log`:
  - `ok=True`
  - `escalated=2`
  - no `unexpected keyword argument 'db_url'` failure remained

Gap result:

- Resolved:
  - `gap.sla-watcher-decision-escalation.sla-watcher-has-no-confirmed-automatic-trigger`

Residual risks:

- none inside this package scope

Final status:

- `CLOSED`
