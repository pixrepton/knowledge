# RFC: Customer Identity Architecture v1

| Pole          | Wartość                                       |
| ------------- | --------------------------------------------- |
| **Data**      | 2026-06-19                                    |
| **Status**    | implemented (case_engagement_bridge, Phase 7) |
| **Powiązane** | P0 Correlation Registry, P1 email dedup       |

---

## 1. Model danych (pseudo-SQL)

### As-Is (P0 — zaimplementowane)

```sql
-- correlation_registry/schema.py
CREATE TABLE topinstal_identities (
    identity_id TEXT PRIMARY KEY,
    primary_email TEXT NOT NULL,  -- brak UNIQUE (multi-investment)
    display_name TEXT NOT NULL DEFAULT '',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE topinstal_engagements (
    engagement_id TEXT PRIMARY KEY,
    identity_id TEXT NOT NULL REFERENCES topinstal_identities(identity_id),
    status TEXT NOT NULL DEFAULT 'open',
    anchor_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE correlation_links (
    link_id TEXT PRIMARY KEY,
    engagement_id TEXT NOT NULL REFERENCES topinstal_engagements(engagement_id),
    link_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    source_repo TEXT NOT NULL DEFAULT 'gmail-agent',
    confidence REAL NOT NULL DEFAULT 1.0,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (link_type, target_id, source_repo)
);
```

### To-Be (P2+ — po osobnej sesji implementacyjnej)

