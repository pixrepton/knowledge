# CAPABILITY-FIX-03 Negative Proof

Status: PASS

## Quote Blocking

`NEG-QUOTE` keeps true quote blockers (`metraz budynku`, `lokalizacja`, `typ budynku`, `obecne ogrzewanie`) in `missing_critical_fields`; next action remains `ask_for_missing_data`. The system does not mark it quote-ready.

## Service Safety

`NEG-SERVICE` allows acknowledgement/escalation for a serious no-heat issue, but the sharpened next step says not to invent diagnosis or visit. Missing identifiers stay as later service data.

## True Uncertainty

`NEG-CONFLICT` keeps `sprzeczny metraz wymaga potwierdzenia` as a current blocker. Conflict/evidence markers are never demoted to later gaps.

## Multi-Intent

`MI-01` keeps the technical Aquarea question and the separate service problem in the next step: answer the technical part now and separately accept the service issue for triage.

## Technical Document

`DOC-02` recommends bounded compatibility assessment or one/two relevant clarification questions. Broad offer data remains later context; the system does not assert full compatibility.
