# WORKFLOW_GAPS.md — AI-OS TOP-INSTAL

Status: first synthesis pass, generated from `WORKFLOW_REGISTRY.yaml` + `WORKFLOW_EVIDENCE.jsonl`
as of the end of Domains 1-9's first pass + Domain 4's mandatory closure. Confirmed gaps only —
every item below has a `workflow_id`/`EV-#####` citation. Not exhaustive: the
`DOMAIN-COMPLETENESS-REVISIT` queue in `PROGRESS.md` lists further, not-yet-investigated
questions that may surface additional gaps.

Priority scale: **P0** confirmed defect with plausible real business/customer impact. **P1**
confirmed defect or architectural risk, lower/unclear immediate impact. **P2** confirmed
inconsistency or duplication, not yet shown to cause harm. **P3** observation/asymmetry worth
tracking, not itself a defect.

## P0 — confirmed defects with plausible real business impact

1. **`query_anything` is structurally broken on 2 of its 4 sources, and hides the failure.**
   `EV-00001/02` (RAG branch: wrong call signature, guaranteed `TypeError`), `EV-00003/04`
   (similar-cases branch: imports a function name that does not exist, guaranteed `ImportError`),
   `EV-00006` (errors counted as answered sources), `EV-00007` (`status="ok"` unconditional).
   Impact: the agent can believe it consulted RAG/precedent knowledge when it structurally could
   not have. Mitigating factor: a SEPARATE, correctly-implemented tool (`search_rag_knowledge`,
   `EV-00077`) covers the RAG capability correctly — `query_anything`'s RAG branch is redundant as
   well as broken. `workflow_id`: `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP`.
2. **Learning-loop row-shape bug can misclassify a real operator approve as a divergence.**
   `EV-00008..EV-00012`: both real call sites of `fetch_open_proposals_for_case` use a bare
   `psycopg.connect()` with no `row_factory`, defaulting to tuple rows; `_row_to_proposal` then
   drops every field except `proposal_id`; `classify_operator_response` reads the now-empty
   `proposal_type` and can produce `RESPONSE_DIVERGENT_ACTION` for a genuine approve. Impact:
   corrupts the learning loop's own input signal (see item 7 below) and could misrepresent
   operator behavior in the divergence audit trail. A sibling function (`fetch_decision_queue`)
   had the identical bug fixed via `dict_row` in a prior session (`OPERATOR_DECISIONS.md`
   2026-07-16) — this one was not. `workflow_id`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`.
3. **Gmail HITL "dry run" reports itself as executed.** `EV-00013`: when the `gmail.send` scope
   is missing, `execute_hitl_gmail_send` returns `executed=True, mode="bounded_dry_run",
   decision_status="executed"` simultaneously — no email is sent, but the record claims
   execution happened. `EV-00014`: the *real* send path uses the identical
   `decision_status="executed"` value, so that field alone never distinguishes a simulated
   effect from a real one anywhere downstream. Impact: any consumer trusting `decision_status`
   alone (not also checking `mode`) will believe a message was sent when it was not.
   `workflow_id`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`.
4. **A working concurrency-safety mechanism has its signal thrown away one layer up.**
   `EV-00060` confirms real optimistic-concurrency CAS protection (`AgentConcurrencyError`) on
   `execute_agent_run`'s snapshot save. `EV-00056/62` confirm that when this CAS conflict fires,
   `run_agent_reconcile`'s Block 3 catches it as a generic `Exception`, folds it into the same
   `agent_run_failed` warning string as any other failure, and (`EV-00051`) mislabels the whole
   event as `rebuild_result.update_reasons=['agent_dry_run']` — indistinguishable from an
   intentional no-op. Impact: a genuine concurrent-write race (two things touching the same
   engagement at once) becomes invisible instead of surfacing as the meaningful signal it is.
   `workflow_id`: `AGENT-GRAPH-EXECUTE-RUN`.
