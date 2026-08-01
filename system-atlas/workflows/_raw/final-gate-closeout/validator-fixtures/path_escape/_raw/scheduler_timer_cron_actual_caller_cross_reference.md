# Reverse-audit category 11 — scheduler/timer/cron ↔ actual caller

- Timestamp: `2026-07-30 21:06:28 +02:00`
- Working directory: `C:\Users\compg\Desktop\top-code workspace`
- Scope: backend schedulers, cron hooks, long-running loop ticks, and cron-capable maintenance entrypoints that materially affect traced workflows across `daszek` and `gmail-agent`.
- Exclusions:
  - Frontend-only `setTimeout` / UI timers in browser code.
  - Third-party bundled libraries.
  - Generic `sleep()` calls that are local retry/backoff inside one request, not scheduling surfaces.
  - Test-only references unless needed to eliminate a false positive.
- Repo SHAs:
  - `gmail-agent`: `468d37ee6553b39bf6009939e9c87c13f3c183c7`
  - `daszek`: `672769d9496359dcfb7f2427d555ad34a2171b1a`
  - `knowledge`: `597b1091a296930ed32afb379ec19b8ab425d4fa`

## Exact commands

1. `rg -n "wp_schedule_event|wp_next_scheduled|register_activation_hook|wp_clear_scheduled_hook|add_action\\(\\s*'daszek_|do_action\\(\\s*'daszek_" "daszek"`
   - exit code: `0`
2. `rg -n "PredictiveScheduler|maybe_worker_bridge_drain_tick|maybe_heartbeat_operational_feed|continuous_poll|_sleep_with_abort|poll_interval|worker_heartbeat|loop_mode" "gmail-agent/tools/gmail_audit/signal_worker.py" "gmail-agent/tools/gmail_audit/agent_runtime/signal_worker_scheduler.py" "gmail-agent/tools/gmail_audit/daszek_v3_feed_runtime.py" "gmail-agent/tools/gmail_audit/daszek_bridge_queue_drain.py"`
   - exit code: `0`
3. `Get-Content "daszek/daszek.php" | Select-Object -First 220`
   - exit code: `0`
4. `Get-Content "gmail-agent/tools/gmail_audit/signal_worker.py" | Select-Object -Index (618..735)`
   - exit code: `0`
5. `Get-Content "gmail-agent/tools/gmail_audit/signal_worker.py" | Select-Object -Index (1000..1228)`
   - exit code: `0`
6. `Get-Content "daszek/includes/cron.php" | Select-Object -First 260`
   - exit code: `0`
7. `Get-Content "gmail-agent/tools/gmail_audit/agent_runtime/signal_worker_scheduler.py" | Select-Object -First 220`
   - exit code: `0`
8. `rg -n "run_backfill_correlation_registry|backfill_correlation_registry|cron_delta|wp-cron|cron" "gmail-agent/tools/gmail_audit" "daszek"`
   - exit code: `0`
9. `rg -n "apscheduler|BackgroundScheduler|schedule\\.every|setInterval\\(|setTimeout\\(|croniter|celery beat|beat_schedule" "gmail-agent" "daszek" "kalk-top" "fast-kalk" "top-instal-generator" "cieplo-orchestrator" "rag-widget" "rag-chat-asystent"`
   - exit code: `0`
10. `Get-Content "gmail-agent/tools/gmail_audit/daszek_bridge_queue_drain.py" | Select-Object -Index (460..530)`
    - exit code: `0`

## Scheduler inventory

