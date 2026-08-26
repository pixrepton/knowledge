# Backlog

Status: active only. Last updated: 2026-08-26 (Cieplo production incident formally closed).

This file is not a proof history or phase archive. Canonical plan + residual narrative: `knowledge/docs/AI_OS_ROADMAP.md`.

## Current residual status

```text
AI_OS_INFRASTRUCTURE_CLEANUP = COMPLETE_LOCAL
CAPABILITY_PROGRAM_READINESS = GO
OPERATOR-COMMAND-RECONCILE-BYPASS-01 = CLOSED
REQUIRED_OPEN = 0
UNKNOWN_NEEDS_PROOF = 0
TASK_ENGINE_ACTIVE = 0
CIEPLO_PRODUCTION_REPAIR_20260826 = CLOSED / DEPLOYED / PROD_PROVEN
CIEPLO_WORKFLOW_POLICY_PROBLEM = CLOSED
CIEPLO_DUPLICATE_RETRY_PROBLEM = CLOSED
CIEPLO_DEPLOYMENT_IDENTITY = CLOSED
CIEPLO_2ZAHE_RECOVERY = REVIEW_REQUIRED / NO_AUTO_REPLAY
CONVERTER_VPS_HARDENING_CLOSEOUT_20260825 = CLOSED
CIEPLO_ORCHESTRATOR_DIRTY_STATE = CLEAN
TOP_INSTAL_GENERATOR_DIRTY_STATE = CLEAN
GMAIL_AGENT_DIRTY_STATE = HOST_WORKTREE_PHANTOM / NO_CONTENT_DIFF / NOT_ACTIVE_WORK
FRESH38_MEASUREMENT_QUALIFICATION = REQUALIFIED
FULL FRESH38 AGAINST CURRENT CODE = RUN (2026-08-16, 38/38 capture QUALIFIED)
CURRENT CAPABILITY BASELINE = 27 CLEAN_PASS / 11 CAPABILITY (v5, threshold 34) → NOT QUALIFIED — CAPABILITY
P2_CAPABILITY_CAUSAL_OBSERVABILITY = PASS / CLOSED
CAPABILITY-OBSERVABILITY-01 = CLOSED
P4_VS_P3B_FORK = CLOSED
SVC-05 = CLOSED
SVC-05_PRODUCT_FIX = PASS
SVC-05_DOWNSTREAM_FIX = PASS
SVC-05_FINAL_PROVIDER_LIVE_PROOF = PASS
AGENT_OPERABILITY_CONVERTER_CIEPLO_20260824 = CLOSED
PROCEDURAL_MEMORY_TOPINSTAL_PROD_20260825 = CLOSED
AIOS_AGENT_BEHAVIOR_SUITE_20260825 = CLOSED
DEPLOY_CIEPLO_VPS_20260824 = SUPERSEDED_AND_ARCHIVED
LOCAL_VERIFY_CIEPLO_DEFAULTS_PRICE_20260825 = ABORTED_WITH_EVIDENCE_AND_ARCHIVED
LOCAL_VERIFY_RECENT_CIEPLO_CALENDAR_20260825 = ABORTED_WITH_EVIDENCE_AND_ARCHIVED
NEXT = STOP
INTELLIGENCE_SPINE_1_2_3_END_TO_END_PROVEN = PASS (bounded)
UNTRUSTED_INPUT_EXECUTION_BOUNDARY = CLOSED
REAL_MAIL_INTELLIGENCE_DISCOVERY_01 = PARKED_DATASET_REQUIRED / NOT_CURRENT
AI_OS_INTELLIGENCE_ARCHITECTURE_AUDIT = PAUSED_HISTORICAL / NOT_CURRENT
FAST_KALK_SCOPE_DIVERSION_COMMIT_832DEA8 = PARKED_BY_OPERATOR / EXPLICIT_DISPOSITION_PENDING / NOT_BLOCKING_STRATEGIC_NEXT
OFFER_CASE_OS_OBSERVABILITY_01 = NEXT_APPROVED / NOT_STARTED
GLOBAL_CASE_FACT_MODEL = OPEN / LATER
REAL_CASE_CONDUCT_BENCHMARK = OPEN / LATER
ARCHITECTURE_INTELLIGENCE = OPEN / LATER
NEXT = OFFER_CASE_OS_OBSERVABILITY_01
```

