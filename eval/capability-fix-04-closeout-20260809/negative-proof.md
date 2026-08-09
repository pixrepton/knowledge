# CAPABILITY-FIX-04 Negative Proof

Focused runtime artifact:

`C:\top-code-session-scratch\capability-closeout-20260809\fix04-post2\fresh38-partial-results.json`

Negative checks applied to generated draft text and fallback reasons:

| Case | 413 absent | unsupported visit absent | invented diagnosis absent | invented price absent | sales service ask absent | safety downgrade absent |
| --- | --- | --- | --- | --- | --- | --- |
| NEW-01 | yes | yes | yes | yes | n/a | yes |
| SVC-02 | yes | yes | yes | yes | yes | yes |
| SVC-05 | yes | yes | yes | yes | yes | yes |

Service draft body used by SVC-02 and SVC-05:

```text
Dzień dobry,

dziękujemy za zgłoszenie. Żeby bezpiecznie zweryfikować kolejny krok, prosimy o przesłanie modelu urządzenia, opisu objawu lub kodu błędu oraz zdjęcia komunikatu, jeśli jest dostępne.

Po otrzymaniu danych sprawa zostanie zweryfikowana i przekażemy ją do dalszej obsługi.

Zespół TOP-INSTAL
```

The body does not claim that a technician will arrive, does not set or promise a visit, does not diagnose the fault, does not invent a price, and does not ask service customers for metraż or OZC.

Guarded blockers remain blockers:
- Service sales asks still fail with `service_draft_asks_sales_fields`.
- Unsupported service promise wording fails with `unsupported_service_promise`.
- Certain diagnosis wording fails with `unsupported_diagnosis_claim`.
- Policy disallow still fails with `policy_disallows_draft`.

