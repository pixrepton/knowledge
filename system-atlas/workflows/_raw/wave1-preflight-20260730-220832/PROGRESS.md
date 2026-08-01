# PROGRESS — AI-OS-WORKFLOW-RECONSTRUCTION-AND-REGISTRY-01

**Canonical resumption ledger.** This file contains ONLY current state. Every counter, status,
and open-item list below is the single authoritative version — there are no competing/stale
copies anywhere in this file. Historical checkpoints, superseded narrative, and the full
correction log live in `PROGRESS_HISTORY.md` (evidence trail preserved, zero authority over
current status).

**Target status: `PARTIAL`** — not a stopping condition. No blocker, required production
mutation, secret exposure, or unresolvable operator decision exists. Work continues per §4.

**2026-07-30 20:35:08 +02:00 — `CODEX_HANDOFF_VALIDATED`.** Recomputed from current disk state,
not from narrative: `knowledge` repo = `master` @ `597b1091a296930ed32afb379ec19b8ab425d4fa`
with `system-atlas/` still untracked and pre-existing modifications in
`ARCHITECTURE_DECISIONS.md`, `TOOLING_POLICY.md`, `memory/ACTIVE_WORKSPACE.md`,
`memory/BACKLOG.md`, `memory/LAST_SESSION.md`; workflow artifacts present `12/12`; evidence
records `182` (`EV-00001`..`EV-00182`, no gaps, no duplicates, `0` bad JSONL); evidence rows
carrying normalized `evidence_type`/`confidence` = `45/182`; evidence rows carrying `workflow_id`
= `0/182`; registry contains `17` workflows + `4` subflows; gaps = `42` (`P0:11`, `P1:22`,
`P2:6`, `P3:3`); reverse-audit state on disk = `8/12 COMPLETE`, `0 PARTIAL`, `4 NOT_STARTED`
(`_raw/` has 8 inventories, including `table_write_reader_cross_reference.md` and
`status_value_writer_consumer_cross_reference.md`). `EV-00181` and `EV-00182` exist, are cited in
`WORKFLOW_REGISTRY.yaml`, and the resulting new status-contract issues are filed as
`WORKFLOW_GAPS.md` items `41` and `42`. First open
atomic step is therefore `§6 category 7: table write ↔ table reader`. Relevant SHAs for closeout:
**Superseding note (2026-07-30 20:35:08 +02:00): the current first open atomic step is `§6 category 9: projection field ↔ backend producer ↔ frontend usage`; the category-7 wording above is historical text left in place only because of encoding-fragile line wrapping in this file.**
`gmail-agent=468d37ee6553b39bf6009939e9c87c13f3c183c7`,
`daszek=672769d9496359dcfb7f2427d555ad34a2171b1a`,
`kalk-top=9d56055be7f293ad17ffb624abc178617f46f5be`,
`cieplo-orchestrator=e68f05386722b4034ca36bd39d169eba759f44e6`,
`top-instal-generator=7e5279551b3919b7ab84547227b3355f45c44bf4`,
`fast-kalk=06a470da94db6069f42c0d20a860815212e80f00`,
`rag-widget=c64707aac69bb4a6cc68e1f097aa8415a3b976a6`,
`rag-chat-asystent=34e9ae2e597076756aa71051382fe18d058776a7`.

---

## 1. How a new session resumes (read this section first)

1. Read §2 (counters) and §3 (domain status) — that is the complete current picture.
2. Pick the first unchecked item in §4 (ordered work queue).
3. Do NOT re-derive anything marked `RESOLVED` in §3 — the evidence stands, cited by `EV-#####`.
4. Do NOT read `PROGRESS_HISTORY.md` for status — it is historical only.
5. Tooling constraints and known blind spots: §5.

---

## 2. Mechanical counters (recomputed from artifacts, never from narrative)

| Counter | Value | Verification command |
|---|---|---|
| Product git repos in scope | 8 | `.git` presence check per directory |
| Non-git harnesses (excluded from repo counts) | 1 (`wp-bridges`) | verified: no own `.git` |
| Workflows (`workflow_id` entries) | 17 | `grep -c "^  - workflow_id:" WORKFLOW_REGISTRY.yaml` |
| Subflows | 4 | `grep -c "^  SUBFLOW-" WORKFLOW_REGISTRY.yaml` |
| Evidence records | 180 (`EV-00001`..`EV-00180`, no gaps, no duplicates) | script-verified |
| Evidence records NOT structurally attached to a workflow | 61 (18 pre-existing + EV-00138..180) | see §4 item N1 |
| `WORKFLOW_GAPS.md` items | 40 (P0:11, P1:22, P2:4, P3:3) | `grep -n "^[0-9]\+\. "` |
| `api_app.py` HTTP routes | 52 direct `@app.*` + 1 dynamically-mounted (`/agent-chat`) = 53 registration sites; unique `(method,path)` pairs NOT yet disambiguated | `ENTRYPOINT_INVENTORY.md` |
| PHP/WordPress routes individually enumerated | 89 total: daszek 82 (v1:7/v2:29/v3:46), kalk-top 3, top-instal-generator 1 REST + 2 admin-ajax, fast-kalk 3 — all repos, no hidden routes found | `EV-00174` |
| GitNexus-indexed repos | 7 of 8 (all except `rag-chat-asystent`) | `gitnexus list` |
| Reverse-audit categories: complete / partial / not started (of 12) | 7 / 0 / 5 | `_raw/` contains 7 inventories (tool registry; signal source kinds; planner tool chain; event type ↔ emitter ↔ handler; proposal type ↔ creator ↔ approver ↔ executor ↔ result writer; fact key ↔ producer ↔ reader ↔ supersession/invalidation; table write ↔ table reader) |
| Evidence records citing a TEST file | 1 (EV-00139, `evidence_type:TEST`, executed live: 7 passed) | see §4 item N3 |
| Final target artifacts present | 12 of 12 | directory listing |
| Executable consistency gate | NOT YET WRITTEN | see §4 item N7 |
| Evidence records already carrying the normalized schema (`evidence_type`/`confidence`) | 43 (EV-00138..180) of 180 | see §4 item N1 |
| Reverse-audit category "planner-schema↔handler↔executor": argument-signature conformance | CLOSED — 24/24 handlers checked, 2 confirmed defects (`EV-00177`) | see Domain 3 status |

---

## 3. Domain status — exactly one current entry per domain

Status vocabulary: `RESOLVED` = all mandatory brief scope covered AND completeness check run.
`FIRST_PASS_COMPLETE + REVISIT_OPEN` = primary trace done, named sub-items still open.
No domain may be labeled closed while any mandatory brief-required scope is deferred.

### Domain 1 — Gmail i signals — **RESOLVED**
Workflows: `GMAIL-SIGNAL-WORKER-LOOP` (+ `SUBFLOW-GMAIL-SIGNAL-RECONCILE`)
Evidence: EV-00015, EV-00018..EV-00030, EV-00114, EV-00121, EV-00122
All mandatory scope covered: production call chain pinned end-to-end; `SIGNAL_HANDLERS` fully
enumerated (4 handlers); journal tables confirmed distinct; **dedup/idempotency mechanics
resolved** (`EV-00121`: two-layer, both with real DB UNIQUE indexes; `content_hash` is
informational-only, not part of dedup); **poll-level vs item-level retry disambiguated**
(`EV-00122`: `_poll_with_retry` covers only the list-API call; per-message stages get exactly one
attempt, no requeue); replay/rebuild CLI recovery paths located (`EV-00114`).
Open: none for this domain's own scope. (Cross-cutting: reverse-audit category 12,
recovery/replay entrypoint ↔ original workflow, still pending — see §4.)

