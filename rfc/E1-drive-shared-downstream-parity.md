# RFC E1: Drive reconcile — shared downstream parity

| Pole   | Wartość                                                                                  |
| ------ | ---------------------------------------------------------------------------------------- |
| Data   | 2026-06-20                                                                               |
| Status | **superseded** — korekta operatora 2026-06-20 (patrz § Korekta wizji)                    |
| Scope  | `gmail-agent/tools/gmail_audit/signal_reconciler.py` — `_reconcile_drive_signal`         |
| Risk   | HIGH — `reconcile_signal` downstream impact CRITICAL (32 symbols, 7 processes, GitNexus) |
| Proof  | `DRIVE_RECONCILE_SHARED_DOWNSTREAM_PROOF_OK` (target)                                    |
| Bloker | Wymaga full master harness PASS po każdym kroku                                          |

---

## Problem

`_reconcile_gmail_signal` używa `run_shared_downstream_stages` (canoniczna spina):

```python
downstream = run_shared_downstream_stages(
    snapshot, intake_result, context_bundle, stage_config,
    options=SharedDownstreamOptions(hot_state_mode="reconcile_signal_apply", ...)
)
```

`_reconcile_drive_signal` **nie używa** shared runner — ręcznie składa:

- `_build_drive_intake_result`, `_build_drive_business_result`, `_build_drive_action_plan`
- Pomija: `ingest_mailbox_memory`, `run_business_reasoning`, `draft_reply`, `finalize_mailbox_memory`
- Hot state: `CaseSnapshotManager.apply_signal` inline (nie przez `hot_state_mode`)
- Policy: `attach_policy_and_proposals` wywołana bezpośrednio (OK — ten sam call)
- Brak `link_case_context`, `build_case_intelligence_layer` z shared runner

---

## Parity checklist (E1 przed kodem)

### Co musi być równoważne między Gmail a Drive path:

| Stage                             | Gmail (`_reconcile_gmail_signal`)         | Drive (cel po E1)                                          |
| --------------------------------- | ----------------------------------------- | ---------------------------------------------------------- |
| Drive-specific store              | N/A (mail only)                           | ✅ `upsert_drive_document`, facts/chunks — **KEEP BEFORE** |
| `link_case_context`               | ✅ via shared runner                      | ⚠️ brak — add to adapter                                   |
| `ingest_mailbox_memory`           | ✅ via shared runner                      | ⚠️ brak — add to adapter                                   |
| `run_business_reasoning`          | ✅ via shared runner                      | ⚠️ brak — add to adapter                                   |
| `draft_reply`                     | ✅ via shared runner                      | ❌ N/A — Drive signals nie piszą draft (no-op OK)          |
| `plan_actions`                    | ✅ via shared runner                      | ⚠️ brak — add to adapter                                   |
| CI layer                          | ✅ via shared runner                      | ⚠️ brak — add to adapter                                   |
| `finalize_mailbox_memory`         | ✅ via shared runner                      | ⚠️ brak — add to adapter                                   |
| Hot state                         | `hot_state_mode="reconcile_signal_apply"` | Inline `CaseSnapshotManager.apply_signal` — unify          |
| `attach_policy_and_proposals`     | ✅ via shared runner                      | ✅ bezpośrednio (OK)                                       |
| Projection                        | ✅ `build_operator_projection_snapshot`   | ✅ bezpośrednio (OK)                                       |
| Agent path                        | `_reconcile_gmail_signal_agent` branch    | ✅ `_reconcile_drive_signal_agent` OK (nie zmieniać)       |
| `SharedDownstreamOptions.dry_run` | ✅ przekazywane                           | ⚠️ brak — add                                              |

### Co Drive ma celowo inaczej:

- `draft_reply` — **nie generować**; Drive sygnał to plik, nie mail; shared runner z `skip_draft_reply=True`
- Drive store writes (doc ingest) — **muszą być PRZED** shared runner (dane wejściowe dla CI)
- `case_intelligence_guard_exceptions=True` — jak Gmail (nie propagować wyjątku CI do upstream)

