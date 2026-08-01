# Reverse-audit category 12 - cross-repo payload ↔ request validator/schema; route ↔ client; recovery/replay entrypoint ↔ original workflow

- Timestamp: `2026-07-30 21:14:30 +02:00`
- Working directory: `C:\Users\compg\Desktop\top-code workspace`
- Scope: current and manually reachable cross-repo contracts that participate in canonical workflow registry entries, plus real recovery/replay entrypoints that re-enter the same workflow core.
- Exclusions:
  - full re-audit of dormant legacy v1/v2 Daszek projection push beyond the live v3/bridge contracts;
  - `gmail_intake.py replay-v2` legacy Daszek projection replay, because its receiver route was not reopened in this slice and it does not target the current canonical v3 workflow;
  - documentation-only contracts and hand-maintained graph files;
  - browser-only frontend calls that do not cross repository boundaries.
- Repo SHAs:
  - `gmail-agent`: `468d37ee6553b39bf6009939e9c87c13f3c183c7`
  - `daszek`: `672769d9496359dcfb7f2427d555ad34a2171b1a`
  - `kalk-top`: `9d56055be7f293ad17ffb624abc178617f46f5be`
  - `fast-kalk`: `06a470da94db6069f42c0d20a860815212e80f00`
  - `top-instal-generator`: `7e5279551b3919b7ab84547227b3355f45c44bf4`
  - `cieplo-orchestrator`: `e68f05386722b4034ca36bd39d169eba759f44e6`
  - `rag-chat-asystent`: `34e9ae2e597076756aa71051382fe18d058776a7`
  - `rag-widget`: `c64707aac69bb4a6cc68e1f097aa8415a3b976a6`
  - `knowledge`: `597b1091a296930ed32afb379ec19b8ab425d4fa`

## Exact commands

1. `Get-Content "gmail-agent/tools/gmail_audit/api_app.py" | Select-Object -Index (996..1088)`
   - exit code: `0`
2. `Get-Content "gmail-agent/tools/gmail_audit/correlation_registry/service.py" | Select-Object -First 220`
   - exit code: `0`
3. `Get-Content "fast-kalk/wp-content/plugins/topinstal-lead-widget/includes/class-lead-registry.php" | Select-Object -Index (630..700)`
   - exit code: `0`
4. `Get-Content "fast-kalk/wp-content/plugins/topinstal-lead-widget/includes/class-os-event-client.php" | Select-Object -First 130`
   - exit code: `0`
5. `Get-Content "fast-kalk/wp-content/plugins/topinstal-lead-widget/includes/class-calculator.php" | Select-Object -Skip 150 -First 130`
   - exit code: `0`
6. `Get-Content "fast-kalk/wp-content/plugins/topinstal-lead-widget/includes/class-offer-dispatch.php" | Select-Object -Skip 100 -First 120`
   - exit code: `0`
7. `Get-Content "gmail-agent/tools/gmail_audit/agent_runtime/kalk_top_client.py" | Select-Object -First 140`
   - exit code: `0`
8. `Get-Content "kalk-top/wp-adapter/rest/CalculateOfferController.php" | Select-Object -First 230`
   - exit code: `0`
9. `Get-Content "top-instal-generator/wp-adapter/rest/GenerateOfferDocumentController.php" | Select-Object -First 260`
   - exit code: `0`
10. `Get-Content "top-instal-generator/core/application/GenerateOfferDocumentUseCase.php" | Select-Object -Index (200..280)`
    - exit code: `0`
11. `Get-Content "cieplo-orchestrator/src/topinstal_cieplo_worker/integrations/kalktop/client.py" | Select-Object -First 220`
    - exit code: `0`
12. `Get-Content "cieplo-orchestrator/src/topinstal_cieplo_worker/integrations/generator/client.py" | Select-Object -First 220`
    - exit code: `0`
13. `Get-Content "cieplo-orchestrator/src/topinstal_cieplo_worker/api/routes.py" | Select-Object -First 180`
    - exit code: `0`