### Domain 2 — Case i memory — **RESOLVED**
Workflows: `GMAIL-RECONCILE-MODE-DISPATCH`, `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`
(+ `SUBFLOW-CASE-LINK-ROUTE-DECISION`, `SUBFLOW-CASE-INTELLIGENCE-TO-AGENT-HANDOFF`)
Evidence: EV-00039..EV-00057, EV-00123..EV-00127
All mandatory scope covered: case-linking/routing decision tree; fail-closed identity/engagement
resolution; `FAST_LINK_CONFIDENCE`=0.92 and its true (narrow) effect (`EV-00123`);
`fetch_case_by_message_id` reachability split by call site (`EV-00124`); **thread memory** full
producer/storage/update-rules/readers/lazy-migration/replay analysis (`EV-00125`); **active-fact
selection + conflicts/gaps** — two distinct mechanisms, mutation-time `case_coherence` gate and
query-time `split_conflicting_facts` (`EV-00126`, `EV-00127`); **`CaseContextPack`/`stage_config`
assembly** with a NEW confirmed partial-write gap in `finalize_case` (`EV-00127`).
Open: none for this domain's own scope.

### Domain 3 — Understanding, decisions, policy, planner, agent runtime — **RESOLVED**
Workflows: `AGENT-GRAPH-EXECUTE-RUN`, `AGENT-GRAPH-TURN-LOOP` (+ `SUBFLOW-SHARED-DOWNSTREAM-STAGES`)
Evidence: EV-00058..EV-00071, EV-00120, EV-00138..EV-00141, EV-00177
Done: `execute_agent_run` full structure (constitution routing, checkpoint/resume, event-spine,
CAS save with real `AgentConcurrencyError`); turn loop with its 3 safety nets and the
`_BRAIN1_OWNED_SNAPSHOT_FIELDS` write guard; brief.md §6.2 resolved `CONFIRMED_OPEN`;
DecisionCandidate/PolicyDecision/ActionProposalV2 traced; `dry_run_only` `False` live;
`_LOOP_TERMINAL_CODES` enumerated with its regression gate (`EV-00120`).
**Closed this pass**: `build_planner`/`OpenAIToolPlanner` internals — multi-endpoint failover with
per-provider circuit breakers, hard timeouts, exponential backoff, hallucination NEVER failed over
(explicit "propose_mutation fallback disabled by security policy"), and a synthesized
`report_gaps_and_stop` when the model returns no tool_calls with `finish_reason=='stop'`
(`EV-00138`). **Full tool-chain cross-reference** schema↔allowlist↔handler↔executor with 3
independent enforcement layers, 1 documented intentional exception, and a 7-test regression
contract **executed live (7 passed)** — the first TEST evidence in this reconstruction
(`EV-00139`, `_raw/planner_tool_chain_cross_reference.md`). `select_sub_agent` traced, with a real
defect found: called with `tool_name=""` at the only offer-restricting call site, making 2 of 4
specialist scopes unreachable (`EV-00140`). **Policy-steering question decisively answered**:
policy steers coarsely by restricting the offer set (hard, 3-layer), but the semantic policy
envelope is observe-only — divergence is measured and never acted on (`EV-00141`).
**Argument-signature conformance CLOSED** (`EV-00177`): all 24 `HANDLERS` entries checked against
their `tool_schemas.py` schemas. 22 of 23 schema'd handlers show exact conformance. 2 confirmed
defects, both filed as new gaps: (1) `request_human_handoff` has NO schema entry at all —
completely unreachable by the planner, and exhaustive grep found no other invocation path either,
genuinely dead code (`WORKFLOW_GAPS.md` item 30). (2) `call_kalk_top_quote`'s schema advertises 3
parameters (`heated_area_m2`/`location`/`building_type`) that the handler — signature
`(_plan: ToolCallPlan, ...)`, explicitly unused — completely ignores, building its request from
`ctx.snapshot` instead; any LLM-supplied value for these fields has zero effect
(`WORKFLOW_GAPS.md` item 31). This closes reverse-audit category 4
(planner-schema↔handler↔executor) from partial to complete. Domain 3 status is now `RESOLVED`.