| ID                                        | Area                       | Status                      | Next action                                                                                                                                                                                                                                                                                                                                               |
| ----------------------------------------- | -------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `OPERATOR-COMMAND-RECONCILE-BYPASS-01`    | gmail-agent                | **CLOSED**                  | `run_operator_command_spine()` now routes newly appended operator commands through `reconcile_signal()`/registered `operator_command` handler; Gate A gmail-agent passed with 0 failed.                                                                                                                                                                   |
| `FRESH38-CAPABILITY-11-ANALYSIS-20260816` | gmail-agent                | **CLOSED**                  | P2 CLOSED. P3A COMPLETE (`EVALUATOR_WRONG` K3). P4-A MI-02, P4-B SVC-05, P4-C CTX-03 and P1.4B closed; no full Fresh38. SVC-05 CLOSED: PRODUCT_FIX PASS (`0a407cb3`), DOWNSTREAM_FIX PASS (`78603fb`), FINAL_PROVIDER_LIVE_PROOF PASS (`70c3d94`; SVC-05/SVC-02/MI-03 3/3 QUALIFIED). Sequence: `eval/mail-agent-intelligence-current/P4_VS_P3B_FORK.md`. No case-id evaluator exceptions. |
| `FRESH38-L0-REPAIR-COMMIT-20260816`       | workspace                  | **CLOSED**                  | L0 repair committed `4210ed5` (workspace, LOCAL_ONLY): `scripts/run_fresh38_case_batch.ps1` + `scripts/tests/test_fresh38_engine_lifecycle_channel.ps1` (incl. behavioral 231 scenarios).                                                                                                                                                                 |
| `INTELLIGENCE-SPINE-1-2-3`                | gmail-agent / knowledge     | **CLOSED_BOUNDED**          | `gmail-agent:3469dbd`, `7fc257b`, `c80be17`; `knowledge:7d2fa39`, `cbf0cda`. Proven invariants: customer/mail ToolEnvelope preservation, execution rejection of semantic drift, decision-safety metadata preservation, dependent action blocked on conflicted critical fact, independent action remains legal. Not a live autonomy claim and no Full Fresh38. |
| `UNTRUSTED-INPUT-EXECUTION-BOUNDARY-01`   | gmail-agent                 | **CLOSED**                  | `gmail-agent:2e1d95b` adds a central pre-execution boundary: inbound mail/attachments remain evidence, not authority; action tools fail closed on untrusted authority arguments or recipient override, while read-only tools remain unaffected. Proof: boundary 4 passed; spine/planner 36 passed; write-lock/tool contract 12 passed; py_compile/diff-check PASS. |
| `REAL-MAIL-INTELLIGENCE-DISCOVERY-01`     | gmail-agent / knowledge     | **PARKED_DATASET_REQUIRED / NOT_CURRENT** | `gmail-agent:a3d3ae6` adds `gmail_intake.py real-mail-discovery`: file-only/no-side-effect JSON/JSONL harness, no Gmail fetch, no LLM calls, no outbound actions, formal `DISCOVERY_QUALIFIED` only for 10-15 labelled historical cases. Not the current approved step during the closeout sweep. |
| `INTELLIGENCE-SPINE-P0-CAD`               | gmail-agent / knowledge     | **CLOSED**                 | P0 closeout 2026-08-21: Delivery COMPLETE, Proof PASS_LOCAL_BOUNDED, Full Gate A PASS (0 failed), Semantic Conservation ENFORCED, First CAD slice PROVEN (ask_for_missing_data/customer/mail). Commits: knowledge:121dde29; gmail-agent:38797c7, c47f8c2, 45a41fa, d12e087, b5c90a1, ccbe5c6, 4e6ec55. semantic_hash propagowany CAD->ActionPlan->NBA->APv2->PolicyActionEnvelopeV1.source_semantic_hash->ToolCallPlan.semantic_hash->ActionItem; guard fail-closed (canonical_semantic_drift). Bounded proof: `.artifacts/intelligence-spine-p0-closeout-20260821T193158/bounded-runtime-trajectory.json`. Residuale -> P0.5 (untrusted input/prompt injection), P1 (DecisionRevisionRequest runtime, unknown-vs-inferred, multi-intent, argument-level ToolEnvelope), P2 (SystemCapabilityState, cost aggregation, legacy cleanup, replay CLI). FULL_FRESH38 NOT_RUN. |
| `INTELLIGENCE-SPINE-P0-5`                 | gmail-agent / knowledge     | **CLOSED**                 | P0.5 DATA vs AUTHORITY HARDENING 2026-08-21: Delivery COMPLETE, Proof PASS_LOCAL_BOUNDED, Full Gate A PASS (2715/15/24/0). Wspólny kontrakt provenance `evidence_authority.py` (source_origin/evidence_authority/instruction_authority); enforcement w `untrusted_input_boundary.py` (UNTRUSTED_AUTHORITY_OVERRIDE, UNTRUSTED_RECIPIENT_OVERRIDE, UNTRUSTED_APPROVAL_CLAIM, CANONICAL_ARGUMENT_MISMATCH); planner context Data vs Authority. Commits: gmail-agent 896c5c6, 604c9e2, 3c8f452. Deterministic adversarial suite A-J + metamorphic (51 tests). Provider micro-cohort n=6 (DeepSeek): forbidden_tool_attempt_rate=0.0, executed_policy_violation_rate=0.0. Artefakty: `.artifacts/intelligence-spine-p0-5-20260821T194500/`. P1 NOT_STARTED. |
| `INTELLIGENCE-SPINE-P1-1`                 | gmail-agent / knowledge     | **CLOSED**                 | P1.1 DECISION REVISION RUNTIME 2026-08-22: Delivery COMPLETE, Proof PASS_LOCAL_BOUNDED, Full Gate A PASS (0 failed). DecisionRevisionRequest -> canonical re-evaluation -> CAD r2; identity decision_id/revision/decision_version_id/semantic_hash; supersession r1 SUPERSEDED; stale invalidation STALE_DECISION_REVISION; approval version binding; expected_revision/duplicate guard; audit trail w DecisionRevisionLedger. Commits: gmail-agent 42440af, 5f0979d, e42f774, 99ae4e8. Artefakt: `.artifacts/intelligence-spine-p1-1-20260822T100000/bounded-revision-trajectory.json`. P1.2-P1.5 NOT_STARTED. |
| `INTELLIGENCE-SPINE-P1-1P`                | gmail-agent / knowledge     | **CLOSED**                 | P1.1P DURABLE REVISION STATE 2026-08-22: Delivery COMPLETE, Proof PASS_LOCAL_BOUNDED, Full Gate A PASS (2772/17/24/0). Decision revision lineage persisted in existing MailboxMemoryStore (2 tables in the same store, no new DB); ledger = projection/cache with rebuild() + fail-closed (0 or >1 CURRENT -> rebuild_one_current_violation; ordering by revision integer, never timestamp); accept transition atomic (old SUPERSEDED / new CURRENT / request ACCEPTED). Final runtime closeout: worker boot wiring ENFORCED — `MailboxMemoryRuntime.bootstrap()` rebuilds store-backed ledger via `build_store_backed_decision_ledger()`; invalid durable state fails closed with reason code REVISION_STATE_INVALID (DecisionRevisionStateInvalidError); real Postgres runtime proof PASS on local canonical mailbox-memory test DB (worker restart round-trip, atomic one-CURRENT, stale r1 guards after restart). Commits: gmail-agent f57028ea, b13945d0. Artefakty: `.artifacts/intelligence-spine-p1-1p-20260822T110000/restart-trajectory.json`, `.artifacts/intelligence-spine-p1-1p-final-20260822T120000/p1-1p-postgres-worker-restart.json`. P1.2-P1.5 NOT_STARTED. |
| `INTELLIGENCE-SPINE-P1-2`                 | gmail-agent / knowledge     | **CLOSED**                 | P1.2 ARGUMENT-LEVEL TOOL ENVELOPE 2026-08-22: Delivery COMPLETE, Proof PASS_LOCAL_BOUNDED, Full Gate A PASS (2851/17/24/0; P1.2A + P1.2B). First enforced argument slice ask_for_missing_data/customer/mail -> generate_draft_reply: typed ArgumentConstraint (EXACT/ONE_OF/SUBSET_OF/PRESENT/ABSENT/PLANNER_GENERATED) projected into PolicyActionEnvelopeV1.argument_constraints; reference monitor validates plan.arguments (intent ONE_OF missing_info; ABSENT case_id/target/channel/recipient/required_information/attachment_ids/approval_receipt/draft_hash; unknown -> ARGUMENT_NOT_ALLOWED); durable-current envelope check via P1.1P ledger (stale -> STALE_DECISION_REVISION); new revision -> new constraint projection; tool schema unchanged (intent-only); no provider-live needed. Fixed pre-existing MetricsCollector flush deadlock (RLock) + regression guard; golden schema regenerated. Commits: gmail-agent 950f9670, 4cc7595a, 5b68efff. P1.2B post-HITL/write binding (write_argument_binding.py, WriteBoundaryDeniedError, bridge wiring) Gate A 2851/17/24/0, LIVE_SEND=false. Artefakty: `.artifacts/intelligence-spine-p1-2-20260822T130000/p1-2-argument-flow-audit.json`, `bounded-argument-trajectory.json`. P1.3-P1.5 NOT_STARTED. |
| `INTELLIGENCE-SPINE-P1-3`                 | gmail-agent / knowledge     | **FROZEN**                 | P1.3 EPISTEMIC CORRECTNESS 2026-08-22: Delivery COMPLETE, Proof PASS_LOCAL_BOUNDED, Full Gate A PASS (0 failed). Per-proposition epistemic status (CONFIRMED/INFERRED/UNKNOWN/CONFLICTED) w llm_contracts/epistemic_claims.py + deterministyczna projekcja agent_runtime/epistemic_projection.py (CONFIRMED wymaga evidence ref + brak conflictu; INFERRED wymaga inference_basis; UNKNOWN bez wartosci/podstawy; CONFLICTED nigdy CONFIRMED). DraftClaimContext zasila generate_draft_reply (potwierdzenie CONFIRMED + pytania tylko o UNKNOWN); evaluate_draft_epistemic_sanity (UNKNOWN_AS_CONFIRMED / INFERRED_AS_CONFIRMED / CONFLICTED_FACT_ASSERTED / CONFIRMED_WITHOUT_EVIDENCE / UNSUPPORTED_CUSTOMER_FACT) przez evaluate_draft_sanity(epistemic_context=...). Nowe CONFIRMED evidence -> legalna rewizja CAD przez P1.1 (r2, semantic_hash recomputed). Provider-live NOT required (draft deterministyczny). Commit: gmail-agent 6cd3ab10. Artefakty: `.artifacts/intelligence-spine-p1-3-20260822T150000/p1-3-epistemic-flow-audit.json`, `bounded-epistemic-trajectory.json`. FREEZE 2026-08-22: status FROZEN/COMPLETE/PASS_LOCAL_BOUNDED; explicit non-guarantees + residuals (free-text fabrication -> P1.5, LLM-composed wording -> future slice, fact consolidation -> P1.5, multi-intent -> P1.4) w docs/AI_OS_INTELLIGENCE_SPINE_CONTRACT.md (sekcja P1.3 FREEZE); freeze guard REOPEN_P1_3. P1.4-P1.5 NOT_STARTED. |
| `INTELLIGENCE-SPINE-P1-4`                 | gmail-agent / knowledge     | **CLOSED**                 | P1.4 MULTI-INTENT 2026-08-22: Delivery COMPLETE, Proof PASS_LOCAL_BOUNDED, Full Gate A PASS (0 failed). Kontrakt llm_contracts/customer_intents.py (CustomerIntent/CustomerIntentProjection; service_problem/schedule_service/document_request/other; READY/NEEDS_INFORMATION/BLOCKED/INFORMATIONAL_ONLY; authority NONE/HITL_ONLY/DRAFT_ONLY) + deterministyczna projekcja agent_runtime/intent_projection.py (kanonizacja, dedupe, stabilna kolejnosc, shared required-info mapping, primary actionable intent). BusinessReasoning addytywny customer_intents; Understanding -> build_case_understanding_projection -> CaseUnderstandingProjection.customer_intents. Multi-intent kompozytor generate_draft_reply (>1 intent; single legacy byte-stabilny), ActionItem.intent_coverage, guardy MULTI_INTENT_DROPPED / INTENT_REQUIRED_INFO_NOT_REQUESTED / INTENT_EXECUTION_ASSERTED_WITHOUT_EVIDENCE / INTENT_FALSELY_COMPLETED fail-closed. CAD single-action zachowany; write intenty HITL_ONLY; P1.3 regression PASS. Commit: gmail-agent f29e1ac0. Artefakty: `.artifacts/intelligence-spine-p1-4-20260822T160000/p1-4-multi-intent-flow-audit.json`, `bounded-multi-intent-trajectory.json`. CLAIM CORRECTION 2026-08-23: RAW_INBOUND_MULTI_INTENT_DETECTION = NOT_BEHAVIORALLY_PROVEN (proof zaczyna sie na seamy projekcji/wiringu; intenty wstrzykiwane jako gotowe customer_intents[]); PROVEN = strukturalna reprezentacja/preservation/coverage/guardy/authority; NOT PROVEN = raw inbound extraction, provider recall/completeness, primary prioritization quality, free-text detection. MULTI_INTENT_DROPPED chroni intent obecny w CustomerIntentProjection, nie wykrywa intentu, ktorego Understanding/BR nie utworzylo. Residual: RAW-INBOUND MULTI-INTENT DETECTION EVALUATION (przyszly provider-live/behavioral cohort; osobny item, nie P1.5). P1.5 NOT_STARTED. |
| `INTELLIGENCE-SPINE-P1-5`                 | gmail-agent / knowledge     | **CLOSED**                 | P1.5 + P1.5B SUBJECT-AWARE PROPOSITION IDENTITY 2026-08-23: Delivery COMPLETE, Proof PASS_LOCAL_BOUNDED, Full Gate A PASS (0 failed) na finalnym HEAD; SPINE_CORE PASS; real Postgres restart proof PASS. Kanoniczny owner: MailboxMemoryStore (InMemory+Postgres) + shared resolver `mailbox_memory.facts` / `split_conflicting_facts`; identity rozdzielona na evidence identity != subject identity != proposition identity. Subject-aware proposition identity = `(subject_kind, subject_id, fact_key)`; `entity_scope` nie jest truth identity proposition, a `message_id` / `document_id` / `source_ref` pozostają evidence only. Bounded SubjectRef: `kind={CASE,CUSTOMER,PROPERTY,DEVICE,SERVICE_EVENT}`, `resolution={EXPLICIT,SINGLE_SUBJECT_DEFAULT,AMBIGUOUS}`. Same-subject cross-source same-value -> one proposition + preserved per-evidence provenance/authority; different subjects -> zero false conflicts; ambiguous subject -> fail-closed + persistence through Postgres reload; legal supersession stays subject-local. Producer wiring: mail/customer, structured attachments, document intelligence, drive promotion, case/internal writes all stamp subject metadata via `attach_subject_metadata`. Artefakty: `.artifacts/intelligence-spine-p1-5-20260823T100000/p1-5b-subject-taxonomy-audit.json`, `bounded-subject-identity-trajectory.json` (22 assertions PASS). Residuale: value normalization on write, behavioral extraction, raw inbound multi-intent detection. P1.3 FROZEN; P1.4 COMPLETE; P1.5B CLOSED. |
| `TASK-ENGINE-SCOPE-UPDATE`                | workspace (scripts)        | **CLOSED**                  | `workspace:7696a26` adds supported `task-scope-add`, `task-adopt-path`, and `task-next-clear` operations with validation, ownership safeguards, audit trail and checkpoint integration. Focused task-engine tests 31 passed; `agent_harness_audit` and `agent_map_audit` passed. |
| `CODING-AGENT-HARNESS-OPTIMIZATION`       | workspace (scripts)        | **CLOSED**                  | Harness ergonomics 2026-08-23: `task-gate --profile <name>` (repo-scoped pytest profiles: P1_MULTI_INTENT, P1_EPISTEMIC, SPINE_CORE, HITL_WRITE, FULL_GATE_A), gate-level `--timeout` z owned-process-tree termination i always-on UTF-8 gate logs, `task-finalize` (deterministyczna orchestracja commit/close; nie omija gate, nie adoptuje cudzych zmian, nie pushuje, nie wymusza commita), `scripts/ai_os_proof_artifact.py` (ProofArtifact: record/assert_invariant/write, redaction). Commit: `workspace:28ad25d5` (LOCAL_ONLY). Testy: 7 gate hardening + 4 finalize + 5 proof + 5 profiles; HARNESS_FOCUSED PASS; audits PASS. MCP: bez zmian (DO_NOT_BUILD duplikatow). |
| `CAPABILITY-OBSERVABILITY-01`             | gmail-agent (eval capture) | **CLOSED**                  | P2 bounded minimum delivered: `draft_path_observability.v1` nested in reply jsonl; runner projects `reply_recommended`, `review_required`, `causal_observability`. INT-01 current reproduction NO; SVC-05 current chain classifiable (`SKIPPED_PRE_DRAFTER`). Not a product-semantics change.                                                             |
| IQ-01-ADJUDICATED                         | eval                       | **CLOSED_NOT_REQUIRED**     | Do not fabricate human-adjudicated labels. IQ-01 is already `COMPLETE_BOUNDED`: synthetic 13/13 PASS plus frozen dual-score on pinned Fresh38 capture with `machine_proposed` labels only. Future human/business labels move to `REAL-MAIL-INTELLIGENCE-DISCOVERY-01`, where real historical cases provide the right label source. |
| GOV-06                                    | knowledge                  | **CLOSED**                  | `.serena/project.yml` is tracked as safe read-only project policy; local `project.local.yml`, memories, cache and logs remain ignored. Serena CLI presence and docs gates verified.                                                                                                                                                                      |
| `AI-OS-INTELLIGENCE-ARCHITECTURE-AUDIT`   | gmail-agent / knowledge    | **PAUSED_HISTORICAL / NOT_CURRENT** | The mixed `01a02cf4...` / `01a022e8...` continuation was discovery/planning only. It is not the current approved step and should not be reopened automatically during closeout work. |
| `FAST-KALK-COMMIT-832DEA8`                | fast-kalk                  | **EXPLICIT_OPERATOR_DISPOSITION_PENDING** | `832dea8` is the known scope-diversion PDF/OfferDTO/mail parity commit on top of the four requested fast-kalk fixes. Keep it classified separately from the bounded four-fix proof and decide explicitly whether to keep or revert it. |
| `OFFER-CASE-OS-OBSERVABILITY-01`          | gmail-agent / cieplo-orchestrator / knowledge | **NEXT_APPROVED / NOT_STARTED** | Next strategic step after the Cieplo administrative closeout. Goal: make Case OS canonically observe the stabilized offer lifecycle facts from lead received through calculation, OfferDTO, PDF, internal review, customer send/hold, revision and response. Do not start implementation until the Cieplo closeout writeback task is closed. |