14. `Get-Content "cieplo-orchestrator/src/topinstal_cieplo_worker/ingress/processor.py" | Select-Object -First 240`
    - exit code: `0`
15. `Get-Content "cieplo-orchestrator/src/topinstal_cieplo_worker/workflow/runner.py" | Select-Object -Index (60..210)`
    - exit code: `0`
16. `Get-Content "cieplo-orchestrator/src/topinstal_cieplo_worker/workflow/runner.py" | Select-Object -Index (210..360)`
    - exit code: `0`
17. `Get-Content "cieplo-orchestrator/src/topinstal_cieplo_worker/workflow/row_updates.py" | Select-Object -First 120`
    - exit code: `0`
18. `Get-Content "cieplo-orchestrator/src/topinstal_cieplo_worker/integrations/node_b_registry/client.py" | Select-Object -First 220`
    - exit code: `0`
19. `Get-Content "gmail-agent/tools/gmail_audit/daszek_client.py" | Select-Object -Index (449..590)`
    - exit code: `0`
20. `Get-Content "daszek/includes/api-v3.php" | Select-Object -Index (92..132)`
    - exit code: `0`
21. `Get-Content "daszek/includes/api-v2.php" | Select-Object -Index (120..140)`
    - exit code: `0`
22. `Get-Content "daszek/includes/api-v3-handlers.php" | Select-Object -Index (997..1060)`
    - exit code: `0`
23. `Get-Content "daszek/includes/api-v3-handlers.php" | Select-Object -Index (1218..1498)`
    - exit code: `0`
24. `Get-Content "gmail-agent/tools/gmail_audit/signal_reconciler.py" | Select-Object -First 95`
    - exit code: `0`
25. `Get-Content "gmail-agent/tools/gmail_audit/signal_reconciler.py" | Select-Object -Index (191..305)`
    - exit code: `0`
26. `Get-Content "gmail-agent/tools/gmail_audit/case_state_rebuilder.py" | Select-Object -First 240`
    - exit code: `0`
27. `Get-Content "gmail-agent/tools/gmail_audit/gmail_intake.py" | Select-Object -Skip 1698 -First 20`
    - exit code: `0`
28. `Get-Content "gmail-agent/tools/gmail_audit/signal_worker.py" | Select-Object -Skip 1060 -First 30`
    - exit code: `0`
29. `rg -n "status' => 'success'|downloadUrl|fallback_docx|converter_mode|mimeType|outputFormat" "top-instal-generator/core/application/GenerateOfferDocumentUseCase.php" "fast-kalk/wp-content/plugins/topinstal-lead-widget/includes/class-offer-dispatch.php" "cieplo-orchestrator/src/topinstal_cieplo_worker/workflow/runner.py"`
    - exit code: `0`
30. `rg -n "replay_signal_from_journal|run_signal_replay_command|run_signal_rebuild_case_command|rebuild_case_from_signal_journal" "gmail-agent/tools/gmail_audit/gmail_intake.py" "gmail-agent/tools/gmail_audit/signal_worker.py"`
    - exit code: `0`
31. `rg -n "def replay_signal\(|def reconcile_signal\(|def for_replay\(|record_processing_attempt\(|def case_rebuild_from_journal\(" "gmail-agent/tools/gmail_audit/signal_reconciler.py" "gmail-agent/tools/gmail_audit/case_state_rebuilder.py"`
    - exit code: `0`
32. `rg -n "api/ingress/cieplo-app|api/workflows/.*/retry|def accept_envelope|def should_retry_workflow|def _can_resume_from_pdf_ready|run_workflow_pipeline" "cieplo-orchestrator/src/topinstal_cieplo_worker/api/routes.py" "cieplo-orchestrator/src/topinstal_cieplo_worker/ingress/processor.py" "cieplo-orchestrator/src/topinstal_cieplo_worker/workflow/runner.py" "cieplo-orchestrator/src/topinstal_cieplo_worker/workflow/row_updates.py"`
    - exit code: `0`