5. **Case Intelligence / Understanding / Business Reasoning / Decision Pipeline failures are
   silently absorbed and the agent proceeds on a blank context that looks like "nothing new."**
   `EV-00054`: `run_agent_reconcile`'s Block 1 catches any exception in this entire stage, leaves
   `case_intelligence_result={}` with no embedded failure marker, and the downstream
   `agent_signal` fields (`understanding_brief_pl`, `case_understanding_projection`, etc.) all
   resolve to empty defaults — structurally identical to a case that genuinely has nothing new to
   report. Terminal status remains `"reconciled"`. No retry (journal dedup blocks natural
   reprocessing). `workflow_id`: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`.
6. **The Daszek feed-push mechanism has no durable retry, and the calendar/visit data model is
   split into two disconnected worlds.** `EV-00089` (feed push: telemetry-only on failure, no
   queue, by design — "best_effort" in the function's own name). `EV-00080/82`: the only code
   capable of detecting "customer proposed a date, nothing confirms it" is reachable exclusively
   via a manual operator CLI command, never the automatic pipeline; `execute_schedule_visit`
   (the agent's entire implementation of "schedule a visit") writes only a text fact, never
   touches the real Google Calendar. Two independent, both already-confirmed-open items from
   `brief.md` (§6.7, §5.4, §6.5), now with direct rather than inferred evidence.
   `workflow_id`: `DASZEK-FEED-PUSH-NO-RETRY`, `CALENDAR-TWO-WORLDS-OF-VISITS`.
7. **The learning loop still does not fully close, but the consumer-side picture was refined.**
   `EV-00181` corrects the older zero-consumer wording from `EV-00108`: approved
   `learning_rule_candidates` DO feed a real, conditional precedent path via
   `divergence_loop.fetch_approved_rules_for_family` ->
   `similar_cases_precedent.fetch_learning_rule_precedent_refs` ->
   `mailbox_memory_runtime.fetch_similar_case_precedent_refs_v1`. So the table is not
   evidence-only in the literal sense anymore. The loop is still architecturally incomplete,
   because this is only a conditional precedent-enrichment reader, not a primary planner/policy
   control loop, and `EV-00109` still stands: no business-outcome capture (sale value, margin,
   win/loss) exists to close the later-outcome side. `EV-00107` also still stands: one of two
   auto-approve triggers requires no confidence check at all, purely observation volume.
   `workflow_id`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`.
8. **The agent-exposed `get_win_rate` business tool is not merely unimplemented but ACTIVELY
   WRONG — it is structurally guaranteed to report 0 wins regardless of real performance.**
   `EV-00136` (found via the reverse-audit tool-registry cross-reference, refines `EV-00132`'s
   `MISSING_PRODUCER` framing to a more precise `CONTRACT_DRIFT`): `get_win_rate` counts
   `mailbox_memory_cases` rows by `status`, reading hardcoded keys `"won"`/`"lost"`. The real
   `CaseLifecycleState` enum's success state is `"completed"`, not `"won"` — `"lost"` matches
   correctly, `"won"` never can. The tool returns a confident, plausible-looking `rate_pct`
   number rather than erroring — an operator or the agent itself could report this fabricated
   0%-or-near-0% win rate as fact. **Confirmed inherited downstream** (`EV-00164`):
   `business_pulse.py:get_revenue_forecast` calls `get_win_rate` directly and multiplies its
   pipeline value by the same broken `rate_pct`, so the revenue forecast tool inherits the
   identical fabricated-confidence defect — both are one bug, not two.
   `workflow_id`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`.

9. **The approved-materialize executor performs its durable side effect BEFORE persisting the
    result, and three non-crash paths return an error after the effect already happened —
    leaving a real mutation with the proposal still marked `pending`.** `EV-00144`: in
    `approve_materialize_proposal`, `execute_materialize_proposal()` (case row upsert,
    correlation link, email identity — all durable) runs at line 155; only afterwards does a CAS
    loop re-read the snapshot and **sleep up to ~1.75s in exponential backoff**, then patch the
    proposal to `approved` (line 199) and save (line 209). A `MaterializeConflictError` (189), a
    CAS-retries-exhausted return (197), or an `AgentConcurrencyError` (211) all fire *after* the
    side effect. The only double-execution guard for non-composite proposal types is the
    entry-time `status != 'pending'` check — exactly the guard that cannot engage, because the
    status was never patched. An operator seeing the error would naturally re-approve and re-run
    the effect. **No durable effect receipt is written before or immediately after the side
    effect** (the `case_os.materialize.approved` os_event is emitted only after the snapshot
    save, and is best-effort/shadow). Partial mitigation only: `create_case`'s email-level dedup
    converts a re-run into `linked_existing` — but only when `customer_email` AND
    `correlation_store` are both present; otherwise a second case with a new uuid is created.
    `workflow_id`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`.
10. **`approve_materialize_proposal`'s docstring promises unconditional idempotency that the code
    delivers for only 1 of its 5 proposal types.** `EV-00143`: the docstring states
    *"idempotency_key: … Jeśli podany, operacja nie zostanie wykonana ponownie"* ("if provided,
    the operation will not be executed again"). Real enforcement (`with_idempotency`:
    `check_idempotency` before, `record_idempotency` after) exists **only** for operations
    dispatched through `WRITE_EXECUTORS`, i.e. only the `composite_plan` type. `create_case`,
    `link_existing`, `create_artifact` and `defer_operator` never consult the key — it is merely
    stuffed into the payload. Additionally the wrapper silently no-ops without a `db_url`, and
    records only on `status == "ok"`, so a side effect that succeeded under a non-ok result is
    never recorded and will re-run. A false safety guarantee on a write path is worse than a
    documented absence. `workflow_id`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`.
11. **The operator-clarification / draft-edit answer channel is a dead field, silently discarded
    end to end, not merely absent.** `EV-00158`: Daszek's UI sends a free-text `draft_pl` /
    `operator_draft_pl` field on both the HITL approve call and the async bridge-queue send row —
    the only candidate channel found anywhere for an operator's clarification answer or draft
    edit to reach the agent. Exhaustively confirmed that NEITHER consumer
    (`engagement_hitl_approve`/`approve_hitl_action`, nor `execute_hitl_send_from_bridge_row`)
    ever reads it. The email body actually sent always comes from `action.payload_pl` (set by the
    agent's own prior turn). An operator can type an answer or an edit, submit it, receive a
    success response, and have it silently ignored — the UI implies a capability the backend
    does not implement. `workflow_id`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`.

