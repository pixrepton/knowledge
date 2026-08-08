# Documentation Policy — TOP-INSTAL AI-OS

Ostatnia aktualizacja: 2026-07-14
Obowiazuje wszystkie sesje agenta.

## Zasady nadrzedne

1. **Jedno Source of Truth**: kazda informacja ma dokladnie jedno miejsce. Nie dubluj.
2. **Zero redundancji**: jesli cos juz jest napisane w jednym dokumencie, nie pisz tego w drugim. Wskaz referencja.
3. **Jeden kanoniczny cold-start**: pelna kolejnosc czytania startowego istnieje wylacznie w `INDEX.md` §Cold-Start. Inne pliki (root `AGENTS.md`, `docs/WORKSPACE_ONBOARDING.md`, root `CLAUDE.md`) tylko odsylaja do niej, nie powielaja listy.
4. **Jeden dokument = jedno pytanie**: kazdy dokument odpowiada na dokladnie jedno pytanie. Jesli musisz odpowiedziec na dwa, to znaczy, ze potrzebujesz dwoch dokumentow.
5. **Archiwum nie wraca**: jesli dokument trafil do `archive/`, nie przywracaj go bez uzasadnienia. Albo wlacz informacje do istniejacego LIVE dokumentu, albo utworz nowy kanoniczny.
6. **CBM > statyczne runtime**: lista write executors, mapa endpointow, dependency graph — pytaj CBM (Codebase Memory MCP). Nie tworz/utrzymuj statycznych kopii w docs.
7. **Kod > dokumentacja**: przy konflikcie dokumentacja vs kod, kod wygrywa. Zaktualizuj dokumentacje.

## Gdzie co pisac

### INDEX.md — punkt startowy

- Podstawowe informacje o systemie
- Lista wszystkich LIVE dokumentow z 1-zdaniowym opisem
- Jedyne miejsce z pelna kolejnoscia cold-start (inne pliki tylko odsylaja)
- Nie zmieniaj struktury INDEX.md bez zgody operatora

### world-state.yaml — stan strukturalny

- ownership (repos.\*.role)
- proof (repos.\*.proof, proof_date, proof_ref)
- open_p0/p1 dla kazdego repo
- gaps (D1-D4)
- local endpoints
- dependencies (kto wola kogo HTTP)
- Nie dodawaj polemik, opisow, historii. Tylko fakty.

### CONTROL_PLANE.md — epistemika

- Evidence Layers: runtime proof, code/contracts, current memory, maintained docs, history
- Claim Labels: implemented in code / runtime enabled / freshly proven locally / operator verified / historical / not proven
- Rules: stability freeze w OPERATOR_DECISIONS.md nadpisuje nieaktualne dokumenty; wygenerowane grafy/snapshoty to widoki, nie dowod
- Nie dodawaj stanu systemu, backlogu, endpointow. To jest w world-state.yaml i BACKLOG.md.

### source-of-truth.md — wlasciciele danych

- Macierz: ktora domena ma ktory SoT (Postgres, plik, API)
- Zasada: runtime kod > dokumentacja
- Nie dodawaj architektury ani endpointow. To jest w SYSTEM_ATLAS.md i world-state.yaml.

### SYSTEM_ATLAS.md — architektura

- Mapa cross-repo + D1-D4 + ownership graph
- Diagramy biznesowe
- Nie powtarzaj kolejnosci czytania (jest w INDEX.md).
- Nie powtarzaj SoT (jest w source-of-truth.md).

### ARCHITECTURE_DECISIONS.md — reguly implementacji

- Tylko obowiazujace reguly, krotkie punkty
- Kazda regula: nazwa + 1-2 zdania + wskazanie SoT
- Data przy SoT to provenance (odwolanie do decyzji w OPERATOR_DECISIONS.md), nie narracja historyczna — bez opisow "co bylo wczesniej"
- Aktualizuj tylko gdy zmienia sie architektura

### memory/OPERATOR_DECISIONS.md — decyzje operatora

- Tylko decyzje z tagiem [ACTIVE]
- Kazda decyzja: scope, decyzja, proof, review date
- Superseded przenies na [SUPERSEDED] (NIE usuwaj)
- Nie dodawaj backlogu ani stanu systemu

### memory/ACTIVE_WORKSPACE.md — stan systemu na dzis

- Tabela: komponent, status, data
- Lista zmian: co sie zmienilo od ostatniej sesji
- Tylko bieżący stan. Bez backlogu, bez reading order, bez listy zrobionych.

### memory/BACKLOG.md — zadania

- Sekcja "Aktualnie otwarte" zawiera tylko otwarte P0-P3
- Zamkniete programy moga zostac nizej tylko jako jawnie oznaczony rejestr proofow/statusu
- Kazdy otwarty item: numer, zadanie, obszar, dowod, uwagi

### memory/LAST_SESSION.md — podsumowanie ostatniej sesji