33. `rg -n "class KalkTopClient|class GeneratorClient|call_calculate_offer|register_links_payload|def get_v2_bridge_queue|def complete_v2_bridge_queue_item|def post_v3_operational_feed_snapshot|/internal/os-events|/internal/registry/links" "gmail-agent/tools/gmail_audit/agent_runtime/kalk_top_client.py" "cieplo-orchestrator/src/topinstal_cieplo_worker/integrations/kalktop/client.py" "cieplo-orchestrator/src/topinstal_cieplo_worker/integrations/generator/client.py" "gmail-agent/tools/gmail_audit/correlation_registry/service.py" "gmail-agent/tools/gmail_audit/daszek_client.py" "gmail-agent/tools/gmail_audit/api_app.py"`
    - exit code: `0`
34. `rg -n "node_b_read|fetch_case_context_pack|fetch_engagement_snapshot|/cases/\{id\}/context-pack|/engagements/\{id\}/snapshot" "rag-chat-asystent" "gmail-agent/tools/gmail_audit/api_app.py"`
    - exit code: `0`

## Contract inventory

| Contract | Client / producer | Route | Validator / acceptor | Payload contract result | Runtime classification |
|---|---|---|---|---|---|
| fast-kalk lead registry | `class-lead-registry.php` builds `identity_email`, `display_name`, `links[]` and Bearer auth | gmail-agent `POST /internal/registry/links` | `register_correlation_links()` -> `CorrelationRegistryService.register_links_payload()` -> `_normalize_links()` | Client supplies the fields the server actually normalizes and enforces (`links` list, `link_type`, `target_id`, numeric confidence). | `BOTH_MATCHED` |
| fast-kalk / kalk-top / top-generator / cieplo os-events | `class-os-event-client.php`, `OsEventClient.php`, `event_spine/client.py` | gmail-agent `POST /internal/os-events` | `publish_os_event_internal()` only requires non-empty `event_type`; `payload`/`correlation` merely need to be dicts if present | Every producer fits the route, but the acceptor does not enforce `schema_version`, `source_repo` vocabulary, or event-specific payload schema. | `BOTH_MATCHED_SCHEMA_LOOSE_ACCEPTOR` |
| fast-kalk calculate-offer | `class-calculator.php` -> remote POST or in-process REST dispatch | kalk-top `POST /wp-json/topinstal/v1/calculate-offer` | `TopInstal_CalcRequest_Validator::validate()` | Client sends canonical CalcRequestDTO body and auth header actually recognized by the route (`X-Top-Instal-Agent-Key` or nonce). | `BOTH_MATCHED` |
| gmail-agent agent runtime calculate-offer | `agent_runtime/kalk_top_client.py::call_calculate_offer()` | same kalk-top route | same validator | Client shape is accepted by the same route; this path reuses the same cross-repo contract as fast-kalk and cieplo. | `BOTH_MATCHED` |
| cieplo calculate-offer | `integrations/kalktop/client.py::KalkTopClient.calculate_offer()` | same kalk-top route | same validator | Cieplo adds both `X-Top-Instal-Agent-Key` and `Authorization: Bearer`; the route authorizes on the custom agent-key header and ignores the extra bearer header. | `BOTH_MATCHED_EXTRA_HEADER_IGNORED` |
| fast-kalk generator request | `class-offer-dispatch.php::generate_pdf()` -> `build_generator_request()` | top-instal-generator `POST /wp-json/topinstal/v1/offer-documents/generate` | `TopInstal_OfferDocumentRequest_Validator::validate()` | Request payload matches canonical `mode=from-offer-dto`, `offerDto`, `outputFormat=pdf`. | `BOTH_MATCHED` |
| cieplo generator request | `integrations/generator/client.py::GeneratorClient.generate()` | same generator route | same validator | Request payload is accepted; client requires agent key and forwards trace header. | `BOTH_MATCHED` |
| Node B -> Daszek feed push | `DaszekClient.post_v3_operational_feed_snapshot()` | Daszek `POST /wp-json/daszek/v3/operational-feed-snapshots` | `daszek_v3_validate_operational_feed_snapshot_payload()` + forbidden-key walk + optional desk-note ref check | Current sender and receiver are aligned; receiver enforces much stricter structural/privacy contract than Node B internal `/internal/os-events`. | `BOTH_MATCHED_STRICT_SCHEMA` |
| Daszek bridge queue read/complete | `DaszekClient.get_v2_bridge_queue()` / `complete_v2_bridge_queue_item()` | Daszek `GET /bridge-queue`, `POST /bridge-queue/complete` | `daszek_api_v2_bridge_queue()` and `daszek_api_v2_bridge_queue_complete()` | Fetch contract is minimal (`status`, `limit`); completion contract allows only `completed|failed|skipped`. Client vocabulary matches route vocabulary. | `BOTH_MATCHED` |
| rag-chat-asystent -> Node B context GET | `integrations/node_b_read.py::fetch_case_context_pack/fetch_engagement_snapshot` | gmail-agent `GET /cases/{id}/context-pack`, `GET /engagements/{id}/snapshot` | route body is read-only GET surface, no mutating validator | Contract is structurally aligned; the mechanism is real, but caller population of `case_context` / `engagement_id` into rag-chat `/chat` remains dormant elsewhere. | `BOTH_MATCHED_CALLER_DORMANT` |

