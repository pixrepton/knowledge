# Reverse-audit category 10 — feature flag/env ↔ loader ↔ branch point ↔ live value

- Timestamp: `2026-07-30 21:03:07 +02:00`
- Working directory: `C:\Users\compg\Desktop\top-code workspace`
- Scope: workflow-critical feature flags and env-derived runtime toggles affecting Node B / Daszek operational-feed, agent runtime, signal worker, event spine, Google Drive ingest, Google Calendar ingest, and projection-canonical branch selection.
- Exclusions:
  - No secret values or raw token strings.
  - No production mutation.
  - No broad audit of every env in `.env.example`; only flags with confirmed branch points in traced workflows.
  - No revisit of already-closed category 8/9 semantics except where a flag gates those paths.
- Repo SHAs:
  - `gmail-agent`: `468d37ee6553b39bf6009939e9c87c13f3c183c7`
  - `daszek`: `672769d9496359dcfb7f2427d555ad34a2171b1a`
  - `knowledge`: `597b1091a296930ed32afb379ec19b8ab425d4fa`

## Exact commands

1. `rg -n "def load_settings|class Settings|projection_canonical_enabled|daszek_operational_feed_auto_push_enabled|AGENT_RUNTIME_ENABLED|AGENT_RUNTIME_MODE|SIGNAL_WORKER_ENABLED|EVENT_SPINE_PROCESSOR_ENABLED|GOOGLE_DRIVE_ENABLED|GOOGLE_DRIVE_INGEST_ENABLED|GOOGLE_CALENDAR_ENABLED|CASE_GUIDANCE_ENABLED|MAILBOX_MEMORY_VECTOR_ENABLED|ATTACHMENT_EXTRACTION_ENABLED|CASE_INTELLIGENCE_VNEXT_ENABLED|UNDERSTANDING_OUTPUT_ENABLED|DECISION_PIPELINE_ENABLED|SERVICE_REQUEST_PLAYBOOK_ENABLED|ACTION_PROPOSAL_V2_ENABLED" "gmail-agent/tools/gmail_audit/config.py" "gmail-agent/tools/gmail_audit/agent_runtime/feed_projection.py" "gmail-agent/tools/gmail_audit/agent_runtime/agent_reconcile.py" "gmail-agent/tools/gmail_audit/agent_hitl_bridge.py" "gmail-agent/tools/gmail_audit/gmail_intake.py" "gmail-agent/tools/gmail_audit/signal_worker.py"`
   - exit code: `0`
2. Inline Python: `load_settings()` + `projection_canonical_enabled()` safe boolean dump
   - exit code: `0`
3. `Get-Content "gmail-agent/tools/gmail_audit/config.py" | Select-Object -Index (820..1085)`
   - exit code: `0`
4. `Get-Content "gmail-agent/tools/gmail_audit/config.py" | Select-Object -Index (480..620)`
   - exit code: `0`
5. `Get-Content "gmail-agent/tools/gmail_audit/agent_runtime/feed_projection.py" | Select-Object -Index (168..210)`
   - exit code: `0`
6. Inline Python: `load_agent_runtime_settings()` safe boolean dump
   - exit code: `0`
7. `Get-Content "gmail-agent/tools/gmail_audit/agent_runtime/settings.py" | Select-Object -First 180`
   - exit code: `0`
8. `Get-Content "gmail-agent/tools/gmail_audit/agent_hitl_bridge.py" | Select-Object -Index (216..250)`
   - exit code: `0`
9. `Get-Content "gmail-agent/tools/gmail_audit/agent_runtime/agent_reconcile.py" | Select-Object -Index (920..950)`
   - exit code: `0`
10. `Get-Content "gmail-agent/tools/gmail_audit/gmail_intake.py" | Select-Object -Index (1438..1455)`
    - exit code: `0`
11. `rg -n "apply_case_os_runtime_profile_overrides|resolve_case_os_runtime_profile_name|load_agent_runtime_settings\\(|projection_canonical_enabled\\(|DASZEK_FEED_SOURCE|engagement_feed_enabled|agent_runtime_active" "gmail-agent/tools/gmail_audit"`
    - exit code: `0`
12. `Get-Content "gmail-agent/tools/gmail_audit/config.py" | Select-Object -Index (680..735)`
    - exit code: `0`
13. `Get-Content "gmail-agent/tools/gmail_audit/signal_worker.py" | Select-Object -Index (404..510)`
    - exit code: `0`
14. `Get-Content "gmail-agent/tools/gmail_audit/gmail_intake.py" | Select-Object -Index (1638..1660)`
    - exit code: `0`
15. `Get-Content "gmail-agent/tools/gmail_audit/gmail_intake.py" | Select-Object -Index (1828..1845)`
    - exit code: `0`
16. Inline Python: compare `load_agent_runtime_settings()` before and after `load_settings()`
    - exit code: `0`
