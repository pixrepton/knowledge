# AUDYT INTELIGENCJI AI-OS — pełny przebieg (2026-08-21)

Status dokumentu: **CURRENT / PARTIAL** — pełny jednoprzebiegowy audyt 23 obszarów
inteligencji (read-only). Nie zawiera runtime proof (poza powołaniem się na istniejące,
wcześniej udowodnione artefakty). Nie wykonano zmian produktowych.

## 0. Metadane przebiegu

- Data: 2026-08-21 (Europe/Warsaw).
- Zakres: `gmail-agent` (Node B) jako źródło inteligencji; `knowledge` jako rejestr.
- Metoda: AI-OS safe mode — Git / `rg` / wąskie odczyty plików. Brak reindeksacji,
  brak CBM MCP (nie wystawione w sesji), GitNexus tylko jako zasób `gitnexus://repos`
  (świeżość = HEAD bieżący dla wszystkich repo).
- Baseline dowodu: `gmail-agent` HEAD `a3d3ae6`, `knowledge` HEAD `ab3b1e5`,
  `top-code-workspace` HEAD `7696a26`; indeksy GitNexus zgodne z HEAD.
- Ograniczenia: bez Full Fresh38, bez zmian produktu, bez reindeksacji, bez VPS.
- Brudny stan worktree zachowany bez zmian (gmail-agent: 2 linie docs + CRLF noise
  w 4 plikach; knowledge: 3 pliki; root: skrypty + untracked nested repo).

## 1. Legenda statusów

| Status | Znaczenie |
| --- | --- |
| PROVEN | mechanizm udowodniony testami/kontraktem w bieżącym źródle |
| PROVEN_USED | udowodniony i faktycznie wywoływany w ścieżce runtime |
| CONFIGURED | obecny w kodzie/konfiguracji, bez pełnego dowodu użycia |
| PARTIALLY_WORKING | działa w udowodnionym podzbiorze; reszta ma luki |
| MISSING | mechanizm nie istnieje w kodzie |
| RISK | istnieje ryzyko semantyczne/bezpieczeństwa wymagające decyzji |
| UNKNOWN | brak wystarczającego dowodu w tym przebiegu |
| DATASET_REQUIRED | wymaga danych/operatora (np. oznaczone przypadki) |

## 2. Executive summary

System ma dziś **spójny, mechanicznie udowodniony rdzeń decyzyjny** dla ścieżki
customer clarification (SVC-05: `collect_data -> prepare_reply ->
ask_for_missing_data/mail -> generate_draft_reply -> HITL`), **fail-closed warstwę
policy i execution** oraz **append-only observability**. Pełny audyt wskazuje 5
obszarów wymagających decyzji operatora (sekcja 24) i 1 obszar zablokowany na
braku danych (A21).

| # | Obszar | Status |
| --- | --- | --- |
| A1 | Understanding | PARTIALLY_WORKING |
| A2 | Fakty / Claims / Evidence | PROVEN_USED (rdzeń) + PARTIALLY_WORKING (konsolidacja) |
| A3 | BusinessReasoning contract | PROVEN |
| A4 | Decision Spine | PARTIALLY_WORKING (bounded PROVEN, general mapping NO_SAFE_MAPPING) |
| A5 | Planner / Tool selection | PARTIALLY_WORKING (RISK: fallback LLM) |
| A6 | Policy / Autonomy | PARTIALLY_WORKING (MISSING: model A0-A4) |
| A7 | HITL | PROVEN (approval), RISK (fallback ROC w promptach) |
| A8 | Draft / komunikacja | PROVEN (kontrakty), UNKNOWN (nie wiem vs zgadnę) |
| A9 | Follow-up / Open Loops | PROVEN_USED (stagnacja), PARTIALLY_WORKING (pełny cykl) |
| A10 | Learning | PARTIALLY_WORKING (hooki + ledger; konsolidacja do weryfikacji) |
| A11 | Prompty / modele LLM | RISK (policy w NL częściowo duplikuje mechanikę) |
| A12 | Structured outputs | CONFIGURED + PROVEN; RISK (second-pass repair) |
| A13 | Security inteligencji | PROVEN (bounded); UNKNOWN (indirect prompt injection poza action-args) |
| A14 | Execution boundary | PROVEN (write path: idempotency + approval + correlation) |
| A15 | Providerzy / failure semantics | PROVEN (router + klasyfikacja); PARTIAL (mapa fallbacków etapów) |
| A16 | Legacy / compatibility | CONFIGURED (shimy), MISSING-ryzyko (dormant legacy) |
| A17 | Duplikacja semantyki | RISK (3 słowniki decyzji, typ NBA dict vs string) |
| A18 | Architektura danych | PARTIALLY_WORKING (provenance obecny; typ NBA niespójny) |
| A19 | Observability | PROVEN_USED; PARTIAL (brak jednego kanonicznego replay CLI udowodnionego) |
| A20 | Testy | PARTIALLY_WORKING (357 plików / 2529 testów; brak property/adversarial) |
| A21 | Realne zachowania | DATASET_REQUIRED |
| A22 | Koszt inteligencji | PARTIALLY_WORKING (tokens_used istnieje; brak agregatu) |
| A23 | „Czy system rozumie siebie" | MISSING |

