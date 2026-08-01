# RP-12 EXECUTION

Package ID: `RP-12`

Status: `CLOSED`

Baseline:

- Wave 2 overlay baseline commit: `bc91f3ad3f86f552dc20e3a871022cafce19cce5`
- gmail-agent package commit: `fb8b42e4ed3adffd96bb41d7d22264046002c696`
- daszek package commit: `c73726873db41bb1b249d784400b54db0f946ed6`
- cieplo-orchestrator inspected commit: `e68f05386722b4034ca36bd39d169eba759f44e6`

Scope:

- current mailbox poller ownership
- stale secondary intake paths in the local runtime
- overlap risk between Node B and other mailbox consumers

Proof inventory:

- `STATIC`
  - `rg -n "cieplo_gmail_poll_enabled|gmail_query|newer_than:3d|poll_enabled" C:\Users\compg\Desktop\top-code workspace\cieplo-orchestrator -g '!**/__pycache__/**'`
  - `rg -n "gmail_ingress_owner|signal_worker_enabled" C:\Users\compg\Desktop\top-code workspace\gmail-agent\tools\gmail_audit -g '!**/__pycache__/**'`
- `RUNTIME_READ_ONLY`
  - `docker top gmail-agent-vps-gmail-agent-worker-1`
  - `docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"`
  - `docker exec daszek-local-wordpress php /tmp/wp_runtime_probe.php`

Findings:

1. The only active local mailbox poller process was `python tools/gmail_audit/gmail_intake.py signal-worker --loop --verbose` in the worker container.
2. Daszek still had a scheduled `daszek_mail_ingest` cron entry even when `mail_ingest=false`; this created stale ownership ambiguity.
3. `cieplo-orchestrator` still contains a Gmail poller code path, but it is guarded by `cieplo_gmail_poll_enabled=False` and a dedicated query `(cieplo.app OR cieplowlasciwie.pl) newer_than:3d`.
4. No active local Cieplo worker container existed in `docker ps`, so the local live path had one poller owner.

Decision:

- `DQ-11`: `RESOLVED_LOCAL`
  - selected current runtime model: `GMAIL_AGENT_SOLE_ACTIVE_LOCAL_POLLER`
  - implementation: remove stale Daszek cron ambiguity and keep Cieplo poller as disabled code path, not a live local owner
- `DQ-08`: `RESOLVED_LOCAL`
  - ownership ambiguity is removed locally
  - automatic per-signal replay is deferred with proof until later idempotency/recovery hardening; item-level failures are durable and visible locally

Rejected variants:

- keeping Daszek cron scheduled while disabled was rejected because it preserved false evidence of a second intake owner.
- removing the entire Cieplo poller code path without separate proof of future workflow ownership was rejected as premature cross-repo scope expansion.

Historical data impact:

- Classification: `NO_ACTION_REQUIRED`
- Notes:
  - current proof did not show active duplicate local polling or contaminated local intake history;
  - no quarantine or replay action was required.

Implementation scope:

- `daszek.php`

Changed behavior:

- `daszek_reconcile_cron_schedule()` now clears `daszek_mail_ingest` when `mail_ingest` is disabled
- the same reconcile function also guarantees cron schedule consistency on `init`, not only on activation

Tests and runtime proof:

- Syntax:
  - `php -l daszek.php`
- Runtime proof artifacts:
  - `.artifacts/wave2-rp06-rp12-rp15/wp_runtime_probe_post_commit.json`
  - `.artifacts/wave2-rp06-rp12-rp15/post_commit_repo_state.json`

Runtime details:

- Worker process list showed exactly one active poller process
- `wp_runtime_probe_post_commit.json` showed:
  - `"mail_ingest": false`
  - `"mail_ingest_next_scheduled": false`

Gap result:

- Resolved:
  - `gap.gmail-signal-worker-loop.shared-mailbox-polled-by-two-independent-workers`
- Deferred with proof:
  - `gap.gmail-signal-worker-loop.gmail-signal-stage-failures-have-no-per-signal-retry`: `DEFERRED_WITH_PROOF`

Residual risks:

- None open for Wave 2 scope; the Cieplo poller remains dormant and automatic per-signal replay is explicitly deferred to a later idempotency/recovery package.

Final status:

- `CLOSED`

## Wave 2 Closeout Addendum

Timestamp UTC: `2026-08-01T22:06:08Z`

Final status: `CLOSED`

Closeout basis:

- Host focused gate: `_raw/wave-02/exit-gate/gmail_focused.log` -> `153 passed`.
- Container parity gate: `_raw/wave-02/exit-gate/gmail_container.log` -> `38 passed`.
- Docker/local runtime health: `_raw/wave-02/exit-gate/docker_health.log` -> exit code `0`.
- Cieplo focused gate: `_raw/wave-02/exit-gate/cieplo.log` -> `18 passed`.
- Workflow Registry v1 final validator: `_raw/wave-02/exit-gate/workflow_v1.log` -> exit code `0`.

Final decision:

- Active local mailbox intake owner remains Node B `signal-worker`.
- Daszek mail-ingest cron ambiguity remains removed.
- Cieplo Gmail poller remains dormant/disabled and must be re-proven before any future enablement.
- Current signal worker persists item-level failures, continues the loop and exposes failures in `SignalWorkerLoopResult.last_errors`.
- Automatic per-signal replay is not implemented in Wave 2 because retrying irreversible stages without the later idempotency work can duplicate business effects.

Historical data impact:

- `NO_ACTION_REQUIRED` for local Wave 2 closeout.
- No duplicate local polling contamination was proven.
- No quarantine, migration or replay campaign was executed.

Gap result:

- `gap.gmail-signal-worker-loop.shared-mailbox-polled-by-two-independent-workers`: `CLOSED`
- `gap.gmail-signal-worker-loop.gmail-signal-stage-failures-have-no-per-signal-retry`: `DEFERRED_WITH_PROOF`

Remaining risks:

- None open for Wave 2 scope; automatic replay is explicitly deferred to a later idempotency/recovery package, not left as an implicit residual.
