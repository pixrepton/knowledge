# RFC E2: Intelligence-First Case OS (TUM)

| Pole      | Wartość                                                                                                         |
| --------- | --------------------------------------------------------------------------------------------------------------- |
| Data      | 2026-06-20                                                                                                      |
| Status    | **active** — normatywny dla W2+ MAX-STACK                                                                       |
| Scope     | `gmail-agent` signal reconcile + `agent_runtime`                                                                |
| Powiązane | [E1 § Korekta](E1-drive-shared-downstream-parity.md) (`docs/max-stack-roadmap-2026-06.md` usunięty w restrukturyzacji korpusu — nie istnieje) |
| Proof     | `DRIVE_ORPHAN_TRIAGE_LIVE_PROOF_OK`, `CASE_OS_INTELLIGENCE_FIRST_CLOSURE_PROOF_OK`                              |

---

## Problem

Live proof `DRIVE_AGENT_INTELLIGENCE_LIVE_PROOF_OK` obejmuje tylko sygnały z `case_id`. Orphan Drive (brak sprawy) kończy na legacy deterministycznym ingest bez warstwy agenta — odwrotnie do wizji produktowej: **najpierw rozumieć, potem materializować**.

## Model TUM (Triage → Understand → Materialize)

```text
Signal → Triage (deterministyczny) → Router
  fast_link   → agent na istniejącym case_id (As-Is)
  deep_understand → StagingEngagement (stg_*) bez case_id
    → Understand (read, extract, RAG, similar cases)
    → Decide (propose_* tools — propozycje only)
    → Materialize (Python executor po HITL approve)
  defer       → desk event / operator queue
```

## Pojęcia

| Pojęcie               | Definicja                                                                 |
| --------------------- | ------------------------------------------------------------------------- |
| `StagingEngagement`   | `engagement_id` prefix `stg_`, `case_id=""` do momentu materialize        |
| `MaterializeProposal` | `link_existing` \| `create_case` \| `create_artifact` \| `defer_operator` |
| `OrchestratorRoute`   | `fast_link` \| `deep_understand` \| `defer` \| `legacy_fallback`          |

## Fast path (konserwatywny)

- Entity link VERIFIED, lub
- Drive `link_confidence >= 0.92` + `linkage_status=deterministic`, lub
- Gmail thread w registry z tym samym `customer_email`

## Narzędzia agenta (propozycje — nie writes SoT)

| Tool                   | Efekt                                                 |
| ---------------------- | ----------------------------------------------------- |
| `propose_case_link`    | Propozycja linku do istniejącej sprawy + HITL         |
| `propose_new_case`     | Propozycja nowej sprawy (case_family, subject) + HITL |
| `propose_artifact`     | Artefakt odłożony (invoice pending link) + HITL       |
| `search_similar_cases` | Wrap Similar Cases v0/v1                              |
| `retry_hard_parse`     | Eskalacja Hard PDF Lane                               |

**Materialize executor:** `agent_runtime/materialize.py` — jedyny writer `upsert_case` po approve.

## Granice (nienaruszalne)

- Brak auto-create spraw bez operator approve
- HITL outbound unchanged
- Drive inteligencja = **agent_runtime TUM** — nie shared downstream (E1 superseded)
- D1–D4 bez zmian

## Implementacja (slice map)

| Slice | Moduły                          | Proof                               |
| ----- | ------------------------------- | ----------------------------------- |
| A     | Hard PDF Lane                   | `HARD_PDF_LANE_PROOF_OK`            |
| B     | staging + propose + materialize | `DRIVE_ORPHAN_TRIAGE_LIVE_PROOF_OK` |
| C     | orchestrator router             | `ORCHESTRATOR_ROUTER_PROOF_OK`      |
| D     | Gmail/Calendar expand           | `GMAIL_ORPHAN_TRIAGE_LIVE_PROOF_OK` |

## Decyzja operatora

Zatwierdzono TUM jako docelowy model reconcile orphan signals (2026-06-20, MAX-STACK plan).