**Superseded (2026-08-16):** `FULL FRESH38 AGAINST CURRENT CODE = NOT_RUN` and
`CURRENT CAPABILITY BASELINE = NOT_REQUALIFIED` — replaced by the requalified measurement and
the v5 capability baseline above. Historical baselines (13 Aug 23/15, 08 Aug 10/28) remain
historical evidence, not the current baseline.

## Closeout sweep notes (2026-08-25)

- `AGENT-OPERABILITY-CONVERTER-CIEPLO-20260824`, `PROCEDURAL-MEMORY-TOPINSTAL-PROD-20260825`, and `AIOS-AGENT-BEHAVIOR-SUITE-20260825` were formally closed after refreshing stale close-gate fingerprints where needed.
- `DEPLOY-CIEPLO-VPS-20260824` is historical only: its blocker was later resolved by the completed converter operability closeout, so the checkpoint was archived as superseded instead of kept active.
- `LOCAL-VERIFY-CIEPLO-DEFAULTS-PRICE-20260825` and `LOCAL-VERIFY-RECENT-CIEPLO-CALENDAR-20260825` were archived as `ABORTED_WITH_EVIDENCE`; both remained unstarted verification stubs.
- `CONVERTER-VPS-HARDENING-CLOSEOUT-20260825` is closed locally by `top-instal-generator:79b2774e0200801b52b237d3b41203ea34bc4b82`; fresh proof: `bash -n converter-vps/scripts/production-smoke.sh` and `docker compose -f converter-vps/docker-compose.yml --env-file converter-vps/.env.example config` both PASS.
- `cieplo-orchestrator` and `top-instal-generator` are now clean. The earlier dirty test slices were explicitly cleaned as stale/non-current work.
- Remaining `gmail-agent` worktree dirt is not a live implementation slice: `git diff` is empty, blob SHAs match HEAD, and the residue behaves like a host/EOL worktree phantom rather than an active code change.

