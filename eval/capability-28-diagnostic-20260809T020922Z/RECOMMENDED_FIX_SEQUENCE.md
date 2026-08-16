# Recommended Fix Sequence

Do not run full Fresh38 until cluster fixes have focused proofs.

## CAPABILITY-FIX-01

root cause cluster: CLUSTER-01 BRAIN1_POLICY_APV2_HANDOFF_MISSING
affected cases: INT-05, INT-06, NEW-02, NEW-04, NEW-05, SVC-03, CTX-02, CTX-03, MI-03
expected recoverable cases: 9
files/components: tools/gmail_audit/eval_planner_spine_handoff.py; Fresh38/recovery capture path; agent_runtime/agent_reconcile.py; tests/test_planner_spine_handoff_closeout.py
minimal change: Prove/enable the existing spine handoff in the Fresh38/recovery planner path so PolicyDecision and APv2 are present before AgentGraphEngine policy enforcement.
required regression tests: Focused replay for the 9 CLUSTER-01 cases proving envelope_presence=present_current and no missing_policy_envelope turn; existing spine handoff unit tests.
proof before Fresh38 rerun: No full Fresh38. Run narrow planner-spine replay with frozen inputs and compare planner envelope/turn status only.

## CAPABILITY-FIX-02

root cause cluster: CLUSTER-02 CASE_LINK_CONTEXT_SIGNAL_NOT_TRUSTED
affected cases: FU-01, FU-02, FU-05, FU-06, FU-07, DOC-03, MI-02, DEC-02
expected recoverable cases: 8
files/components: gmail_intake.link_case_context; case_linker.py; intake_shared_downstream.py; case_intelligence/understanding.py; understanding_output.py
minimal change: Carry verified CaseContextPack/entity-link identity into case_link_result or explicitly mark context-pack-linked so Brain1 stops treating seeded follow-ups as unlinked.
required regression tests: Fixture/replay for FU-01/FU-06/MI-02/DOC-03 proving case_link_decision linked/weak_link and no fabricated 'brak powiazania' gap when pack has the prior fact.
proof before Fresh38 rerun: Run deterministic case-link + Understanding projection micro-harness on the 8 cases; inspect active facts, case_link_decision, missing_critical_fields.

## CAPABILITY-FIX-03

root cause cluster: CLUSTER-03 OVERSTRICT_GAP_AND_REVIEW_GUIDANCE
affected cases: INT-01, INT-04, NEW-03, SVC-01, SVC-04, DOC-02, MI-01
expected recoverable cases: 7
files/components: business_reasoner.py; case_intelligence/missing_info.py; case_intelligence/risks.py; understanding_output.py; case_guidance_reasoner.py
minimal change: Demote helpful technical data from critical blockers when the current customer ask is answerable/triageable; separate quote-ready prerequisites from response-ready prerequisites.
required regression tests: Focused Understanding semantic checks for INT-01, INT-04, SVC-04, DOC-02, MI-01, NEW-03 with expected missing_critical_fields boundaries.
proof before Fresh38 rerun: No full Fresh38; run stage-level Business/Understanding replay and frozen judge only for the affected Understanding dimensions.

## CAPABILITY-FIX-04

root cause cluster: CLUSTER-04/05 DRAFT_INPUT_AND_DRAFT_SEMANTICS
affected cases: NEW-01, SVC-02, SVC-05
expected recoverable cases: 3
files/components: reply_drafter.py; central_llm_stage context budget settings; agent_runtime/draft_sanity.py; tests/test_aios_1_4_draft_content_contracts.py
minimal change: Add reply_drafter prompt-budget proof for NEW-01 and service-draft safety coverage for SVC-02/SVC-05 without changing planner policy.
required regression tests: Draft-only replay for NEW-01/SVC-02/SVC-05 proving no 413, safe clarification draft, and no unsupported scheduling promise.
proof before Fresh38 rerun: Draft-stage replay only; verify draft_enabled/body/do_not_send_reasons and deterministic draft score before any Fresh38 rerun.

## CAPABILITY-FIX-05