## P1 — confirmed architectural risks, unclear or lower immediate impact

12. **The operator-clarification flow has no channel for the operator's actual answer text to
    reach the agent.** `EV-00148`: `request_operator_clarification` sets a blocking gap and
    `hitl_gate.required`; resolution goes through the same `/hitl/approve` route and
    `approve_hitl_action`, which accepts only `action_id`+`operator_id`. Any extra payload field
    is recorded for learning/audit only (`_record_hitl_operator_action` → learning hooks), never
    consumed by the next agent turn. Clarification therefore depends on the answer arriving via
    some other channel entirely (most plausibly a new inbound signal re-ingested normally) —
    not confirmed, and not exposed anywhere in this API surface. `workflow_id`:
    `HITL-PROPOSAL-APPROVAL-DUAL-PATH`.
13. **Restart/duplicate-call recovery quality is inconsistent across the codebase's 3
    proposal/execution shapes, not a system-wide property.** `EV-00149/150` vs. `EV-00144`: the
    3rd shape (`execution_runtime.ExecutionResult`) durably persists a result on every exit path;
    the Gmail-send HITL action has a real atomic claim + 2-second poll-for-completion restart
    guard; the materialize-proposal path has neither. A component built correctly elsewhere in
    the same codebase was not applied uniformly. `workflow_id`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`.

14. **Global company-knowledge RAG is architecturally unreachable from gmail-agent's agent
   runtime.** `EV-00078/79`: "company knowledge" surfaced to the agent is a static local text
   file; the real `rag-chat-asystent` retrieval/embedding/reranking pipeline is confirmed live
   and healthy but has zero HTTP client anywhere in gmail-agent's code reaching it. It IS reached
   by `rag-widget` (WordPress), so the producer works — this is a pure `MISSING_CONSUMER` gap on
   gmail-agent's side. Directly confirms `brief.md` §6.6.
   `workflow_id`: `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP`.
15. **CONFIRMED: gmail-agent and cieplo-orchestrator's Gmail pollers share the exact same live
   mailbox account, not just similar-looking credentials.** `EV-00170`:
   `docker-compose.cieplo-local.yml`'s mount of `gmail-agent/.env.local-vps` carries an explicit
   inline comment naming the shared account (`biuro.topinstal@gmail.com`). cieplo-orchestrator's
   own poll query is narrowly content-scoped (`(cieplo.app OR cieplowlasciwie.pl) newer_than:3d`),
   and gmail-agent has a dedicated, first-class integration (`cieplo_orchestrator_hook.py`,
   `source_kind='cieplo_orchestrated'`) that creates/patches cases FROM cieplo-orchestrator's
   structured `os_event`s rather than by re-scraping the raw email — proving this was designed
   for, not an accidental discovery. **Narrowed, still-open residual**: whether gmail-agent's own
   raw Gmail-polling loop (independent of the os_event bridge) also independently ingests the
   same incoming cieplo-lead email and creates a competing/duplicate case row was not conclusively
   traced — gmail-agent's own live poll query/filter was not located this pass.
   `workflow_id`: `GMAIL-SIGNAL-WORKER-LOOP`, `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`.
16. **At least 3, possibly 4, coexisting proposal/execution lifecycle shapes.** `EV-00074/75/76`:
    `action_proposals_v2` (gated on a real `decision_candidate`), materialize proposals (proposal_id +
    real Idempotency-Key + CAS retry, `EV-00110`), and `execution_runtime.ActionProposal`/
    `ExecutionResult` (confirmed live callers in `calendar_runtime.py`, `daszek_bridge_queue_drain.py`,
    and 3 still-unopened `gmail_intake.py` call sites). `EV-00111` shows the first two *converge*
    on one executor for proposal-shaped `action_id`s, so the real count of genuinely independent
    lifecycles is smaller than "3" suggests, but not fully resolved — richer than `brief.md`'s
    original "2 systems" framing either way.
    `workflow_id`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`.
17. **`ThreadPoolExecutor` used for the core Case Intelligence pipeline achieves no real
    concurrency.** `EV-00068`: `run_shared_downstream_stages` submits each LLM stage to a thread
    pool but immediately blocks on `.result()` before submitting the next — the stages that could
    theoretically overlap never do. Latency cost, not a correctness bug.
    `workflow_id`: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF` (uses `SUBFLOW-SHARED-DOWNSTREAM-STAGES`).
18. **Draft and ActionPlanner run before Understanding, confirmed directly (not inferred) in
    current code, function relocated since `brief.md` was written.** `EV-00066/67`:
    `run_shared_downstream_stages`' own docstring/code order is business_reasoning → draft_reply →
    plan_actions → case_intelligence (last). The code is self-aware of this dependency
    constraint (comment explains why full parallelism isn't possible) — an intentional
    consequence of the pipeline's data dependencies, not an accident, but still means action
    planning happens before the system has synthesized its fullest understanding of the case.
    `workflow_id`: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF` (uses `SUBFLOW-SHARED-DOWNSTREAM-STAGES`).