---

## Plan implementacji (E1-1)

```text
1. W signal_reconciler.py, _reconcile_drive_signal legacy path:
   a. Zachować drive store writes PRZED wywołaniem shared runner.
   b. Zbudować minimal intake_result z danych drive (już są - _build_drive_intake_result).
   c. Wywołać run_shared_downstream_stages(
          snapshot, drive_intake_result, context_bundle, stage_config,
          options=SharedDownstreamOptions(
              hot_state_mode="reconcile_signal_apply",
              entity_link_signal=drive_signal,   # lub None jeśli mail-only
              dry_run=dry_run,
              case_intelligence_guard_exceptions=True,
              skip_draft_reply=True,             # Drive nie generuje draft
          )
      )
   d. Usunąć manualne wywołania CI, hot_state, policy (teraz w shared runner).
   e. Zachować projekcję (build_operator_projection_snapshot) po shared runner.

2. Dodać parametr skip_draft_reply do SharedDownstreamOptions.
3. W intake_shared_downstream.run_shared_downstream_stages: honor skip_draft_reply.

4. Test (E1-2):
   - Rozszerzyć test_signal_reconciler_runtime.py o parity assertions.
   - case_os_learning_loops_closure_proof.py PASS.
```

---

## Ryzyka

| Ryzyko                                                       | Mitigacja                                                 |
| ------------------------------------------------------------ | --------------------------------------------------------- |
| Hot state ordering zmiana → błędy w projekcji                | Benchmark test przed/po z tymi samymi danymi              |
| `business_reasoning` na drive signal bez maila → pusty wynik | Guard w shared runner: skip jeśli brak message content    |
| Projekt drive CI ≠ Gmail CI (inne fakty)                     | Akceptowane — drive ma inne etapy, CI ma guard exceptions |
| Regresja Gmail path                                          | Master harness obowiązkowy po każdym kroku                |

---

## Warunek sukcesu

```text
python scripts/case_os_learning_loops_closure_proof.py
→ CASE_OS_LEARNING_LOOPS_CLOSURE_PROOF_OK

python scripts/agent_runtime_full_chain_proof.py
→ AGENT_RUNTIME_FULL_CHAIN_PROOF_OK

# Nowy:
DRIVE_RECONCILE_SHARED_DOWNSTREAM_PROOF_OK
```

## Decyzja operatora (2026-06-20)

**Zatwierdzona wizja (skorygowana):** gmail-agent i agenci LLM mają **samodzielnie rozumować** o plikach Drive — odczytać treść (`read_google_drive_file`), ocenić typ dokumentu i zdecydować co zrobić — **na warstwie agent_runtime** (constitution + planner + tools), analogicznie do myślenia o mailu, **nie** przez mechaniczne spięcie `_reconcile_drive_signal` z `run_shared_downstream_stages`.

### § Korekta wizji (2026-06-20)

| Aspekt   | Błędna interpretacja (E1-1)                              | Właściwy target                                                                                                       |
| -------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Warstwa  | Shared downstream spine (business reasoning, CI, policy) | **Agent runtime** — LLM planner + tools (`list_drive_folder`, `read_google_drive_file`, `extract_facts_from_text`, …) |
| Analogia | „Ten sam pipeline co Gmail reconcile”                    | „Ten sam **sposób myślenia** co agent przy mailu”                                                                     |
| Proof    | `DRIVE_RECONCILE_SHARED_DOWNSTREAM_PROOF_OK`             | `DRIVE_AGENT_INTELLIGENCE_PROOF_OK` + **`DRIVE_AGENT_INTELLIGENCE_LIVE_PROOF_OK`** (Gate B)                           |
| Fallback | Shared runner dla legacy drive                           | Legacy deterministyczny ingest + projekcja; **inteligencja tylko przez agent path** gdy `AGENT_RUNTIME_ENABLED=1`     |

Implementacja: `_reconcile_drive_signal_agent` + rozszerzony `signal_payload_for_agent` (drive metadata). Shared downstream parity **wycofane** z drive legacy path.