### Domain 4 — HITL i execution — **PRIMARY_APPROVE_REJECT_EXECUTION_PATHS_RESOLVED — CLARIFICATION/NO-EXECUTOR_PATH_OPEN**
Workflows: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`
Evidence: EV-00072..EV-00076, EV-00110, EV-00111, EV-00115, EV-00142..EV-00152, EV-00157, EV-00158
**Status precisely two-part per operator instruction**: the approve/reject/execution paths ARE
fully resolved (including the two mandatory residual questions below); the label is NOT
`RESOLVED` outright because one of those two questions resolved to a **confirmed missing/dead
mechanism** (clarification answer channel), which is itself the domain's most important finding,
not a loose end to hide behind a clean status.
Done: proposal → persistence (`pending` gate, fail-closed on re-approve) → APPROVE → mutation
gateway (CAS) → executor → snapshot save → Daszek projection push; both approval routes confirmed
to converge on one executor (`EV-00111`); `_stable_bridge_key` idempotency; real CAS retry with
backoff in `approve_materialize_proposal`. `execute_materialize_proposal` internals — 5
proposal-type branches, Python-only ("never called from LLM"), with an email-level dedup layer
inside `create_case` (`EV-00142`). Idempotency — REAL but scoped to `composite_plan` ONLY, while
the docstring promises it unconditionally for all 5 types (`EV-00143`). **The crash-window
question is ANSWERED AND CONFIRMED**: the side effect runs BEFORE result persistence, with up to
~1.75s of deliberate backoff sleep in between, and three non-crash error paths already return
after the effect is durable — no durable effect receipt exists (`EV-00144`). Task reject traced,
distinct from materialize reject — fabricates a synthetic `DIVERGENT_ACTION` learning-loop entry
(`EV-00145`). `case_write_gateway` corrected (`EV-00146`, see §5/ARCHITECTURAL_RULES_AUDIT.md).
`ExecutionResult` durably persisted on all 3 exit paths of the 3rd proposal shape — a well-built
pattern absent from the materialize path (`EV-00149`). Gmail-send HITL has a REAL claim-based
restart-recovery state machine (`EV-00150`) — restart-recovery quality is confirmed NOT uniform
across the 3 proposal shapes. Materialize-proposal reject CONFIRMED ABSENT by exhaustive route
search (`EV-00151`). `gmail_intake.py`'s 3 `execution_runtime` call sites — approve/reject/execute
are ALSO reachable live via the bridge-queue-drain path (not CLI-only after all, `EV-00157`),
alongside the CLI (`EV-00152`).

**Mandatory residual question 1 — RESOLVED, TWO-PHASE DESIGN CONFIRMED (`EV-00157`)**: for
non-`prop_` action_ids, `AgentMcpService.approve_hitl_action` clears `hitl_gate` and sets
`ready_for_quote` but calls no executor directly. The actual executor is
`execute_hitl_send_from_bridge_row` (`EV-00150`'s restart-safe state machine), triggered via a
**separate** Daszek route (`daszek_api_v2_agent_hitl_send`) that enqueues a `bridge_queue` row
(`domain=agent_hitl`), drained asynchronously by the worker loop. That executor explicitly
requires `hitl_gate.required==False` as a precondition — the two phases (approve, then send) are
deliberately sequenced by design, not a missing executor or missing consumer. Confirmed for the
`draft_reply`/Gmail-send action type specifically; not independently verified for other
action_ids (a genuinely minor residual, does not change this question's resolution).

**Mandatory residual question 2 — RESOLVED, CONFIRMED MISSING AND WORSE THAN ABSENT (`EV-00158`,
new P0 gap)**: Daszek's UI DOES send a free-text `draft_pl`/`operator_draft_pl` field on both the
approve call and the bridge-queue send row — the only candidate answer-content channel found
anywhere. It is a **dead field**: neither `engagement_hitl_approve`/`approve_hitl_action` nor
`execute_hitl_send_from_bridge_row` ever reads it. The actual email body sent always comes from
`action.payload_pl` (set by the agent's own prior turn), never from any operator-submitted field.
An operator's draft edit OR a clarification answer submitted through this channel is silently
discarded end to end — this is not "clarification can be approved without transmitting
information," it is "the transmission field exists and is unconditionally ignored." Orphaned
clarification / restart behavior is governed by the same general CAS/re-approve snapshot
semantics already traced (no special-cased orphan handling found).

### Domain 5 — RAG i documents — **RESOLVED**
Workflows: `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP`, `RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE`
Evidence: EV-00077..EV-00079, EV-00128, EV-00129, EV-00153, EV-00154, EV-00159, EV-00160,
EV-00161, EV-00162
Done: brief.md §6.6 `CONFIRMED_OPEN — VERIFICATION_COMPLETE` (the gap is verified, NOT fixed);
`search_rag_knowledge` confirmed as the correct sibling of `query_anything`'s broken branch;
query-side 9-stage pipeline traced with its legacy-vs-orchestrator routing split (`EV-00128`);
ingest-side manifest-gated delta ingest, fingerprint safety, write lock, Chroma parent/child +
BM25 ownership, parser router, real OCR fallback lane (`EV-00129`); RRF fusion (correct, standard
implementation) and FlashRank reranker with an honest no-op fallback traced (`EV-00154`);
Node-B caller of the RAG pipeline confirmed (`EV-00153`); `hybrid_search`/`_single_hybrid_search`
full trace — adaptive retrieval, PRF, gated multi-query, query rewriting, HyDE, BM25/vector
candidate generation with client-side metadata filtering, RRF fusion, hard-token rescue
(`EV-00159`); `compute_gating` confidence classifier (never mixes rerank 0-1 scores with RRF
ranking scores) and `apply_diversity_policy`, plus the more granular V2 stage docstring
"retrieval -> rerank -> diversity -> dedupe -> evidence -> generation -> validation" (`EV-00160`);
`entities/`/`reflection/`/`adaptive_retrieval/` all confirmed wired with real callers; GraphRAG
split confirmed — retrieval side (`graphrag/__init__.py` re-exporting `application/services/`)
is LIVE via `agentic_graph.py`/`domain/pipeline.py`/`services/chat_service.py`, but ingest-time
`ingest/community_summaries.py:build_community_summary` has ZERO callers anywhere — confirmed
ORPHANED, not merely unverified (`EV-00161`); ingest partial-failure isolation (per-file
try/except, ERROR-logged, continues to next file) and the hard-PDF fallback cascade
(parser → Docling → Unstructured → pdfplumber-text, picks longest successful extraction) traced
as a genuine positive finding; ownership closed — Chroma parent/child + BM25 (chunks/embeddings),
on-disk `KNOWLEDGE_BASE_DIR` + in-memory `document_index` (documents), manifest/chunk_manifest
JSON (delta tracking) (`EV-00162`).
Residual (non-blocking, minor): `_apply_domain_boosts`/`_apply_entity_boosts` internals not
traced field-by-field; `document_intelligence`/`structured_extraction` internals confirmed wired
via real callers but not traced at full field-level depth. Neither rises to gap-worthy severity;
both noted here for completeness rather than left silently unmentioned.
New gap filed from this domain: GraphRAG ingest-time community-summary enrichment is dead code
(zero callers) — see `WORKFLOW_GAPS.md` new item below.
**Node-B context integration CLOSED, with a correction**: the mechanism is real and live-wired
CODE (`EV-00128`), but `EV-00153` found NO confirmed live CALLER anywhere — the earlier
presumption that Daszek's `proxy-agent-chat.php` populates `case_context` was WRONG (that proxy
targets gmail-agent's own `/agent-chat`, a different feature entirely); rag-widget's confirmed
`/chat` client does not send these fields either. This is a caller-dormant capability, same shape
as several other findings this session.
**OPEN (mandatory, narrower now)**: diversity/gating/grounding/citations stage internals; parent-child
expansion; query rewriting/HyDE if active; structured extraction; document intelligence; entities;
reflection; adaptive retrieval; GraphRAG internals; ingest partial-failure/recovery; ownership of
documents/chunks/embeddings/indexes. → §4 item D5 (narrowed; RRF/rerank and the Node-B-caller
question are now closed, not open).
Tooling constraint: `rg`/AST/direct read ONLY — no GitNexus, no reliable CBM for this repo.

### Domain 6 — Calendar i czas — **RESOLVED**
Workflows: `CALENDAR-TWO-WORLDS-OF-VISITS`, `SLA-WATCHER-DECISION-ESCALATION`
Evidence: EV-00016/17, EV-00031..EV-00038, EV-00044..EV-00046, EV-00080..EV-00084, EV-00130,
EV-00131, EV-00137
All mandatory scope covered: brief.md §5.4/§6.5 decisively closed; **SLA mechanism found real**
but manual-CLI-triggered only, contradicting its own docstring (`EV-00130`); `PredictiveScheduler`
confirmed to be a poll-interval tuner, NOT a stagnation/deadline trigger (`EV-00130`);
**Calendar-triggered `create_action_proposal` confirmed `MISSING_PRODUCER`** (`EV-00131`);
**reschedule/cancel confirmed ABSENT** by exhaustive name search, not merely unfound (`EV-00131`);
**NEW: `google_calendar` vs `calendar` signal-handler naming mismatch** makes a registered
handler structurally unreachable (`EV-00137`).
Open: none for this domain's own scope.

### Domain 7 — Daszek — **RESOLVED**
Workflows: `DASZEK-FEED-PUSH-NO-RETRY`, `DASZEK-COMMAND-OUTBOX-DRAIN`
Evidence: EV-00085..EV-00091, EV-00116, EV-00117, EV-00119, EV-00155, EV-00156, EV-00163,
EV-00164, EV-00165, EV-00166
Done: push-mechanism lineage across 3 generations, only v3 live; brief.md §6.7 `CONFIRMED_OPEN`
on the correct live path; **auto-push gate runtime-confirmed `True`** on the production worker
(`EV-00119`); **command-outbox transport CORRECTED** — the JSONL `bridge_queue.jsonl` store is
the live mechanism, the DB-backed `wp_daszek_command_outbox` has no confirmed live producer
(`EV-00116`, `EV-00117`). **DB-outbox dynamic-hook question CLOSED** (`EV-00155`): exhaustive
`add_action`/`do_action`/`register_activation_hook`/`wp_schedule_event` search found exactly 3
real cron registrations (backup, `bridge_queue_gc` — confirming the JSONL GC has a genuine live
cron trigger, and `mail_ingest`), none referencing the DB outbox — upgraded to
`DORMANT_PATH, hook-search-exhausted`. **`ReconcileResult.warnings` search COMPLETE and CLOSED**
(`EV-00163`): all remaining 12 candidate files confirmed false positives (each references an
unrelated `.warnings` field on a different result type — `AgentRunResult`, `CoherenceResult`,
mailbox-memory ingest/finalize, `Neo4jPilotResult`, `PolicyReport`, LLM warnings tray); the one
real `ReconcileResult.warnings` call site (`materialize_bridge.py`'s
`reconcile_linked_after_materialize`) was traced end-to-end through `api_app.py`'s
materialize-approve route → `daszek/includes/api-v3-handlers.php` (forwarded verbatim) →
`daszek/public/app.js` (`approveProposalViaApi`/`decideActionProposal`, which never reads
`response.reconcile` or its `.warnings`) — classified **`MISSING_CONSUMER`**: the data is
computed and shipped all the way to the browser, and silently discarded there. New P1 gap filed
(`WORKFLOW_GAPS.md` item 27). **Karta dnia, Business Pulse, health endpoints, v3 ingest endpoint
all traced and confirmed LIVE** (`EV-00164`): Business Pulse's 9 agent-callable tools genuinely
read-only-aggregate existing data and are honest about untracked values (`None` +
`value_tracking: not_implemented`, not fabricated zeros) — but `get_revenue_forecast` directly
inherits `get_win_rate`'s `CONTRACT_DRIFT` bug (gap item 8 updated); Karta dnia has 2 independent
live paths (gmail-agent's `compose_day_sections` feeding the engagement-feed push, and Daszek's
own `daszek_v2_build_day_read_model` reading back ingested feed data at `GET /daszek/v2/day`,
plus a separate simpler `/agent-chat?brief=true` auto-briefing text consumed by
`public/app.js`); health endpoints (`/system/health/status`, `/system/agent-health`) confirmed
live and rendered in Daszek's "System" dashboard view; the v3 ingest endpoint is
`POST daszek/v2/ingest` (`daszek_check_auth` + CSRF gated). **Non-HITL feed-push triggers
confirmed** (`EV-00166`): `maybe_push_operational_feed_after_reconcile` fires from ordinary
Gmail signal-reconcile paths (`gmail_intake_process.py`, `signal_worker.py`) and
`_maybe_push_feed_after_bridge_drain` fires after every bridge-queue drain tick — both distinct
from and in addition to the HITL-specific push. **`bridge_queue` retry/dead-letter semantics
CLOSED** (`EV-00165`): confirmed NONE exist — a failed row is marked `bridge_status='failed'`
once, never retried, and is treated identically to a success by every reader (`pending`
exclusion, the one operator-facing summary dashboard) — the failure is not just un-retried, it
is completely invisible to the operator. New P1 gap filed (`WORKFLOW_GAPS.md` item 28).
Residual (non-blocking, minor): exhaustive field-by-field backend↔frontend projection mapping
was not done beyond the views directly traced above (System, Day, materialize-approve);
sufficient live-path evidence exists for all mandatorily-named items, so this is noted rather
than left silently unmentioned, matching Domain 5's residual-disclosure pattern.

### Domain 8 — Integracje ofertowe i WordPress — **RESOLVED**
Workflows: `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`, `KALK-TOP-CALCULATE-OFFER-PIPELINE`,
`TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`, `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`
Evidence: EV-00092..EV-00105, EV-00113, EV-00132, EV-00133, EV-00134, EV-00135, EV-00167..EV-00175
Done: cross-repo offer pipeline traced (A–D); D1/D2/D3 adjudicated; ownership of
CalcRequestDTO/OfferDTO/documents/pipeline-status established; **margin and sale-outcome
confirmed `MISSING_PRODUCER` cross-system** (`EV-00132`); GitNexus spot-checks on all Domain 8
repos (`EV-00134`, `EV-00135`). **`class-chat.php`/`class-answer-extractor.php` CLOSED**
(`EV-00167`): `Topinstal_Lead_Widget_Chat::handle` is the `POST /chat` route callback for
fast-kalk's lead widget — a self-contained step-B conversational assistant (DeepSeek → Anthropic
→ rule-based fallback, in that order), entirely independent of gmail-agent/kalk-top;
`Topinstal_Lead_Widget_Answer_Extractor::extract_from_text` is a pure regex/keyword heuristic
(no AI call) for multi-field extraction from one free-text answer. Confirmed a genuine guardrail:
`scrub_ai_insulation_guess` strips AI-inferred insulation/hydraulics fields before merge — only a
direct user answer may set them. Confirmed the plugin's entire REST surface is exactly 3 routes:
`/chat`, `/calculate`, `/register` — no 4th hidden route. **kalk-top pricing engine internals
CLOSED** (`EV-00168`): every line item's `unitPriceNet` traced to a static, versioned JSON file
(`core/infrastructure/master-data/equipment-catalog.json`) via `MasterDataRepositoryWp` →
`PriceBookRepositoryWp` → injected `$price_book` — not a WP options table, not an admin-editable
DB row. DECISIVE: the pricing engine's item schema structurally has NO cost-basis/margin field at
all — this is WHY margin is `MISSING_PRODUCER`, not merely unwired telemetry. Labor is likewise
never decomposed (a single flat `installation_net` catalog line, never hours × rate).
**`FAILED_RETRYABLE` consumer CLOSED** (`EV-00169`): a real, live `POST /api/workflows/{id}/retry`
endpoint exists (manual-trigger-only, no automatic scheduler). **Cieplo's two sibling
`run_workflow_pipeline` implementations RESOLVED** (`EV-00169`, closing the prior
UNRESOLVED-escalated item): `topinstal_cieplo_worker` is `LIVE_PATH` (packaged CLI + documented
uvicorn target); `topinstal_cieplo_orchestrator` is `DEAD_PATH` (zero external importers, and its
own `main.py` doesn't even use its own router).
**Shared Gmail credential/mailbox question CONFIRMED** (`EV-00170`): gmail-agent and
cieplo-orchestrator's pollers share the exact same live mailbox account
(`biuro.topinstal@gmail.com`, confirmed via an explicit docker-compose inline comment), narrowed
by cieplo's own content-scoped query and a dedicated `cieplo_orchestrator_hook.py` integration —
proving deliberate design, not an accidental collision. Narrow residual: whether gmail-agent's own
raw poll loop independently double-ingests the same email was not conclusively traced.
`call_kalk_top.py` re-confirmed as a thin re-export (downstream handler already covered by
`EV-00113`). **Generator legacy AJAX path/field mapping/converter contract CLOSED** (`EV-00171`):
2 admin-ajax actions (`simple_generate` self-logged deprecated, `topinstal_generate_offer_document`)
both converge on the same `TopInstal_GenerateOfferDocument_UseCase` as the canonical REST route —
convergent adapters, not competing implementations; converter contract is an honest
degraded-fallback (DOCX always rendered first, PDF attempted only if requested, any conversion
failure returns the real DOCX with an explicit warning, never a broken/silent PDF).
**rag-widget local-vs-prod URL mechanism CLOSED** (`EV-00172`): the widget IS mounted into
`docker-compose.daszek-local.yml`, but no `HVAC_RAG_API_URL` override exists in the compose file
or `.env.daszek-local`; the plugin also supports a wp-admin-settable option as a fallback, so
whether local testing actually reaches the local backend depends on manual admin-UI state outside
any inspectable file — genuinely `RUNTIME_UNVERIFIED`, not resolved either way, but the exact
mechanism is now fully understood.
**WordPress compose mounts CLOSED** (`EV-00173`): all 3 root compose files traced —
`daszek-local` (port 8090) hosts 4 plugins on ONE WP instance (daszek, generator, fast-kalk lead
widget, rag-widget); `kalk-top-local` (port 8091) is a SEPARATE co-located runtime for
kalk-top + fast-kalk (ro) + generator (ro) — confirms `KALKTOP_BASE_URL`/`GENERATOR_BASE_URL`
both point at this same instance; `cieplo-local` has no WordPress at all. All 3 share
`gmail-agent/.env.local-vps`, reinforcing the shared-Gmail-account finding across all 3 stacks.
**PHP route enumeration CLOSED** (`EV-00174`): daszek has 82 REST routes across 3 namespaces
(v1:7, v2:29, v3:46 — overwhelmingly the largest surface in the system); kalk-top has exactly 3
(2 health + 1 canonical calculate-offer); top-instal-generator has exactly 1 REST route + 2
admin-ajax actions (already traced); fast-kalk has exactly 3. No hidden 4th+ routes found in any.
**Every `ONE-SIDED`/`PATTERN` cross-repo contract row CLOSED to `BOTH`** (`EV-00175`): all 9
remaining rows in `CROSS_REPO_CONTRACTS.md` — fast-kalk→generator PDF path, cieplo's
`KalkTopClient`/`GeneratorClient` internals, kalk-top's/generator's `OsEvent` clients,
rag-widget's document-upload route, gmail-agent's case/engagement-snapshot serving routes for
rag-chat-asystent, and gmail-agent's v3/v1/v2 feed-push receiving routes on daszek's side — all
had both producer and consumer opened directly in code this pass, with exact path/schema matches
confirmed in every case. `CROSS_REPO_CONTRACTS.md` now has 0 `ONE-SIDED` and 0 `PATTERN` rows.
Domain 8 is now fully `RESOLVED` — every mandatory item closed.

### Domain 9 — Learning i outcomes — **RESOLVED**
Workflows: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`
Evidence: EV-00008..EV-00012, EV-00106..EV-00109, EV-00136, EV-00176, EV-00181
Done: divergence→candidate chain; row-shape bug and its downstream misclassification;
`CANDIDATE_THRESHOLD=3` corrected to adaptive + cross-family boost; auto-approval CAN approve
without a confidence check; **approved learning signals refined to conditional precedent
consumers, not a primary control-loop consumer**;
**business-outcome capture confirmed missing**; **`get_win_rate` `CONTRACT_DRIFT`**
(`EV-00136`) — queries `status='won'` when the lifecycle enum uses `'completed'`, so it
structurally always reports 0 wins, and `get_revenue_forecast` inherits the bad `rate_pct`
(reconfirmed independently via `EV-00164`'s Business Pulse trace). **All remaining named modules
CLOSED** (`EV-00176`): `pattern_learner.py` is live, wired via `divergence_loop._run_pattern_learner`,
feeding the same learning table later refined by `EV-00181` to have a conditional precedent
consumer; `pattern_discovery.py` is a genuinely separate,
on-demand-only mechanism (`POST /system/patterns/discover`), no persistence, no auto-consumer;
`agent_runtime/decision_divergence.py` matches the already-closed gap 26 (semantic policy
envelope); `operator_feedback_runtime.py` is fully live via `adjudication_executioner.py`;
`operator_learning_hooks.py` is partially dead (`hook_process_operator_action` is called, but
`hook_record_action_proposal_v2`/`hook_record_agent_draft` have zero callers — the live path
calls `record_agent_proposal` directly instead). **Refined by reverse-audit category 7**
(`EV-00181`): `learning_rule_candidates` and `world_model_insights` both have real conditional
reader-side precedent hooks through `similar_cases_precedent.py` -> `mailbox_memory_runtime.py`;
the actual unwired edge is producer-side for `world_model.py`'s
`ingest_corpus_message`/`ingest_corpus_fact`/`distill_insights_from_corpus` family, not the
consumer side previously described too strongly in `EV-00176`.

---

## 4. Ordered work queue (the only authoritative TODO)

Execute in this order. Each item states its exit condition.

**Phase A — remaining domain closure**
- [x] **D3 — DONE** (`EV-00138`..`EV-00141`, `EV-00177`,
      `_raw/planner_tool_chain_cross_reference.md`). Planner internals, full tool-chain
      cross-reference (3 enforcement layers, live test run), `select_sub_agent` defect found,
      policy-steering question answered, and argument-signature conformance now checked for all
      24 `HANDLERS` entries — 2 confirmed defects (`request_human_handoff` has no schema and no
      other invocation path, genuinely dead; `call_kalk_top_quote`'s schema advertises 3 params
      the handler ignores entirely), both filed as new gaps (30, 31). Domain 3 status is now
      `RESOLVED`.
- [~] **D4 — MOSTLY DONE, two-part status per operator instruction, NOT plain `RESOLVED`**
      (`EV-00142`..`EV-00152`, `EV-00157`, `EV-00158`). All mandatory branches traced: executor
      internals, idempotency scope + its false docstring contract, the crash-window question
      (CONFIRMED, reachable without a crash — P0 gaps 9 & 10), task-reject (distinct from
      materialize-reject), `case_write_gateway` corrected, durable `ExecutionResult` on all 3
      exit paths, Gmail-send's real claim-based restart recovery (P1 gap 12 notes the
      cross-shape inconsistency), materialize-reject CONFIRMED ABSENT, and the 3
      `gmail_intake.py` execution_runtime call sites (CLI **and** bridge-queue-drain, `EV-00157`).
      **Both mandatory residual questions now RESOLVED**: (1) `approve_hitl_action` for
      non-`prop_*` actions — CONFIRMED two-phase design (approve clears gate synchronously, a
      separate `agent_hitl_send` route enqueues an async bridge-queue row that
      `execute_hitl_send_from_bridge_row` drains, itself requiring the gate already cleared —
      `EV-00157`), not `MISSING_EXECUTOR`. (2) Clarification answer-content channel — CONFIRMED
      MISSING as a **dead field**: Daszek sends `draft_pl`/`operator_draft_pl`, nothing on the
      gmail-agent side ever reads it (`EV-00158`, new P0 gap 11). Domain 4's status label is
      `PRIMARY_APPROVE_REJECT_EXECUTION_PATHS_RESOLVED — CLARIFICATION/NO-EXECUTOR_PATH_OPEN`
      exactly per operator instruction — not because work remains undone, but because one
      resolution is itself "confirmed missing," which the label must carry, not hide.