## 3. A1 — Understanding

- Kontrakt: [understanding_output.py](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/understanding_output.py:1>)
  „projection-safe situation understanding"; źródło `deterministic_projection`
  (:236); walidacja invariantów :254.
- RC-IQ-R1 (:97-103): niezadane pytanie klienta = OPEN LOOP, nie dana do
  rozumienia; usunięte z powierzchni gap.
- Stage w pipeline: [gmail_intake.py:3164-3189](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/gmail_intake.py:3164>)
  — `understanding_output_enabled`, deterministyczna projekcja.
- Operator snapshot: [case_intelligence/understanding.py:93](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/case_intelligence/understanding.py:93>).

Ustalenia: projekcja nie „rozumuje ponownie" — kopiuje canonical state
(conflicting_facts, open_questions, missing fields) z CaseContextPack. **Luka**:
intencja klienta jest reprezentowana jako pojedyncze pole
`customer_intent_pl`/`current_customer_intent`; wiele intencji naraz nie jest
pierwszorzędnym modelem (sygnał jest 1:intencja + lista unresolved questions).
Konflikt intencji nie jest modelowany osobno od konfliktu faktów.

## 4. A2 — Fakty, Claims, Evidence, pamięć

- Active vs superseded: [mailbox_memory/active_facts.py:64](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/mailbox_memory/active_facts.py:64>)
  (`is_live_fact`), :100 `annotate_decision_fact_use` (conflict -> `decision_usable=False`),
  :134 `action_conflict_block`.
- Supersession (RP-29) + conflict-preservation: [understanding_output.py:421](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/understanding_output.py:421>);
  commity `56cee32` (preserve merge conflicts without newer wins) i `7683299`
  (customer-message value change = conflict, nie cicha supersession).
- Fakty mają confidence + observed_at + status: [mailbox_memory/facts.py:65](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/mailbox_memory/facts.py:65>).
- Testy: `test_fact01_snapshot_supersession.py`, `test_rp29_fact_supersession.py`.

Ustalenia: jedna filozofia prawdy dla rdzenia faktów = **active rows + jawny
conflict set**; timestamp sam nie czyni wartości „prawdziwą" (nowszy wpis nie
usuwa starszego — status superseded + conflict). **Residual**: konsolidacja
Mem0-style ([memory_consolidation/__init__.py:40](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/memory_consolidation/__init__.py:40>)
`dedupe_facts`) nie została w tym przebiegu mechanicznie dowiedziona jako
bezpieczna względem hierarchii dowodu — do weryfikacji reachability i testów.

## 5. A3 — BusinessReasoning contract

- Pydantic: [llm_contracts/business_reasoning.py:7](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/llm_contracts/business_reasoning.py:7>)
  (`extra=ignore`, enum-y w walidatorze).