19. **`top-instal-generator` supports two live document-generation modes and two converter paths,
    not one canonical path.** `EV-00101`: `mode='from-offer-dto'` (canonical) and
    `mode='direct-config'` (legacy) are BOTH live; converter is `gotenberg` (real) or
    `fallback-docx` (degraded, but the degradation is honestly tracked in telemetry).
    `workflow_id`: `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`.
20. **A real, well-built durable-retry outbox (DB-backed, claim/lease/dead-letter) appears to be
    orphaned in favor of a weaker, older JSONL-file mechanism actually driving live traffic.**
    `EV-00116/EV-00117` (supersedes the P2 item this replaced): `daszek_command_outbox_enqueue`'s
    only confirmed caller is a one-time JSONL-migration function with zero confirmed callers of
    its own (3 independent static checks: GitNexus `context` twice, exhaustive repo-wide `rg`).
    Meanwhile the JSONL-backed `bridge_queue.jsonl` store IS confirmed live: written by 3+ REST
    call sites (operator approve/reject of action proposals, `daszek_api_v2_append_action_decision`,
    plus 2 more sites) and drained every worker-loop tick by `gmail-agent`'s
    `maybe_worker_bridge_drain_tick`, via REST fetch/complete — not via the DB table's claim/lease
    API. Whether the DB table is genuinely dead, an incomplete cutover, or reachable through a
    dynamic WordPress hook neither static tool could see, is NOT resolved — stated as an open
    caveat, not a confirmed-dead-code claim. `workflow_id`: `DASZEK-COMMAND-OUTBOX-DRAIN`.