## Cieplo production incident closeout (2026-08-26)

- `CIEPLO-PROD-REPAIR-20260826` is formally closed in task-engine after refreshing stale close-gate fingerprints on the final `cieplo-orchestrator` HEAD.
- Production code and runtime identity are unified at `cieplo-orchestrator:4aba5afcbf5b90aafc77f3708db53d7fcf100bfa`; VPS runtime reports the same revision via `/opt/topinstal/cieplo-worker/REVISION` and `cieplo-worker version --json`.
- Closed defects: `4b99a23` customer-send policy overblock, terminal workflow retry loop, duplicate downstream execution after terminal poll, and split deployment revision markers.
- Proof: local full suite `python -m pytest -q` = `121 passed`; production preflight DB/Gmail/kalk-top/generator/SMTP OK; `cieplo-worker.timer` enabled/active; worker oneshot `0/SUCCESS`; repeated poll of `2zahe` produced no additional calculation, generator/PDF, SMTP or workflow events.
- Recovery: workflow `1ff01a40-c642-4abd-b8b7-a1a0b6369c32` / result `2zahe` is held as `REVIEW_REQUIRED / MANUAL_REVIEW_REQUIRED`; no automatic customer replay was performed because the historical row predates per-channel send markers.
- No active Cieplo problem remains for workflow policy, duplicate retry, or deployment identity. Broader `Offer -> Case OS observability` remains a separate next strategic task.