- Normalizacja decyzyjna: [intake_schema.py:321-445](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/intake_schema.py:321>)
  — SVC-05: `escalate_review -> collect_data` gdy `customer_clarification_possible`;
  DEC-02: `post_offer + collect_data -> escalate_review` (jednokierunkowo w stronę
  eskalacji). Żadnych case-id, żadnych wyjątków tekstowych.
- Prompt: [business_reasoner.py:76](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/business_reasoner.py:76>)
  „przy słabych dowodach preferuj escalate_review"; default walidatora
  `escalate_review` (:264, :333).
- Testy: [test_svc05_customer_clarification.py:68-125](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/tests/test_svc05_customer_clarification.py:68>)
  (positive + negative cohort SVC-01/SVC-02/MI-03/DEC-01).

Ustalenia: kontrakt kompletny (input -> prompt -> structured output -> validator ->
fallback -> confidence -> missing info -> risk -> action). **Uwaga**: „low
confidence -> inna akcja" istnieje tylko w tekście promptu („preferuj
escalate_review"), nie jako mechaniczny warunek — decyzja zostaje w modelu.

## 6. A4 — Decision Spine

Pełna tabela transformacji w sekcji 24.1. Kluczowe dowody:

- ActionPlan: [action_planner.py:66-97](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/action_planner.py:66>).
- NBA: [case_intelligence/next_best_action.py:47-113](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/case_intelligence/next_best_action.py:47>).
- Policy proposal: [policy_action_proposal.py:118-160](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/policy_action_proposal.py:118>).
- PolicyDecision: [policy_decision.py:30-90](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/policy_decision.py:30>).
- APv2: [action_proposal_v2.py:28-123](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/action_proposal_v2.py:28>).
- Envelope/tool guard: [policy_action_spine.py:47-77](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/policy_action_spine.py:47>);
  [graph.py:759-885](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/graph.py:759>).

Ustalenia: dla ścieżki customer clarification każda warstwa zachowuje adresata
pytania (customer/mail) — `forbidden_tools=[request_operator_clarification]`.
Jednak `ACTION_INTENT_TOOL_MAPPING_CLASSIFICATION = "NO_SAFE_MAPPING_EXISTS"`
([policy_action_spine.py:29](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/policy_action_spine.py:29>))
— poza tym jednym invariantem ogólne action->tool mapowanie nie jest ustalone.

## 7. A5 — Planner / Tool selection

- Allowlist: [policy_guardrails.py:19-28](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/policy_guardrails.py:19>),
  [effective_tools.py](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/effective_tools.py:47>).
