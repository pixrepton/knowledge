# Raw inventory — event type ↔ emitter ↔ handler cross-reference (reverse-audit category 4)

Generated during the mechanical reverse-audit pass (2026-07-30), continuation session.

## Command used

```
rg -n "event_type" gmail-agent/tools/gmail_audit/event_spine/
rg -n "event_type\s*[:=]\s*['\"]" gmail-agent/tools/gmail_audit --type py -g '!*test*'
rg -rn "HandlerRegistry|build_default_registry|build_event_processor" gmail-agent/tools/gmail_audit
```

## Scope

All Python event-type dispatch mechanisms in gmail-agent (the only repo with a generic
event-processing registry). Cross-repo `os_event` emitters (fast-kalk, kalk-top,
top-instal-generator, cieplo-orchestrator) already enumerated in `CROSS_REPO_CONTRACTS.md`
(all confirmed `BOTH` via `EV-00175`) — not re-listed here, only their consumption-side handling
is in scope.

## Exclusions

Test files; `daszek`'s own PHP-side event/feed dispatch (a different, already-traced mechanism,
see `DASZEK-FEED-PUSH-NO-RETRY`/`DASZEK-COMMAND-OUTBOX-DRAIN`).

## Finding: TWO parallel, non-overlapping event-handling mechanisms exist

### Mechanism A — inline synchronous hook at ingestion time (ALWAYS LIVE)

`POST /internal/os-events` (`api_app.py:996+`) is the single ingestion route every producer in
the system posts to (fast-kalk, kalk-top, top-instal-generator, cieplo-orchestrator, gmail-agent
itself). Inline, synchronously, on every single POST, it calls
`cieplo_orchestrator_hook.maybe_apply_cieplo_hook_from_os_event(event_type=event_type, ...)`
(`api_app.py:1041`), which does direct string-matching against `event_type` (`is_cieplo_orchestrator_event`:
`cieplo.workflow.done` / `cieplo.workflow.failed` / `cieplo.workflow.state_changed`) and, on a
match, calls `apply_cieplo_orchestrator_result` to create/patch a `mailbox_memory_cases` row with
`source_kind='cieplo_orchestrated'`. This is the REAL, always-on, unconditional consumption path
for cieplo events — no feature flag, no opt-in.

All OTHER event types (`kalk.offer.calculated`, `kalk.offer.failed`, `generator.document.*`,
`case_os.materialize.approved`, `gmail_feed_push`, etc.) are simply STORED as rows in
`unified_os_events` by this same route (persisted, not further dispatched inline) — read later by
`fetch_recent_os_events`/`build_health_status` for the `/system/health/status` dashboard
(confirmed live, `EV-00164`), not routed through any type-specific handler.

### Mechanism B — `event_spine.processor` + `HandlerRegistry` (CLI-ONLY, OPT-IN, NOT LIVE BY DEFAULT)

A SEPARATE, general-purpose async event-processing framework:
`event_spine/handlers/registry.py`'s `HandlerRegistry` maps `event_type` string → handler
instance, built by `build_default_registry()`:

| event_type | handler | file |
|---|---|---|
| `correlation_links_registered` | `ShadowCorrelationLinksHandler` | `event_spine/handlers/shadow_correlation.py` |
| `cieplo_workflow_persisted` | `ShadowCieploWorkflowPersistedHandler` | `event_spine/handlers/shadow_cieplo_workflow.py` |
| (any other type) | `UnknownEventHandler` (fallback, `event_types = frozenset()`) | `event_spine/handlers/unknown.py` |

`UnknownEventHandler.handle`: if `ctx.mode == "shadow"` → `outcome="skipped"`; otherwise →
`outcome="failed"`. So an unmatched event_type is loud-failed only in non-shadow mode.

Reachability: `build_event_processor(settings)` reads `settings.event_spine_processor_mode`
(default `"off"` unless `event_spine_processor_enabled` is set, in which case it defaults to
`"shadow"`) — confirmed via `gmail_intake.py:1645-1651`'s
`run_event_spine_processor_command`, a standalone CLI subcommand that RAISES `ConfigError` if
`EVENT_SPINE_PROCESSOR_ENABLED` is not `1`, with its own error message recommending
`EVENT_SPINE_PROCESSOR_MODE=shadow` for safe dry-run use. Not called from the worker loop, not
called from any HTTP route, not called automatically anywhere — confirmed via exhaustive grep
(only 1 caller: this CLI command).

## Classification

- Mechanism A (inline hook): `LIVE_PATH`, always-on, no gate. The real production consumption
  path for cieplo events specifically; everything else is store-only (feeding the health
  dashboard, not type-specific handling).
- Mechanism B (`event_spine.processor`): `CONDITIONAL_PATH`/`MANUAL_TRIGGER_ONLY` — CLI-only,
  requires an explicit env flag, defaults to a safe shadow mode even when enabled. A deliberately
  narrow, opt-in, staged framework covering only 2 of the many live event types; NOT a silent
  production gap, because it is not live by default and its own tooling steers operators toward
  shadow mode.

## Unresolved / not independently re-verified this pass

- Whether `event_spine_processor_enabled=1` in non-shadow mode is actually set anywhere in a
  deployed environment (VPS/local Docker) was not checked — if it ever were, the majority of
  live event types would surface as `outcome="failed"` batch results, which would be visible in
  CLI output/logs but not confirmed to alert anyone.
- The full list of every `event_type` string ever emitted across all producers was not
  exhaustively cross-checked against Mechanism A's `is_cieplo_orchestrator_event` classifier
  beyond the 3 cieplo-specific strings already known — no other type-specific inline hooks were
  found via grep, but a fully exhaustive enumeration of every possible emitted `event_type`
  literal across all 5 producing repos was not performed (would require its own dedicated pass).

## Evidence

`EV-00178` (this category's summary record).
