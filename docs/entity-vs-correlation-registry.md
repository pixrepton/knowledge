# Entity Registry vs Correlation Registry — wyjasnienie

## Dla kogo

- **Operator biznesowy:** sekcje [BIZ]
- **Asystent AI / przyszly developer:** sekcje [DEV]

---

## [BIZ] Problem w jednym zdaniu

Gdy system przyjmuje email klienta (np. `jan@example.com`), zapisuje go **do dwoch roznych tabel** w dwoch roznych formatach, bez synchronizacji miedzy nimi. To oznacza, ze ten sam klient moze miec dwa rozne ID w systemie — a co gorsza, nikt nie wie ktore jest wlasciwe.

---

## [BIZ] Dwa swiaty

### Swiat 1: Entity Registry

**Co to:** Prosta lista "email -> unified_id". Kazdy email wystepuje tylko raz.
**Cel:** Szybkie znalezienie klienta po emailu.
**Gdzie zapisany:** W nowej tabeli `entity_registry`, utworzonej podczas sesji z 24 czerwca 2026.
**Jak powstaje:** Automatycznie, przy kazdej nowej sprawie (w `mailbox_memory_runtime.py`).

### Swiat 2: Correlation Registry

**Co to:** Pelny system identyfikacji. Jeden email moze miec wiele "tozsamosci" (bo jedna skrzynka pocztowa moze nalezec do malzenstwa, firmy, lub inwestycji).
**Cel:** Lczenie wszystkich kanalow (Gmail, cieplo.app, kalk-top, lead widget) pod jednym identyfikatorem.
**Gdzie zapisany:** W tabelach `topinstal_identities` + `topinstal_engagements` + `correlation_links`.
**Jak powstaje:** Rejestrowany przez kazdy system (gmail-agent, cieplo-orchestrator, fast-kalk) przez endpoint `/internal/registry/links`.

### Ktory jest "prawdziwy"?

**Zaden nie jest.** To dwa osobne zrodla prawdy:

- Entity Registry mowi: "email X nalezy do klienta Y"
- Correlation Registry mowi: "email X moze byc powiazany z wieloma tozsamosciami"

Gdy potrzebujesz odpowiedziec na pytanie "ile spraw ma klient jan@example.com", dostajesz dwie rozne odpowiedzi w zaleznosci od tego, ktorej tabeli zapytasz.

---

## [DEV] Szczegoly techniczne

### Entity Registry

```sql
CREATE TABLE IF NOT EXISTS entity_registry (
    unified_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email          TEXT NOT NULL,
    canonical_name TEXT NOT NULL DEFAULT '',
    phone          TEXT NOT NULL DEFAULT '',
    source_system  TEXT NOT NULL DEFAULT 'gmail-agent',
    metadata       JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_entity_registry_email_lower
    ON entity_registry (LOWER(email));
```

**Kluczowe cechy:**

- `UNIQUE` na `LOWER(email)` — jeden email = jedna encja
- Automatyczne tworzenie podczas `ingest_message()` w `mailbox_memory_runtime.py` (linia ~300)
- Funkcje: `link_entity_identity(email, ...)`, `resolve_entity_by_email(email)`, `merge_entity_registry(source, target)`
- **Brak DDL w bootstrappie** — dodane PO utworzeniu kodu (24.06.2026 wieczorem)

### Correlation Registry

```sql
CREATE TABLE IF NOT EXISTS topinstal_identities (
    identity_id   TEXT PRIMARY KEY,
    primary_email TEXT NOT NULL,
    display_name  TEXT NOT NULL DEFAULT '',
    metadata      JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- UWAGA: brak UNIQUE na primary_email!
CREATE INDEX IF NOT EXISTS idx_topinstal_identities_primary_email_lookup
    ON topinstal_identities (lower(primary_email));

CREATE TABLE IF NOT EXISTS topinstal_engagements (
    engagement_id TEXT PRIMARY KEY,
    identity_id   TEXT NOT NULL REFERENCES topinstal_identities(identity_id) ON DELETE CASCADE,
    ...
);

CREATE TABLE IF NOT EXISTS correlation_links (
    ...
    link_type TEXT NOT NULL,  -- 'cieplo_workflow', 'gmail_message', 'calc_request_snapshot', etc.
    ...
);
```

**Kluczowe cechy:**

- **Brak UNIQUE na primary_email** — swiadoma decyzja (komentarz w kodzie: "one mailbox may represent multiple investments")
- Pelny model engagementow: jedna tozsamosc moze miec wiele engagementow (spraw, workflowow, sesji kalkulatora)
- Historia merge'ow: `identity_merge_log` z audit trail
- Sugestie bindingow: `identity_binding_suggestions` — L2 suggest-only (operator zatwierdza)
- Rejestrowany przez: `gmail-agent` (przy ingescie), `cieplo-orchestrator` (przez HTTP POST), `fast-kalk` (lead widget)

### Gdzie są zapisywane (stan po 2026-06-25)

W `mailbox_memory_runtime.py` podczas `ingest_message()`:

```python
# Jeden zapis tożsamości — fasada nad Correlation Registry
link_entity_identity(sender_email, canonical_name=..., db_url=_db_url)

# Osobno: sync sprawy z correlation_registry (engagementy, linki)
self.correlation_registry.sync_mailbox_case(customer_email=sender_email, ...)
```

`link_entity_identity()` wywołuje `CorrelationRegistryStore` (`topinstal_identities`). Tabela `entity_registry` jest **wycofana** — nie tworzyć nowych rekordów.

### Decyzja wdrożona (2026-06-25)

**Scenariusz B (uproszczony):** Correlation Registry jest jedynym SoT tożsamości. `entity_linker.py` zachowuje fasady API (`resolve_entity_by_email`, `link_entity_identity`, `backfill_entity_registry`) ale zapisuje wyłącznie do `topinstal_identities`.

- `POST /identity/merge` używa `CorrelationRegistryStore` (nie `merge_entity_registry`)
- `backfill_entity_registry()` migruje emaile z `mailbox_memory_cases` do correlation registry
- Stara tabela `entity_registry` może pozostać w PG (dane historyczne) — **nie używać w nowym kodzie**

### Rekomendacja (historyczna — przed wdrożeniem)

~~Scenariusz A~~ — zastąpione przez Scenariusz B (fasada + Correlation Registry jako SoT).

**Pozostaje dla operatora:** L3 merge UI — ręczne scalenie ~28 grup duplikatów email w Daszek System tab.