```sql
-- Additive metadata only; no UNIQUE on primary_email
ALTER TABLE topinstal_identities
  -- metadata.identity_kind: 'person' | 'organization'
  -- metadata.contact_roles: ['billing', 'technical', 'decision_maker']

ALTER TABLE topinstal_engagements
  -- metadata.property_anchor: {address_norm, nip, investment_key}
  -- metadata.binding_level_applied: 1 | 2 | 3

-- Poziom 2 suggestions (nie auto-merge)
CREATE TABLE identity_binding_suggestions (
    suggestion_id TEXT PRIMARY KEY,
    source_identity_id TEXT NOT NULL,
    target_identity_id TEXT NOT NULL,
    signal_type TEXT NOT NULL,  -- nip_match | phone_match | fuzzy_name_address
    confidence REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending_operator',  -- pending_operator | approved | rejected
    evidence_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Hierarchia korelacji:** `engagement_id` > `identity_id`. Timeline, RAG D1, Similar Cases, agent runtime kluczują po `engagement_id`.

---

## 2. Trzy poziomy pewności wiązania

| Poziom | Nazwa             | Mechanizm (kod)                                                            | Auto-bind? | Confidence |
| ------ | ----------------- | -------------------------------------------------------------------------- | ---------- | ---------- |
| **1**  | Technical         | `_TECHNICAL_PRECEDENCE` w `heuristics.py`: message, thread, case, workflow | Tak        | 0.95–1.0   |
| **2**  | Heuristic suggest | NIP/telefon/fuzzy name+address — wzorzec z `entity_linker.py`              | **Nie**    | 0.55–0.85  |
| **3**  | Operator explicit | Daszek: link / unlink / merge identity                                     | Po HITL    | 1.0        |

### Przykłady

| Scenariusz                                            | Poziom          | Wynik                                        |
| ----------------------------------------------------- | --------------- | -------------------------------------------- |
| Ten sam `gmail_message_id` w mailu i Cieplo           | 1               | Jeden `engagement_id`, case + workflow linki |
| Ten sam email, nowy `mailbox_case` (druga inwestycja) | 1 (split guard) | Osobny `identity_id` + `engagement_id`       |
| Ten sam NIP, inny email, brak technical link          | 2               | Sugestia `pending_operator` w Daszku         |
| Operator ręcznie łączy duplikaty po audycie           | 3               | Merge po zatwierdzeniu                       |

---

## 3. Pytanie 1: person vs household vs dual

### Opcje

| Opcja | Opis                                                | Werdykt                                                                      |
| ----- | --------------------------------------------------- | ---------------------------------------------------------------------------- |
| A     | `identity_id` = wyłącznie osoba                     | Odrzucone — łamie `test_same_email_different_cases_get_separate_engagements` |
| B     | `identity_id` = wyłącznie gospodarstwo/nieruchomość | Odrzucone — traci email jako anchor P0                                       |
| **C** | **Model dualny**                                    | **Przyjęte**                                                                 |

### Dowód z kodu

- `schema.py`: `-- No UNIQUE on primary_email: one mailbox may represent multiple investments (HVAC).`
- `test_correlation_registry.py::test_same_email_different_cases_get_separate_engagements`: ten sam email, dwa case → dwa identity + engagement.

### Decyzja operatora: **C — model dualny**

- `identity_id` = kanał kontaktowy / aktor (osoba lub reprezentant firmy).
- `engagement_id` = wątek biznesowy; scope nieruchomości w `engagement.metadata.property_anchor` (P2+).
- `identity_kind` ∈ `{person, organization}` w `identity.metadata` (P2+).
- Wspólny email rodziny: jeden identity, wiele engagementów przy różnych inwestycjach; jeden engagement przy tym samym thread/message.

---

## 4. Pytanie 2: heurystyka Poziomu 2

### Opcje

| Opcja | Opis                           | Werdykt                                   |
| ----- | ------------------------------ | ----------------------------------------- |
| A     | Rozszerzyć auto-bind email 30d | Już istnieje (conf 0.7) — nie rozszerzać  |
| B     | Auto-bind fuzzy w registry     | Odrzucone — ryzyko powtórki 28 duplikatów |
| **C** | **Suggest-only + HITL**        | **Przyjęte**                              |

### Dowód z kodu

- `entity_linker.py`: fuzzy phase z `ENTITY_LINK_THRESHOLD=0.85`, wyniki `PENDING_ADJUDICATION` — case-scoped HITL.
- Registry dziś nie ma fuzzy; Poziom 2 = nowa tabela `identity_binding_suggestions`, nie auto-merge.

### Decyzja operatora: **C — Poziom 2 = tylko sugestia operatorowi**

**Kiedy sugerować (bez nowego tekstu w mailu):**

- Ten sam znormalizowany NIP lub telefon na różnych emailach w oknie **90 dni**
- Fuzzy score name+address ≥ **0.85**
- Nigdy auto-merge dwóch `identity_id` z różnymi aktywnymi engagementami

---

## 5. Pytanie 3: migracja 28 duplikatów vs równoległy Poziom 1

### Opcje

| Opcja | Opis                                              | Werdykt                                      |
| ----- | ------------------------------------------------- | -------------------------------------------- |
| A     | Czekaj na model household                         | Odrzucone — duplikaty = artefakt backfill P0 |
| B     | Big-bang fuzzy merge                              | Odrzucone                                    |
| **C** | **P1 email dedup równolegle + additive Poziom 1** | **Przyjęte**                                 |

### Dowód z kodu

- `P1-mini-identity-email-dedup.md`: staging `merged_groups=28`, `engagements_repointed=97`.
- `reconcile_identity_emails.py`: merge tylko `lower(primary_email)` identical, canonical = najstarszy.

### Decyzja operatora: **C — równolegle, konserwatywnie**

---

## 6. Plan migracji 28 duplikatów (kolejka ręczna)

1. `python scripts/reconcile_identity_emails.py --dry-run` — raport grup lokalnych
2. Operator review raportu (multi-investment false positive check)
3. `python scripts/reconcile_identity_emails.py` — merge email-identical only
4. `--require-zero-after` na czystym środowisku
5. Pozostałe edge cases (różne emaile, ten sam klient) → kolejka Daszek Poziom 3, bez auto-merge

---

## 7. Integracja z engagement_id

`engagement_id` jest warstwą nadrzędną ([`CORRELATION_REGISTRY_P0_CONTRACT.md`](../../gmail-agent/docs/core/CORRELATION_REGISTRY_P0_CONTRACT.md)):

- Mail case ↔ Cieplo workflow: wspólny `engagement_id` przez technical links
- `GET /cases/{id}/engagement`, merged timeline, RAG D1 scope, Similar Cases — wszystko po `engagement_id`
- `identity_id` = parent FK; nie zastępuje engagement w korelacji cross-repo
- **Nigdy** `engagement_id = case_id` (test kontraktowy)

---

## 8. Edge cases (propozycje, bez implementacji w tej sesji)

| Case                           | Propozycja                                                                      |
| ------------------------------ | ------------------------------------------------------------------------------- |
| Mąż/żona, wspólny email        | Jeden identity; engagement split przy różnych inwestycjach / threadach          |
| Firma vs osoba fizyczna        | `identity_kind=organization` + contact person w metadata                        |
| Lead → klient → serwis         | Widget placeholder email → `heuristics._enrich_identity_email_from_placeholder` |
| Property manager, 5 inwestycji | 5 engagementów; opcjonalnie wspólny identity jeśli ten sam email kontaktowy     |
| Fałszywa korelacja             | Poziom 3 unlink w Daszku (P2 UI)                                                |

---

## 9. Fazy implementacji przyszłej sesji + proof gates

| Faza | Zakres                                                      | Proof                                  |
| ---- | ----------------------------------------------------------- | -------------------------------------- |
| P2.0 | `identity_kind` + `property_anchor` metadata (additive DDL) | `CUSTOMER_IDENTITY_METADATA_PROOF_OK`  |
| P2.1 | `identity_binding_suggestions` + API read                   | `IDENTITY_BINDING_SUGGEST_PROOF_OK`    |
| P2.2 | Daszek UI: kolejka sugestii + merge/unlink                  | `IDENTITY_OPERATOR_UI_PROOF_OK`        |
| P3   | Integracja Poziom 2 z entity_linker signals                 | `IDENTITY_LEVEL2_INTEGRATION_PROOF_OK` |

---

## 10. Co NIE wchodzi w RFC

- UNIQUE na `primary_email`
- Auto-merge fuzzy bez operatora
- Neo4j jako SoT identity
- Merge `mailbox_memory` + `cieplo_worker` DB
- Win/loss CBR na identity
- VPS / produkcja bez osobnej decyzji operatora
