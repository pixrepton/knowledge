# Registry Validation Report

## Scope

Read-only preview normalizacji kontraktu `knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml`.
Zakres obejmuje wyłącznie:

- finalny podział semantyk `status` vs `runtime` vs `workflow_test_status`
- zamknięte taksonomie dla statusów ścieżki, defektów kontraktu, runtime, test coverage i confidence
- wykrycie wartości użytych dziś w niewłaściwym polu
- przygotowanie merge-ready planu bez mutowania plików kanonicznych

MCP nie użyto.

## Files inspected

- `AGENTS.md`
- `CLAUDE.md`
- `knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml`
- `knowledge/system-atlas/workflows/WORKFLOW_EVIDENCE.jsonl`
- `knowledge/system-atlas/workflows/WORKFLOW_GAPS.md`
- `knowledge/system-atlas/workflows/PROGRESS.md`
- `knowledge/system-atlas/workflows/_raw/status_value_writer_consumer_cross_reference.md`
- `knowledge/system-atlas/workflows/_raw/test_evidence_mapping_cross_reference.md`

## Assumptions

- Source of truth to aktualny working tree i istniejące `_raw` artefakty, nie starsza narracja.
- Ten preview nie zmienia kanonicznego rejestru ani plików syntezy końcowej.
- `workflow_test_status` zostaje osobnym top-level indeksem, bo już istnieje i ma pełne pokrycie `17/17`.
- `confidence` pozostaje własnością rekordów w `WORKFLOW_EVIDENCE.jsonl`, a nie workflowów.
- `runtime` musi zostać rozbite na pola strukturalne; wolny tekst może zostać tylko jako `runtime.note`.

## Findings

### Facts

- `WORKFLOW_REGISTRY.yaml` ma dziś `17` workflowów, `4` subflowy i top-level `workflow_test_status` z `17` wpisami.
- Bieżący płaski słownik `status` zawiera dokładnie: `BROKEN_CALL`, `CONDITIONAL_PATH`, `CORRECTED`, `DORMANT_PATH`, `LIVE_PATH`, `MANUAL_TRIGGER_ONLY`, `MISSING_CONSUMER`, `MISSING_PRODUCER`, `RUNTIME_CONFIRMED`, `RUNTIME_UNVERIFIED`.
- `WORKFLOW_EVIDENCE.jsonl` ma już osobne pola `evidence_type` i `confidence`; znalezione wartości to `ABSENCE_SEARCH`, `CODE`, `TEST` oraz `HIGH`, `MEDIUM`.
- Header komentarza rejestru nadal dokumentuje `TEST_ONLY`, `PROOF_ONLY` i `RUNTIME_*` jako elementy `status`, mimo że test coverage już żyje osobno w `workflow_test_status`.

### Wrong-field usage detected

- `RUNTIME_CONFIRMED` albo `RUNTIME_UNVERIFIED` występuje w `status` dla `16/17` workflowów. To jest semantyka dowodu runtime, nie statusu workflow.
- `MANUAL_TRIGGER_ONLY` występuje w `status` workflowu `SLA-WATCHER-DECISION-ESCALATION`. To jest tryb wyzwalania, nie status.
- `CORRECTED` występuje w `status` workflowu `DASZEK-COMMAND-OUTBOX-DRAIN`. To jest historia korekty/opis rewizji, nie status kanoniczny.
- Nawet po odjęciu `RUNTIME_*`, płaski `status` dalej miesza co najmniej dwie osie: stan ścieżki i defekt kontraktu. Najbardziej jawne przykłady:
  - `CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP`: `LIVE_PATH + BROKEN_CALL + MISSING_CONSUMER`
  - `CALENDAR-TWO-WORLDS-OF-VISITS`: `LIVE_PATH + DORMANT_PATH + MISSING_PRODUCER`

### Conclusions

- Minimalny sensowny fix kontraktu to nie tylko wyjęcie `RUNTIME_*` ze `status`, ale rozdzielenie płaskiego `status` na `path_statuses` i `contract_statuses`.
- `workflow_test_status` jest już poprawnym miejscem dla semantyki testowej i nie powinien wracać do `status`.
- `confidence` nie powinno być promowane do rejestru workflowów, bo agregowałoby wiele `EV-*` o różnych scope i różnej sile dowodu do jednego subiektywnego skrótu.

