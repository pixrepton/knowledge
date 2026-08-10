# FIX-RT02 — Crash-Looping Gmail Worker: root cause and runtime proof

## Observed defect

`gmail-agent-vps-gmail-agent-worker-1` was restarting continuously with exit code 1 under
`restart: unless-stopped`, while `daszek-local-wordpress` and `daszek-local-db` had been
`Exited (137)` for 43 hours.

```text
restart_count = 692        state = restarting        exit_code = 1
error: HTTPConnectionPool(host='host.docker.internal', port=8090):
       Max retries exceeded with url: /wp-json/daszek/v1/login
       (Connection refused)
logged as: "File/OS error in intake"   step="io"
```

## Architectural ownership determination

Per the workspace constitution: **Daszek is projection / operator UI. Node B owns operational
truth.** The flag that triggered the dependency was `DASZEK_OPERATIONAL_FEED_AUTO_PUSH=1`
(`DASZEK_V2_PUSH=0`), i.e. a background *projection push*, not a precondition for the worker's
canonical duties (polling Gmail, reconciling signals, persisting Node B state).

Verdict: **OPTIONAL_DEPENDENCY_HANDLING + STARTUP_FAILURE_POLICY.**

The repair therefore weakens, rather than strengthens, the Node B → Daszek runtime coupling. No
new dependency was introduced.

## Root cause, two faults in series

1. **Startup precondition.** `signal_worker.run_signal_loop` called `attach_daszek_client()`
   *before* the `try:` block that runs the poll loop. `attach_daszek_client` calls
   `client.login()` immediately, so an unreachable Daszek meant the worker never reached its
   poll loop at all — it died during startup, every time.

2. **Transport error mislabeled as local I/O.** `DaszekClient` let raw
   `requests.ConnectionError` escape. That subclasses `OSError`, so `gmail_intake.main()`'s
   `except OSError` caught it, logged "File/OS error in intake", and returned 1. Docker's
   `unless-stopped` policy then restarted the container, forever.

Neither fault was a Daszek problem. A projection outage is expected; converting it into a
process exit was the defect.

## Repair

| Change | File | Effect |
|---|---|---|
| `_DaszekSession` wraps `requests.Session.request` and re-raises transport failures as `DaszekClientError` | `daszek_client.py` | A network failure can never again be caught by `except OSError` and mislabeled as local file I/O. One translation point covers all 13 call sites. |
| `attach_daszek_projection_client(..., mandatory=)` | `signal_worker.py` | Optional push (`DASZEK_V2_PUSH` / `DASZEK_OPERATIONAL_FEED_AUTO_PUSH`) degrades and continues. An explicit operator `--push-daszek` still fails fast. |
| `_maybe_reattach_daszek` with 30s→600s bounded exponential backoff, driven from `_run_worker_idle_maintenance` | `signal_worker.py` | Automatic recovery without hammering a dead host. |
| `manifest.daszek_dependency` + `summary.daszek_degraded` + `DASZEK_DEPENDENCY_DEGRADED` / `DASZEK_DEPENDENCY_RECOVERED` | `signal_worker.py` | Degradation is visible rather than silent. |

Downstream push already handled a missing client (`skipped_no_daszek_client` in
`daszek_v3_feed_runtime.py`), so no exception is suppressed — the degraded path was already
modelled, it just could never be reached.

## Runtime proof

Runtime rebuilt from source (`gmail-agent-runtime:local`) and both affected containers
recreated. Host↔container SHA256 parity verified for all 11 changed files in **both**
`gmail-agent-nodeb-api` and the worker: **0 mismatches**.

### Degraded operation, Daszek still down

```text
restart_count = 0        state = running

DASZEK_DEPENDENCY_DEGRADED  dependency=daszek_projection  required=false
  error  = "Daszek transport failure (POST http://host.docker.internal:8090/wp-json/daszek/v1/login): ..."
  impact = "worker stays alive; projection push paused until Daszek returns"
```

Canonical Node B processing continued during degradation — from the same log window:

```text
WORKER_CHECKPOINT_RESTORE
[gmail-api] GET /profile ok (200)
[gmail-api] GET /history ok (200)
BP_EXECUTED               (business pulse)
sla_watcher               SLA CRITICAL: proposal ... waiting >24h
```

Note the error text: the transport failure is now attributed to Daszek, not reported as
"File/OS error in intake".

### Controlled recovery

`daszek-local-db` + `daszek-local-wordpress` restarted; the login endpoint answered `HTTP 400`
(alive, rejecting an empty body). The worker recovered **by itself**, with no container restart:

```text
DASZEK_DEPENDENCY_RECOVERED  dependency=daszek_projection  attempts=3
restart_count = 0            state = running
```

### Before / after

| | before | after |
|---|---|---|
| restart count | 692 and climbing | 0 |
| container state | `restarting` | `running` |
| reached the poll loop | never | yes |
| Daszek outage visible | as "File/OS error in intake" | as `DASZEK_DEPENDENCY_DEGRADED`, `required=false` |
| recovery when Daszek returns | container restart roulette | automatic, 3 bounded attempts, no restart |

No business data was mutated to produce this proof. The only runtime actions were rebuilding the
image, recreating two containers, and starting the two Daszek containers that were already part
of the local stack.

## Side effect worth recording

While crash-looping, the worker re-created run directories under the bind-mounted
`tools/gmail_audit/runs/` several times a minute. That contention produced an intermittent
`PermissionError [WinError 5]` in `tests/chaos/test_db_outage.py` during a full-suite run (the
test passed in isolation immediately afterwards). Removing the crash loop removes that
interference.