21. **`finalize_case` writes thread memory, next-action, and the case event log as 3 separate,
    non-transactional store calls — a mid-sequence failure leaves state partially updated with no
    rollback.** `EV-00127`: `persist_thread_memory` → `store.upsert_next_action` →
    `self._append_event`, each independently committed (matching the Postgres store's per-call
    `_upsert` pattern, no multi-statement transaction wrapper found). Concrete scenario: if
    `persist_thread_memory` succeeds and `upsert_next_action` then raises, thread memory reflects
    the new message but `next_action`/the event log do not — a real, not hypothetical,
    partial-write gap consistent with the codebase's broader best-effort-no-atomicity pattern.
    `workflow_id`: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`.
22. **The Calendar-triggered `create_action_proposal` flow is confirmed `MISSING_PRODUCER`, not
    merely unconfirmed.** `EV-00131`: `build_calendar_event_action_proposal` (which would create
    an `action_type=create_calendar_event` proposal) has ZERO callers anywhere in gmail-agent, by
    exhaustive repo-wide search. The executor side is genuinely real and conditionally live
    (`execution_runtime.execute_action_proposal` calls the real `calendar_client.create_event()`
    if a `GoogleCalendarClient` is configured) — unlike the confirmed-always-dead Gmail
    label/archive actions — but is unreachable in practice since nothing ever creates the
    proposal it needs, and its own entrypoint is a manual CLI command besides. Reschedule/cancel
    of a visit are similarly confirmed ABSENT by exhaustive name search, not merely unfound.
    `workflow_id`: `CALENDAR-TWO-WORLDS-OF-VISITS`.
23. **A real, well-built pure-time-as-trigger SLA escalation mechanism exists but has no
    confirmed automatic trigger, contradicting its own module docstring.** `EV-00130`:
    `sla_watcher.py` computes genuine wall-clock `hours_waiting` on unresponded proposals
    (4h/24h thresholds) and emits dedup-safe `os_events` — a real, correct mechanism. Its
    docstring claims it "runs as FastAPI BackgroundTask (every 15 min) or CLI --oneshot," but the
    ONLY caller found anywhere is a manual CLI subcommand; no systemd/BackgroundTask/cron wiring
    was found in any deploy config. Same shape as the daszek command-outbox and calendar
    `context_for_case` findings — a real capability that requires a human to remember to run it.
    `workflow_id`: `SLA-WATCHER-DECISION-ESCALATION`.
24. **A registered signal-reconcile handler is structurally unreachable due to a source_kind
    naming mismatch between producer and registry.** `EV-00137` (reverse-audit finding):
    `build_calendar_signal` produces `source_kind="google_calendar"`, but `SIGNAL_HANDLERS` only
    registers `"calendar"` — `_reconcile_calendar_signal` (a real, substantial handler) can never
    be dispatched to for any signal this producer creates. Currently bounded: the producer
    (`CalendarRuntime.ingest_events`) never calls `reconcile_signal` itself anyway (journals
    only), so the mismatch is latent, not a live crash. It WOULD surface as a hard failure if the
    `signal-replay` recovery CLI were ever invoked on a calendar-sourced signal. `workflow_id`:
    `CALENDAR-TWO-WORLDS-OF-VISITS`.

25. **Two of the four specialist sub-agent scopes are structurally unreachable at the only point
    where they would restrict what the planner is offered.** `EV-00140`: at `graph.py:167` —
    executed every turn, before `plan_next_tool` — `select_sub_agent` is called with
    `tool_name=""`, so the `TOOL_SCOPE_MAP` registry lookup can never match and the function can
    only ever return `policy` (when materialize proposals exist) or `general`. The `document` and
    `draft` scopes, and their whole registry-driven narrowing machinery, therefore never
    constrain the offer set. The one call site that DOES pass a real `tool_name` (`graph.py:235`)
    runs after the tool is already chosen and feeds only a telemetry label. Not dead code — it
    runs constantly, it just cannot reach 2 of its 4 branches. `workflow_id`:
    `AGENT-GRAPH-TURN-LOOP`.
26. **The semantic policy envelope measures planner divergence but nothing acts on it.**
    `EV-00141`: `_observe_policy_plan`'s own docstring states it correlates and observes a plan
    "without changing its selected tool/arguments". It writes
    `semantic_policy_plan_consistency` and `decision_divergence_observation` into the snapshot as
    telemetry; no branch anywhere reads them to block, correct, or escalate. Policy DOES genuinely
    steer coarsely (by restricting which tools are offered at all — a hard constraint enforced at
    3 layers), but if the planner picks a tool that diverges from the action the decision pipeline
    actually decided on, that divergence is recorded and ignored. This is the previously
    un-adjudicated `policy → tool enforcement` rule in `ARCHITECTURAL_RULES_AUDIT.md`, now
    resolved. `workflow_id`: `AGENT-GRAPH-TURN-LOOP`.
27. **`ReconcileResult.warnings` reaches the browser but no frontend code ever reads it —
    `MISSING_CONSUMER`, not `MISSING_PROJECTION`.** `EV-00163`: the one real production call site
    (`materialize_bridge.py`'s `reconcile_linked_after_materialize`, invoked from
    `approve_materialize_proposal`) nests `reconcile.warnings` into the return dict, which
    `api_app.py`'s `POST /engagements/{id}/materialize/approve` returns verbatim as the HTTP
    response body, which `daszek/includes/api-v3-handlers.php`'s
    `daszek_api_v2_engagement_materialize_approve` forwards verbatim as the WP REST response —
    reaching `daszek/public/app.js`'s `approveProposalViaApi`/`decideActionProposal`, which reads
    only `decision_key`/`queued.queue_id`/`decision_status` from the response and never touches
    `response.reconcile` or `response.reconcile.warnings`. Any reconcile warning surfaced during a
    materialize-approve (e.g. entity-link ambiguity, projection refresh issues) is silently
    dropped — the operator is never shown it despite the backend explicitly producing it for that
    purpose. The other 11 files matching a `.warnings` search near `ReconcileResult` are confirmed
    false positives (unrelated result types: `AgentRunResult`, `CoherenceResult`, mailbox-memory
    ingest/finalize results, `Neo4jPilotResult`, `PolicyReport`, LLM warnings tray).
    `workflow_id`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`.