17. `Get-Content "gmail-agent/tools/gmail_audit/gmail_intake_doctor.py" | Select-Object -Index (60..90)`
    - exit code: `0`
18. `Get-Content "gmail-agent/tools/gmail_audit/daszek_engagement_feed/__init__.py" | Select-Object -Index (1..155)`
    - exit code: `0`
19. `Get-Content "gmail-agent/tools/gmail_audit/agent_runtime/agent_reconcile.py" | Select-Object -Index (210..250)`
    - exit code: `0`

## Safe live-value snapshot

Safe boolean/value dump from the current local environment, without secrets:

- `daszek_operational_feed_auto_push_enabled = true`
- `daszek_v2_readback_enabled = true`
- `case_guidance_enabled = false`
- `attachment_extraction_enabled = true`
- `mailbox_memory_vector_enabled = true`
- `google_drive_enabled = true`
- `google_drive_ingest_enabled = true`
- `google_calendar_enabled = false`
- `signal_worker_enabled = true`
- `event_spine_processor_enabled = false`
- `case_intelligence_vnext_enabled = true`
- `understanding_output_enabled = true`
- `decision_pipeline_enabled = true`
- `service_request_playbook_enabled = true`
- `action_proposal_v2_enabled = true`
- raw `load_agent_runtime_settings()` result: `enabled=false`, `mode=prep`, `rag_enabled=false`
- `projection_canonical_enabled = true`

Loader-order proof in one process:

- `load_agent_runtime_settings()` before `load_settings()` → `enabled=false`, `mode=prep`
- `load_agent_runtime_settings()` after `load_settings()` → `enabled=true`, `mode=prep`

## Flag inventory

| Flag / env | Loader / source of truth | Confirmed branch point(s) | Safe current value | Transition meaning | Runtime classification |
|---|---|---|---|---|---|
| `CASE_OS_RUNTIME_PROFILE` | `config.load_settings()` calls `apply_case_os_runtime_profile_overrides()` before parsing booleans | forces `CASE_INTELLIGENCE_*`, `AGENT_RUNTIME_ENABLED`, `AGENT_RUNTIME_MODE`, `DECISION_PIPELINE_DRY_RUN_ONLY`, `DASZEK_FEED_SOURCE` | profile-derived; not printed directly, but effective flags prove `full`-style overrides are active inside `load_settings()` | single resolution point for Case OS mode | `LIVE_COMPLETE_BUT_ORDER_SENSITIVE` |
| `AGENT_RUNTIME_ENABLED` | two loaders: `config.load_settings()` mutates env first; `agent_runtime.settings.load_agent_runtime_settings()` reads raw env directly | `agent_runtime_reconcile_active`, `engagement_feed_source_enabled`, many agent entrypoints | raw loader alone: `false`; after `load_settings()`: `true` | decides whether reconcile uses agent runtime and whether engagement feed should be considered active | `LOADER_ORDER_SENSITIVE_DEFECT` |
| `AGENT_RUNTIME_MODE` | raw `agent_runtime.settings`; can also be profile-overridden to `prep` by `load_settings()` | `agent_runtime_reconcile_active`; `validate_agent_runtime_mode_not_primary` rejects `primary` in config path | `prep` | selects prep/primary/legacy behavior; `primary` permanently blocked by config path | `LIVE_COMPLETE` |
| `AGENT_PROJECTION_CANONICAL` | env-only helper `projection_canonical_enabled()` | `agent_runtime.agent_reconcile` canonical-vs-thin projection branch | `true` | enables canonical operator snapshot branch with fallback on exception | `LIVE_TRUE` |
| `DASZEK_OPERATIONAL_FEED_AUTO_PUSH` | `config.load_settings()`; if env unset, defaults to `not DASZEK_V2_PUSH` | `agent_hitl_bridge.best_effort_push_engagement_feed_after_hitl`; `signal_worker` / `gmail_intake` Daszek-client attach + manifest bits | `true` | enables Node B -> Daszek v3 operational-feed push path | `LIVE_TRUE_DEFAULT_DERIVED` |
| `SIGNAL_WORKER_ENABLED` | `config.load_settings()` bool parse | `signal_worker.run_signal_worker_loop` hard gate | `true` | allows signal worker commands to run at all | `LIVE_TRUE_HARD_GATE` |
| `EVENT_SPINE_PROCESSOR_ENABLED` | `config.load_settings()` bool parse | `gmail_intake.run_event_spine_processor_command` hard gate | `false` | disables event-spine processor command path entirely | `LIVE_FALSE_HARD_GATE` |
| `GOOGLE_DRIVE_ENABLED` + `GOOGLE_DRIVE_INGEST_ENABLED` | `config.load_settings()`; ingest defaults to drive-enabled value | `_require_drive_runtime`, `signal_worker` drive-change detection precondition | `true` + `true` | enables Drive ingest runtime and allows change-detection path to bootstrap | `LIVE_TRUE_COMPOSITE_GATE` |
| `GOOGLE_CALENDAR_ENABLED` | `config.load_settings()` bool parse | `gmail_intake.run_calendar_ingest_command` returns disabled if false | `false` | disables calendar ingest workflow | `LIVE_FALSE_HARD_GATE` |
| `ATTACHMENT_EXTRACTION_ENABLED` | `config.load_settings()` bool parse | doctor/health branch and downstream extraction enablement | `true` | allows attachment extraction path | `LIVE_TRUE_SUPPORTING` |
| `MAILBOX_MEMORY_VECTOR_ENABLED` | `config.load_settings()` bool parse | canonical-production validation, mailbox vector readiness checks | `true` | enables vector retrieval readiness path | `LIVE_TRUE_SUPPORTING` |
| `CASE_INTELLIGENCE_VNEXT_ENABLED`, `UNDERSTANDING_OUTPUT_ENABLED`, `DECISION_PIPELINE_ENABLED`, `SERVICE_REQUEST_PLAYBOOK_ENABLED`, `ACTION_PROPOSAL_V2_ENABLED` | `config.load_settings()` / Case OS profile overrides | downstream Case OS branches and startup profile summary | all `true` | activate current Case OS intelligence stack | `LIVE_TRUE_PROFILE_DERIVED` |

