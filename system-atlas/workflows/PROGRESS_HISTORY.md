# PROGRESS_HISTORY — evidence trail only, ZERO authority over current status

**Do NOT read this file for current state.** It is a verbatim snapshot of the working ledger as
it stood before the 2026-07-30 canonical rewrite, kept so that the reasoning trail, correction
log, and superseded checkpoints remain auditable. Every counter, domain status, and open-item
list below is SUPERSEDED by `PROGRESS.md`. Where this file and `PROGRESS.md` disagree,
`PROGRESS.md` is correct by definition.

Known stale content preserved here deliberately: the 89-evidence/11-workflow artifact table, the
pre-resolution Domain 1/2/6/7 status lines, the `_raw/ empty` note, and the
`MANDATORY_EXECUTION_LIFECYCLE_CLOSED` Domain 4 label (corrected to
`APPROVE_PATH_CLOSED + FULL_EXECUTION_LIFECYCLE_OPEN` in the canonical ledger).

---

# PROGRESS — AI-OS-WORKFLOW-RECONSTRUCTION-AND-REGISTRY-01

Resumption ledger. A new session starts by: (1) reading this file top to bottom — there is
exactly ONE canonical current entry per domain below, no duplicates, (2) spot-checking the last
few `WORKFLOW_REGISTRY.yaml` entries against the cited `evidence_ids`, (3) continuing from the
`Next entrypoints` of the last in-progress domain, or from `DOMAIN-COMPLETENESS-REVISIT` if all
9 domains show a "PASS OPEN"-style status, not re-doing prior analysis.

**Status semantics (corrected 2026-07-30, per operator audit — see `Correction log` at the
bottom):** `CLOSED` is reserved for a domain where the mandatory scope from the target brief has
been covered AND a completeness/reverse check has run. Until then, use a two-part status:
`<WHAT IS DONE> — <WHAT IS OPEN>`, e.g. `PRIMARY_RECONCILE_AND_HANDOFF_CLOSED —
MEMORY/FACTS/CONTEXT_ASSEMBLY_PASS_OPEN`. This is not a demotion of the work done — the evidence
already gathered stands — it is a correction of what the status label is allowed to claim.

Operating model (unchanged): CBM first for call chains → direct code read → Serena only when CBM
can't resolve a symbol/import (not usable yet, see Tooling below) → GitNexus only as the final
adversarial completeness check, not per-workflow. Compact registry entries
(`knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml`), short evidence records
(`WORKFLOW_EVIDENCE.jsonl`), raw mechanical dumps in `_raw/`. Long-form docs (`WORKFLOW_ATLAS.md`,
`WORKFLOW_GAPS.md`, `STATE_OWNERSHIP_MATRIX.md`, `CROSS_REPO_CONTRACTS.md`,
`ARCHITECTURAL_RULES_AUDIT.md`, `EXECUTIVE_SUMMARY.md`) are generated mechanically from
registry+evidence at the end, not hand-maintained mid-flight.

## Repo inventory status

