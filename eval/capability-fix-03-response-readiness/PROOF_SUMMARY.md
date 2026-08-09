# CAPABILITY-FIX-03 Response Readiness Proof

Status: PASS

CAPABILITY-FIX-03 = CLOSED_LOCAL
CL-03_ROOT_CAUSE = FIXED
FOCUSED_CL03_PROOF = PASS

No full Fresh38 run was executed. Official frozen baseline remains CLEAN_PASS = 10, CAPABILITY = 28.

## Re-base After FIX-02

All seven original CL-03 cases were reclassified as STILL_CL03 on the current post-FIX-02 code path before the FIX-03 change. FIX-02 did not resolve these cases because their failures were not trusted-case-context redundant reasks; they were current-action readiness versus later-step gap severity/projection failures.

| case | original CL03 | still present on current HEAD | current first divergence |
|---|---:|---:|---|
| INT-01 | yes | yes | MISSING_INFO_SEVERITY+UNDERSTANDING_GAP_PROMOTION+GUIDANCE_OVERREVIEW |
| INT-04 | yes | yes | MISSING_INFO_SEVERITY+GUIDANCE_OVERREVIEW |
| NEW-03 | yes | yes | MISSING_INFO_SEVERITY+UNDERSTANDING_GAP_PROMOTION+GUIDANCE_OVERREVIEW |
| SVC-01 | yes | yes | MISSING_INFO_SEVERITY+GUIDANCE_OVERREVIEW |
| SVC-04 | yes | yes | UNDERSTANDING_GAP_PROMOTION+RISK_OVERESCALATION+NEXT_STEP_TOO_BROAD |
| DOC-02 | yes | yes | NEXT_STEP_TOO_BROAD+UNDERSTANDING_GAP_PROMOTION |
| MI-01 | yes | yes | NEXT_STEP_TOO_BROAD+INTENT_WEIGHTING+UNDERSTANDING_GAP_PROMOTION |

## Focused 7-Case Matrix

| case | actionable now | blockers before | blockers after | later gaps preserved | next step correct | CL03 removed |
|---|---:|---|---|---|---:|---:|
| INT-01 | yes | dokładny adres instalacji (ulica, numer),; preferowany termin realizacji lub harmonogram budowy; dane potrzebne do wyliczenia OZC (izolacja, współczynnik przenikania ciepła, zapotrzebowanie na ciepło),; preferencje co do marki pompy (Panasonic, Mitsubishi, Daikin) | - | dokladny adres instalacji; OZC; pelny harmonogram; preferowana marka | yes | yes |
| INT-04 | yes | numer telefonu kontaktowego; adres instalacji; model pompy ciepła lub numer seryjny; numer zlecenia/umowy z marca; potwierdzenie pilności i dostępności klienta; ewentualne kody błędów ze sterownika | - | numer telefonu; adres instalacji; model i numer seryjny; numer umowy | yes | yes |
| NEW-03 | yes | pełny adres / potwierdzenie lokalizacji i odległości od Jaworzna; telefon kontaktowy i preferowany termin; obliczeniowe zapotrzebowanie ciepła (OZC) lub dane do audytu; rok budowy / poziom izolacji budynku; rodzaj instalacji wewnętrznej (grzejniki / podłogówka) i temperatura zasilania; aktualny piec gazowy – dane techniczne; zapotrzebowanie na CWU i liczba osób; zgoda na ewentualną dopłatę dojazdową dla projektu poza strefą | - | pelny adres; OZC; rodzaj odbiornikow; CWU; rok budowy | yes | yes |
| SVC-01 | yes | lokalizacja instalacji (adres, numer mieszkania); numer telefonu kontaktowego do klienta; dokładny opis objawów (np. czy pompa się włącza, czy wyświetla błędy); potwierdzenie priorytetu (czy wymaga pilnej interwencji w ciągu 24 h); numer umowy lub faktury potwierdzający, że instalacja została wykonana przez TOP‑INSTAL | - | dokladny adres instalacji; numer telefonu; model pompy; szczegolowy opis objawow | yes | yes |
| SVC-04 | yes | model i numer seryjny jednostki zewnętrznej; dokładny opis sytuacji (czy dźwięk pojawia się przy uruchomieniu, wyłączaniu, w jakich temperaturach); czy jednostka pracuje w trybie grzania czy chłodzenia; czy była ostatnio przeprowadzona konserwacja lub przegląd | - | model i numer seryjny; potwierdzenie pilnosci; warunki wystepowania dzwieku | yes | yes |
| DOC-02 | yes | planowany termin realizacji; powierzchnia użytkowa budynku; obliczeniowe zapotrzebowanie cieplne (OZC); typ i liczba grzejników lub podłogówki; dystans od siedziby TOP‑INSTAL (czy mieszka w strefie dojazdu); czy istnieje już bufor cieplny lub planowany; preferowany model pompy ciepła (Panasonic, Mitsubishi, Daikin); dane o instalacji CWU (zasobnik, wężownica) | - | adres instalacji; numer telefonu; powierzchnia domu; OZC; termin realizacji | yes | yes |
| MI-01 | yes | numer telefonu kontaktowego do klienta; model i moc istniejącej pompy w domu przy ul. Kwiatowa 5 (aby zweryfikować ewentualną gwarancję/serwis); szczegółowy opis objawów awarii (np. czy pompa nie włącza się, czy brak ciepłej wody, czy wyświetla błędy); potwierdzenie pilności (czy brak ciepłej wody jest krytyczny); dane techniczne budynku, w którym planowane jest zastosowanie Aquarea (powierzchnia, rodzaj instalacji grzewczej, istniejące grzejniki) | - | numer telefonu; model pompy; szczegolowy opis objawow; dostepnosc na wizyte | yes | yes |

## Code Path Before

BusinessReasoning produced a flat `missing_information` checklist. `case_intelligence.missing_info` classified broad address/phone/OZC/model/schedule items as `critical` by keyword. `case_intelligence.understanding` converted any `critical` item into a blocker/review reason. `understanding_output._missing_fields()` then flattened `critical`, `important`, `helpful`, and raw BusinessReasoning gaps into `missing_critical_fields`, which promoted later-step gaps into current blockers and risks. `recommended_next_step_quality` then treated non-empty `missing_critical_fields` as complete-info, not response-ready.

## Implemented Fix

The existing `critical/important/helpful` contract now carries the readiness distinction:

- `critical`: blocks the current safe action.
- `important`: needed for a later concrete step such as full quote, visit, diagnosis, or final technical decision.
- `helpful`: optional context.
- trusted known facts and hard blockers remain protected by the existing FIX-02 filters and context quality rules.

`UnderstandingOutput.missing_critical_fields` now receives only `critical` gaps plus deterministic pending-outcome gaps. Later gaps remain visible under `missing_information.important/helpful` and are passed to NBA sharpening as later-step context.

## Focused Proof

Focused tests: `12 passed`.
FIX-02 regression: `7 passed`.
Relevant Understanding/Case Intelligence/NBA tests: `79 passed`.
Gate A: `2378 passed, 28 skipped, 24 subtests passed`.