| Scheduler / timer surface | Registration / loader | Actual caller | Trigger cadence | Terminal action | Runtime classification |
|---|---|---|---|---|---|
| `daszek_daily_backup` | `register_activation_hook` → `daszek_activate()` → `wp_schedule_event(..., 'daily', 'daszek_daily_backup')`; handler bound by `add_action` | WordPress cron subsystem | daily | `daszek_cron_backup()` copies `tasks.json` and deletes backups older than 7 days | `LIVE_WP_CRON` |
| `daszek_bridge_queue_gc` | same activation path; daily WP-Cron schedule | WordPress cron subsystem | daily | `daszek_cron_bridge_queue_gc()` calls `daszek_v2_bridge_queue_gc(90)` and logs errors | `LIVE_WP_CRON` |
| `daszek_mail_ingest` | scheduled only when `daszek_get_config()['mail_ingest']` is truthy; otherwise cleared | WordPress cron subsystem | every 5 minutes via custom `daszek_5min` schedule | `daszek_cron_mail_ingest()` -> legacy IMAP poll path `daszek_process_mailbox()` | `LEGACY_CONDITIONAL_WP_CRON` |
| `signal_worker` continuous loop | no external scheduler registration in repo; explicit long-running process command | `run_signal_worker_loop(... loop_mode='continuous_poll')` | unbounded while-loop with sleep between iterations | Gmail/Drive change polling, worker heartbeat, idle maintenance | `LIVE_PROCESS_LOOP` |
| `PredictiveScheduler` | instantiated only inside `signal_worker` when Gmail change detection is enabled | same worker loop | adjusts next sleep interval from observed Gmail event volume | returns sleep seconds; does not call business code directly | `INTERNAL_TIMER_HELPER` |
| worker idle feed heartbeat | no cron registration; called from `_run_worker_idle_maintenance()` | `signal_worker` continuous loop | every continuous-poll iteration before sleep | `maybe_heartbeat_operational_feed()` | `LOOP_TICK_CALLER` |
| remote bridge queue drain tick | no cron registration; called from `_run_worker_idle_maintenance()` | `signal_worker` continuous loop | every `daszek_bridge_drain_interval_iterations` iterations (default from settings) | `maybe_worker_bridge_drain_tick()` fetches remote pending rows, drains, may push feed | `LOOP_TICK_CALLER` |
| `run_backfill_correlation_registry.py --cron` | CLI supports `--cron` / `cron_delta` mode | no scheduler registration found in repo | operator/external scheduler only | correlation-links backfill / delta resync | `CRON_CAPABLE_BUT_UNSCHEDULED` |

## Key findings

1. Exactly three real WordPress cron hooks are registered by Daszek plugin activation.
   - `daszek_daily_backup`
   - `daszek_bridge_queue_gc`
   - `daszek_mail_ingest`
   - All three are also explicitly cleared on deactivation and uninstall.

2. `daszek_mail_ingest` is a genuinely schedulable legacy lane, not dead text.
   - It is registered only when `mail_ingest` config is enabled.
   - Its handler is the old IMAP polling path in `includes/cron.php`, explicitly documented as legacy and separate from Node B Gmail intake.
   - Classification: legacy but live-capable if the config is turned on.

3. The active Node B scheduler in repo code is not cron; it is the `signal_worker` process loop.
   - `while True` loop
   - sleep computed by `_poll_sleep_seconds(...)`
   - optional `PredictiveScheduler`
   - heartbeat write each iteration
   - idle maintenance after each continuous-poll cycle

4. Two important maintenance actions are loop-tick driven, not independently scheduled.
   - `maybe_heartbeat_operational_feed()` runs from `_run_worker_idle_maintenance()`
   - `maybe_worker_bridge_drain_tick()` runs there every `bridge_interval`
   - Meaning: if the signal worker is not running in continuous poll, neither maintenance lane has its caller.

5. `run_backfill_correlation_registry.py --cron` is only cron-shaped CLI, not a scheduled workflow.
   - Repo grep found mode flags/tests/docs, but no registration/hook/service/timer that actually runs it.

6. No backend APScheduler/Celery-beat/native schedule registry was found in the audited repos.
   - Remaining `setTimeout` hits are frontend/browser timers or bundled libraries and are excluded from workflow scheduling.

## False positives

1. `sleep()` inside `_poll_with_retry` or other backoff code is not a scheduler.
   - It is request-local retry delay, not an independent caller.

2. Browser `setTimeout` calls in `fast-kalk` / `rag-widget` are not backend workflow schedulers.

3. `run_backfill_correlation_registry.py --cron` is not evidence of an actual cron until an external scheduler or in-repo registration is proven.

## Unresolved

1. This slice proves registrations/callers, not whether an operator or host actually keeps `signal_worker` running continuously in the current environment.

2. This slice does not measure real wall-clock cadence of the continuous poll loop; it proves only the sleep-selection mechanics and caller wiring.

## New findings suitable for registry/gap updates

- No new gap filed from category 11.
- Category 11 mainly closed caller truth and eliminated cron-like false positives.

## Evidence IDs

- Existing evidence referenced during continuation: `EV-00184`
- New evidence to append after this artifact: `EV-00185`