**Non-blocking harness notes (audit `AI-OS-FINAL-INFRA-CLOSEOUT-01`, not tracked as gating residuals):** gmail-agent `tests/test_aios_canonical_runtime_ingress.py` has no `MAILBOX_MEMORY_TEST_DATABASE_URL`-style skip gate unlike its Postgres-test siblings (unconditional live-DB dependency; ~140s of Gate A wall-clock, fails ungracefully instead of skipping when DB is briefly down); rag-chat-asystent `backend/engine.py:79` ORs `PYTEST_CURRENT_TEST` into `use_fake_embeddings`, so a test trying to opt into real embeddings via `USE_FAKE_EMBEDDINGS=0` silently still gets fake ones unless it also `monkeypatch.delenv("PYTEST_CURRENT_TEST")`; `daszek_engagement_feed/desk.py:58` has a dead-by-coincidence membership gate (`DESK_OPERATIONAL_CODES` happens to equal the full `OperationalStatus.code` Literal today — reactivates silently if a status code is ever added without updating both).

**RAG staged activation:** `STAGED_ACTIVATION_EXECUTED` (see `OPERATOR_DECISIONS.md`). Allowlist `technical_manual,price_list` only. **No** global `RAG_CORE=v2`.

**4.4 Install-prep:** `REJECTED_BY_OPERATOR / NO PRODUCT ACTIVATION` — scaffold may exist; do not develop.