- Hint deterministyczny: [recommended_next_step_quality.py:144-178](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/recommended_next_step_quality.py:144>)
  — `ask_for_missing_data` + mail -> `generate_draft_reply`; ale szerokie fallbacki
  zwracają `request_operator_clarification` (serwis bez draft, „dopytaj",
  „decyz", fallback końcowy).
- Prompt LLM: [openai_agent_client.py:417-439](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/openai_agent_client.py:417>)
  — follow-up bez gotowego draftu ma domyślnie `request_operator_clarification`.
- Runtime guard odrzuca mismatch: [graph.py:759-885](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/graph.py:759>).

Ustalenia: wybór toola jest **wolny dla LLM w obrębie allowlisty**, a hint jest
tylko preferencją. Guard chroni tylko ścieżkę, w której NBA dotarł do envelope.
Jeżeli NBA/hint nie dotrze, prompt może zmienić adresata pytania (operator zamiast
klienta). **RISK (HIGH)**: semantic drift w warstwie LLM.

## 8. A6 — Policy / Autonomy

- Reguły: [policy_engine.py:240-575](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/policy_engine.py:240>)
  (LIVE_REPLY first-contact NEEDS_HUMAN; relationship risk REJECTED; fact change
  bez authoritative evidence NEEDS_HUMAN; offer bez verdict REJECTED; technical
  bez sizing NEEDS_HUMAN; conflict/identity/calendar rules; trust defaults).
- P0 gate: [policy_decision.py:38-54](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/policy_decision.py:38>)
  — `_SAFE_P0_ACTIONS` + `_FORBIDDEN_EXTERNAL_ACTIONS`; `dry_run_only` -> fail-closed.
- Authz: [authz.py:146-156](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/authz.py:146>)
  (tool/write permission per scope); constitution allowlist.

Ustalenia: policy **ogranicza „czy/jak wolno"**, nie podmienia „co zrobić"
(action_class pochodzi wyłącznie z `primary_action` planu). **MISSING**: model
autonomy A0-A4 nie istnieje jako pierwszo­rzędny stan; nie znaleziono go w
`agent_runtime`.

## 9. A7 — HITL

- Materializacja: [materialize.py:376](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/materialize.py:376>)
  „Python-only executor after operator approve — never called from LLM";
  append wymusza `hitl_gate` (:159-183).
- Send: [hitl_gmail_send.py:95-141](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/hitl_gmail_send.py:95>)
  (manual operator delivery; Node B read-only dla Gmail/Calendar writes).
- Bridge: [agent_hitl_bridge.py](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_hitl_bridge.py:39>)
  — decision_key + exactly-once; approval binding przez parent refs.
- Rozdzielenie: `request_operator_clarification` (pytanie do operatora) vs HITL
  approval (zatwierdzenie) — rozdzielone w `policy_action_spine` (forbidden dla
  ask_for_missing_data) i w `policy_decision` (adjudication vs missing info).

Ustalenia: approval jest stanem workflow, nie tool-callem. **Residual**: prompt
LLM (A5) może wciąż wybrać ROC jako domyślny pierwszy krok follow-upu.

## 10. A8 — Draft / komunikacja

- Gate: [reply_drafter.py:61-67](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/reply_drafter.py:61>);
  fallback `reply_not_recommended` :144.
- Commitment gating: [reply_drafter.py:355-407](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/reply_drafter.py:355>)
  — niedozwolone obietnice są przepisywane; dozwolone tylko gdy `case_state`
  wspiera.
- Content sanity: [reply_drafter.py:434](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/reply_drafter.py:434>)
  + [draft_sanity.py:48-94](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/draft_sanity.py:48>)
  (service missing_info bez service scope; policy_disallows_draft).
- Odbiorca/intencja: draft budowany z case_state + active facts
  ([reply_drafter.py:233](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/reply_drafter.py:233>)).

Ustalenia: kontrakt draftu udowodniony testami (`test_reply_drafter_contract`,
`test_pf01_draft_sanity_coverage`, `test_aios_1_4_draft_content_contracts`).
**UNKNOWN**: brak mechanicznego rozróżnienia „nie wiem" vs „domyślę się" w samym
drafterze — pokryte tylko pośrednio przez commitment/content gates.

## 11. A9 — Follow-up / Open Loops

- SoT stagnacji: [follow_up_guardian.py:7-42](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/follow_up_guardian.py:7>)
  (delegacja do `stagnation_sot.evaluate_waiting_vs_stagnation`; FG-03: closed
  statusy nie dostają propozycji; dedup; draft sanity przed `enabled`).
- Cykl życia: [case_intelligence/lifecycle.py:109](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/case_intelligence/lifecycle.py:109>).
- Oczekiwanie na kogo: `CASE_GUIDANCE_WAITING_FOR` (client/operator/supplier/...)
  w [case_intelligence/constants.py:37](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/case_intelligence/constants.py:37>).

Ustalenia: guardian działa na 3 stanach (honest scope w docstringu) i nie
proponuje follow-upu dla closed. Reaktywacja = nowy sygnał na sprawie. **Luka**:
pełny cykl „deadline -> follow-up -> reactivate -> close" nie jest jednym
mechanizmem (SLA watcher + guardian + lifecycle osobno).

## 12. A10 — Learning

- Hooks: [operator_learning_hooks.py:9/37/63](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/operator_learning_hooks.py:9>)
  (proposal v2, draft, operator action).
- Ledger: [correction_ledger.py:15](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/correction_ledger.py:15>).
- Konsolidacja: [memory_consolidation/__init__.py:19-61](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/memory_consolidation/__init__.py:19>).
- Test integralności: `test_rp31_learning_integrity.py`.

Ustalenia: rozróżnienie accepted/edited/rejected/overridden/escalated jest
rejestrowane przez hooks/ledger; test rp31 chroni integralność. **Residual**:
ścieżka konsolidacji (dedupe) nie została w tym przebiegu dowiedziona jako
niemożliwa do nadpisania mocniejszego evidence — wymaga osobnego focused proof
lub klasyfikacji jako nieużywana.

## 13. A11 — Prompty / modele LLM

- Pliki promptów: `prompts/` (7 plików, w tym `intake_system_v1.txt`,
  `reply_drafter_system_prompt.md`); kontrakty LLM: `llm_contracts/` (14 plików).
- System prompt agenta: [openai_agent_client.py:400-455](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/openai_agent_client.py:400>).
- Prompt BR: [business_reasoner.py:76](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/business_reasoner.py:76>).

Ustalenia: policy jest częściowo powielona w naturalnym języku („o metraż pytaj
tylko dla ofert", „pierwszym działaniem musi być request_operator_clarification")
i częściowo w mechanicznych gate'ach (draft_sanity, known_fact_guard, spine
forbidden). Natural-language policy może dryfować od mechaniki — **RISK**.