28. **A failed `bridge_queue.jsonl` row is not merely un-retried — it is completely invisible to
    the operator, indistinguishable from a success.** `EV-00165`: `drain_bridge_rows` marks any
    exception as `bridge_status='failed'` via a single completion call, with no attempt counter,
    no requeue, and no dead-letter store in either repo. Daszek's own
    `daszek_v2_bridge_queue_completion_ids` treats `'completed'`, `'failed'`, and `'skipped'` as
    identically terminal, so `daszek_v2_bridge_queue_pending_rows` excludes failed rows from
    "pending" exactly like successes. The one operator-facing dashboard metric
    (`daszek_api_v3_system_bridge_queue_summary`, confirmed live in `EV-00164`) only counts
    `pending`/`stuck` rows — a failed row is invisible there too, and an exhaustive grep found no
    `bridge_status='failed'` filter anywhere in Daszek's PHP or frontend JS. A genuinely failed
    HITL-send or action-decision execution disappears from all operator visibility the instant
    the drain marks it failed.
    `workflow_id`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`, `DASZEK-COMMAND-OUTBOX-DRAIN`.
29. **`world_model.py` is not consumer-orphaned after all; it is producer-unwired.**
    `EV-00181` corrects `EV-00176` here: `similar_cases_precedent.py`'s
    `fetch_world_model_precedent_refs` IS called from `fetch_similar_case_precedent_refs_v1`,
    and that v1 precedent chain IS called by `mailbox_memory_runtime.py`. So
    `world_model_insights` has a real conditional reader path. The actual defect is on the
    producer side: exhaustive grep found ZERO callers of `ingest_corpus_message`,
    `ingest_corpus_fact`, `distill_insights_from_corpus`, `fetch_insights`, or
    `update_insight_status`, so `historical_corpus_messages`, `historical_corpus_facts`, and
    the producer/update side of `world_model_insights` are unwired. This remains a real,
    independent learning-loop gap, but it is a `MISSING_PRODUCER`, not a missing consumer.
    `workflow_id`: `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`.
30. **`request_human_handoff` is a real, working handler with zero reachability from anywhere —
    not merely planner-deprioritized, genuinely dead code.** `EV-00177`: registered in `HANDLERS`
    (`agent_runtime/tools/handlers.py:1102`), the handler itself works correctly (sets
    `hitl_gate`/`operational_status`), but it has NO entry in `tool_schemas.py`'s `specs` dict —
    `openai_tool_definitions`'s final filter (`[specs[name] for name in allowlist if name in
    specs]`) silently drops it even if allowlisted. Exhaustive grep confirms the string
    `request_human_handoff` appears nowhere else in the codebase: no schema, no direct/automatic
    call site. The LLM planner can never select it, and nothing else invokes it either.
    `workflow_id`: `AGENT-GRAPH-TURN-LOOP`.
31. **`call_kalk_top_quote`'s OpenAI schema advertises 3 parameters the handler silently
    discards.** `EV-00177`: the schema declares `heated_area_m2`/`location`/`building_type` as
    available (non-required) arguments; the handler signature is
    `def call_kalk_top_quote(_plan: ToolCallPlan, ...)` — explicitly unused — and instead builds
    its entire kalk-top request from `ctx.snapshot.model_dump(...)`. Any value the LLM supplies
    for these 3 fields has zero effect on the actual calculation. Not a crash risk, but a genuine
    schema-honesty defect that could mislead the LLM's reasoning about what it's controlling.
    `workflow_id`: `KALK-TOP-CALCULATE-OFFER-PIPELINE`, `AGENT-GRAPH-TURN-LOOP`.
32. **4 of 5 `MaterializeProposalItem.proposal_type` values have a real, working executor and NO
    confirmed creator anywhere.** `EV-00179`: `link_existing`/`create_case`/`create_artifact`/
    `defer_operator` each have a genuine branch in `execute_materialize_proposal`
    (`create_case` does full case-row creation with email-level dedup; `link_existing` registers
    a real correlation link), and `materialize_bridge.py:246` explicitly treats `create_case`/
    `link_existing` as first-class types for triggering post-approve reconcile — but the only
    confirmed creator function (`append_materialize_proposal`) has exactly one real caller
    (`_proposal_result`, 2 call sites), and BOTH hardcode the literal `"composite_plan"`. Even the
    test/seed fixture only creates `composite_plan`. These 4 types are schema-validated,
    executor-ready, downstream-reconcile-aware, and structurally uncreatable by any live path
    found — a `MISSING_PRODUCER`, not a duplicate of the already-known `learning_rule_candidates`/
    `world_model.py` consumer-side gaps (items 7, 29).
    `workflow_id`: `HITL-PROPOSAL-APPROVAL-DUAL-PATH`.
33. **The agent's `extract_facts_from_text` tool can never update a fact it already recorded —
    the write silently no-ops and reports success.** `EV-00180`: `append_fact_rows` (the sole
    writer behind this tool) uses `ON CONFLICT (fact_id) DO NOTHING`; `_agent_fact_row` computes
    `fact_id` deterministically from `case_id`+`fact_key` only (no message/timestamp component),
    so once a value is recorded for a given case+key pair, any later call — even carrying a
    genuine customer correction from a different message — silently fails to persist, with
    `ToolResult` still reporting success. The main document/message-ingestion pipeline
    (`replace_message_facts`) does NOT have this problem — it deletes-and-reinserts per message,
    correctly superseding old values. This is scoped specifically to the agent-tool write path; a
    data-staleness risk, not a crash risk.
    `workflow_id`: `AGENT-GRAPH-TURN-LOOP`, `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`.

## P2 — confirmed inconsistencies/duplications, no shown harm yet

34. **3 independent implementations of `calendar_risk` computation.** `EV-00016/36/37`: only
    `calendar_runtime.infer_calendar_risk` can emit `customer_proposed_date` (and it's
    CLI-only-reachable, see P0 item 6); `mailbox_memory_runtime.py` and `gmail_intake.py` each
    have their own independent, binary-only (`exists`/`missing`) reimplementations that feed the
    actually-live path.
    `workflow_id`: `CALENDAR-TWO-WORLDS-OF-VISITS`.
35. **`ARCHITECTURE_DECISIONS.md` (2026-07-27) and `brief.md` (2026-07-30) disagree about whether
    the "three action dictionaries" problem is resolved.** `brief.md` frames it as
    `NO_SAFE_MAPPING_EXISTS`; the newer doc claims resolution via `decision_pipeline` +
    `policy_action_proposal`. `EV-00069/70` confirm the 3 dictionaries exist and DO converge at
    `attach_policy_and_proposals`, gated on a real decision candidate — partially supporting the
    newer doc, but full adjudication of whether this fully resolves the older concern was not
    completed this pass.
    `workflow_id`: `AGENT-GRAPH-TURN-LOOP` (cross-cutting; not owned by one workflow_id — the 3
    dictionaries converge in the tool-dispatch/policy layer this workflow represents).
36. **`rag-widget`'s default API URL is a production VPS hostname, not localhost — and the local
    Docker stack provides no automated override.** `EV-00104`, `EV-00172`: the widget IS mounted
    into `docker-compose.daszek-local.yml`, but its `WORDPRESS_CONFIG_EXTRA` defines only Daszek's
    own Node-B constants, no `HVAC_RAG_API_URL`; `.env.daszek-local(.example)` has zero references
    to it either. The widget maps this constant to a WP option (`hvac_rag_chat_api_url`), so an
    operator COULD set it manually via wp-admin — whether that manual step was ever taken is
    outside any file this reconstruction can inspect, genuinely `RUNTIME_UNVERIFIED` rather than
    resolved either way.
    `workflow_id`: `RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE`.
37. **GraphRAG's ingest-time community-summary enrichment is dead code — zero callers anywhere.**
    `EV-00161`: `ingest/community_summaries.py:build_community_summary` is never invoked by the
    ingest pipeline or any other module (exhaustive grep confirmed). The retrieval-side GraphRAG
    split (`graphrag/__init__.py` re-exporting `application/services/graph_query_builder.py` and
    `retrieval_plan_executor.py`) IS live via `agentic_graph.py`/`domain/pipeline.py`/
    `services/chat_service.py`, so query-time GraphRAG works; it can just never benefit from
    community-level summarization because nothing builds or persists those summaries. Not a
    crash-risk defect, but likely unintentional given the retrieval side expects it.
    `workflow_id`: `RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE`.

## P3 — asymmetries and observations worth tracking

38. Fast-kalk's public "price" is always a fuzzed ±range (0.93x/1.16x) around kalk-top's real
    computed gross total — intentional business behavior, not a defect, but worth knowing when
    reasoning about "what price did the customer actually see." `EV-00093`.
    `workflow_id`: `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`.
39. `/identity/merge` is the only route in `api_app.py` carrying FastAPI's native
    `deprecated=True` flag — a self-documented example of how the rest of the dead/legacy surface
    is NOT similarly marked. `EV-00112`.
    `workflow_id`: none specific — an `api_app.py` route-inventory-level observation, see
    `ENTRYPOINT_INVENTORY.md`, not tied to one registered workflow.
40. The "best-effort, no durable retry" pattern recurs consistently across the whole system
    (Daszek feed push, Daszek v1/v2 push lineage, fast-kalk↔gmail-agent telemetry, kalk-top's
    presumed os-event client) — a genuine, consistent architectural choice, not scattered
    oversights. Worth naming explicitly as a design principle to either ratify or revisit
    deliberately, rather than continuing to discover it piecemeal. **New confirmed instance
    (`EV-00122`)**: individual Gmail signal ingestion failures (`gmail_fetch`/`gmail_reconcile`
    stages in `signal_worker.py`) get exactly one attempt each, no retry/requeue — distinct from
    and weaker than the poll-level list-API retry, which IS real (bounded backoff +
    circuit-breaker). Also distinct from and weaker than the DASZEK-COMMAND-OUTBOX-DRAIN
    correction (`EV-00116/117`) — three now-confirmed "no real retry where you might assume one"
    findings in one session reinforce this as the dominant pattern, not the exception.
    `workflow_id`: `DASZEK-FEED-PUSH-NO-RETRY`, `DASZEK-COMMAND-OUTBOX-DRAIN`,
    `GMAIL-SIGNAL-WORKER-LOOP` (cross-cutting pattern, spans multiple workflows).

## P2 addenda — EV-00182

41. **Cieplo's `FAILED_FINAL` state is not final in the actual recovery contract.**
    `EV-00182`: both the authenticated retry endpoint
    (`topinstal_cieplo_worker/api/routes.py:retry_workflow`) and the internal
    `workflow.row_updates.should_retry_workflow` helper explicitly accept
    `WorkflowState.FAILED_FINAL` as retryable, alongside `FAILED_RETRYABLE` and `PDF_READY`.
    Impact: the status name overstates terminality and can mislead an operator or consumer into
    treating the row as irrecoverable when the code deliberately allows manual re-drive.
    `workflow_id`: `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`.
42. **`top-instal-generator` reports `status='success'` even when PDF generation degraded to
    DOCX fallback after conversion failure.**
    `EV-00182`: `GenerateOfferDocumentUseCase` always returns top-level `status='success'` on a
    document result payload; when PDF conversion fails it only switches `meta.converter` to
    `fallback-docx` and appends a warning (`FALLBACK_DOCX_RETURNED`). Impact: any consumer reading
    `status` alone will classify a degraded DOCX fallback as a full PDF success. This is not a
    silent failure because the warning exists, but it is a real status-contract ambiguity.
    `workflow_id`: `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`.

## P2/P3 addenda — EV-00183

43. **Operational-feed ingest persists `validation_warnings`, but Daszek never shows them to the
    operator.**
    `EV-00183`: `daszek_v3_validate_operational_feed_desk_note_refs` mutates the ingested payload
    with `validation_warnings` when desk `note_id` references are missing from the v2 store; the
    full snapshot is then upserted. Exhaustive grep of `daszek/public/app.js` found no reader for
    `validation_warnings`, so referential-integrity warnings are transport-live but UI-invisible.
    Impact: Daszek can detect a degraded projection but present a clean operator surface with no
    warning banner or badge.
    `workflow_id`: `DASZEK-FEED-PUSH-NO-RETRY`.
44. **`feed.quality_readonly` is contract-valid and stored, but currently has no frontend
    consumer.**
    `EV-00183`: `build_operational_feed_snapshot(... quality_readonly=...)` and both Python/PHP
    validators support `feed.quality_readonly`, yet no `app.js` reader was found. This is a live
    transport/persistence path with an absent UI surface, so the slice is effectively dormant from
    the operator's perspective.
    `workflow_id`: `DASZEK-FEED-PUSH-NO-RETRY`.

## P2 addendum — EV-00184

45. **The effective `AGENT_RUNTIME_ENABLED` branch depends on loader order, not only on one
    stable configuration truth.**
    `EV-00184`: in one process, `load_agent_runtime_settings()` returned `enabled=false` before
    `config.load_settings()` and `enabled=true` after it. Root cause: `config.load_settings()`
    mutates `os.environ` through `apply_case_os_runtime_profile_overrides()`, while
    `agent_runtime.settings.load_agent_runtime_settings()` reads raw env directly and does not
    apply the same profile logic. Impact: helpers such as `agent_runtime_reconcile_active()` and
    `daszek_engagement_feed.engagement_feed_source_enabled()` can choose different runtime/feed
    branches for the same workspace depending only on whether `load_settings()` ran first.
    `workflow_id`: `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`, `DASZEK-FEED-PUSH-NO-RETRY`.

## P2 addendum â€” EV-00186

46. **Cross-repo consumers misclassify generator DOCX fallback as PDF-ready success.**
    `EV-00186`: `top-instal-generator` can return top-level `status='success'` with
    `document.format='docx'` and `meta.converter='fallback-docx'`
    (`GenerateOfferDocumentUseCase.php:181,203-217,240-255`). Both reopened downstream consumers
    ignore that discriminator: `fast-kalk` `class-offer-dispatch.php:152-165` reads only
    `downloadUrl` inside helper `generate_pdf()`, while `cieplo-orchestrator`
    `workflow/runner.py:309-311` stores the same URL into `pdf_download_url` and advances straight
    to `WorkflowState.PDF_READY`. Impact: the producer honestly reports degraded DOCX fallback,
    but at least two consumers continue as if PDF readiness were proven, creating state/contract
    drift across repos.
    `workflow_id`: `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`,
    `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`,
    `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`.

## Explicitly NOT included here (would need `DOMAIN-COMPLETENESS-REVISIT` or further work first)

- Anything from the `DOMAIN-COMPLETENESS-REVISIT` queue (`PROGRESS.md`) that hasn't produced a
  confirmed finding yet — e.g. reject-path execution (`adjudication_executioner`, `EV-00114`,
  found but not traced), `pattern_learner.py` internals, `rag-chat-asystent`'s own pipeline.
- A full mechanical reverse-audit (producer↔consumer, event emitter↔handler, feature
  flag↔active branch) across all 9 domains — only spot-checks were performed this pass, not the
  exhaustive version the target mandates before final completion.

## P2 addendum - EV-00187

47. **`fast-kalk` has no direct automated test file for the full lead -> calculate -> register -> dispatch chain.**
    `EV-00187`: the mechanical candidate scan found only script/harness assets
    (`scripts/e2e-scenarios-smoke.php`, `local-rest-smoke.php`, `os-event-w2-harness.php`,
    `buffer-hydraulics-smoke.php`, `repro-calculate-502.php`), plus bootstrap helper
    `configure-local.php`. No direct unit or integration test file was found for the canonical
    public workflow that crosses widget intake, kalk-top calculation, Node-B registry links, and
    generator dispatch. Impact: a critical cross-repo revenue path currently depends on ad hoc
    smoke/proof scripts instead of a stable direct automated gate.
    `workflow_id`: `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`.
48. **`cieplo-orchestrator`'s mocked E2E workflow test is currently non-executable because it fails at collection time.**
    `EV-00187`: fresh local run of `pytest tests/test_workflow_e2e_mocked.py -q` exited `1`
    before any scenario ran, due to a circular import between `ingress.processor` and
    `workflow.repository`. The repo still has unit/event tests and a manual one-email script, but
    the named mocked E2E artifact cannot currently serve as execution proof. Impact: the workflow
    advertises an end-to-end-like test surface that is presently broken, leaving only unit/synthetic
    coverage plus manual proof for this path.
    `workflow_id`: `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`.