## Recovery / replay inventory

| Recovery / replay entrypoint | Entry symbol | Re-entry target | Relation to original workflow | Classification |
|---|---|---|---|---|
| gmail-agent signal replay | `gmail_intake.py::run_signal_replay_command` -> `signal_worker.replay_signal_from_journal` | `signal_reconciler.replay_signal()` -> same `reconcile_signal()` core | Reuses the same reconcile core as live signal handling, but skips original Gmail fetch, canonical signal build, journal append, and sets `for_replay()` semantics (`persist_entity_links=False`). Still records new processing attempts. | `SAME_CORE_SKIPS_INGRESS_AND_APPEND` |
| gmail-agent case rebuild from journal | `gmail_intake.py::run_signal_rebuild_case_command` -> `signal_worker.rebuild_case_from_signal_journal` | `case_state_rebuilder.case_rebuild_from_journal()` -> repeated `reconcile_signal()` over stored signals | Replays the same reconcile core over journaled signals only; does not re-enter original Gmail ingress, raw observation capture, or signal creation stages. | `SAME_CORE_MULTI_SIGNAL_REBUILD` |
| cieplo HTTP ingress retry-on-duplicate | `IngressProcessor.accept_envelope()` duplicate branch | `run_workflow_pipeline()` when existing row passes `should_retry_workflow()` | Original envelope is validated once. Retry of an existing `message_id` does not re-validate or re-persist a fresh envelope; it resumes from persisted `WorkflowRow` identity. | `RESUME_FROM_PERSISTED_ROW` |
| cieplo manual workflow retry | `POST /api/workflows/{workflow_id}/retry` | direct `run_workflow_pipeline(workflow_id)` | Re-enters the same downstream pipeline core, but bypasses `accept_envelope()` validation and correlation re-registration. It accepts `FAILED_RETRYABLE`, `FAILED_FINAL`, and `PDF_READY`, so it is broader than its route name suggests. | `SAME_CORE_BYPASSES_INGRESS_VALIDATION` |

## Key findings

1. Current live cross-repo contracts are structurally better than the remaining docs implied.
   - Registry links, os-events, calculate-offer, generator request, Daszek bridge queue, Daszek v3 feed push, and rag-chat Node-B context GETs all have both client and server sides present in code in this slice.

2. `/internal/os-events` is a deliberately loose acceptor, not a schema-locked contract surface.
   - The route enforces only `event_type` plus "payload/correlation must be dict if present".
   - All current producers conform, but the contract is validator-light compared with Daszek v3 feed ingest or kalk-top / generator REST routes.

3. Gmail replay paths re-enter the reconcile core, not the full original ingress workflow.
   - `signal-replay` and `signal-rebuild-case` both call the same `reconcile_signal()` core.
   - They do not re-run Gmail fetch, signal normalization, or signal-journal append.
   - They still write fresh processing-attempt rows, so replay is not a no-op readback.