## 14. A12 — Structured outputs

- Pydantic `extra=ignore` we wszystkich kontraktach; enumy/string-listy
  normalizowane w `intake_schema` (z `coercion_notes`).
- Second-pass repair: [gmail_intake.py:2654-2703](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/gmail_intake.py:2654>)
  — `pydantic_failed` -> dodatkowy call LLM z `second_pass_applied` (jawnie
  logowane).

Ustalenia: klasyfikacja free text / typed / validated / normalized / fallback jest
jawna i logowana. **RISK**: parser potrafi „naprawić" zły wynik zamiast go
odrzucić (second-pass merge); ryzyko kontrolowane flagą, ale zmiana znaczenia
przez repair nie jest wykluczona mechanicznie.

## 15. A13 — Security inteligencji

- Fail-closed boundary: [untrusted_input_boundary.py:70-114](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/untrusted_input_boundary.py:70>)
  (untrusted authority/recipient args blokowane; załącznik nie ustanawia
  authority/recipient).
- Known-fact guard: [known_fact_guard.py:107](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/known_fact_guard.py:107>)
  (zakaz re-asku znanych faktów).
- Test: `test_untrusted_input_execution_boundary.py`; commit `2e1d95b`.

Ustalenia: action-args chronione; **UNKNOWN**: indirect prompt injection przez
treść RAG/załącznika poza action-args (np. próba zmiany intencji w długiej
konwersacji) nie ma osobnego mechanicznego guarda — do focused review.

## 16. A14 — Execution boundary

- Lifecycle: [execution_runtime.py:141-261](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/execution_runtime.py:141>)
  (policy_gate -> approve/reject -> execute; decision_key).
- Writes z idempotency: [write_executors.py:873-921](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/tools/write_executors.py:873>);
  [idempotency.py:46-105](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/idempotency.py:46>).
- Stale/correlation: [policy_action_spine.py:299-330](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/policy_action_spine.py:299>)
  (`conflicting`/`stale_policy_envelope`).
- Postcondition: `test_outbound_receipt.py` (mismatch nie przechodzi do
  communication_sent).

Ustalenia: recipient/resource z canonical state, approval binding, idempotency i
stale-decision check obecne. **Dowód runtime poza zakresem tego przebiegu** —
status oparty o kod + testy.

## 17. A15 — Providerzy / failure semantics

- Router z fallbackiem: [llm_provider_router.py:60-203](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/llm_provider_router.py:60>)
  (budżet na providera, `classify_provider_error`: rate_limit/timeout retryable,
  401 nie; empty content retryable delivery).
- Taksonomia: [failure_taxonomy.py:57-115](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/failure_taxonomy.py:57>).
- Deadline: [llm_deadline.py](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/llm_deadline.py>).

