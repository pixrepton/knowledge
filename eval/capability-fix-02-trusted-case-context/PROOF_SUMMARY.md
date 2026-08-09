# CAPABILITY-FIX-02 Focused Proof
Status: focused CL-02 proof, no full Fresh38 recapture/rescore.
Source artifact: `C:\Users\compg\Desktop\top-code workspace\knowledge\eval\fresh38-recapture-20260808\fresh-full38-results.json`

| case | link before | link after | CL-02 removed | remaining missing fields after |
| ---- | ----------- | ---------- | ------------- | ------------------------------ |
| FU-01 | no_link | linked:case_recovery_FU-01 | True | Preferowany kanał i numer telefonu do dalszego kontaktu. || Konkretna data lub dzień kontaktu klienta („przyszły tydzień” jest nieprecyzyjny). || Czy klient ma pytania techniczne, prośbę o zmianę oferty lub potrzebę audytu/OZC. |
| FU-02 | no_link | linked:case_recovery_FU-02 | True | dane adresowe i techniczne niezbędne do oceny kwalifikacji do programu Czyste Powietrze (np. rok budowy, rodzaj instalacji grzewczej) || informacja, czy klient potrzebuje wsparcia przy przygotowaniu wniosku o dofinansowanie |
| FU-05 | no_link | linked:case_recovery_FU-05 | True | Dane kontaktowe klienta (imię, nazwisko, telefon) || Adres instalacji / budynku || Termin, w którym klient faktycznie planuje wrócić do tematu || Zakres oferty (model pompy ciepła, parametry budynku) |
| FU-06 | no_link | linked:case_recovery_FU-06 | True | Preferowany termin realizacji || Dane techniczne budynku: OZC, typ instalacji grzewczej (grzejniki/podłogówka), powierzchnia || Lokalizacja inwestycji (ocena strefy dojazdu) |
| FU-07 | no_link | linked:case_recovery_FU-07 | True | Brak pełnego kontekstu wątku (poprzednie wiadomości, szczegóły techniczne) || Brak danych o powierzchni budynku i wyliczonym OZC niezbędnych do aktualizacji doboru pompy || Brak informacji o wymaganym buforze przy istniejącej instalacji podłogowej |
| DOC-03 | no_link | linked:case_recovery_DOC-03 | True | adres zamieszkania lub siedziby w celu weryfikacji adresowej || potwierdzenie zgodności danych z dowodu z danymi klienta w systemie || podpisana umowa lub inny dokument potwierdzający akceptację warunków |
| MI-02 | no_link | linked:case_recovery_MI-02 | True | dokładna data nowej wizyty (piątek – czy 2026‑07‑24?) || czy wywóz starego pieca jest objęty ceną oferty (lub ewentualny koszt dodatkowy) |
| DEC-02 | no_link | linked:case_recovery_DEC-02 | True | szczegóły techniczne oferty (wybrany model pompy, moc, bufor, CWU) || potwierdzenie, czy klient jest gotowy do dalszych negocjacji (np. termin realizacji) || porównawcze warunki oferty konkurencji (kwota, zakres) |

Result: 8/8 CL02_ROOT_CAUSE_REMOVED at trusted case-link/context projection. Remaining gaps are not scored as global CLEAN_PASS until a future frozen Fresh38 run.