## Key findings

1. `AGENT_RUNTIME_ENABLED` does not have one stable live value across loaders.
   - `load_settings()` mutates `os.environ` via `apply_case_os_runtime_profile_overrides()`.
   - `load_agent_runtime_settings()` does not call that override logic; it reads raw env directly.
   - In the same process, the effective value flips from `false` to `true` depending on whether `load_settings()` ran first.
   - This is a real branch-selection defect, not only a reporting mismatch.

2. Feed-source activation can therefore become loader-order sensitive.
   - `engagement_feed_source_enabled()` calls `agent_runtime_reconcile_active()` with no explicit settings when `DASZEK_FEED_SOURCE` is empty.
   - That falls through to raw `load_agent_runtime_settings()`.
   - Result: a caller that did not run `load_settings()` first may treat agent runtime as inactive and choose the wrong feed source.

3. `DASZEK_OPERATIONAL_FEED_AUTO_PUSH` is not a plain env toggle; it has a derived default.
   - If `DASZEK_OPERATIONAL_FEED_AUTO_PUSH` is unset, the effective value becomes `not DASZEK_V2_PUSH`.
   - Current safe live result is `true`.
   - Consumers include HITL feed push and signal-worker Daszek client attach logic.

4. Current local environment intentionally disables some workflows while leaving adjacent ones on.
   - `signal_worker_enabled=true`
   - `event_spine_processor_enabled=false`
   - `google_drive_enabled=true`, `google_drive_ingest_enabled=true`
   - `google_calendar_enabled=false`
   - This is not itself a defect; it is the current live branch map.

5. `AGENT_PROJECTION_CANONICAL=true` is independently controlled from `AGENT_RUNTIME_ENABLED`.
   - The canonical projection branch is enabled if the env flag is set.
   - It is not derived from the Case OS profile helper.
   - This is acceptable only when the agent-runtime path is already active; otherwise it becomes dormant configuration.

## False positives

1. `agent_runtime_enabled=false` from the raw agent loader does not prove the app as a whole is currently in legacy mode.
   - Entry points that call `load_settings()` first can flip the same process to effective `enabled=true`.
   - The defect is loader-order sensitivity, not a single universally-false runtime state.

2. `google_calendar_enabled=false` is not a bug by itself.
   - The code explicitly returns a disabled status and exits cleanly.
   - This is a configuration choice unless a workflow claims calendar ingest is active.

3. `event_spine_processor_enabled=false` is not evidence that event spine is absent everywhere.
   - This category only proves the dedicated processor command is hard-gated off.

## Unresolved

1. This slice did not prove every single process entrypoint calls `load_settings()` before any agent-runtime checks.
   - The defect is already proven because some direct helpers read raw agent settings.
   - A full process-by-process audit remains for a later category if needed.

2. `CASE_GUIDANCE_ENABLED=false` was captured as a live value but not traced to a workflow-critical branch point in this category's narrowed scope.

## New findings suitable for registry/gap updates

1. Loader-order-sensitive agent runtime activation.
   - Same workspace env yields different `AGENT_RUNTIME_ENABLED` depending on whether `config.load_settings()` ran first.
   - Impacts feed-source selection and any helper that infers agent-runtime activity from raw `load_agent_runtime_settings()`.

## Evidence IDs

- Existing evidence referenced during continuation: `EV-00183`
- New evidence to append after this artifact: `EV-00184`