## Closed — RAG-V2-FINAL-TECHNICAL-GATE-01 (2026-08-08)

| ID                             | Disposition             | Note                                                                                                                                                                                                                 |
| ------------------------------ | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RAG-V2-FINAL-TECHNICAL-GATE-01 | COMPLETE / proven_local | Closed `RAG-TEMPORAL-COMPLETE-01` + `RAG-IMAGE-BAKE-01`; container-only Gate B; dual-read; staged activate/rollback/restore; proof `eval/rag-v2-final-technical-gate-20260808/`; status `STAGED_ACTIVATION_EXECUTED` |
| RAG-TEMPORAL-COMPLETE-01       | COMPLETE / proven_local | 3/3 COMPLETE + resume + idempotency on tracked ingest worker                                                                                                                                                         |
| RAG-IMAGE-BAKE-01              | COMPLETE / proven_local | Tracked `Dockerfile.rag-v2-ingest` + lock; runtime `:local` (not docker-commit tags)                                                                                                                                 |

## Closed — RAG-WIDGET-ADMIN-SECURITY-CLOSEOUT-01 (2026-08-08)

| ID                                    | Disposition                | Note                                                                                                                                                                                                 |
| ------------------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RAG-WIDGET-ADMIN-SECURITY-CLOSEOUT-01 | COMPLETE / CONFIRMED_LOCAL | P0-4 option namespace mismatch fixed; P0-5 nopriv+PIN removed; document admin = `manage_options` + nonce; Gate A jest 43/43 + PHP harness PASS; public chat remains anonymous without doc-admin caps |