4. Cieplo retry is a downstream resume, not a fresh ingress replay.
   - The authenticated retry route does not call `accept_envelope()`.
   - It queues `run_workflow_pipeline()` directly from persisted `WorkflowRow`.
   - This is why `FAILED_FINAL` and `PDF_READY` are retryable in practice: recovery is modeled as pipeline re-drive from stored state, not envelope re-acceptance.

5. New decisive cross-repo contract drift: generator fallback DOCX is treated as PDF-ready by downstream consumers.
   - Server side:
     - `GenerateOfferDocumentUseCase.php:181,203-217,240-255` can return top-level `status='success'` with `document.format='docx'`, `mimeType` DOCX, and `meta.converter='fallback-docx'`.
   - fast-kalk consumer side:
     - `class-offer-dispatch.php:152-165` reads only `document.downloadUrl`, names the helper `generate_pdf`, and never checks `document.format` or `meta.converter`.
   - cieplo consumer side:
     - `workflow/runner.py:309-311` reads only `document.downloadUrl`, stores it as `pdf_download_url`, and transitions to `WorkflowState.PDF_READY` with no `document.format` check.
   - Meaning:
     - top-instal-generator is honest enough to tell consumers that the result is DOCX fallback;
     - at least two consumers ignore that signal and advance as if PDF readiness were proven.

## Full list of audited results

1. `POST /internal/registry/links` is a real validated contract, not a write-anything sink.
   - Writer fields and route normalizer are aligned.

2. `POST /internal/os-events` is intentionally permissive.
   - This is a contract surface with very weak validation, but current producers stay within the expected shape.

3. `POST /wp-json/topinstal/v1/calculate-offer` is a shared canonical backend for fast-kalk, cieplo, and gmail-agent.
   - No client-specific payload fork was found in this slice.

4. `POST /wp-json/topinstal/v1/offer-documents/generate` is also a shared canonical backend.
   - The real drift is not request shape but response interpretation.

5. Daszek bridge queue fetch/complete contracts align across repos.
   - Consumer status vocabulary matches receiver vocabulary.

6. Daszek v3 operational feed push is strict on the receiver side.
   - This is the strongest cross-repo validator in the slice.

7. rag-chat Node-B context reads are real and aligned.
   - The dormancy is at the caller population layer, not in the HTTP contract itself.

8. gmail-agent replay entrypoints are partial-stage replays, not full ingress reruns.

9. cieplo retry is a persisted-row resume path, not a full envelope replay.

## False positives

1. Cieplo's extra `Authorization: Bearer` header on kalk-top requests is not a contract mismatch.
   - The route authorizes on `X-Top-Instal-Agent-Key`; the bearer header is simply ignored.

2. `retry_workflow` sounds narrower than it is.
   - In reality it also accepts `FAILED_FINAL` and `PDF_READY`; this is a naming overstatement, not a missing consumer.

3. `signal-replay` is not evidence that gmail-agent can reconstruct the full original Gmail ingress path.
   - It only proves replay of the reconcile stage from stored signal data.

4. `generate_pdf` and `pdf_download_url` names on consumers overstate what the generator contract guarantees.
   - The actual bug is consumer-side interpretation, not server-side absence of a warning.

## Unresolved

1. `gmail_intake.py replay-v2` was intentionally excluded from this slice because it targets the superseded Daszek v2 projection path and its receiver route was not reopened here.

2. `/internal/email/personalize-offer` was not paired with a producer in this slice.
   - Route exists; no current client was reopened.

3. This slice classifies recovery/replay entrypoints structurally.
   - It does not prove live operator use frequency or success rate.

## New findings suitable for registry/gap updates

- New P2 gap: top-instal-generator's DOCX fallback is contract-honest on the producer side but misclassified by fast-kalk and cieplo consumers as PDF-ready.
- No new route/client missing-consumer gap was found for the audited live contracts themselves.

## Evidence IDs

- Existing evidence referenced during continuation: `EV-00175`, `EV-00182`, `EV-00185`
- New evidence to append after this artifact: `EV-00186`