root cause cluster: CLUSTER-06 EVAL_EXPECTATION_FALSE_NEGATIVE
affected cases: CTX-04
expected recoverable cases: 1
files/components: fresh-understanding-judge.json evidence only; eval_measurement_scoring.py only if operator authorizes frozen-contract adjudication
minimal change: Adjudicate CTX-04 budget-preservation evidence and NEW-03 extraction scoring-spec side issue before product changes.
required regression tests: One-case scorer/judge audit using captured output only; no SUT calls.
proof before Fresh38 rerun: Show captured budget in Understanding fields and explain whether frozen score should remain as-is for comparability.

W nowym oknie zacząłbym od **diagnostyki 28 CAPABILITY**, bez implementowania fixów w pierwszym przebiegu.

# CAPABILITY-28-DIAGNOSTIC-01

Pracujesz w repo `top-code workspace`.

## KONTEKST STARTOWY

Faza infrastrukturalna AI-OS została formalnie zamknięta.

Aktualny stan:

```text
AI_OS_INFRASTRUCTURE_CLEANUP = COMPLETE_LOCAL
CAPABILITY_PROGRAM_READINESS = GO

REQUIRED_OPEN = 0
UNKNOWN_NEEDS_PROOF = 0
Gate A = GREEN
active tasks = 0
```

Ostatni blocker:

```text
OPERATOR-COMMAND-RECONCILE-BYPASS-01 = CLOSED
```

Remote:

```text
gmail-agent:
a764fb0f6520a9cb2f04fb3ae880cc68b5071063

knowledge:
77efc95efa8996a96ed0d0b26dc5268c2381bb41
```

Nie otwieraj ponownie zamkniętych programów infrastrukturalnych bez dowodu regresji.

## AKTUALNY BASELINE JAKOŚCI

Ostatni poprawny Fresh38:

```text
38/38 captured
30/30 Understanding scored
0 capture gaps
0 judge errors

CLEAN_PASS = 10
CAPABILITY = 28

HARNESS = 0
DELIVERY = 0
CAPACITY = 0

unsafe_non_escalation = 0

verdict:
NOT QUALIFIED — CAPABILITY
```

Measurement infrastructure jest zdrowe.

Problemem nie jest już harness/wiring/infra.

Problemem jest jakość produktu.

---

# CEL

Przeprowadź **read-only root-cause diagnostic wszystkich 28 przypadków CAPABILITY**.

Nie naprawiaj jeszcze kodu.

Nie rób 28 pojedynczych patchy.

Nie zaczynaj od zgadywania „co poprawić”.

Najpierw ustal dla każdego przypadku:

> **jaki jest pierwszy punkt, w którym zachowanie systemu rozjeżdża się z oczekiwanym poprawnym zachowaniem?**

To jest `FIRST_DIVERGENCE`.

Dopiero pierwszy rozjazd może być przypisany jako root cause.

---

# ZASADA ANALIZY

Nie wystarczy klasyfikacja:

```text
UNDERSTANDING
PLANNER
DRAFT
```

Prześledź każdy przypadek możliwie end-to-end przez rzeczywisty system:

```text
SOURCE FIDELITY
↓
CORRELATION / IDENTITY
↓
TRUTH / CURRENT FACTS
↓
CASE HOT STATE
↓
CONTEXT SELECTION
↓
BUSINESS REASONING
↓
CASE INTELLIGENCE
↓
CASE GUIDANCE
↓
UNDERSTANDING SYNTHESIS
↓
DECISION CANDIDATE
↓
POLICY DECISION
↓
ACTION PROPOSAL
↓
BRAIN1 → BRAIN2 HANDOFF
↓
ENGAGEMENT SNAPSHOT
↓
TOOL AVAILABILITY
↓
PLANNER INPUT
↓
PLANNER DECISION
↓
PLANNER / POLICY GUARDS
↓
TOOL RESULT
↓
SNAPSHOT DELTA
↓
DRAFT
↓
HITL / EXECUTION
↓
CASE STATE CONVERGENCE
↓
READINESS / VISIBILITY
↓
PROJECTION
↓
OPERATOR OUTCOME
```

Przykład:

```text
CaseContextPack ma metraż
Understanding ma metraż
EngagementSnapshot ma metraż
Planner pyta ponownie o metraż
```

→ root cause jest przy plannerze/guardzie.

Ale:

```text
CaseContextPack już nie ma metrażu
```

→ planner nie jest root cause.

---

# 1. ORIENTACJA

Najpierw przeczytaj:

- root `AGENTS.md`;
- `gmail-agent/AGENTS.md`;
- aktualny `knowledge/INDEX.md`;
- aktualny roadmap/status;
- ostatni Fresh38 artifact i frozen scoring contract;
- pliki odpowiedzialne za wykonanie/scoring Fresh38.

Sprawdź HEAD-y i dirty state.

Nie dotykaj zastanych obcych zmian.

Użyj:

- GitNexus;
- Codebase Memory;
- bezpośredniego tracingu aktualnego kodu.

Jeżeli GitNexus jest stale względem HEAD, traktuj go tylko jako mapę pomocniczą.

Kod aktualnego HEAD jest źródłem rozstrzygającym.

---

# 2. ZREKONSTRUUJ 28 CAPABILITY

Zidentyfikuj dokładnie wszystkie CaseId sklasyfikowane jako:

```text
CAPABILITY
```

w ostatnim frozen Fresh38.

Dla każdego utwórz kartę:

```text
case_id
expected_behavior
observed_behavior
component_score_failure
first_divergence_stage
first_divergence_evidence
upstream_state_at_divergence
downstream_effect
suspected_root_cause
confidence
shared_cluster
```

Nie opieraj się tylko na finalnym judge reason.

Prześledź dostępne:

- capture;
- stage outputs;
- structured contracts;
- context packs;
- policy/action envelopes;
- planner inputs/outputs;
- draft inputs/outputs;
- snapshots;
- traces;
- proof artifacts.

---

# 3. ROOT CAUSE, NIE OBJAW

Dla każdego Case rozróżnij:

```text
SYMPTOM
FIRST_DIVERGENCE
ROOT_CAUSE
DOWNSTREAM_DAMAGE
```

Przykład:

```text
SYMPTOM:
draft pyta ponownie o metraż

FIRST_DIVERGENCE:
Understanding nie przeniosło istniejącego active fact

ROOT_CAUSE:
context selection / fact projection

DOWNSTREAM_DAMAGE:
planner i draft zachowują się jakby metrażu nie było
```

Nie klasyfikuj draftu jako root cause, jeżeli dostał już błędny input.

---

# 4. KLASTRY

Po wszystkich 28 przypadkach zbuduj klastry wspólnych przyczyn.

Preferowana forma:

```text
CLUSTER-01
root cause:
affected cases:
count:
first divergence:
shared code path:
likely leverage:
confidence:
```

Szukaj przede wszystkim **koncentracji**.

Chcemy wiedzieć, czy 28 CAPABILITY to np.:

```text
8 przypadków — Context/known facts
6 przypadków — Understanding/NBA
5 przypadków — planner decision quality
4 przypadki — draft semantics
3 przypadki — projection
2 przypadki — inne
```

a nie dostać listę 28 niezależnych błędów.

---

# 5. PARETO

Policz:

```text
ile przypadków zamknie naprawa każdego klastra
```

i przygotuj ranking:

| rank | cluster | affected cases | % of 28 | expected leverage | risk |
| ---- | ------- | -------------: | ------: | ----------------- | ---- |

Interesują nas przede wszystkim poprawki, które rozwiązują **wiele przypadków jednocześnie**.

---

# 6. ROZRÓŻNIJ TYP PROBLEMU

Każdy root cause sklasyfikuj jako jedno z:

```text
DATA_TRUTH
CORRELATION
CONTEXT_SELECTION
BUSINESS_REASONING
CASE_INTELLIGENCE
GUIDANCE
UNDERSTANDING_SYNTHESIS
DECISION_LOGIC
POLICY
ACTION_PROPOSAL
BRAIN1_BRAIN2_HANDOFF
PLANNER_CONTEXT
PLANNER_REASONING
TOOL_AVAILABILITY
PLANNER_GUARD
TOOL_BEHAVIOR
DRAFT_INPUT
DRAFT_REASONING
EXECUTION
STATE_CONVERGENCE
PROJECTION
MODEL_LIMITATION
EVAL_EXPECTATION_ISSUE
OTHER
```

`MODEL_LIMITATION` stosuj dopiero, gdy poprawny i kompletny context wszedł do modelu, kontrakty były prawidłowe, a model mimo tego systematycznie podjął złą decyzję.

---

# 7. SPRAWDŹ CZY TO NIE REGRESJA INFRA

Jeżeli podczas analizy zobaczysz coś wyglądającego na:

```text
HARNESS
DELIVERY
CAPACITY
WIRING
SAFETY
```

nie otwieraj od razu starego programu.

Najpierw udowodnij regresję na aktualnym HEAD.

Jeżeli brak dowodu regresji:

```text
NOT_INFRA_REGRESSION
```

i kontynuuj CAPABILITY.

---

# 8. NIE IMPLEMENTUJ JESZCZE

Ten task jest diagnostyczny.

Dozwolone:

- read-only analysis;
- lokalne jednorazowe scripts/notebooks poza tracked product code, jeśli potrzebne do analizy;
- generowanie proof artifacts;
- aktualizacja `knowledge` dopiero po zakończeniu analizy.

Niedozwolone:

- product fixes;
- refactor;
- prompt tuning;
- zmiany modeli;
- nowe guardy;
- nowe heurystyki;
- kolejne pełne Fresh38 po każdej obserwacji.

Najpierw chcę zobaczyć mapę przyczyn.

---

# 9. ARTEFAKT

Utwórz:

```text
knowledge/eval/capability-28-diagnostic-<timestamp>/
```

Minimum:

```text
PROOF_SUMMARY.md
CASE_MATRIX.csv
ROOT_CAUSE_CLUSTERS.md
PARETO.md
FIRST_DIVERGENCE.json
RECOMMENDED_FIX_SEQUENCE.md
```

`CASE_MATRIX.csv` musi mieć 28 wierszy — dokładnie jeden na każdy CAPABILITY Case.

---

# 10. RECOMMENDED FIX SEQUENCE

Na końcu zaproponuj maksymalnie kilka **systemowych** następnych tasków.

Format:

```text
CAPABILITY-FIX-01
root cause cluster:
affected cases:
expected recoverable cases:
files/components:
minimal change:
required regression tests:
proof before Fresh38 rerun:
```

Nie twórz 28 tasków.

Jeżeli trzy poprawki potencjalnie rozwiązują 20/28 przypadków, właśnie tego chcemy.

---

# 11. KIEDY WOLNO PONOWNIE URUCHOMIĆ FULL FRESH38

Nie uruchamiaj nowego full Fresh38 w tym tasku.

Nowy frozen full run ma sens dopiero:

```text
diagnostic
→ root-cause clusters
→ systemowe fixes
→ focused regression proofs
→ dopiero potem full Fresh38
```

---

# RAPORT KOŃCOWY

## A. RESULT

```text
PASS_DIAGNOSTIC
PARTIAL
BLOCKED
```

## B. BASELINE CONFIRMED

Potwierdź 10 CLEAN_PASS / 28 CAPABILITY i integralność źródła.

## C. 28-CASE MATRIX

Tabela wszystkich przypadków:

| case | symptom | first divergence | root cause | cluster | confidence |

## D. ROOT CAUSE CLUSTERS

Od największego do najmniejszego.

## E. PARETO

Ile przypadków obejmuje top 1 / top 2 / top 3 przyczyn.

## F. FIRST-DIVERGENCE FINDINGS

Najważniejsze miejsca w kodzie, gdzie poprawny stan po raz pierwszy staje się błędny/niepełny.

## G. MODEL VS SYSTEM

Ile przypadków wygląda na:

```text
system/context problem
vs
actual model reasoning limitation
```

## H. RECOMMENDED FIX SEQUENCE

Maksymalnie kilka systemowych kolejnych tasków.

## I. WHAT NOT TO FIX

Wskaż objawy downstream, których nie należy patchować bez naprawienia upstream root cause.

## J. INFRA REGRESSION CHECK

Czy znaleziono jakąkolwiek prawdziwą regresję infrastrukturalną.

## K. NEXT

Wskaż dokładnie jeden następny task o najwyższym leverage.

---

Po raporcie **STOP**.

Nie implementuj jeszcze pierwszego CAPABILITY fixu.
Nie rozpoczynaj kolejnego roadmap itemu.
Nie otwieraj ponownie zakończonej fazy infrastrukturalnej bez nowego dowodu regresji.

To jest dobry prompt do **zupełnie nowego okna Codexa**, bo zawiera stan zamknięcia infrastruktury i od razu ustawia nowy sposób pracy: od teraz szukamy jakościowego first-divergence, a nie kolejnych technicznych residuali.
