# RFC addendum: D3 — jeden kanoniczny Gmail poll (Case OS P4)

| Pole       | Wartość                                                       |
| ---------- | ------------------------------------------------------------- |
| **Data**   | 2026-06-18                                                    |
| **Status** | accepted                                                      |
| **Rodzic** | `knowledge/docs/case-os-target-architecture-proposal.md` § P4 |

## Werdykt

**Kanoniczny poll Gmail dla korespondencji sprawowej jest wyłącznie w gmail-agent (Node B spine).** `cieplo-orchestrator` **nie** polluje Gmaila domyślnie.

## Implementacja

| Element                            | Zmiana                                                                            |
| ---------------------------------- | --------------------------------------------------------------------------------- |
| `CIEPLO_GMAIL_POLL_ENABLED`        | Domyślnie `false` w `cieplo-orchestrator` settings                                |
| `IngressProcessor.process_batch()` | Gdy poll wyłączony → `{ ok: true, processed: 0, skipped: "gmail_poll_disabled" }` |
| gmail-agent spine                  | Pozostaje jedynym źródłem ingest mailowego dla Case OS                            |

## Włączenie legacy poll (tylko lab / migracja)

```bash
CIEPLO_GMAIL_POLL_ENABLED=true
```

Wymaga świadomej decyzji operatora — ryzyko duplikatów względem spine.

## Proof

- `cieplo-orchestrator/tests/test_case_os_d3_ingress.py`
- `gmail-agent/tools/gmail_audit/scripts/case_os_architecture_proof.py` → `CASE_OS_P4_PROOF_OK`
