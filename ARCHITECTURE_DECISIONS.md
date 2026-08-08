# Architecture Decisions — obowiazujace reguly architektury

Status: canonical architectural contract with limited freshness. Verify repo-specific symbol and runtime claims in current source before relying on them.

Ostatnia aktualizacja: 2026-07-14

Kazda regula jest obowiazujaca podczas implementacji. Nie lam bez RFC.

## Wzorce implementacji

- **Agent-as-Gateway**: wszystkie mutacje danych przechodza przez agent LLM (API nie zapisuje bezposrednio). SoT: source-of-truth.md
- **Generic Hands / propose_mutation -> write_executors**: agent proponuje akcje (propose*mutation), 17 write_executorow wykonuje. Lista: CBM `search_code(gmail-agent, "^execute*")`. SoT: kod
- **Intelligence First**: LLM zawsze pierwszy przed heurystyka/regulami. SoT: OPERATOR_DECISIONS.md 2026-06-09
- **Ogolna inteligencja operacyjna, nie workflow per typ sygnalu**: system przyjmuje dowolny sygnal i dobiera kompetencje/moduly (nie galezie per typ maila/dokumentu); jeden sygnal moze uruchomic kilka kompetencji. LLM interpretuje, laczy kontekst, syntetyzuje i planuje; deterministyczny runtime pozostaje wlascicielem persistence, id, dedup, checkpointow, auth, policy, execution, idempotencji, recovery, audytu i potwierdzenia wyniku. SoT: OPERATOR_DECISIONS.md 2026-07-14
- **Idempotent Writes**: operacje write maja gwarancje idempotencji (ON CONFLICT, idempotency_key). SoT: kod

## Source of Truth

- **Event Spine**: unified_os_events jako jedyny event bus (append-only, trace_id). SoT: source-of-truth.md + kod
- **Correlation Registry**: jedyne SoT tozsamosci (entity_registry wycofane). SoT: docs/entity-vs-correlation-registry.md
- **Mailbox Memory = SoT spraw**: case_id i engagement_id tylko w PostgreSQL (gmail-agent). SoT: source-of-truth.md
- **Daszek = projection only**: WordPress nigdy nie jest SoT. SoT: source-of-truth.md + AGENTS.md

## Architektura

- **Runtime Authorization Gate**: kazdy endpoint ma autoryzacje (Bearer token). SoT: kod
- **Snapshot Versioning**: kazdy snapshot ma wersje (engagement_snapshot_v2). SoT: kod
- **SIGNAL_RUNTIME_MODE=active**: jedyna dozwolona wartosc. legacy/shadow/compat -> ConfigError. SoT: OPERATOR_DECISIONS.md 2026-06-02

## Case vs internal_task (mailbox memory)

- **internal_task nigdy nie trafia do feed.cases/feed.desk** — filtrowane w operational feed identycznie jak w business_pulse.py (`case_family != 'internal_task'`). Zadania firmowe są widoczne w Sprawach (sekcja Do zrobienia) przez `GET /tasks` shim oraz w UI scalonym Phase 4.

## Biurko — filtr priorytetu (feed projection)

- **Biurko (feed.cases/desk) = podzbiór desk_eligible (P1+P2 + reguły Cieplo informacyjne)**, nie pełna lista spraw operacyjnych. Filtr: `desk_filter: P1_P2_operational` w `feed_meta`.

## Sprawy — pełny rejestr (Phase 4)

- **Pełna lista spraw klientów** = Node B `GET /cases` (filtry: `requires_action`, `case_family`, `desk_only`, `view=full`). Daszek proxy: `GET /daszek/v2/mailbox-cases`.
- **UI Sprawy** = sekcje **Do zrobienia** (`requires_action=true` + zadania firmowe) i **Informacyjne** (`requires_action=false`). Zakładka Zadania usunięta; `?view=tasks` → Sprawy.
- **GET /tasks** = deprecated shim dla `internal_task` (mutacje POST zachowane).

## Granice (lamanie wymaga RFC)

`EVOLUTION_BOUNDARIES.md` usuniety w restrukturyzacji korpusu (nie istnieje na dysku) — granice D1-D4 ponizej sa jedynym zywym opisem; szczegolowa mapa wariantow integracji nie jest utrzymywana osobno.

- D1: RAG nie w pipeline Cieplo oferty. SoT: ten dokument + kod
- D2: Sprawa Gmail nie generuje auto OfferDTO. SoT: ten dokument + kod
- D3: Jeden poller Gmail docelowo (ryzyko dual ingress). SoT: ten dokument + `rfc/case-os-d3-gmail-ingress-addendum-v1.md`
- D4: Daszek = projection only. SoT: ten dokument + source-of-truth.md
