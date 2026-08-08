# RFC: cieplo-orchestrator PHP mail-ingress retirement

| Pole       | Wartość    |
| ---------- | ---------- |
| **Data**   | 2026-06-11 |
| **Status** | **proven_local** (bounded — no PHP plugin removal on WP) |

## Cel

Retire legacy PHP `mail-ingress` on WordPress when worker path covers 100% ingress.

## Preconditions (met locally 2026-06-11)

1. Fresh E2E proof: cieplo worker → kalk-top → generator (local bounded tests + prior Gate B 2026-06-08)
2. Preflight downstream: `cieplo-worker preflight` exit 0 in Docker — `docs/P0_PREFLIGHT_DOWNSTREAM_PROOF.md`
3. Ingress retirement proof: `docs/P0_CP2_PHP_INGRESS_RETIREMENT_PROOF.md`

## Checklist

- [x] Python `cieplo-worker poll` is canonical ingress (`IngressProcessor` in-process)
- [x] No `TOPINSTAL_MAIL_BACKEND_URL` in worker settings
- [x] RAG `CIEPLO_INGRESS_ENABLED=0` default
- [x] pytest `test_ingress_retirement.py` — no HTTP to legacy mail-ingress
- [ ] Operator: disable PHP `wp topinstal-mail` on WP when production resumes
- [ ] Operator sign-off on VPS timer enable

## Nie w scope (firma w zawieszeniu)

Fizyczne usunięcie pluginu PHP z WordPressa — dopiero przy wznowieniu produkcji.