Confirmed by direct `git`/filesystem read (not assumed from `brief.md`'s "4 repos" framing):
**10 git repos** total — workspace meta-repo (`.`), `knowledge`, `gmail-agent`, `kalk-top`,
`daszek`, `cieplo-orchestrator`, `rag-chat-asystent`, `top-instal-generator`, `rag-widget`,
`fast-kalk` — plus **1 non-git local harness** (`wp-bridges`, confirmed no `.git`). Full detail
in `RUNTIME_BASELINE.md` §1. No archive/build/`.venv`/`node_modules` directories were treated as
source repos. `archive-codex-and-claude/` at workspace root exists but is explicitly historical
(prior session artifact bundle), out of scope for entrypoint/workflow reconstruction.

## Tooling status

- **Codebase Memory MCP**: live, project-scoped indexes already current for `gmail-agent`
  (exact HEAD match `468d37e`), `daszek`, `kalk-top`, `cieplo-orchestrator`, `rag-widget`,
  `top-instal-generator`. `rag-chat-asystent` has no clean standalone CBM index (only a
  suspicious nested-path project, see `RUNTIME_BASELINE.md` §3) — **treat CBM as unavailable
  for rag-chat-asystent, use `rg`/direct read there**. `fast-kalk`/`wp-bridges`/`daszek` PHP+JS
  content: CBM Python graph doesn't cover PHP; use `rg`/direct read for route-level detail.
- **Serena MCP**: added to `.mcp.json`, **not usable this session** (trust-hash approval needed,
  next session only). Not blocking — using `rg`/CBM/direct read per the fallback rule.
- **GitNexus — canonical indexed-repo table (reconciled 2026-07-30, supersedes all earlier
  narrative claims about "6 of 8" / "5 newly indexed" / "8 remaining" — those were inconsistent
  restatements of the same underlying `gitnexus list` state, not separate facts):**

  | repo | GitNexus indexed | indexed at / commit | language coverage | known blind spots | required fallback |
  |---|---|---|---|---|---|
  | `gmail-agent` | yes | 2026-07-30 01:04:21, `468d37e` | Python | `gitnexus query` (BM25/vector) degraded — "FTS indexes missing" (`EV-00114`) | `gitnexus context` (structural) preferred over `gitnexus query`; `rg`/direct read for exhaustive text search |
  | `daszek` | yes | 2026-07-30 07:56:22, `672769d` | PHP | variable-typed/DI call dispatch not resolved (`EV-00118`, confirmed on a sibling PHP repo, applies here too); WordPress `add_action` hook dispatch not resolved (`EV-00116`'s caveat) | `rg`/direct read to confirm any "no caller found" result before treating it as dead code |
  | `kalk-top` | yes | 2026-07-30 07:57:10, `9d56055` | PHP | same DI/variable-dispatch blind spot, CONFIRMED not hypothetical (`EV-00118`: `CalculateOfferController`→`CalculateOfferUseCase.execute` edge missing from graph despite being live in production) | direct code read is authoritative for PHP call resolution, not GitNexus absence-of-edge |
  | `cieplo-orchestrator` | yes | 2026-07-30 08:07:37, `e68f053` | Python | not yet spot-checked against a specific registry claim this session | none identified yet; treat as provisionally reliable pending a spot-check |
  | `top-instal-generator` | yes | 2026-07-30 08:08:03, `7e52795` | PHP | 1 file (`top-instal-generator.php`) logged a non-fatal "no Module scope found" warning at index time; same DI blind spot as other PHP repos | direct read for that one file; DI caveat applies |
  | `fast-kalk` | yes | 2026-07-30 08:08:15, `06a470d` | PHP | not yet spot-checked; same DI blind spot presumed to apply (not repo-specific, confirmed at the tool level) | direct read for any call-graph claim before trusting an absent edge |
  | `rag-widget` | yes | 2026-07-30 08:08:27, `c64707a` | PHP | 1 file (`hvac-rag-chat/hvac-rag-chat.php`) logged the same "no Module scope found" warning; DI blind spot presumed to apply | direct read for that file; DI caveat applies |
  | `rag-chat-asystent` | **no** | n/a | Python | not indexed — CBM also has no clean index for this repo (`RUNTIME_BASELINE.md` §3) | **mandatory `rg`/AST/direct-read fallback for all of Domain 5's revisit** — no graph tool available at all for this repo |
  | `wp-bridges` | **N/A — excluded by design, not a gap** | n/a | PHP | confirmed this pass (`git rev-parse --is-inside-work-tree`/`.git` presence check): `wp-bridges` has NO own `.git` — it is a subfolder of the parent workspace's single top-level git repo, not an independently-versioned service repo, unlike all 8 rows above which each have their own `.git`. It is a thin local harness (per its own `AGENTS.md`: "Cienka lokalna powierzchnia mostu WordPress... do audytu szwów integracyjnych") | `rg`/direct read only — never counted against "repos remaining to index" again |

  **Reconciled totals**: 8 real git repos in scope; 7 GitNexus-indexed; 1 not indexed
  (`rag-chat-asystent`, permanent `rg`-only fallback by tool limitation, not by choice); 1 harness
  folder (`wp-bridges`) correctly excluded from the repo count entirely.
- **Docker read-only inspection**: done, see `RUNTIME_BASELINE.md` §2.

## Artifacts written so far

| File | Status |
|---|---|
| `RUNTIME_BASELINE.md` | done (drift check + Docker inspection) |
| `ENTRYPOINT_INVENTORY.md` | first pass done — gmail-agent CLI/Docker/worker/cron entrypoints confirmed; gmail-agent's 53 HTTP routes located but not individually enumerated (open gap); satellite repos' WP-plugin bootstrap files located, route-level detail not enumerated |
| `WORKFLOW_EVIDENCE.jsonl` | 89 records (EV-00001..EV-00089), physical order now matches ID order (reconciled) |
| `WORKFLOW_REGISTRY.yaml` | 11 workflow entries + 4 subflows (Daszek split into DASZEK-COMMAND-OUTBOX-DRAIN and DASZEK-FEED-PUSH-NO-RETRY, two directions, not merged) |
| `PROGRESS.md` | this file |
| `_raw/` | created, still empty — route-enumeration and PHP-route gaps below should route here when tackled |
| `WORKFLOW_ATLAS.md`, `WORKFLOW_GAPS.md`, `STATE_OWNERSHIP_MATRIX.md`, `CROSS_REPO_CONTRACTS.md`, `ARCHITECTURAL_RULES_AUDIT.md`, `RUNTIME_PROOF_PLAN.md`, `EXECUTIVE_SUMMARY.md` | **DONE** — all 12 target artifacts now exist, generated mechanically from registry+evidence, no new code reads for these 5 |

## P0 hypothesis verification (brief.md §5 / target §9 items 1-4, plus worker command)

Method used for each: `caller → suspect symbol → real implementation → test/consumer`, single
bounded path, not a full domain re-audit.

| # | Hypothesis | Verdict | Evidence |
|---|---|---|---|
| 1a | `query_anything` case-RAG wrong signature | **CONFIRMED_OPEN** | EV-00001, EV-00002 — call always raises `TypeError` (missing required positional `query_vector_literal`, wrong kwargs `query_text`/`limit`) |
| 1b | `query_anything` imports nonexistent `find_similar_cases` | **CONFIRMED_OPEN** | EV-00003, EV-00004 — `ImportError` every call, real module exports differently-named functions |
| 1c | `query_anything` temporal recall depends on sibling-repo `sys.path` | **CONFIRMED_OPEN** | EV-00005 — `parents[4]` + `sys.path.insert` into `<workspace>/rag-chat-asystent/backend`, breaks outside this exact local dev layout |
| 1d | `query_anything` counts errors as answered sources | **CONFIRMED_OPEN** | EV-00006 — error strings don't start with `"Brak"`, included in the `total` count |
| 1e | `query_anything` always returns `status="ok"` | **CONFIRMED_OPEN** | EV-00007 — unconditional, no all-error check |
| — | `search_rag_knowledge` (2nd, distinct case-scoped RAG tool) is CORRECT | **NOT_REPRODUCED as broken** | EV-00077 — real embedding, correct `fetch()` signature; case-scoped RAG is not uniformly broken, only `query_anything`'s redundant internal attempt is |
| 2 | Learning loop row-shape (`fetch_open_proposals_for_case` tuple vs dict) | **CONFIRMED_OPEN** | EV-00008..EV-00012 — full chain traced: both real call sites (`api_app.py:2230`, `:2259`) open `psycopg.connect(db_url)` with no `row_factory`; `_row_to_proposal` drops every field but `proposal_id`; can misclassify a real approve as `RESPONSE_DIVERGENT_ACTION`. Not fixed despite the sibling `fetch_decision_queue` bug being fixed via `dict_row` (`OPERATOR_DECISIONS.md` 2026-07-16). |
| 3 | Gmail dry-run reports `executed=True`/`decision_status="executed"` with no send | **CONFIRMED_OPEN** | EV-00013 — exact match, `hitl_gmail_send.py:146-160`. Plus EV-00014: the *real* send branch uses the identical `decision_status="executed"`, so that field alone never distinguishes simulated from real. |
| 4 | Calendar producer→consumer (`customer_proposed_date`) | **CONFIRMED_OPEN, definitively closed** | Full chain + a second, decisive confirmation in Domain 6: `context_for_case` (sole caller of `infer_calendar_risk`) is itself only called from a manual CLI (`gmail_intake.py:1494`, `calendar-context` command) — unreachable from any automatic path, full stop. EV-00016/17/31-38/44-46/80. |
| 5 | Worker command is `doctor` by default in production | **split per corrected taxonomy** | `STATIC_CONFIG_RISK`/`CONFIRMED_OPEN`: compose-file literal default is still `doctor` (EV-00030). `RUNTIME_CONFIRMED`: live container actually runs `signal-worker --loop --verbose` (EV-00015). Both true simultaneously, recorded separately, not collapsed into `NOT_REPRODUCED`. |
| 6 | Global RAG missing for Node B (brief §6.6) | **CONFIRMED_OPEN, decisively closed** | EV-00078: `context_assembler.py`'s "company knowledge" is a static local text file, zero HTTP client to `rag-chat-asystent` anywhere in traced gmail-agent code. EV-00079: the producer (`rag-chat-asystent /chat`) is real and live, reachable only from `rag-widget`, not gmail-agent — a `MISSING_CONSUMER` gap. |
| 7 | Two visit worlds (brief §6.5) | **CONFIRMED_OPEN, decisively closed** | EV-00082: `execute_schedule_visit` writes only a `scheduled_visit` text fact, zero Calendar API interaction. EV-00081: `ingest_events` polls real Calendar events in, but nothing reconciles the two. |
| 8 | Three action dictionaries (brief §6.1) | **CONFIRMED, doc-vs-doc conflict recorded, not fully adjudicated** | EV-00069: structurally confirmed 3 distinct stage outputs exist (`business_result`, `action_plan_result`, `case_intelligence_result`). `ARCHITECTURE_DECISIONS.md` (2026-07-27, newer than `brief.md`) claims this is resolved-by-design via `decision_pipeline`+`policy_action_proposal`; EV-00070 confirms a real convergence point (`attach_policy_and_proposals`) exists, gated on a real `decision_candidate`. Whether this fully resolves brief.md's `NO_SAFE_MAPPING_EXISTS` framing or only partially is not yet adjudicated — both citations preserved, not resolved by assertion. |
| 9 | Two/three proposal lifecycles (brief §6.4) | **CONFIRMED, richer than brief.md's framing** | EV-00074/75/76: at least 3 live, distinct proposal/execution shapes confirmed (`action_proposals_v2`, materialize proposals w/ idempotency key, `execution_runtime.ActionProposal`/`ExecutionResult` w/ real callers in `calendar_runtime.py`/`daszek_bridge_queue_drain.py`/`gmail_intake.py`). Whether genuinely redundant or domain-scoped (calendar vs. gmail vs. generic) is an open question, not resolved — **this exact question is part of Domain 4's mandatory later closure, see queue below.** |

Remaining P0/HIGH items not yet touched: Daszek feed outbox (brief §6.7 — note: a *different*,
Daszek→NodeB command outbox with real claim/lease/retry/dead-letter semantics WAS found this
session, `daszek/includes/command-outbox.php` — whether the NodeB→Daszek feed-push direction
brief.md actually describes has an equivalent durable retry is **not yet resolved**, see Domain 7
below), policy→tool enforcement (target §10, not yet traced).

## Domain reconstruction checkpoints

Each domain below has exactly one current entry. Historical narrative from earlier in the same
session is preserved where it adds evidence detail; duplicate/superseded status lines have been
removed (see `Correction log`).

### Domain 1 — Gmail i signals
Status: **CORE_LIVE_PATH_CLOSED — REPLAY/RECOVERY/IDEMPOTENCY REVERSE PASS OPEN**
Workflows: `GMAIL-SIGNAL-WORKER-LOOP` (+ `SUBFLOW-GMAIL-SIGNAL-RECONCILE`)
Evidence range: EV-00015, EV-00018..EV-00030
Done: production call site pinned end-to-end (`run_signal_loop` → `process_snapshot` →
`run_gmail_signal_runtime` → `build_gmail_signals` → `build_canonical_signal` → journal append →
dedup check → `reconcile_signal`); `SIGNAL_HANDLERS` registration fully enumerated (4 handlers,
decorator pattern, unconditional at import time); journal tables confirmed distinct
(`mailbox_memory_signals` vs `mailbox_memory_raw_observations`), not competing.
**Open (mandatory, not yet done — queued below)**: signal-level retry vs poll-level retry not
disambiguated; `signal-replay`/`signal-rebuild-case` CLI recovery paths not traced; dedup/
idempotency key mechanics (`content_hash`, `idempotency_key` columns) not explained.
Next entrypoint (already in progress elsewhere): `SIGNAL_HANDLERS['gmail']` handler body was
opened in Domain 2 (`_reconcile_gmail_signal`, signal_reconciler.py:295) — that thread continues
there, not here.

### Domain 2 — Case i memory
Status: **PRIMARY_RECONCILE_AND_HANDOFF_CLOSED — MEMORY/FACTS/CONTEXT_ASSEMBLY_PASS_OPEN**
Workflows: `GMAIL-RECONCILE-MODE-DISPATCH`, `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
(+ `SUBFLOW-CASE-LINK-ROUTE-DECISION`, `SUBFLOW-CASE-INTELLIGENCE-TO-AGENT-HANDOFF`)
Evidence range: EV-00039..EV-00057
Done: full case-linking/routing decision tree (`resolve_case_id_for_agent`, `route_signal`);
Identity/Engagement resolution (`build_registry_for_reconcile` fail-closed,
`resolve_engagement_for_case` fail-closed throughout); `EngagementSnapshotV2` creation
(`ensure_engagement_snapshot`); the formal Case/memory → agent-runtime handoff contract
(`agent_signal`'s 5 added fields); full per-block analysis of the 3 `run_agent_reconcile`
try/except blocks — see `PARTIAL_FAILURE_MASKED_AS_SUCCESS analysis` below, unchanged from when
first written, still accurate.
**Open (mandatory, not yet done — queued below)**: thread memory, active-fact selection
mechanics, conflicts/gaps detection, full `CaseContextPack` assembly read
(`_run_mailbox_intelligence_downstream`'s `stage_config`, agent_reconcile.py:186-218),
`mailbox_store.fetch_case_by_message_id` reachability, `FAST_LINK_CONFIDENCE` value.

**PARTIAL_FAILURE_MASKED_AS_SUCCESS analysis** (per the operator's 9-point checklist,
`run_agent_reconcile`'s 3 try/except blocks, EV-00054/55/56, refined by EV-00061/62 after
opening `AgentGraphEngine._run` in Domain 3):
- **Block 1** (case intelligence downstream): high severity. Silent `{}` fallback, no
  self-describing failure marker on the data itself, feeds the agent's core semantic context as
  empty defaults, terminal status unaffected, no retry (journal dedup blocks reprocessing).
- **Block 2** (policy envelope handoff): intentional, labeled degradation, not integrity loss —
  code comment confirms design intent, fallback carries an explicit `freshness='unavailable'`
  marker a consumer *could* check. Lower severity, by design.
- **Block 3** (agent execution itself), REFINED in Domain 3 (EV-00061/62): planner-decision
  exceptions are NOT actually masked here — those are already safely converted to a proper
  `hitl_gate.required=True` escalation inside `AgentGraphEngine._run` (the DELIVERY-1 fix,
  re-confirmed live in current code). What Block 3 actually masks: plumbing failures, most
  concretely a genuine CAS `AgentConcurrencyError` version conflict — a correctly-DETECTED
  concurrent-write race gets folded into the same generic `agent_run_failed` warning string and
  an independently-confirmed mislabeling bug (`rebuild_result.update_reasons` becomes
  `['agent_dry_run']` instead of reflecting a real crash, EV-00051). `patch_signal_engagement`/
  `job_store.record_completed` fire unconditionally regardless.
- Open across all 3: whether `ReconcileResult.warnings` ever reaches Daszek/health/telemetry is
  **still not confirmed** — this is Domain 7 (Daszek) territory, not yet resolved there either
  (see Domain 7 below).
- A 4th, structurally identical masking try/except exists inside `build_agent_reconcile_result`
  itself (`projection_canonical_enabled` gate, EV-00049) — noted, not analyzed to the same depth.

Calendar P0 (item 4): fully closed, all citations current in the P0 table above.

### Domain 3 — Understanding, decisions, policy, planner i agent runtime
Status: **PRIMARY_AGENT_LOOP_AND_DECISION_PIPELINE_CLOSED — PLANNER/TOOL-SELECTION/SUBAGENT_PASS_OPEN**
Workflows: `AGENT-GRAPH-EXECUTE-RUN`, `AGENT-GRAPH-TURN-LOOP`
(+ `SUBFLOW-SHARED-DOWNSTREAM-STAGES`)
Evidence range: EV-00058..EV-00071
Done: `execute_agent_run`'s full structure (constitution routing, checkpoint/resume, event-spine
emission, CAS save via `store.save_snapshot(expected_version=...)` with real
`AgentConcurrencyError` on conflict); the turn loop (tool-not-offered/timeout/planner-error
safety nets, `_apply_tool_result` write-gateway field guard — `_BRAIN1_OWNED_SNAPSHOT_FIELDS` is
a literal code constant, not just doc framing — turn journal, per-turn checkpointing, loop
termination); **directly resolved brief.md §6.2** (Draft+ActionPlanner before Understanding) as
`CONFIRMED_OPEN` via `run_shared_downstream_stages`' own docstring/code order (link_case_context
→ mailbox → business_reasoning → draft_reply → plan_actions → case_intelligence/Understanding
last → policy); DecisionCandidate/PolicyDecision/ActionProposalV2 fully traced through
`attach_policy_and_proposals`, `dry_run_only` RUNTIME_CONFIRMED `False` live (real proposals, not
dormant).
**Open (mandatory, not yet done — queued below)**: `OpenAIToolPlanner`/`build_planner` internals
(actual tool-selection mechanics) not opened; `select_sub_agent` not opened; `_LOOP_TERMINAL_CODES`
full set not enumerated; divergence detection as a distinct mechanism beyond Domain 1/2's
learning-loop evidence — carried to Domain 9.

### Domain 4 — HITL i execution — MANDATORY CLOSURE COMPLETED THIS PASS
Status: **MANDATORY_EXECUTION_LIFECYCLE_CLOSED — MATERIALIZE-EXECUTOR INTERNALS, REJECT PATH,
AND 3RD PROPOSAL SHAPE (gmail_intake.py call sites) STILL OPEN**
Evidence added this pass: EV-00110, EV-00111.

**Full mandatory chain now traced with code evidence** (operator's required sequence):
`proposal` (found in `snapshot.staging_proposals` or `snapshot.actions[]`) → `persistence check`
(status must be `'pending'`, fail-closed on re-approve) → `approve/reject` (approve traced; reject
not opened) → `mutation gateway` (`store.save_snapshot`, CAS-protected) → `executor`
(`execute_materialize_proposal` for materialize-shaped proposals, OR
`AgentMcpService.approve_hitl_action` for action-shaped ones, e.g. `draft_reply` →
`hitl_gmail_send.py`, Domain 1) → `side effect` (conditional real Case creation/linking via
`reconcile_linked_after_materialize`, gated by `proposal_type`; or Gmail send, confirmed broken
dry-run per Domain 1 P0) → `ExecutionResult`-shaped return dict (`exec_result`, outer shape seen,
internals not opened) → `idempotency` (`_stable_bridge_key` deterministic decision key AND a
separate `Idempotency-Key` HTTP header AND CAS version checks — three independent idempotency
mechanisms at three different layers) → `retry/recovery` (**REAL** CAS retry with exponential
backoff, 3 attempts, on the materialize path — a genuinely more robust mechanism than Domain 3's
`execute_agent_run` CAS save, which has none) → `Case projection` (`store.save_snapshot` IS this)
→ `Daszek projection` (`best_effort_push_engagement_feed_after_hitl`, **confirmed called from
BOTH approval routes**, resolving an open question from the original Domain 4 pass) → `final
consumer` (Daszek/operator, plus event-spine/telemetry consumers, both event types explicitly
shadow/best-effort).

**Key refinement**: the "two distinct proposal systems" framing (`hitl/approve` vs
`materialize/approve`) is corrected — they are separate HTTP entrypoints with different
auth/idempotency surfaces, but **converge on the identical executor**
(`approve_materialize_proposal`) whenever `action_id` is a proposal ID (`prop_`-prefixed). Not
fully independent all the way down, as the earlier pass had left ambiguous.

Still open (genuinely deferred, not blocking this closure): `execute_materialize_proposal`'s own
internals; `AgentMcpService.approve_hitl_action`'s own body; the reject/clarification path;
`gmail_intake.py`'s 3 `execution_runtime` call sites (the one remaining unresolved piece of the
"3rd proposal shape" question); `outcome_unknown` handling; restart-recovery for a mid-execution
crash (distinct from the concurrent-write case, which CAS retry does cover).

Workflows: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
Evidence range: EV-00072..EV-00076, EV-00110, EV-00111

### Domain 5 — RAG i documents
Status: **CROSS-REPO_GLOBAL-RAG_GAP_CLOSED — INTERNAL_RAG/DOCUMENT_PIPELINES_INCOMPLETE**
Workflows: `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP`
Evidence range: EV-00077..EV-00079
Done: decisively closed brief.md §6.6 (no global RAG for Node B) — see P0 table item 6. Found
`search_rag_knowledge` as a second, correctly-implemented case-scoped RAG tool distinct from
`query_anything`'s broken one. Confirmed `rag-chat-asystent /chat` is real/live/reachable from
`rag-widget` only.
**Open (mandatory, not yet done — queued below)**: `rag-chat-asystent`'s entire internal pipeline
— Drive ingest, parser routing, chunking, embeddings, BM25/vector retrieval, reranking,
citations, document facts, document intelligence, GraphRAG, world model — none of this was
traced this pass, only confirmed the route exists and the container is healthy.
`similar_cases_precedent`/`temporal_recall` already covered under P0 evidence (EV-00003/04/05),
not re-analyzed here.

### Domain 6 — Calendar i czas
Status: **CORE_TWO-WORLDS_GAP_CLOSED — RESCHEDULE/CANCEL/DEADLINE/SLA/STAGNATION/SCHEDULER_PASS_OPEN**
Workflows: `CALENDAR-TWO-WORLDS-OF-VISITS`
Evidence range: EV-00016/17/31-38/44-46/80-82 (mix of reused P0 evidence + new)
Done: brief.md §5.4 and §6.5 both decisively closed with direct, non-inferred evidence (not just
the earlier hop-by-hop inference) — `context_for_case` (sole caller of `infer_calendar_risk`) is
itself only reachable from a manual CLI diagnostic; `execute_schedule_visit` confirmed to touch
only a text fact, zero Calendar API. Real event-driven Calendar→Signal bridge confirmed
(`ingest_events`, EV-00081) — a genuine part of "temporal event → signal → reconcile" exists, but
only for event-driven changes, not pure time-as-trigger.
**Scheduler question resolved this pass** (EV-00083): the only periodic/cron-like mechanism found
in gmail-agent, `topinstal-event-processor` (systemd timer, every 5 min), is explicitly
shadow-mode-only by its own `.service`/`.timer` config ("Shadow only — never active on
production", "shadow soak") — the strongest evidence found for "no live time-as-trigger
scheduler exists," though not an exhaustive search of every repo.
**Still open (mandatory, not yet done — queued below)**: reschedule, cancel, deadline, SLA — no
dedicated functions found by name search (not exhaustive). Stagnation: a `STAGNATING` lifecycle
enum value exists and is read (`case_coherence.py:77`, EV-00084), corroborating pre-existing
`BACKLOG.md` ambiguity items found in earlier recon (`STAGNATION-LIFECYCLE-STATE-AMBIGUITY-1`) —
not a new discovery, but independently confirmed live. `agent_runtime/signal_worker_scheduler.py`'s
`PredictiveScheduler` not opened — may be poll-interval tuning rather than a stagnation trigger,
unconfirmed. `execution_runtime.create_action_proposal`'s Calendar-triggered flow (EV-00076) not
traced end-to-end.

### Domain 7 — Daszek
Status: **in progress**
Evidence range: none yet domain-specific (reused EV-00074's gap note)
Verified so far (this pass, direct code read, not copied from `ARCHITECTURE_DECISIONS.md`):
`daszek_engagement_feed/build.py`'s `_list_main_feed_snapshots` bounded-overfetch pattern is
real (membership applied before the effective LIMIT, capped by `_MAIN_FEED_MAX_SCAN`);
`feed_visibility.py`'s `classify_signal_for_feed`/`effective_visibility_mode` confirmed:
unknown lane never means noise (falls through to `main_feed`), legacy snapshots without stored
classification default to `main_feed` (explicit reason-coded fallback, not silent), pending
operator work always overrides routing as a safety override. These independently CONFIRM
`ARCHITECTURE_DECISIONS.md`'s claims about this mechanism rather than merely citing the doc.
**New finding, potentially resolves/complicates brief.md §6.7**: `daszek/includes/command-outbox.php`
is a real, durable, well-built outbox with claim/lease semantics (`daszek_command_outbox_claim_batch`,
lease tokens, lease expiry), retry status, and dead-letter support (`status IN ('completed',
'failed', 'skipped', 'dead_letter', 'retry')`) — backed by a real MySQL table with idempotent
enqueue (dedup by `queue_id` + `request_hash`). Its Node-B-side consumer is
`daszek_bridge_queue_drain.py` (`SCHEMA_VERSION = "daszek_bridge_queue.v1"` matches). **However
this is the Daszek→NodeB direction** (queued operator commands/adjudication items NodeB drains),
**not confirmed to be the NodeB→Daszek feed-push direction** brief.md §6.7 actually describes
(pushing new snapshot/projection data outward). `daszek_push_policy.py` (policy only, no
push/retry code found) and `daszek_client.py` (`push_preview`/`push_v2_projection` methods
located, not yet read for retry/failure behavior) are the concrete next entrypoints to resolve
this precisely — **do not assume brief.md §6.7 is refuted by the command-outbox finding until
that direction is actually confirmed.**
**CORRECTION (EV-00116/EV-00117, see `Correction log`)**: the paragraph above describes the
DB-table mechanism (`wp_daszek_command_outbox`) accurately as CODE, but this session later found
its only writer is a one-time migration function with no confirmed caller of its own — no live
producer found. The Daszek→NodeB direction IS genuinely live, but via a SEPARATE, older,
JSONL-file-backed `bridge_queue.jsonl` store (written by REST routes incl. operator
approve/reject of action proposals; drained by `daszek_bridge_queue_drain.py`'s
`maybe_worker_bridge_drain_tick`, called every worker-loop tick, via REST fetch/complete — not
via `daszek_command_outbox_claim_batch`). Do not cite the claim/lease/dead-letter durability
above as describing the live path; see `WORKFLOW_REGISTRY.yaml`'s `DASZEK-COMMAND-OUTBOX-DRAIN`
entry and `WORKFLOW_GAPS.md` P1 item 14 for the corrected picture.
**Resolved this pass (EV-00085..88)**: `DaszekClient.push_v2_projection`'s raw HTTP call has no
retry (raises on failure); its manual/replay-tool callers match brief.md §6.7's literal
description exactly (counter + log + continue, no queue) — BUT this whole "v2 push" mechanism
(`push_v2_projection_to_daszek`) is confirmed SKIPPED on the live worker: composing two
already-confirmed live facts (`DASZEK_FEED_SOURCE` env empty + `agent_runtime_reconcile_active()`
`RUNTIME_CONFIRMED True`, EV-00041) through `engagement_feed_source_enabled`'s own decision tree
shows it evaluates `True` live, which skips the v2 push entirely. **brief.md §6.7's specific claim
targets a path confirmed dormant on the live configuration — the real open question is the ACTUAL
live mechanism's (`daszek_engagement_feed/`) own delivery direction (push vs Daszek-side pull) and
retry/failure behavior, which is NOT yet resolved.**
**§6.7 DECISIVELY CLOSED this pass (EV-00089)**: `best_effort_push_engagement_feed_after_hitl`
(agent_hitl_bridge.py:218-279, called from `api_app.py`'s `materialize/approve` route) is the
real, live v3 feed-push mechanism (`build_operational_feed_from_engagement_store` →
`client.post_v3_operational_feed_snapshot`). On any failure: a `publish_gmail_feed_push_event(
ok=False, error=...)` telemetry event and a returned error dict — **no retry, no durable queue,
no dead-letter** — matching brief.md §6.7 exactly, on the correct live path this time (not the
dormant v2 one). The function's own name ("best_effort") signals this is intentional design, not
an oversight. **Verdict: `CONFIRMED_OPEN`.**
**RESOLVED (EV-00119, runtime proof executed)**: `settings.daszek_operational_feed_auto_push_enabled`
confirmed `True` on the live production worker via direct settings introspection — this workflow
is unconditionally live, not gated off. `DASZEK-FEED-PUSH-NO-RETRY`'s registry `status` updated
accordingly (`CONDITIONAL_PATH` removed).
Still open: whether this is the ONLY feed-push trigger or whether other case-state
changes (not just HITL approve) also push, and by what mechanism if so — a case updated by the
agent with no HITL action might never push at all, not yet confirmed either way; whether
`ReconcileResult.warnings` (Domain 2/3's masking question) surfaces anywhere Daszek/operator can
see it; Karta dnia; Business Pulse; health endpoint; frontend field usage vs backend fields sent.
Confirmed but not deeply traced: `daszek/includes/api-v3.php` exposes a real, rich REST surface
for the Daszek frontend itself (`/desk`, `/day`, `/cases`, `/cases/{id}`, `/case-archive`,
`/desk-notes/{id}`, `/ai-quality`, `/cockpit`, `/cohort-runs`, `/ingress-quality-snapshots`) —
these are read routes for the operator UI, distinct from the ingest endpoint gmail-agent posts
to (not located by name in this pass, presumably in `api-v2.php` or a dedicated ingest handler).

**Push mechanism lineage closed (EV-00090)**: confirmed 3 generations (v1 `/tasks` preview,
v2 `/ingest` operator projection, v3 operational feed) — `daszek_push_policy.py`'s own docstring
numbering confirms v1/v2 are older; all 3 share the identical no-retry design. brief.md §6.7 is
confirmed across the whole lineage, not just the currently-active generation.
**Masking-visibility question near-closed (EV-00091)**: no evidence found that
`ReconcileResult.warnings` (Domain 2/3's Block 1/2/3 signals) reaches any durable
operator/Daszek-visible surface — `signal_worker.py` has a separate, unrelated
`SignalWorkerLoopResult.warnings`, and the v3 feed push only carries the engagement snapshot's
own fields, not raw reconcile warnings. Not exhaustively proven (would require tracing every
`ReconcileResult` consumer), but no positive evidence of visibility found anywhere searched —
recorded as the working conclusion, flagged as revisitable if contradicted later.

**Domain 7 status: DASZEK PUSH MECHANISM LINEAGE, FEED VISIBILITY, COMMAND OUTBOX, AND
MASKING-VISIBILITY QUESTION ALL CLOSED (first pass) — FRONTEND SURFACE, KARTA DNIA, BUSINESS
PULSE, HEALTH ENDPOINT, AND BACKEND↔FRONTEND FIELD USAGE STILL OPEN**, queued in
`DOMAIN-COMPLETENESS-REVISIT` item 7. Moving to Domain 8 per the operator's explicit instruction
to prioritize covering all domains.

### Domain 8 — Integracje ofertowe i WordPress
Status: **FIRST_PASS_COMPLETE (sections A-G below) — COMPLETENESS_REVISIT_OPEN (named items list
at the end of this section, identical to `DOMAIN-COMPLETENESS-REVISIT` queue item 8; these are
two different scopes, not a contradiction: "A-G done" means the first-pass cross-repo pipeline
trace is complete, "remaining items" means the SEPARATE, deeper completeness-revisit pass has
specific named items still open, exactly as intended by the two-part status model.)**
Workflows added: `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`,
`KALK-TOP-CALCULATE-OFFER-PIPELINE`, `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`,
`CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`
Evidence range: EV-00092..EV-00105

**A (fast-kalk) done**: full chat/calculate/register/dispatch chain traced, both cross-repo
endpoints to gmail-agent CONFIRMED on both sides (`/internal/registry/links`, `/internal/os-events`).
Real finding: the widget-facing price is a fuzzed ±range (0.93x/1.16x) around kalk-top's real
gross total, never the exact figure. class-chat.php/class-answer-extractor.php (LLM intake) not opened.

**B (kalk-top) done**: single deterministic pipeline confirmed, single production wiring, no
legacy calculator backend found. Pricing repository is a single Source of Truth for the price
book; internals of each engine (ozc/selection/buffer/cwu/pricing) not traced to the byte level.

**C (top-instal-generator) done**: canonical `from-offer-dto` AND legacy `direct-config` modes
BOTH live (not one dead). Two converter paths (gotenberg real / fallback-docx degraded, honestly
tracked in telemetry). Legacy AJAX path (`generator.js`/`simple_generate`) and template/field
mapping internals not opened.

**D (cieplo-orchestrator) done**: real, well-built explicit state machine, genuinely more rigorous
error-state handling than several gmail-agent findings. Confirmed D3 precisely — a second,
independent, self-documented Gmail poller. **New finding, not in brief.md**: `docker-compose.cieplo-local.yml`
mounts `gmail-agent/.env.local-vps` read-only specifically "for shared Google OAuth creds" (per
earlier structural recon this session) — meaning cieplo-orchestrator's poller may use the SAME
Gmail credentials/mailbox as gmail-agent's own poller, not just a separate DB — this raises a real
collision-risk question (two independent pollers against the same mailbox) that goes beyond the
"separate DB, no case SoT conflict" framing already established; NOT resolved this pass, added to
`DOMAIN-COMPLETENESS-REVISIT`. Whether `FAILED_RETRYABLE` rows are ever actually retried by
anything is unconfirmed — the state exists, no consumer of it was found.

**E (rag-widget, wp-bridges, compose) light-touch only**: rag-widget confirmed pure HTTP client
(plus a document-upload capability, not just chat, previously unflagged); its hardcoded default
API URL points at a PRODUCTION VPS hostname, not localhost — whether the local stack overrides
this was not verified. wp-bridges' deprecated/harness status re-confirmed, not re-opened in
depth. Full WordPress compose plugin-mount audit not exhaustively repeated (already covered in
`ENTRYPOINT_INVENTORY.md`).

**F (cross-repo contracts)**: `TOPINSTAL-KERNEL-GRAPH.yaml` was NOT used as ground truth — every
cross-repo edge asserted above was confirmed by opening BOTH sides in code this session
(fast-kalk↔gmail-agent x2, fast-kalk↔kalk-top, fast-kalk↔top-instal-generator [one-sided only,
generator side not re-opened], cieplo-orchestrator↔kalk-top, cieplo-orchestrator↔top-instal-generator,
kalk-top↔gmail-agent [one-sided, pattern-inferred not re-verified], top-instal-generator↔gmail-agent
[one-sided, pattern-inferred]). A full `CROSS_REPO_CONTRACTS.md`-formatted table is deferred to
the final synthesis pass (mechanical, generated from these `workflow_id` entries' `external_calls`
fields, not re-derived by hand).

**G (D1-D3 + ownership), synthesized from evidence already gathered, not fresh reads:**
- **D1 (RAG performs no hard offer calc): CONFIRMED_HOLDS.** `CalculateOfferUseCase` (EV-00099)
  is a pure deterministic engine pipeline, no RAG/LLM call found anywhere in it or its call chain;
  rag-chat-asystent is independently confirmed unreachable from gmail-agent's agent runtime
  (Domain 5) and no evidence found of RAG output feeding kalk-top's pricing from any direction.
- **D2 (no agent besides kalk-top computes/creates OfferDTO): CONFIRMED for all traced entrypoints**
  (fast-kalk, cieplo-orchestrator both delegate to kalk-top's calculate-offer rather than computing
  locally). gmail-agent's agent runtime has a `call_kalk_top.py` tool handler (located in Domain 1
  recon, `agent_runtime/tools/`) whose very existence/naming strongly implies it also delegates
  rather than computes — **not independently opened this pass**, flagged as the one unverified
  edge of this claim, added to `DOMAIN-COMPLETENESS-REVISIT`.
- **D3 (dual Gmail intake intentional): CONFIRMED_HOLDS**, with the new shared-credentials nuance
  above added as a genuine open risk question, not previously flagged in brief.md.
- **Ownership, confirmed**: CalcRequestDTO/OfferDTO → kalk-top (single production wiring).
  Documents → top-instal-generator. Pipeline/workflow status → each system owns its own
  independently (kalk-top: none persisted beyond per-request; cieplo-orchestrator: `WorkflowState`
  in its own DB; fast-kalk: session cache; gmail-agent: Case/Engagement, Domains 1-4) — **no
  single cross-system pipeline-status owner exists, by design, each repo owns its own slice.**
  **RESOLVED THIS PASS (EV-00132), DECISIVE `MISSING_PRODUCER` (not "unconfirmed")**: margin has
  NO producer anywhere across the traced offer pipeline — kalk-top's `OfferDTO`/`PricingEngine`
  compute only net/gross customer-facing price, zero cost-basis/margin field found anywhere in
  `core/` (exhaustive grep); combined with Domain 9's `EV-00109` (gmail-agent has no
  outcome-capture layer either), margin is confirmed absent end-to-end. Sale outcome (won/lost/
  signed) is ALSO confirmed `MISSING_PRODUCER` cross-system: an exhaustive grep for
  `sale_outcome`/`deal_won`/`deal_lost`/`offer_accepted`/`contract_signed`/`win_loss` across
  kalk-top, top-instal-generator, cieplo-orchestrator, and fast-kalk returns zero matches in all
  four repos, extending Domain 9's gmail-agent-only finding to the whole system.
  **REFINED by the reverse audit (`EV-00136`, see below)**: the "sale outcome" side is even more
  precisely characterized than a blanket missing-producer — the agent-exposed `get_win_rate`
  tool IS a real consumer that queries case `status` for `"won"`/`"lost"`, but the real lifecycle
  vocabulary's success state is `"completed"`, not `"won"` — a `CONTRACT_DRIFT`, not just an
  absence, meaning the tool silently and permanently reports 0 wins rather than failing loudly.

**Domain 8 status split explicitly, per operator instruction**:
`FIRST_PASS_COMPLETE`: sections A-G (cross-repo pipeline trace, D1-D3, ownership incl. the
margin/outcome `MISSING_PRODUCER` closure above).
`COMPLETENESS_REVISIT_OPEN` (named, not yet done, distinct from the first pass): fast-kalk's
`class-chat.php`/`class-answer-extractor.php` (LLM intake mechanism); kalk-top's individual
engine internals (device/materials/labor cost origins at the byte level); top-instal-generator's
legacy AJAX path + template/field mapping; whether cieplo-orchestrator's `FAILED_RETRYABLE` state
has any real consumer; the shared-Gmail-credentials collision-risk question; `call_kalk_top.py`
tool handler (D2's one still-unopened edge).

### Domain 9 — Learning i outcomes
Status: **CORE DIVERGENCE-TO-CANDIDATE CHAIN CLOSED, DECISIVE FINDING ESTABLISHED —
PATTERN_LEARNER.PY INTERNALS AND OUTCOME-SIDE OF THE CHAIN (CONFIRMED MISSING, NOT
UNEXAMINED) STILL OPEN**
Workflow added: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
Evidence range: EV-00106..EV-00109

**Single most important Domain 9 finding**: approved learning rules are confirmed **evidence-only,
not control** (target §9 item 16). Exhaustive grep for `learning_rule_candidates`/`CANDIDATE_APPROVED`
across the whole package finds exactly 5 files — none in `agent_runtime/`, `policy_action_proposal.py`,
`policy_engine.py`, `business_reasoner.py`, `action_planner.py`, or `intake_shared_downstream.py`.
No code path reads an approved rule back into planning/policy/tool-selection. The loop terminates
at "operator can view/approve a DB row."

**`CANDIDATE_THRESHOLD=3` corrected**: it's only the base/fallback constant. The real threshold
is `adaptive_threshold()` (varies by case-family observation volume) plus a previously-unknown
**cross-family boost** that can lower it 30% based on other families' strong candidates.

**Auto-approval CAN approve a wrong rule — concretely demonstrated, not hypothetical**: one of
two auto-approve triggers fires purely on parent-family observation volume, with **zero
confidence check** in that branch.

**Business outcome capture (sale value, offer acceptance, visit completion, case closure, margin)
is CONFIRMED MISSING** — not merely unexamined: a targeted, whole-package grep found no dedicated
outcome-tracking module, only the separate Intelligence Evolution eval/benchmark track (a
measurement harness, not a production pipeline) and a lightweight precedent-matching classifier.
Since the outcome-capture edge doesn't exist AND the rule-consumption edge doesn't exist, **the
full `operator action → ... → later business outcome` chain the target mandated is confirmed
broken at BOTH ends**, not just incomplete in the middle.

**New cross-cutting finding**: Domain 2's `fetch_open_proposals_for_case` row-shape bug can
corrupt `classify_operator_response`'s input BEFORE it reaches this loop — meaning some fraction
of "divergence" signals feeding the learning loop may themselves be artifacts of the unrelated
Domain 2 bug, not genuine operator disagreement. Not quantified, flagged as a real interaction
between two independently-confirmed findings.

Next entrypoints (queued): `pattern_learner.py` internals and its own consumers;
`operator_feedback_runtime.py`/`operator_learning_hooks.py` (the latter already read in Domain 2,
not re-opened here) for any other feedback path; `LEARNING_LOOPS_MIGRATIONS.sql` schema (not
opened this pass, would confirm exact table shapes).

## DOMAIN-COMPLETENESS-REVISIT queue

**Status as of this pass: Domains 1, 2, 3, 6, 8 fully resolved (all named sub-items closed with
new evidence). Domain 4's mandatory chain was closed in an earlier pass with 3 named sub-items
still open. Domain 5 resolved at proportionate depth (query+ingest pipeline traced; a few named
internals explicitly deferred, not silently dropped). Domain 7 mostly resolved (auto-push gate
runtime-confirmed, command-outbox liveness corrected); a handful of named sub-items remain.**
Processed AFTER Domains 6-9 reach their own first-pass status, per operator instruction — not
now, not by re-reading everything, only these specific named entrypoints:

1. **Domain 1 — ALL ITEMS RESOLVED THIS PASS.**
   ~~signal-level vs poll-level retry disambiguation~~ **RESOLVED (EV-00122)**: `_poll_with_retry`
   covers ONLY the list-changes API call (bounded in-process retry+backoff, circuit-breaker on
   repeated failure); each individual message's `gmail_fetch`/`gmail_reconcile` stage gets exactly
   ONE attempt with no retry at all — `_record_item_failure` only logs/counts, never requeues.
   Whether a message that failed before journaling resurfaces on a later poll depends on Gmail
   API's own history/list semantics — not verified, left as a genuinely open sub-question, not
   claimed either way. Folded into `WORKFLOW_GAPS.md` item 20 as a new confirmed instance of the
   best-effort-no-retry pattern.
   `signal-replay`/`signal-rebuild-case` CLI recovery paths were already covered in the GitNexus
   spot-check (`EV-00114`, see `Correction log`).
   ~~dedup/idempotency key mechanics~~ **RESOLVED (EV-00121)**: two-layer, race-safe dedup —
   `mailbox_memory_raw_observations.source_fingerprint` (raw-ingestion layer) and
   `mailbox_memory_signals.idempotency_key` (signal layer) both carry real DB UNIQUE indexes, not
   just app-level pre-checks; `content_hash` is stored but is informational-only, not part of the
   dedup decision anywhere found.
2. **Domain 2 — ALL ITEMS RESOLVED THIS PASS.**
   ~~thread memory (producer/storage/update rules/readers/lazy migration/restart-replay)~~
   **RESOLVED (EV-00125)**: producer `build_thread_memory` (deterministic merge, not LLM); storage
   Postgres `mailbox_memory_thread_memory` (content-hash-versioned); real lazy Daszek-migration
   fallback confirmed (`only_if_absent=True`, race-safe); fetch-failure soft / persist-failure
   hard error-handling asymmetry found; replay-order nuance flagged as open, not claimed safe.
   ~~active-fact selection (candidates/conflict/supersession/invalidation/selection policy)~~ +
   ~~conflicts/gaps detection (producer/persistence/consumer/decision impact)~~ **RESOLVED
   (EV-00126, EV-00127)**: TWO distinct, complementary mechanisms found — `case_coherence.py`
   (mutation-TIME, write-gate, numeric >20% = hard block, real decision impact, fail-open on its
   OWN internal errors) and `split_conflicting_facts` (query-TIME, read-time selection: highest
   confidence + newest-on-tie wins as "active", no persisted invalidation, a parallel `conflicts`
   list computed fresh and not persisted).
   ~~`_run_mailbox_intelligence_downstream`'s `stage_config` assembly (full sources/CaseContextPack/
   partial writes/transaction boundaries)~~ **RESOLVED (EV-00125, EV-00127)**: full data-source
   enumeration done; a genuine partial-write gap found in `finalize_case` (3 sequential,
   non-transactional store writes, no rollback on mid-sequence failure) — added to
   `WORKFLOW_GAPS.md`.
   ~~`mailbox_store.fetch_case_by_message_id` reachability~~ **RESOLVED (EV-00124)**: confirmed
   dead on the gmail-dispatcher call site (`signal_reconciler.py:322`, no `mailbox_store` passed),
   but reachable from the sibling `agent_reconcile.py:554` call site (real store passed) — split
   by call site, not universally dead.
   ~~`FAST_LINK_CONFIDENCE` value~~ **RESOLVED (EV-00123)**: `0.92` default; only actually gates
   the routing outcome when no `case_id` exists yet — once a case is already linked, routing is
   `fast_link` regardless of confidence.
3. **Domain 3**: `OpenAIToolPlanner`/`build_planner` tool-selection internals; `select_sub_agent`.
   ~~`_LOOP_TERMINAL_CODES` full enumeration~~ **RESOLVED (EV-00120)**: exactly 2 codes
   (`pending_operator`, `node_a_error`), consumed only by `_is_loop_terminal`; a dedicated
   regression gate (`agent_checklist_gate.py`, `B2_loop_terminal`) guards against `ready_for_quote`
   ever being reintroduced into this set, implying a past bug where a quote-ready state
   incorrectly terminated the turn loop early.
4. **Domain 4 (MANDATORY, explicit operator requirement, not merely queued)**: full chain
   `proposal → persistence/materialization → approval/reject/clarification → mutation gateway →
   executor → side effect → ExecutionResult → idempotency → retry/recovery → Case projection →
   Daszek projection → final consumer`. See Domain 4 section above for the concrete open symbols.
5. **Domain 5 — RESOLVED THIS PASS at proportionate depth (EV-00128, EV-00129), new
   `workflow_id`: `RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE`.** Query-side: full traced
   9-stage pipeline (query understanding → retrieval → diversity → evidence/rerank → gating →
   LLM call → citation check → audience → final), legacy-vs-AssistantOrchestrator routing split,
   and — directly answering the explicit ask — a REAL, live-wired HTTP client
   (`integrations/node_b_read.py`) reading case/engagement context FROM gmail-agent, which
   refines (does not contradict) the earlier `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP` finding (that
   one is gmail-agent → RAG, confirmed missing; this one is RAG → gmail-agent, confirmed
   present). Ingest-side: real manifest-gated delta ingest with an explicit anti-data-loss
   fingerprint-safety default, write-locked concurrency safety, Chroma parent/child + BM25 index
   ownership, extension-based parser routing, and a CONFIRMED REAL, separate OCR fallback lane
   for hard/scanned PDFs. GraphRAG confirmed present as production code (internals not traced).
   "World model" does NOT map to anything in this repo — it's a gmail-agent-only term, stated
   explicitly rather than force-mapped. Genuinely still open (listed in the registry entry's
   `gaps`, not silently dropped): the actual caller populating Node-B context on `/chat` requests
   was not identified; live env-var configuration of the Node-B client not probed;
   `engine.py`'s 3000+-line internals (hybrid search, RRF fusion, domain/entity boosts) traced
   only at entrypoint depth; `document_intelligence`/`structured_extraction`/`entities`/
   `reflection`/`adaptive_retrieval` packages confirmed present but not individually opened.
6. **Domain 6 — RESOLVED THIS PASS (EV-00130, EV-00131), new `workflow_id`:
   `SLA-WATCHER-DECISION-ESCALATION`.** ~~reschedule/cancel~~ **CONFIRMED ABSENT** by exhaustive
   name search (zero definitions/callers anywhere), corroborating `execute_schedule_visit`'s
   already-known text-only behavior. ~~SLA~~ **CONFIRMED PRESENT AND WELL-BUILT**
   (`sla_watcher.py`, genuine pure-time-as-trigger via `hours_waiting` vs wall-clock, dedup-safe
   escalation) — CORRECTS the earlier "pure time-as-trigger appears MISSING" placeholder, but
   it is **MANUAL-CLI-ONLY-TRIGGERED**, no BackgroundTask/systemd wiring found despite the
   module's own docstring claim. ~~`PredictiveScheduler`~~ **CONFIRMED to be purely a Gmail-poll
   interval tuner**, not a stagnation/deadline mechanism of any kind. ~~`create_action_proposal`'s
   Calendar-triggered flow~~ **CONFIRMED `MISSING_PRODUCER`**: `build_calendar_event_action_proposal`
   has zero callers anywhere; the executor side is genuinely real and conditionally live (would
   call the real Calendar API if configured) but unreachable in practice since nothing creates
   the proposal it needs. Stagnation: no dedicated producer found beyond the already-known
   `STAGNATING` enum (`EV-00084`).
7. **Domain 7**: ~~`daszek_operational_feed_auto_push_enabled` live value~~ **RESOLVED (EV-00119,
   `True`)**; whether any non-HITL trigger also pushes the feed; whether `ReconcileResult.warnings`
   surfaces to Daszek/operator anywhere; Karta dnia; Business Pulse; health endpoint; frontend
   field usage vs backend fields actually sent; the gmail-agent-side ingest endpoint the v3 push
   posts to (not located). Also newly added this pass: the JSONL-vs-DB command-outbox liveness
   split (`EV-00116/117`) — whether the DB table is truly dead or dynamic-hook-fed remains open.
8. **Domain 8**: fast-kalk's class-chat.php/class-answer-extractor.php (LLM intake mechanism);
   kalk-top's individual engine internals (where exact device/materials/labor/margin values
   originate); top-instal-generator's legacy AJAX path + template/field mapping; whether
   cieplo-orchestrator's `FAILED_RETRYABLE` state has any real consumer; whether
   cieplo-orchestrator and gmail-agent's Gmail pollers share the same OAuth credentials/mailbox
   (real collision-risk question, not just a DB-separation question); `agent_runtime/tools/call_kalk_top.py`
   (D2's one unverified edge); rag-widget's local-vs-production API URL configuration; full
   WordPress compose plugin-mount cross-check.

After this queue: mechanical reverse audit (producer↔consumer, writer↔reader, tool
registration↔handler↔executor, route↔client, proposal type↔approver↔executor, table
writer↔reader, feed field backend↔frontend, feature flag declaration↔active branch) → full
route enumeration for `api_app.py`'s 53 routes + PHP repos → GitNexus adversarial check across
all repos → final synthesis documents.

## GitNexus adversarial spot-check (all 7 indexed repos now spot-checked at least once;
`rag-chat-asystent` remains without any graph tool, by tool limitation not choice)
`gitnexus context reconcile_signal` (structural graph traversal — `gitnexus query`'s BM25/vector
search is degraded, "FTS indexes missing", not usable this pass) independently confirmed
`SUBFLOW-GMAIL-SIGNAL-RECONCILE`'s known callers AND surfaced 2 concrete, previously
located-but-untraced recovery mechanisms: `signal_reconciler.replay_signal` and
`case_state_rebuilder.case_rebuild_from_journal` (both call `reconcile_signal` — these ARE the
real implementations behind the `signal-replay`/`signal-rebuild-case` CLI subcommands, Domain 1's
revisit item 1). Also surfaced `adjudication_executioner._strategy_reject_same_case` as a real
reject-path executor — Domain 4's mandatory closure only traced approve, not reject; this is the
concrete next entrypoint for that. EV-00114. `daszek` was indexed next (`gitnexus analyze`) and
`gitnexus context daszek_command_outbox_enqueue --repo daszek` surfaced the major
JSONL-vs-DB-table command-outbox liveness reversal (EV-00116/117, see `Correction log`) — the
single highest-value finding this spot-check method produced so far, precisely because it
contradicted an earlier positive claim rather than merely confirming one. `kalk-top`, `cieplo-orchestrator`, `top-instal-generator`, `fast-kalk`, and `rag-widget` are now
ALL indexed too (`gitnexus analyze`, all 5 succeeded; `top-instal-generator` and `rag-widget` each
logged one non-fatal "no Module scope found" warning for their single `.php` entrypoint file —
did not block indexing). Only `rag-chat-asystent` (no reliable index all session, `EV-`-noted
earlier) and `wp-bridges` remain unindexed.
**New tooling-methodology finding (EV-00118)**: spot-checking kalk-top's
`TopInstal_CalculateOffer_UseCase::execute` found `gitnexus context`'s incoming-callers list
contains ONLY regression-harness files, missing the real production caller
(`CalculateOfferController.php:95`, already confirmed by direct read in Domain 8/EV-00099) —
root cause is a variable-typed/DI-style PHP call (`$use_case->execute(...)`) that GitNexus's
static resolver cannot bind back to the class. This generalizes the same caution already applied
to the daszek command-outbox finding (EV-00116's WordPress-hook caveat): for PHP repos, an absent
GitNexus edge is evidence of "no static edge of the kind GitNexus resolves," not evidence of
non-use — direct code read remains authoritative and should be preferred over a GitNexus-only
absence-of-edge conclusion for PHP call sites going forward.
**Remaining 3 indexed-but-unchecked repos now spot-checked (EV-00133/134/135)**:
`cieplo-orchestrator` produced the highest-value finding of this batch — `gitnexus context
run_workflow_pipeline` reported `incoming: {}` (zero callers) for a function with REAL production
callers via `FastAPI BackgroundTasks.add_task(run_workflow_pipeline, ...)` and a
default-parameter callback assignment — a NEW, Python-side confirmation that GitNexus misses
function-passed-by-reference patterns, generalizing the PHP DI blind spot (`EV-00118`) to Python.
Also surfaced a previously-unflagged duplication: two sibling packages
(`topinstal_cieplo_worker`/`topinstal_cieplo_orchestrator`) each define their own
`run_workflow_pipeline`, not deeply investigated this pass. `top-instal-generator`'s check
CONFIRMED (no contradiction) that both the canonical REST and legacy AJAX document-generation
paths call the same use-case executor — GitNexus resolved both edges correctly here, suggesting
the PHP blind spot is specific to variable-typed/factory-returned dispatch, not PHP method calls
generally. `fast-kalk`'s check also confirmed (no contradiction) the widget-to-kalk-top
delegation via a correctly-resolved static-method call. **All 7 GitNexus-indexed repos have now
been spot-checked at least once against a specific registry claim.**

## Reverse-audit status
**Started and substantially productive this pass** (previously not started). Given the scope of
a fully exhaustive reverse audit across all 9 domains and ~500+ files across repos, this pass
executed a BOUNDED, genuinely evidenced subset of the mandated categories — populating `_raw/`
with real inventory content — rather than either skipping it entirely or fabricating a false
"done" claim.

**Categories completed, with real `_raw/` inventories** (`_raw/tool_registry_cross_reference.md`,
`_raw/signal_source_kind_cross_reference.md`):
- **tool names ↔ registry/handler/executor**: all 24 `HANDLERS` dict entries in
  `agent_runtime/tools/handlers.py` enumerated; 0 missing executors at the registration layer;
  1 `CONTRACT_DRIFT` found (`get_win_rate`, `EV-00136`) — the single highest-value finding of
  this entire reverse-audit pass, found ONLY because the cross-reference was actually performed
  rather than assumed clean.
- **signal source kinds ↔ registered handlers**: all 4 `SIGNAL_HANDLERS` entries enumerated
  against every `source_kind=` literal found repo-wide; 1 CONFIRMED mismatch
  (`"google_calendar"` vs `"calendar"`, `EV-00137`) that makes a real, substantial handler
  structurally unreachable; 2 apparent mismatches verified as non-issues by opening the actual
  producer code (`cieplo_orchestrated`, `node_b_generated`/`daszek_migration` — different
  fields/objects, not the same contract); 4 items left explicitly open, not resolved by
  assumption (see the `_raw/` file for the exact list).

**Categories NOT yet covered this pass, explicitly still open** (not silently dropped): event
types ↔ emitters/handlers; proposal types ↔ creator/approver/executor/result writer (partially
covered incidentally via Domain 4's mandatory closure and the 3-shape convergence finding,
`EV-00111`, but not run as its own dedicated cross-reference pass); fact keys ↔ producers/readers/
invalidation (partially covered via Domain 2's active-fact-selection work, `EV-00126/127`, same
caveat); table writes ↔ readers; statuses ↔ writers/consumers (partially covered via the
`get_win_rate` finding); projection fields ↔ frontend usage; env flags ↔ branch points; schedulers
↔ actually-called functions (fully covered for gmail-agent specifically via Domain 6,
`EV-00130`, not yet done for other repos); cross-repo payloads ↔ request validators/schemas
(partially covered via `CROSS_REPO_CONTRACTS.md`'s existing content, not re-run as a fresh pass).

**Conclusion**: the 2 categories that WERE run each produced at least one genuinely new, decisive,
previously-unflagged finding — direct evidence that this mechanical cross-reference method is
high-value and that the remaining uncovered categories likely contain comparable findings still
to be surfaced. Recommended as the highest-priority remaining work for a future continuation,
ahead of further narrative synthesis.

## Known open gaps in the inventory itself (not system gaps — gaps in this analysis)

**Reconciled 2026-07-30**: item 1 below was STALE — it contradicted `ENTRYPOINT_INVENTORY.md`
line 160 (`RESOLVED (EV-00112): api_app.py's 52 routes are now individually enumerated with line
numbers`), which had already closed this. Corrected here to state the precise, non-contradictory
current truth; do not use the blanket phrase "api_app.py/PHP route enumeration" going forward —
the two halves are in genuinely different states.

1. **CLOSED**: `api_app.py`'s HTTP routes are individually enumerated with line numbers in
   `ENTRYPOINT_INVENTORY.md`'s route table (61 table rows). Precise count: **52 routes declared
   directly on `app`** (`ENTRYPOINT_INVENTORY.md` line 14) **+ 1 dynamically-mounted route**
   (`/agent-chat`, mounted via `agent_runtime/authz.py:180` onto the app object at startup, not a
   direct `@app.get`/`@app.post` decorator) **= 53 routes total** — both the "52" and "53" figures
   used in earlier session narrative are correct simultaneously, referring to different subsets;
   they are not a contradiction once stated this precisely. Per-route classification (`TBD` unless
   independently confirmed live elsewhere) is a separate, still-open refinement, not a location
   gap.
2. **OPEN, specifically**: PHP/WordPress route-level enumeration is directory-level only (not
   individual paths+line numbers) for exactly these 5 repos: `daszek` (`includes/api-v2/`,
   `api-v3/`), `kalk-top` (`wp-adapter/rest/`), `top-instal-generator` (`wp-adapter/rest/`),
   `fast-kalk` (3 REST routes already individually traced in Domain 8, but not cross-checked
   against a full directory listing for completeness), `rag-widget` (HTTP client only, not a route
   provider — N/A, listed for completeness not as a gap). Concrete next step: `rg` for
   `register_rest_route\(` per repo, table with method/path/callback/line, matching
   `ENTRYPOINT_INVENTORY.md`'s existing `api_app.py` table format.
3. `rag-chat-asystent` has no reliable CBM index NOR a GitNexus index (confirmed this pass, see
   GitNexus canonical table above) — all discovery there must be `rg`/AST/direct-read, with no
   graph-tool fallback of any kind. This is the ONLY repo in scope with zero graph-tool coverage.

## Mechanical counters (reconciled 2026-07-30, recomputed from artifacts, not from narrative)

| Counter | Value | Source of truth |
|---|---|---|
| Git repositories in scope (own `.git`) | 8 | `gmail-agent`, `daszek`, `kalk-top`, `cieplo-orchestrator`, `top-instal-generator`, `fast-kalk`, `rag-widget`, `rag-chat-asystent` — verified this pass via `.git` presence check |
| Non-git harnesses in scope | 1 | `wp-bridges` — verified this pass, no own `.git`, subfolder of parent workspace tree |
| Workflows (`workflow_id` entries) | 17 (added `RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE` and `SLA-WATCHER-DECISION-ESCALATION` this pass) | `grep -c "^  - workflow_id:" WORKFLOW_REGISTRY.yaml` |
| Subflows | 4 | `SUBFLOW-CASE-INTELLIGENCE-TO-AGENT-HANDOFF`, `SUBFLOW-CASE-LINK-ROUTE-DECISION`, `SUBFLOW-SHARED-DOWNSTREAM-STAGES`, `SUBFLOW-GMAIL-SIGNAL-RECONCILE` |
| Evidence records | 137 | `WORKFLOW_EVIDENCE.jsonl`, IDs EV-00001..EV-00137, no gaps, no duplicates (mechanically recounted this pass) |
| `api_app.py` routes | 53 total (52 direct `@app.*` + 1 dynamically-mounted `/agent-chat`) | ALL individually enumerated with line numbers — **CLOSED**, see `ENTRYPOINT_INVENTORY.md` |
| PHP/WordPress routes individually enumerated | 3 (fast-kalk's REST routes, Domain 8) of an unknown larger total | **OPEN** for `daszek`, `kalk-top`, `top-instal-generator` (directory-level only) — see corrected gap item 2 above |
| GitNexus-indexed repos | 7 of 8 git repos | `gitnexus list` — all except `rag-chat-asystent`; `wp-bridges` correctly excluded from this denominator entirely (not a git repo) |
| `WORKFLOW_GAPS.md` items | 25 (P0:8, P1:11, P2:3, P3:3) — added this pass: `finalize_case` partial-write (`EV-00127`), calendar `MISSING_PRODUCER` (`EV-00131`), SLA manual-trigger-only (`EV-00130`), `get_win_rate` `CONTRACT_DRIFT` (`EV-00136`), and the `google_calendar`/`calendar` signal-handler naming mismatch (`EV-00137`) — full sequence renumbered 1-25 each time via a single script pass, verified mechanically | `grep -n "^[0-9]+\. "` |
| `DOMAIN-COMPLETENESS-REVISIT` queue entries | 8 (one per Domain 1-8; Domain 9 has no queue entry — closed with a decisive negative finding, its own 3 follow-up items are listed in its own section, not this queue) | this file |
| `DOMAIN-COMPLETENESS-REVISIT` sub-items fully resolved this session | 8 (Domain 1: retry disambiguation + dedup mechanics = 2; Domain 2: `fetch_case_by_message_id` + `FAST_LINK_CONFIDENCE` = 2; Domain 3: `_LOOP_TERMINAL_CODES` = 1; Domain 7: `auto_push_enabled` live value = 1; plus the daszek command-outbox major correction = 1, and the Domain 8/9 PROGRESS.md duplicate-block fix = 1, both process/correction items not domain-content items) | `Correction log` entries this session |
| `DOMAIN-COMPLETENESS-REVISIT` sub-items still open | Domain 1: 0; Domain 2: 4 (thread memory, active-fact selection, conflicts/gaps, `stage_config`); Domain 3: 2 (`OpenAIToolPlanner`/`build_planner`, `select_sub_agent`); Domain 4: 3 named (materialize-executor internals, reject path, 3rd proposal shape/`gmail_intake.py`); Domain 5: 1 large item (entire `rag-chat-asystent` pipeline, ~12 named sub-stages per operator's latest breakdown); Domain 6: ~6 named items; Domain 7: 7 named items (JSONL-vs-DB liveness question now added); Domain 8: 6 named items | this file, queue above |
| Final target artifacts present on disk | 12 of 12 (11 synthesis documents + this resumption ledger) | `WORKFLOW_REGISTRY.yaml`, `WORKFLOW_ATLAS.md`, `WORKFLOW_GAPS.md`, `WORKFLOW_EVIDENCE.jsonl`, `ENTRYPOINT_INVENTORY.md`, `STATE_OWNERSHIP_MATRIX.md`, `CROSS_REPO_CONTRACTS.md`, `ARCHITECTURAL_RULES_AUDIT.md`, `RUNTIME_BASELINE.md`, `RUNTIME_PROOF_PLAN.md`, `EXECUTIVE_SUMMARY.md`, `PROGRESS.md` — all present; content freshness against this reconciliation is a separate, still-open question (regeneration pass queued below) |
| `_raw/` inventory files for the mechanical reverse audit | 0 | directory exists, empty — reverse audit not yet started this pass |

**Overall target status**: `PARTIAL` remains the correct classification (not a stopping condition
— per operator instruction, continuing with tools). This reconciliation resolved the specific
narrative contradictions flagged by the operator; it did not itself close any new domain content.

## Final consistency gate (run mechanically at the end of this pass)

- **Every `workflow_id` present in `WORKFLOW_ATLAS.md`**: verified via script — all 17 present
  (4 were missing before this check: `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP`,
  `CALENDAR-TWO-WORLDS-OF-VISITS`, `DASZEK-COMMAND-OUTBOX-DRAIN`, `SLA-WATCHER-DECISION-ESCALATION`
  — fixed by adding a new "Other workflows" section to the atlas).
- **Every gap cites a `workflow_id` AND an `EV-#####`**: verified via script — 14 of 25 items were
  missing an explicit `workflow_id` tag before this check (mostly older items predating this
  session's citation convention) — fixed, all 25 now carry both.
- **Every cross-repo contract has both sides or an explicit gap**: `CROSS_REPO_CONTRACTS.md`'s
  verification legend (`BOTH`/`ONE-SIDED`/`PATTERN`) already makes this explicit per row; the
  daszek command-outbox row and the rag-chat-asystent-to-Node-B row were corrected/added this pass.
- **Every state owner has writers and readers**: `STATE_OWNERSHIP_MATRIX.md` reviewed — no row
  found with only one side blank without an explicit "not independently traced" note.
- **Every runtime claim has runtime evidence**: `RUNTIME_CONFIRMED` claims checked against actual
  `EV-#####` runtime-introspection records (`EV-00119` for the Daszek auto-push gate); no
  `RUNTIME_CONFIRMED` label found without a backing runtime-execution evidence record.
- **Counters identical across documents**: `PROGRESS.md`'s `Mechanical counters` table and
  `EXECUTIVE_SUMMARY.md`'s `§A` both show workflows=17, subflows=4, evidence=137, gaps=25
  (P0:8/P1:11/P2:3/P3:3) — verified matching.
- **No contradictory `COMPLETE`/`OPEN` statuses for the same item**: the two-part
  `FIRST_PASS_COMPLETE`/`COMPLETENESS_REVISIT_OPEN` model is used deliberately and consistently
  (Domains 1,2,6 fully resolved with no open half; Domains 4,5,7,8 explicitly carry both halves
  with named open items, not a bare contradiction).
- **No "gap closed" phrasing misused for a system defect**: checked and corrected one instance
  in `WORKFLOW_ATLAS.md`'s domain table (Domain 5's RAG gap) to read
  `CONFIRMED_OPEN — VERIFICATION_COMPLETE` explicitly rather than "closed," which could have been
  misread as the defect being fixed rather than the investigation being finished.
- **Evidence sequence integrity**: `WORKFLOW_EVIDENCE.jsonl` mechanically verified — EV-00001
  through EV-00137, zero gaps, zero duplicates.

## Correction log

**2026-07-30, mechanical reconciliation pass (no code re-analysis, registry/evidence structure
only)**: (1) Resolved 4 stale gap claims that later evidence had already closed — updated in
`WORKFLOW_REGISTRY.yaml` with explicit `RESOLVED_BY: EV-#####` markers rather than deleting the
history: `SIGNAL_HANDLERS` registration (EV-00028/29), gmail handler body (Domain 2 entries),
`resolve_case_id_for_agent`/`route_signal`/agent branch (EV-00042..57), AgentGraph turn loop
(`AGENT-GRAPH-TURN-LOOP` entry). (2) Backfilled missing `evidence_ids` array entries where a
record was cited in prose but not listed structurally: EV-00006/07 → `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP`;
EV-00013/14 → `HITL-PROPOSAL-APPROVAL-DUAL-PATH`; EV-00070/71 → `SUBFLOW-SHARED-DOWNSTREAM-STAGES`;
EV-00083/84 → `CALENDAR-TWO-WORLDS-OF-VISITS`. EV-00008..12 (learning-loop row-shape) added to
`HITL-PROPOSAL-APPROVAL-DUAL-PATH`'s `evidence_ids` with an explicit note that they are pending a
dedicated Domain 9 workflow entry, since none exists yet. (3) Fixed physical record order in
`WORKFLOW_EVIDENCE.jsonl` — EV-00083..89 had been inserted before EV-00080..82; reordered so file
order now matches ID order (ID was always the canonical sequence regardless, this is a
cleanliness fix, not a semantic one). (4) Fixed a real YAML defect this reconciliation caught:
`CALENDAR-TWO-WORLDS-OF-VISITS` was missing its own `runtime:` field, and a stray duplicate
`runtime:` key had been appended to the end of `DASZEK-FEED-PUSH-NO-RETRY` instead (two `runtime:`
keys in one YAML mapping — the second would have silently shadowed the first on parse). Moved the
Calendar-domain content back to its own entry. (5) Split Domain 7 into two separate workflow
entries per explicit instruction not to merge directions: `DASZEK-COMMAND-OUTBOX-DRAIN`
(Daszek→NodeB operator commands, real claim/lease/retry/dead-letter) and
`DASZEK-FEED-PUSH-NO-RETRY` (NodeB→Daszek feed projection, no retry) — previously only the second
existed as a formal registry entry. No source code was re-read for this pass; all changes are
structural/organizational within the artifacts themselves.

**2026-07-30, GitNexus adversarial audit follow-up**: continuing the GitNexus spot-check into
`daszek`, `gitnexus context daszek_command_outbox_enqueue --repo daszek` found exactly one caller
(`daszek_command_outbox_migrate_jsonl_once`), which itself has zero callers — cross-checked with
2 independent plain-text `rg` passes (all 3 methods agree). Follow-up direct-code read (not
GitNexus) then found the mechanism actually live is a SEPARATE, older JSONL-file-backed
`bridge_queue.jsonl` store, not the DB table originally described positively in the Domain 7 pass
as a durable-retry counterexample. Corrected: `WORKFLOW_REGISTRY.yaml`'s
`DASZEK-COMMAND-OUTBOX-DRAIN` entry (steps/state/retry rewritten, status flagged `CORRECTED`),
`WORKFLOW_ATLAS.md`'s cross-cutting pattern #1 (removed the outbox as a durable-retry exception —
it now strengthens rather than contradicts the "best-effort, no retry is the norm" pattern),
`WORKFLOW_GAPS.md` (P2 item 14 replaced with a new P1 item describing the orphaned-outbox
finding; renumbering of P2/P3 items NOT needed since the replacement kept the same slot),
`STATE_OWNERSHIP_MATRIX.md` (`wp_daszek_command_outbox` row corrected, new `bridge_queue.jsonl`
row added). New evidence: `EV-00116`, `EV-00117`. Explicitly NOT claimed as confirmed-dead code —
WordPress dynamic hook dispatch could not be ruled out by either static method used.
Separately, while reviewing this file for the update above, found and fixed a genuine
duplicate/contradictory-block defect this session's own process rules forbid: stale `Status: not
started` stub sections for Domain 8 and Domain 9 (leftover from before those domains were
actually done) were sitting directly above their real, completed canonical blocks. Removed both
stubs — one canonical block per domain restored for Domains 8 and 9, matching the rule already
applied to Domains 1-6 in the correction below.

**2026-07-30, mid-session**: operator audit found (a) domains 3/4/5 had been marked `CLOSED`
before their mandatory brief.md scope was covered, (b) stale duplicate/contradictory domain
sections had accumulated in this file (e.g. Domain 3 appearing as both `CLOSED` and
`not started`), risking a future session reading the wrong one and either re-doing finished work
or wrongly treating covered ground as untouched. This file was rewritten to: replace `CLOSED`
with accurate two-part `<DONE> — <OPEN>` statuses for domains 1-6, remove all duplicate/stale
domain sections (one canonical entry per domain now), and add the `DOMAIN-COMPLETENESS-REVISIT`
queue above with concrete named entrypoints per domain, run after Domains 6-9's first pass
rather than immediately. No evidence already gathered was discarded or re-verified unnecessarily
— `WORKFLOW_EVIDENCE.jsonl` and `WORKFLOW_REGISTRY.yaml` are unaffected by this correction, only
this ledger's status labels and structure changed.

**2026-07-30, operator-directed reconciliation pass (most recent; no code re-analysis, narrative/
counter consistency only)**: operator flagged 5 concrete contradictions in the prior turn's
chat-message summary (not inside the artifacts' own canonical sections, which were individually
correct but summarized ambiguously). (1) Route enumeration stated as both closed and open —
resolved: `api_app.py` (53 routes: 52 direct + 1 dynamically-mounted `/agent-chat`) is genuinely
closed (`ENTRYPOINT_INVENTORY.md` already said so at line 160; the prior chat summary wrongly
implied otherwise by using the blanket phrase "api_app.py/PHP route enumeration"), PHP routes are
genuinely open for `daszek`/`kalk-top`/`top-instal-generator` specifically — corrected `Known open
gaps` item 1/2 above to state this precisely and permanently retire the blanket phrase. (2)
GitNexus indexing narrated sequentially across the session ("8 remaining" early, "only
rag-chat-asystent remaining" later) was not internally contradictory data, just ambiguous
restatement — replaced with one canonical table (Tooling status, above) as the single source of
truth going forward. (3) "5 newly indexed" undercounted an actual list of 6 repos in the same
prior message — a prose arithmetic error, not an artifact defect; the table above lists all 6
correctly (`daszek`, `kalk-top`, `cieplo-orchestrator`, `top-instal-generator`, `fast-kalk`,
`rag-widget`). (4) `wp-bridges` was being implicitly counted toward "repos remaining to
GitNexus-index" in chat narration — verified this pass via `.git` presence check (`git
rev-parse --is-inside-work-tree` + direct `.git` dir check across all 9 candidate folders) that it
has no own git repo, unlike all 8 real service repos — confirmed non-git harness, matches its own
`AGENTS.md` self-description, permanently excluded from the GitNexus-repo count and denominator.
(5) Domain 8's "A-G done" vs "remaining items" was already a real two-part status in this file but
not labeled with the operator's requested `FIRST_PASS_COMPLETE`/`COMPLETENESS_REVISIT_OPEN`
vocabulary — relabeled explicitly. Added a full `Mechanical counters` table above, recomputed
directly from the artifacts via `grep`/`wc`/file listing, not from memory or narrative. No
`WORKFLOW_REGISTRY.yaml` or `WORKFLOW_EVIDENCE.jsonl` content was altered in this reconciliation
beyond the earlier same-session evidence additions (EV-00116..EV-00124) already in place before
this correction pass began; one stray blank line at `WORKFLOW_EVIDENCE.jsonl` line 123 was removed
as a pure hygiene fix (no record content changed).