Ustalenia: awaria providera nie zmienia decyzji — etapy mają safe fallbacki
(BR -> `escalate_review`). **PARTIAL**: nie sporządzono w tym przebiegu pełnej
mapy „failure -> fallback -> decision" dla każdego etapu (BR/draft/intake/planner).

## 18. A16 — Legacy / compatibility

- `_case_intelligence_legacy.py` (~1600 linii, własne kopie NBA/risk/missing_info):
  **brak importów** w `tools/gmail_audit` (rg: 0 trafień) — dormant, nie reachable.
- `_mailbox_memory_legacy.py`: re-export shim z placeholderami (facts/document) —
  reachable przez `mailbox_memory/__init__`.
- `case_intelligence.py`: compat shim -> package (reachable, poprawny).
- Adaptery sygnałów (calendar/drive/gmail) — aktywne.

Ustalenia: dormant legacy NIE jest drugim „mózgiem" w runtime, ale jest hazardem
utrzymaniowym (kod do usunięcia lub oznaczenia DEAD w backlogu).

## 19. A17 — Duplikacja semantyki

Konkretne duplikaty (dowody):

| Semantyka | Wystąpienia |
| --- | --- |
| `_has_customer_clarification_reply_path` | [action_planner.py:45](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/action_planner.py:45>) vs [next_best_action.py:18](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/case_intelligence/next_best_action.py:18>) — RÓŻNA logika |
| `_truthy` | action_planner.py:37, next_best_action.py:10 |
| `_normalize_urgency/_string_or_default/_bounded_float` | case_intelligence/validators.py:91-127 + `_case_intelligence_legacy.py:1569-1589` |
| `collect_data` | BR action -> ActionPlan `prepare_reply` -> APv2 alias `prepare_reply` -> NBA `ask_for_missing_data` (3 słowniki) |
| `review_required` | flaga intake / `create_review` (ActionPlan) / `review_required` (NBA action_type) |
| Typ NBA | orchestrator.py:112 przekazuje **dict**; action_proposal_v2.py:61 robi `str(...)` i porównuje z kodami — branch string jest martwy |

Status: RISK — spójne dla udowodnionej ścieżki, ale każde z tych miejsc może
rozjechać się niezależnie.

## 20. A18 — Architektura danych

- CaseContextPack normalizacja + provenance:
  [case_context_contract.py:453-512](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/case_context_contract.py:453>),
  :658-697, :1005-1090 (provenance_note per pole).
- Hot state: `case_snapshot_hot_state_primary` + legacy fields zachowane
  (orchestrator + legacy).
- **Sprzeczność znaleziona**: `DecisionCandidate.next_best_action` jest dict,
  a konsumenci v2 oczekują stringa (A17) — pole bez spójnego typu.

Ustalenia: provenance obecny; pola derived mają provenance_note; ryzyko lossy
transformacji skoncentrowane w typie NBA.

## 21. A19 — Observability

- Append-only: [turn_journal.py:27-131](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/agent_runtime/turn_journal.py:27>)
  (redact args, trace_id, tokens_used); [event_memory.py:32-104](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/event_memory.py:32>)
  (replay_case); snapshot_delta wersjonowany.
- Stage metadata: orchestrator `execution_metadata` z input_* per stage; intake
  `stage_call` z parse_status/second_pass.
- Replay CLI istnieje (`run_replay_v2_command`, gmail_intake.py:831).

Ustalenia: łańcuch „co system zobaczył -> ... -> co wykonano" jest odtwarzalny z
dziennika zdarzeń + journal + stage metadata. **PARTIAL**: brak jednego,
udowodnionego canonical replay CLI spinającego BR->policy->planner->execution
(istniejące replay_v2/event replay nie były w tym przebiegu uruchamiane).

## 22. A20 — Testy

- Inwentarz: 357 plików testowych / 2529 funkcji `test_*` (+25 w `tests/unit`).
- Kluczowe mapowania: `test_svc05_customer_clarification`, `test_fact01_*`,
  `test_rp29_fact_supersession`, `test_rp31_learning_integrity`,
  `test_untrusted_input_execution_boundary`, `test_planner_spine_handoff_closeout`,
  `test_v2_semantics`, `test_hitl_no_send_without_approve`,
  `test_outbound_receipt`, `test_understanding_to_decision_quality`.