## Proposed changes

1. Zamienić obecne `status` na dwa pola:
   - `path_statuses`: zamknięta taksonomia ścieżki/liveness
   - `contract_statuses`: zamknięta taksonomia defektów kontraktu
2. Zamienić obecne `runtime` z wolnego tekstu na obiekt:
   - `classification`
   - `evidence_scope`
   - `trigger_mode`
   - `note`
   - opcjonalnie `evidence_ids`
3. Zachować `workflow_test_status` jako jedyne miejsce dla test coverage i wymusić relację `1:1` z `workflows`.
4. Pozostawić `confidence` wyłącznie w `WORKFLOW_EVIDENCE.jsonl`.
5. Zaktualizować komentarz schema header, bo dziś opisuje stary kontrakt i aktywnie zachęca do mieszania semantyk.

Docelowe taksonomie są zapisane w:

- `knowledge/system-atlas/workflows/_raw/subagents/registry/registry_normalization_plan.yaml`

## Unresolved

- Czy `path_statuses` ma zawsze dopuszczać współwystępowanie `LIVE_PATH` i `DORMANT_PATH`, czy część takich rodzin powinna docelowo zostać rozbita na dwa workflowy. Ten preview zostawia współwystępowanie jako dozwolone, bo tak wygląda aktualny modeling.
- Czy `runtime.evidence_ids` ma być obowiązkowe, czy może domyślnie dziedziczyć z top-level `evidence_ids`. W planie zostawiono je jako opcjonalne, żeby nie dublować referencji bez realnej potrzeby.
- Czy część dzisiejszych wolnych tekstów w `gaps` i `runtime` wymaga później dodatkowego skrócenia po migracji do pola strukturalnego. To jest kwestia redakcyjna, nie blocker kontraktu.

## Validation commands

```powershell
git -C knowledge rev-parse HEAD
git -C knowledge status --short
rg -n "^  - workflow_id:|^workflow_test_status:|statuses: \[|status: \[|runtime:" knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml
rg -n "MANUAL_TRIGGER_ONLY|CORRECTED|RUNTIME_CONFIRMED|RUNTIME_UNVERIFIED|TEST_ONLY|PROOF_ONLY" knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml
rg -n '"confidence"|"evidence_type"' knowledge/system-atlas/workflows/WORKFLOW_EVIDENCE.jsonl
python -c "import pathlib, re; txt=pathlib.Path(r'knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml').read_text(encoding='utf-8'); ids=re.findall(r'^  - workflow_id: (.+)$', txt, re.M); tail=txt[txt.index('workflow_test_status:'):]; tests=re.findall(r'^  ([A-Z0-9-]+):$', tail, re.M); print({'workflow_count': len(ids), 'unique_workflows': len(set(ids)), 'test_status_entries': len(tests), 'unique_test_keys': len(set(tests))})"
python -c "import json, pathlib, re; ev={json.loads(line)['id'] for line in pathlib.Path(r'knowledge/system-atlas/workflows/WORKFLOW_EVIDENCE.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()}; txt=pathlib.Path(r'knowledge/system-atlas/workflows/WORKFLOW_REGISTRY.yaml').read_text(encoding='utf-8'); refs=set(re.findall(r'EV-\\d{5}', txt)); missing=sorted(refs-ev); print({'referenced_evidence_ids': len(refs), 'missing_count': len(missing), 'missing_preview': missing[:20]})"
python -c "import yaml, pathlib; yaml.safe_load(pathlib.Path(r'knowledge/system-atlas/workflows/_raw/subagents/registry/registry_normalization_plan.yaml').read_text(encoding='utf-8')); print('registry_normalization_plan.yaml: YAML_OK')"
```

## Repo SHA

- `knowledge`: `597b1091a296930ed32afb379ec19b8ab425d4fa`

## Timestamp

- `2026-07-30 22:15:56 +02:00`
