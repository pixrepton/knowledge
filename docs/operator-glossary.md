# Operator glossary — Case/Task & operational feed

## Operational feed lists

| Term                | Status                                 | Description                                                                       |
| ------------------- | -------------------------------------- | --------------------------------------------------------------------------------- |
| `feed.action_items` | **Canonical** (schema 1.2+)            | Agent-proposed next actions for operator review. Not internal firm tasks.         |
| `feed.tasks`        | **Deprecated** (shim until schema 1.3) | Alias of `action_items` for backward compatibility. New exporters emit both keys. |
| `feed.desk`         | Active                                 | Desk cards (Biurko) — attention, gaps, conflicts, Cieplo info.                    |
| `feed.cases`        | Active                                 | Operational case projection subset (P1/P2 + Cieplo info).                         |

## Sprawy vs zadania firmowe

| Term                  | Description                                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| Sprawy (Do zrobienia) | Customer cases with `requires_action=true` from Node B `GET /cases`.                                   |
| Sprawy (Informacyjne) | Customer cases with `requires_action=false` (e.g. Cieplo orchestrator success).                        |
| Zadania firmowe       | Legacy manual items; migrating from `internal_task` to `operations` + `source_kind=manual` (Phase 10). |
| Okazja dostawcy       | `supplier_opportunity` — wartościowa promocja hurtowni (Biurko jeśli P1/P2, akcja „przeanalizuj”).     |

## Schema versions

| Version       | Notes                                            |
| ------------- | ------------------------------------------------ |
| 1.0 / 1.1     | Legacy; `feed.tasks` accepted                    |
| 1.2           | Requires `feed.action_items`; emits `tasks` shim |
| 1.3 (planned) | `feed.tasks` removed                             |