Ustalenia: silna siatka regresji + testy invariantów w spine. **Luki**: brak
systematycznych property/metamorphic/adversarial/multi-intent/stale-state testów;
część testów jest case-ID-anchored. Rekomendacja: warstwa property dla A4/A5.

## 23. A21 — Realne zachowania

- Ostatni bounded provider-live proof SVC-05: [LAST_PROVEN_STATE.md:21](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/docs/runbooks/LAST_PROVEN_STATE.md:21>)
  (`operator_clarification_requested=false`), artefakt
  `.artifacts/svc05-final-live-proof-fix-20260820T113843/recovery-attempt-2`.
- Harness real-mail: [gmail_intake.py:736](<C:/Users/compg/Desktop/top-code workspace/gmail-agent/tools/gmail_audit/gmail_intake.py:736>)
  (`real-mail-discovery`, no-side-effect; commit `a3d3ae6`).
- Formal cohort: **DATASET_REQUIRED** — 10-15 oznaczonych historycznych spraw.

Status: DATASET_REQUIRED. Nie można w tym przebiegu przeprowadzić audytu
realnych zachowań bez danych operatora.

## 24. Cross-cutting — tabela transformacji semantycznych (Decision Spine)

| Warstwa | Plik:linia | Wejście -> wyjście |
| --- | --- | --- |
| BR validation | intake_schema.py:321-445 | LLM action -> `collect_data`/`escalate_review` + `customer_clarification_possible` |
| ActionPlan | action_planner.py:66-97 | BR + reply + intake.review -> `prepare_reply`/`create_review`/... |
| NBA | next_best_action.py:47-113 | BR + plan + missing_info -> `ask_for_missing_data`/`review_required`/... |
| DecisionCandidate | decision_candidate.py:101-207 | NBA dict -> `next_best_action` (sanitized) + `recommended_mode` |
| Policy proposal | policy_action_proposal.py:118-160 | primary_action -> action_class (LIVE_REPLY/REVIEW_ESCALATION/...) |
| PolicyDecision | policy_decision.py:30-90 | PolicyReport -> status + allowed/blocked actions |
| APv2 | action_proposal_v2.py:28-123 | candidate+policy+planner primary -> `action_type` P0-safe |
| Tool envelope | policy_action_spine.py:47-77 | NBA -> target/channel/allowed_action_tools/forbidden_tools |
| Runtime guard | graph.py:759-885 | ToolCallPlan + envelope -> correlation/consistency |
| Planner hint | recommended_next_step_quality.py:144-178 | tekst+NBA+channel -> preferred tool class |
| LLM prompt | openai_agent_client.py:400-455 | hint + allowlist -> tool choice (LLM) |

## 25. Kluczowe residuale do decyzji operatora

1. **A5/A7 (HIGH)**: domyślny fallback promptu follow-up = `request_operator_clarification`
   może zmienić adresata pytania, gdy NBA/hint nie dotrze do planner-a.
2. **A17 (MEDIUM)**: typ NBA dict vs string w APv2 + zdublowane helpery
   (`_has_customer_clarification_reply_path`) — kontrakt do ujednolicenia.
3. **A23 (MEDIUM)**: brak modelu A0-A4 i stanu providerów w kontekście planner-a;
   `effective_tools` celowo nie sprawdza health (config presence only).
4. **A16 (LOW)**: `_case_intelligence_legacy.py` dormant (~1600 linii) — do
   usunięcia/oznaczenia DEAD.
5. **A22 (LOW)**: brak agregatu kosztu LLM na sprawę mimo `tokens_used` w journal.

## 26. Czego ten dokument NIE twierdzi

- Nie jest runtime proof produktu (wymagany osobny proof dla zmian).
- Nie jest pełnym Fresh38 (nie uruchamiano).
- Nie zawiera oceny wydajności jakościowej modeli (wymaga A21).
- Nie zmienia żadnego kodu ani konfiguracji.

