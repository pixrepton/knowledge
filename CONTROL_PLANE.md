# Control Plane

Status: active. Last updated: 2026-07-13.

## Evidence Layers

| Layer | Evidence | Use |
| --- | --- | --- |
| Runtime proof | fresh proof artifacts, targeted tests, local smoke | readiness claims |
| Code/contracts | source, tests, migrations, schemas | implementation claims |
| Current memory | four files in `knowledge/memory/` | operator decisions and open work |
| Maintained docs | this canon and repo deep manuals | routing and operational context |
| History | Git and operator external copy | audit only, not cold-start |

## Claim Labels

- `implemented in code`
- `runtime enabled`
- `freshly proven locally`
- `operator verified`
- `historical`
- `not proven`

## Rules

- Stability freeze decisions in `OPERATOR_DECISIONS.md` override stale docs.
- Generated graphs and static snapshots are views, not proof.
- Do not keep repo-local memory systems or shadow backlogs.
- Documentation cleanup does not imply runtime proof.