## Closed — FACT-SUPERSESSION-WRITE-01 (2026-08-08)

| ID                         | Disposition                | Note                                                                                                                                                                                                                                                |
| -------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FACT-SUPERSESSION-WRITE-01 | COMPLETE / CONFIRMED_LOCAL | Canonical write supersession on `replace_message_facts` + merge `reassign_case_facts`; PG==InMemory; Gate A effective PASS; bounded PG proof PASS; illegal dual-active reconciled (4 groups / 12 rows); legal same-message conflicts preserved (50) |

## Closed — RAG-V2-LIVE-CUTOVER-READINESS-01 (2026-08-08)

| ID                               | Disposition      | Note                                                                                                                                                                                                               |
| -------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RAG-V2-LIVE-CUTOVER-READINESS-01 | COMPLETE_BOUNDED | Live plane + ingest worker + host Gate B PASS + dual-read/rollback; Activation `STAGED_ACTIVATION_AUTHORIZED — BLOCKED_BY_TECHNICAL_GATE`; proof `eval/rag-v2-live-cutover-20260808/`; **no** global `RAG_CORE=v2` |
| RAG-01 (redefined)               | COMPLETE_BOUNDED | Docling live in canonical containerized ingest worker                                                                                                                                                              |
| RAG-12 (host E2E bar)            | COMPLETE_BOUNDED | Real PDF→MinIO→PG→Qdrant→retrieve→restart; Temporal COMPLETE = residual `RAG-TEMPORAL-COMPLETE-01`                                                                                                                 |
| RAG-09                           | COMPLETE_BOUNDED | Opt-in + staged compose ready; product default legacy; staged auth already given                                                                                                                                   |