- Co zrobiono (fakty, nie opinie)
- Stan systemu po sesji
- Co dalej (rekomendacje, nie backlog)
- Zrobione itemy z BACKLOG.md tu migruja

### AGENTS.md (root) — router ekosystemu

- Krotki (max 1 ekran)
- Logical products + ownership
- Cold-start read order (krotko)
- Lokalne endpointy
- Nie powtarzaj tresci z knowledge/. Tylko wskazuj.

### docs/\* — dokumenty referencyjne

- Tylko jesli odpowiedz nie miesci sie w dokumentach kanonicznych
- Kazdy dokument: jedno zagadnienie, cel, status

### rfc/\* — propozycje zmian

- Tylko aktywne RFC (open lub w trakcie implementacji)
- Zamkniete RFC przenies do `rfc/archive/`
- README.md + \_TEMPLATE.md zostaja

## Kiedy co aktualizowac

| Okazja                      | Dokument                       | Zakres                        |
| --------------------------- | ------------------------------ | ----------------------------- |
| Koniec kazdej sesji         | `memory/LAST_SESSION.md`       | Pelne podsumowanie            |
| Koniec kazdej sesji         | `memory/BACKLOG.md`            | Usun zrobione, dodaj nowe     |
| Koniec kazdej sesji         | `memory/ACTIVE_WORKSPACE.md`   | Zaktualizuj stan + zmiany     |
| Nowa decyzja operatora      | `memory/OPERATOR_DECISIONS.md` | Dodaj [ACTIVE], zamknij stare |
| Zmiana architektury         | `ARCHITECTURE_DECISIONS.md`    | Dodaj/usun regule             |
| Zmiana endpointow/ownership | `world-state.yaml`             | Aktualizuj pola               |
| Zmiana cross-repo           | `TOPINSTAL-KERNEL-GRAPH.yaml`  | Dodaj/usun krawedz            |
| Nowe/zmienione SoT          | `source-of-truth.md`           | Aktualizuj macierz            |
| Nowy bug/system change      | `memory/BACKLOG.md`            | Dodaj P0/P1/P2/P3             |
| Zmiana w diagramach         | `SYSTEM_ATLAS.md`              | Aktualizuj diagramy           |
| RFC closed                  | Przenies do `rfc/archive/`     | —                             |
| Nowa sesja                  | Czytaj INDEX.md                | —                             |

## Czego nie robic

- Nie tworz nowych plikow w root knowledge/ bez uzasadnienia. LIVE dokumentow jest 22 (root 9 + docs/ 6 + rfc/ 7) — kazdy nowy to decyzja.
- Nie twórz dokumentow "na wszelki wypadek". Jesli informacja jest w kodzie, pytaj CBM.
- Nie powtarzaj w docs/ tego co jest w kanonicznych dokumentach. Wskaz referencja.
- Nie przywracaj dokumentow z archive/ bez konkretnego uzasadnienia.
- Nie twórz duplikatow world-state.yaml jako plikow .md. world-state jest SoT.
- Nie pisz "jak to dziala" w docs/ — to jest w kodzie i w diagramach SYSTEM_ATLAS.md.

## Dokumentacja a CBM

CBM (Codebase Memory MCP) zastepuje nastepujace archiwalne dokumenty:

| Pytanie               | Zamiast czytac          | Uzyj CBM                                                                |
| --------------------- | ----------------------- | ----------------------------------------------------------------------- |
| Lista write executors | WRITE_EXECUTOR_GRAPH.md | `search_code(gmail-agent, "^execute_")`                                 |
| Mapa endpointow API   | API_INGRESS.md          | `get_architecture(project, "routes")` lub `query_graph MATCH (r:Route)` |
| Mapa repozytoriow     | REPOSITORY_MAP.md       | `AGENTS.md` + `world-state.yaml repos.*`                                |
| Kto wola ten symbol   | impact_analysis skill   | `trace_path(project, symbol, callee)`                                   |
| Kontrakty miedzyrepo  | SYSTEM_CONTRACTS.md     | `TOPINSTAL-KERNEL-GRAPH.yaml` + CBM cross-project                       |

Nie utrzymuj statycznych kopii tych informacji. CBM generuje je z kodu.

## Zasada ostatniej deski ratunku

Jesli nie wiesz gdzie cos napisac:

1. Czy to fakt o systemie? → world-state.yaml
2. Czy to decyzja operatora? → OPERATOR_DECISIONS.md
3. Czy to regula implementacji? → ARCHITECTURE_DECISIONS.md
4. Czy to zadanie? → BACKLOG.md
5. Czy to diagram? → SYSTEM_ATLAS.md
6. Czy to wlasciciel danych? → source-of-truth.md
7. Czy to stan sesji? → LAST_SESSION.md / ACTIVE_WORKSPACE.md
8. Czy to RFC? → rfc/
9. Czy to odpowiedz na konkretne pytanie ktore nie miesci sie nigdzie indziej? → docs/
10. Czy agent moze to wyciagnac z CBM? → nie pisz, pytaj CBM.