- [x] **D5 — DONE** (`EV-00153`, `EV-00154`, `EV-00159`, `EV-00160`, `EV-00161`, `EV-00162`).
      Node-B-caller question CLOSED; RRF fusion + FlashRank reranker traced, no defect;
      `hybrid_search`/`_single_hybrid_search` fully traced (adaptive retrieval, PRF, gated
      multi-query, query rewriting, HyDE, candidate generation, RRF, hard-token rescue);
      `compute_gating`/`apply_diversity_policy` traced; `entities/`/`reflection/`/
      `adaptive_retrieval/` confirmed wired with real callers; GraphRAG split confirmed
      (retrieval side LIVE, ingest-time `build_community_summary` ORPHANED — filed as new P2 gap
      30); ingest partial-failure isolation + hard-PDF fallback cascade traced; ownership of
      chunks/embeddings/indexes/documents closed. Domain 5 status is now `RESOLVED`. Residual
      (non-blocking): `_apply_domain_boosts`/`_apply_entity_boosts` and
      `document_intelligence`/`structured_extraction` field-level depth not traced further —
      both minor, noted in Domain 5's canonical status block, not gap-worthy.
- [x] **D7 — DONE** (`EV-00155`, `EV-00156`, `EV-00163`, `EV-00164`, `EV-00165`, `EV-00166`).
      DB-outbox dynamic-hook question CLOSED; `ReconcileResult.warnings` search COMPLETE
      (`MISSING_CONSUMER`, new P1 gap 27); Karta dnia/Business Pulse/health endpoints/v3 ingest
      endpoint all traced and confirmed LIVE (`EV-00164`, `get_revenue_forecast` inherits
      `get_win_rate`'s bug); non-HITL feed-push triggers confirmed (`EV-00166`); `bridge_queue`
      retry/dead-letter semantics CLOSED — none exist, failures fully invisible to the operator,
      new P1 gap 28 (`EV-00165`). Domain 7 status is now `RESOLVED`. Residual (non-blocking):
      exhaustive field-by-field backend↔frontend projection mapping not done beyond the traced
      views — minor, noted in Domain 7's canonical status block.
- [x] **D8 — DONE** (`EV-00167`..`EV-00175`). `class-chat.php`/`class-answer-extractor.php`
      CLOSED; kalk-top pricing engine internals CLOSED (traced to `equipment-catalog.json`,
      decisive root-cause for the margin `MISSING_PRODUCER` gap); `FAILED_RETRYABLE` consumer
      CLOSED; Cieplo's two `run_workflow_pipeline` implementations RESOLVED; shared Gmail
      credential/mailbox question CONFIRMED; `call_kalk_top.py` re-confirmed thin re-export;
      generator legacy AJAX path/field mapping/converter contract CLOSED; rag-widget
      local-vs-prod URL mechanism CLOSED; WordPress compose mounts CLOSED; **D8b: PHP route
      enumeration CLOSED** (daszek 82 / kalk-top 3 / generator 1+2-ajax / fast-kalk 3); **every
      `ONE-SIDED`/`PATTERN` cross-repo contract row CLOSED to `BOTH`** (`EV-00175`,
      `CROSS_REPO_CONTRACTS.md` now has 0 `ONE-SIDED`/0 `PATTERN`). Domain 8 status is now
      `RESOLVED`.
- [x] **D9 — DONE** (`EV-00176`, refined by `EV-00181`). All remaining named modules traced (`pattern_learner.py`,
      `pattern_discovery.py`, `decision_divergence.py`, `operator_feedback_runtime.py`,
      `operator_learning_hooks.py`, `LEARNING_LOOPS_MIGRATIONS.sql`'s 6 tables). Decisive new
      finding: `world_model.py`'s producer side is unwired even though a conditional reader path
      exists through `similar_cases_precedent.py` -> `mailbox_memory_runtime.py`; gap 29 is now
      classified as `MISSING_PRODUCER`, not missing consumer. Domain 9 status is now `RESOLVED`.

**Phase B — cross-cutting investigations**
- [x] **N4 — DONE** (`EV-00169`). `topinstal_cieplo_worker` is `LIVE_PATH` (packaged `cieplo-worker`
      CLI script, documented `uvicorn topinstal_cieplo_worker.main:app` launch command).
      `topinstal_cieplo_orchestrator` is `DEAD_PATH` — zero external importers anywhere, and its
      own `main.py` doesn't even use its own `api/routes.py` (imports the worker's router
      verbatim). Same pass closed the `FAILED_RETRYABLE` consumer question: a real
      `POST /api/workflows/{id}/retry` endpoint exists in the live package, manual-trigger-only,
      no automatic scheduler.
- [x] **N5 — DONE** (`EV-00146`). `case_write_gateway` EXISTS; the `NAME NOT FOUND` verdict was
      wrong and is corrected in `ARCHITECTURAL_RULES_AUDIT.md`. Verdict: a real, working
      operator/API-facing write gateway with a genuine `upsert_allowed` guard, but **not the sole
      writer** — 7+ paths bypass it via `enrich_case_row_before_upsert`, and `materialize.py`
      bypasses it by documented design. Enforcement is duplicated per-caller, not centralized.
- [ ] **N2** — complete the remaining 5 reverse-audit categories, one `_raw/` inventory each
      (see §6 for the list and required inventory shape).
- [ ] **N3** — map test evidence for every workflow and architectural rule (locate + classify;
      running the full suite is not required). Must distinguish tests that manually inject state
      from tests that prove a live producer.

**Phase C — normalization (do NOT start before Phase A/B land)**
- [ ] **N1** — normalize `WORKFLOW_EVIDENCE.jsonl` to the full schema (`workflow_id`,
      `related_workflow_ids`, `evidence_type`, `confidence`, `raw_artifact`); attach all 39
      currently-unattached records: the original 18 — EV-00104, 00105, 00112, 00113, 00114,
      00115, 00118, 00120, 00121, 00122, 00125, 00126, 00127, 00132, 00133, 00134, 00135, 00136 —
      **plus 21 added since**: EV-00138..00158 inclusive. IDs must not change. EV-00138..158
      already carry `evidence_type`/`confidence` (added at creation time) but still lack
      `workflow_id` — 0 of 158 records have it yet, this remains fully open. **DO NOT update this
      count incrementally per-batch again — wait until Phase A/B fully land (see below), then do
      N1 exactly once**, over the final evidence count.
- [ ] **N6** — normalize `WORKFLOW_REGISTRY.yaml` to the full mandatory schema (all fields
      present, using `none`/`unknown`/`not_applicable`/`not_confirmed` rather than omission);
      move `CORRECTED`→`revision_status`, `MANUAL_TRIGGER_ONLY`→`trigger_mode`; split
      `RUNTIME_CONFIRMED` into the 7 runtime dimensions.
- [ ] **N8** — atomic gap registry: stable `gap_id` per gap, one problem per gap, full schema;
      split the currently-merged multi-problem gaps; resolve gap 24's `workflow_id: none specific`.
- [ ] **N9** — fix `ENTRYPOINT_INVENTORY.md`: separate counters (direct decorators / dynamic
      registrations / unique `(method,path)` / duplicates / shadowed), resolve `/agent-chat`,
      delete superseded "not yet enumerated" narrative.

**Phase D — regeneration + gate (single pass, from the normalized core only)**
- [ ] Regenerate in order: state ownership → cross-repo contracts → architectural rules →
      runtime proof register → atlas → executive summary.
- [ ] **N7** — write `validate_workflow_atlas.py`, run it, emit `FINAL_CONSISTENCY_REPORT.md`.
      Must exit non-zero on every failure class listed in the operator's §15.
- [ ] Generate `FINAL_MANIFEST.json` (path, size, SHA-256, timestamp). No artifact edits after.

---

## 5. Tooling status and known blind spots

- **GitNexus** — canonical indexed-repo table:

  | repo | indexed | commit | language | known blind spots | required fallback |
  |---|---|---|---|---|---|
  | `gmail-agent` | yes | `468d37e` | Python | `gitnexus query` (BM25/vector) degraded (`EV-00114`) | `gitnexus context` + `rg` |
  | `daszek` | yes | `672769d` | PHP | variable-typed/DI dispatch; WordPress hook dispatch | `rg`/direct read before any "no caller" conclusion |
  | `kalk-top` | yes | `9d56055` | PHP | DI dispatch — CONFIRMED, not hypothetical (`EV-00118`) | direct read authoritative |
  | `cieplo-orchestrator` | yes | `e68f053` | Python | **function-passed-by-reference not resolved** — CONFIRMED (`EV-00133`: `BackgroundTasks.add_task`) | direct read authoritative |
  | `top-instal-generator` | yes | `7e52795` | PHP | 1 file no-Module-scope warning; DI dispatch | direct read |
  | `fast-kalk` | yes | `06a470d` | PHP | DI dispatch (tool-level, presumed); static-method calls DO resolve (`EV-00135`) | direct read for indirect dispatch |
  | `rag-widget` | yes | `c64707a` | PHP | 1 file no-Module-scope warning; DI dispatch | direct read |
  | `rag-chat-asystent` | **no** | n/a | Python | no GitNexus AND no clean CBM index — zero graph coverage | **mandatory `rg`/AST/direct read** |
  | `wp-bridges` | **N/A** | n/a | PHP | not a git repo — thin local harness, excluded from all repo counts by design | `rg`/direct read |

  **Rule established this pass**: an ABSENT GitNexus edge is never proof of non-use, in any
  language — confirmed blind spots now exist for both PHP (DI/variable-typed) and Python
  (function-passed-by-reference). Direct code read is authoritative.
- **Codebase Memory MCP**: current for gmail-agent/daszek/kalk-top/cieplo-orchestrator/
  rag-widget/top-instal-generator. Not usable for `rag-chat-asystent`. Does not cover PHP.
- **Serena MCP**: configured but not usable (trust-hash approval pending). Not blocking.
- **Docker read-only inspection**: done, see `RUNTIME_BASELINE.md` §2.

---

## 6. Reverse-audit status — 7 of 12 categories complete, 0 partial, 5 not started

**Complete, with real `_raw/` inventories:**
1. ✅ tool names ↔ registry/handler/executor — `_raw/tool_registry_cross_reference.md`
   (24/24 registered; found `get_win_rate` `CONTRACT_DRIFT`, `EV-00136`)
2. ✅ signal source kinds ↔ registered handlers — `_raw/signal_source_kind_cross_reference.md`
   (4/4 registered; found `google_calendar`/`calendar` mismatch, `EV-00137`; 2 apparent
   mismatches verified as non-issues; 4 items left explicitly open)
3. ✅ planner tool schema ↔ handler ↔ executor — `_raw/planner_tool_chain_cross_reference.md`
   (schema/handler/allowlist name-level cross-reference complete, 3 enforcement layers confirmed,
   1 live test run, argument-signature conformance now checked for all 24 handlers — 2 confirmed
   defects: `request_human_handoff` has no schema/no other invocation path, `call_kalk_top_quote`
   ignores 3 schema-advertised params, `EV-00177`)
4. ✅ event type ↔ emitter ↔ handler — `_raw/event_type_emitter_handler_cross_reference.md`
   (`EV-00178`): 2 parallel mechanisms found — Mechanism A (`/internal/os-events` inline hook,
   always live, cieplo-specific string match) and Mechanism B (`event_spine.processor`'s
   `HandlerRegistry`, 2/N types registered, CLI-only + env-flag-gated, not live by default).
   No silent gap; deliberately staged design.
5. ✅ proposal type ↔ creator ↔ approver ↔ executor ↔ result writer —
   `_raw/proposal_type_creator_executor_cross_reference.md` (`EV-00179`): of
   `MaterializeProposalItem`'s 5 `proposal_type` values, only `composite_plan` has a confirmed
   creator; the other 4 (`link_existing`/`create_case`/`create_artifact`/`defer_operator`) each
   have a real, schema-validated, downstream-reconcile-aware executor but NO creator anywhere —
   `MISSING_PRODUCER` for 4/5 types, new P1 gap 32.
6. ✅ fact key ↔ producer ↔ reader ↔ supersession/invalidation —
   `_raw/fact_key_producer_reader_supersession_cross_reference.md` (`EV-00180`): 2 writers with
   different supersession semantics found. `replace_message_facts` (main ingestion pipeline)
   correctly supersedes via delete+upsert per message. `append_fact_rows` (sole writer behind the
   agent's `extract_facts_from_text` tool) uses `ON CONFLICT DO NOTHING` on a `fact_id` derived
   only from `case_id`+`fact_key` — meaning this tool can NEVER update a fact it already recorded,
   silently, with `ToolResult` still reporting success. New P1 gap 33.
7. ✅ table write ↔ table reader —
   `_raw/table_write_reader_cross_reference.md` (`EV-00181`): 52 real tables adjudicated across
   mailbox_memory, correlation_registry, agent_runtime, learning loops, business_dictionary,
   event_spine, graph_store, and operator_memory. Confirmed intentional audit/manual one-sided
   tables (`agent_runtime_jobs`, `drive_ingest_runs`, `event_spine_handler_effects`,
   `identity_merge_log`, `sync_outbox`, `mailbox_memory_calendar_case_links`), corrected the
   earlier overstatement that `learning_rule_candidates` / `world_model_insights` had zero
   consumers, and reclassified `world_model.py` as reader-wired but producer-unwired. Also found
   one confirmed schema-only dead table: `mailbox_memory_document_conflicts`.

**Remaining 5, each needs its own `_raw/` inventory (§4 item N2):**
8. ⬜ status value ↔ writer ↔ consumer
9. ⬜ projection field ↔ backend producer ↔ frontend usage (overlaps §4 D7)
10. ⬜ env/feature flag ↔ loader ↔ branch point ↔ live value
11. ⬜ scheduler/timer/cron ↔ actual caller
12. ⬜ cross-repo payload ↔ request validator/schema; route ↔ client; recovery/replay entrypoint
    ↔ original workflow

**Required shape for every inventory**: command used, scope, exclusions, full result list,
per-item classification, unresolved items, evidence IDs. A category is NOT complete on `rg`
output alone — false positives must be manually adjudicated (as was done for
`cieplo_orchestrated` and `node_b_generated` in category 2).

**Method validation**: both completed categories produced a decisive, previously-unflagged
finding. Neither would have been found by reading producer or consumer in isolation. This is
direct evidence the remaining 10 categories are high-value, not ceremonial.

---

**Superseding reverse-audit note (2026-07-30 20:35:08 +02:00)**:
- Current reverse-audit status is `8/12 COMPLETE`, `0 PARTIAL`, `4 NOT_STARTED`.
- Category 8 is now complete via `_raw/status_value_writer_consumer_cross_reference.md` (`EV-00182`).
- New gap items from category 8: `WORKFLOW_GAPS.md` items `41` and `42`.
- The current first open reverse-audit step is category `9`:
  `projection field ↔ backend producer ↔ frontend usage`.

## 6A. Canonical override after category 9

- Timestamp: `2026-07-30 20:55:59 +02:00`
- Category 9 complete: `_raw/projection_field_backend_producer_frontend_reader_cross_reference.md`
- New evidence: `EV-00183`
- Canonical reverse-audit status: `9/12 COMPLETE`, `0 PARTIAL`, `3 NOT_STARTED`
- Canonical evidence count: `183` (`EV-00001`..`EV-00183`)
- Canonical normalized evidence count: `46/183`
- Canonical gap count: `44` (`P0:11`, `P1:22`, `P2:7`, `P3:4`)
- Canonical `_raw/` inventory count: `9`
- New gap items from categories 8-9: `41`..`44`
- Current first open reverse-audit step: `category 10 — env/feature flag ↔ loader ↔ branch point ↔ live value`

## 6B. Canonical override after category 10

- Timestamp: `2026-07-30 21:03:07 +02:00`
- Category 10 complete: `_raw/feature_flag_env_loader_branchpoint_live_value_cross_reference.md`
- New evidence: `EV-00184`
- Canonical reverse-audit status: `10/12 COMPLETE`, `0 PARTIAL`, `2 NOT_STARTED`
- Canonical evidence count: `184` (`EV-00001`..`EV-00184`)
- Canonical normalized evidence count: `47/184`
- Canonical gap count: `45` (`P0:11`, `P1:22`, `P2:8`, `P3:4`)
- Canonical `_raw/` inventory count: `10`
- New gap item from category 10: `45`
- Current first open reverse-audit step: `category 11 — scheduler/timer/cron ↔ actual caller`

## 7. Known limitations of this analysis (not system gaps)

1. `rag-chat-asystent` has zero graph-tool coverage — all Domain 5 work is `rg`/direct-read.
2. ~~PHP/WordPress route enumeration incomplete~~ RESOLVED — 89 routes enumerated across all 4
   PHP repos (`EV-00174`).
3. No test evidence mapped yet (§4 item N3) — every "tests: not checked" note in
   `ARCHITECTURAL_RULES_AUDIT.md` remains literally true.
4. `RUNTIME_CONFIRMED` is currently overloaded across 8 workflows — it mostly means
   "entrypoint/flag active + statically reachable", NOT "path observed end-to-end". Only 5
   evidence records are genuine runtime introspection (`EV-00015`, `EV-00041`, `EV-00046`,
   `EV-00071`, `EV-00119`), and none observes a business path completing. §4 item N6 fixes the
   semantics; the underlying evidence is not being discarded, only re-labeled honestly.
5. ~~Cross-repo contracts: 7 BOTH, 8 ONE-SIDED, 3 PATTERN~~ RESOLVED — all rows in
   `CROSS_REPO_CONTRACTS.md` are now `BOTH` (`EV-00175`).

## 6C. Canonical override after category 11

- Timestamp: `2026-07-30 21:06:28 +02:00`
- Category 11 complete: `_raw/scheduler_timer_cron_actual_caller_cross_reference.md`
- New evidence: `EV-00185`
- Canonical reverse-audit status: `11/12 COMPLETE`, `0 PARTIAL`, `1 NOT_STARTED`
- Canonical evidence count: `185` (`EV-00001`..`EV-00185`)
- Canonical normalized evidence count: `48/185`
- Canonical gap count: `45` (`P0:11`, `P1:22`, `P2:8`, `P3:4`)
- Canonical `_raw/` inventory count: `11`
- New gap items from category 11: `none`
- Current first open reverse-audit step: `category 12 - cross-repo payload ↔ request validator/schema; route ↔ client; recovery/replay entrypoint ↔ original workflow`

## 6D. Canonical override after category 12

- Timestamp: `2026-07-30 21:14:30 +02:00`
- Category 12 complete: `_raw/cross_repo_payload_validator_route_client_recovery_replay_cross_reference.md`
- New evidence: `EV-00186`
- Canonical reverse-audit status: `12/12 COMPLETE`, `0 PARTIAL`, `0 NOT_STARTED`
- Canonical evidence count: `186` (`EV-00001`..`EV-00186`)
- Canonical normalized evidence count: `49/186`
- Canonical gap count: `46` (`P0:11`, `P1:22`, `P2:9`, `P3:4`)
- Canonical `_raw/` inventory count: `12`
- New gap item from category 12: `46`
- Reverse-audit status: `COMPLETE`
- Current first open step: `N3 - test-evidence mapping`

## 6E. Canonical override after N3

- Timestamp: `2026-07-30 21:32:07 +02:00`
- N3 complete: `_raw/test_evidence_mapping_cross_reference.md`
- New evidence: `EV-00187`
- Canonical evidence count: `187` (`EV-00001`..`EV-00187`)
- Canonical normalized evidence count: `50/187`
- Canonical gap count: `48` (`P0:11`, `P1:22`, `P2:11`, `P3:4`)
- Canonical `_raw/` inventory count: `13`
- New gap items from N3: `47`, `48`
- Fresh execution logs saved: `_raw/logs/20260730-212839/`
- Reverse-audit status remains: `COMPLETE`
- Current first open step: `Phase C step 1 - freeze findings`

## 6F. Canonical override after Phase C step 1

- Timestamp: `2026-07-30 21:46:00 +02:00`
- Freeze findings complete:
  - `_raw/phase_c_freeze_findings_snapshot.md`
  - `_raw/n1_evidence_workflow_attachment_seed.md`
- Canonical evidence count unchanged: `187`
- Canonical gap count unchanged: `48`
- Canonical `_raw/` inventory count: `15`
- Frozen pre-normalization hashes captured for:
  - `WORKFLOW_EVIDENCE.jsonl`
  - `WORKFLOW_GAPS.md`
  - `WORKFLOW_REGISTRY.yaml`
  - `PROGRESS.md`
- N1 seed result:
  - registry/test-status index already attaches `154/187` evidence
  - `33/187` evidence remain unattached and need manual primary/related workflow classification
  - no evidence row currently has `workflow_id`
- Current first open step: `Phase C step 2 / N1 - normalize WORKFLOW_EVIDENCE.jsonl`

## 6G. Canonical override before N1 JSONL rewrite

- Timestamp: `2026-07-30 21:56:00 +02:00`
- New N1 working artifacts:
  - `_raw/n1_unattached_evidence_triage.md`
  - `_raw/n1_attachment_policy.md`
  - `_raw/n1_unattached_preview_seed.json`
- Unattached-evidence preview seed now covers: `33/33`
- Proposed normalization policy:
  - workflow-specific rows -> canonical owner workflow
  - shared-subflow rows -> earliest owning workflow + downstream `related_workflow_ids`
  - atlas-global rows -> sentinel `workflow_id: ATLAS-GLOBAL` + non-empty `related_workflow_ids`
- Current evidence-schema gap before rewrite:
  - missing `workflow_id`: `187/187`
  - missing `related_workflow_ids`: `187/187`
  - missing `raw_artifact`: `184/187`
  - missing `evidence_type`: `137/187`
  - missing `confidence`: `137/187`
- Current first open step: `WORKFLOW_EVIDENCE.jsonl` full-schema rewrite using `_raw/n1_attachment_policy.md` and `_raw/n1_unattached_preview_seed.json`