## Closed — FACT-4.1-HIGH-01 (2026-08-08)

| ID               | Disposition                | Note                                                                                                                   |
| ---------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| FACT-4.1-HIGH-01 | COMPLETE / CONFIRMED_LOCAL | Read-side CURRENT_STATE consumers safe (`unsafe=0`); Gate A **2357**/15; write residual → `FACT-SUPERSESSION-WRITE-01` |

## Closed — FRESH38-RECAPTURE-01 (2026-08-08)

| ID                   | Disposition                | Note                                                                                                                      |
| -------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| FRESH38-RECAPTURE-01 | COMPLETE / CONFIRMED_LOCAL | Measurement healthy: 38/38; CLEAN_PASS=10 CAPABILITY=28 → product **NOT QUALIFIED — CAPABILITY** (not a harness residual) |

## Closed — GOV-09 (2026-08-08)

| ID     | Disposition      | Note                                                                                                                                        |
| ------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| GOV-09 | COMPLETE_BOUNDED | Auth OK; remotes pushed; knowledge on clean `docs/aios-residuals-wave-sync` (no poison secret ancestry). Workspace root: no `origin` (N/A). |

## Closed — RESIDUALS-WAVE-02 (2026-08-07)

| ID                     | Disposition      | Note                                                                            |
| ---------------------- | ---------------- | ------------------------------------------------------------------------------- |
| RAG-05                 | COMPLETE_BOUNDED | Temporal worker module + compose Temporal + live `start_ingest` PASS            |
| RAG-12                 | COMPLETE_BOUNDED | Compose profile `rag-v2-data-plane` + Gate B smoke PASS (`RequireLiveAdapters`) |
| RAG-01                 | COMPLETE_BOUNDED | Host live Docling PDF→graph                                                     |
| RAG-09                 | COMPLETE_BOUNDED | Opt-in `RAG_V2_LIVE_DATA_PLANE`                                                 |
| X1-01 / X1-02          | COMPLETE         | Live Playwright re-proof **2 passed**                                           |
| SPINE-WORKER-TICK-01   | COMPLETE_BOUNDED | Chunked idle drain                                                              |
| DASZEK-HITL-HARNESS-01 | COMPLETE         | node HITL **16/16**                                                             |
| GROQ-KEY-DEAD-01       | COMPLETE_BOUNDED | dead key disable                                                                |

## Closed — RESIDUALS-WAVE-01 (2026-08-07)

| ID     | Disposition              | Note                                                                                              |
| ------ | ------------------------ | ------------------------------------------------------------------------------------------------- |
| RAG-02 | COMPLETE_BOUNDED         | Ephemeral MinIO live                                                                              |
| RAG-04 | COMPLETE_BOUNDED         | Ephemeral Qdrant live                                                                             |
| 4.2    | COMPLETE_BOUNDED         | Daszek superseded UI + live Drive                                                                 |
| 4.4    | **REJECTED_BY_OPERATOR** | Scaffold implemented in WAVE-01; **no product activation**; do not develop (`OPERATOR_DECISIONS`) |
| FG-01  | RESOLVED_OPTION_B        | Guardian joins mailbox `case_status` for SLA                                                      |
| FG-04  | COMPLETE_BOUNDED         | CLI oneshot live                                                                                  |
| IQ-01  | COMPLETE_BOUNDED         | Frozen dual-score; machine_proposed only                                                          |
| PF-01  | COMPLETE_BOUNDED         | Exhaustive draft inventory                                                                        |

## Closed — hygiene / POST32 (2026-08-07)

See prior sections in git history if needed. POST32 4.3/5.1/5.2/6.1/6.2/6.3 = CLOSED in HEAD.
