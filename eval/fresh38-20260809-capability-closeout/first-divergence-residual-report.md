# Fresh38 Residual First-Divergence Report

Status: generated from full Fresh38 v5 rescore.

| case | new first divergence | root cause | cluster |
| --- | --- | --- | --- |
| INT-01 | QUALITY_SCORER_BORDERLINE | Understanding/draft judge marked gaps/next step/draft as BORDERLINE despite base CLEAN_PASS. | QUALITY_SCORER_BORDERLINE |
| INT-05 | KNOWN_FACT_REASK_BLOCKED | Planner attempted missing_info for known heated_area_m2; known-fact guard correctly blocked, no alternate action succeeded. | KNOWN_FACT_REASK_BLOCKED |
| NEW-03 | UNDERSTANDING_GAPS_BORDERLINE | Understanding judge marked gaps BORDERLINE for contact/address despite extraction and base path otherwise present. | UNDERSTANDING_GAPS_BORDERLINE |
| SVC-05 | DRAFT_CAPTURE_RECOMMENDED_EMPTY | Planner tool produced bounded draft OK, but top-level draft selected for scoring is reply_not_recommended/fallback empty. | DRAFT_CAPTURE_RECOMMENDED_EMPTY |
| DOC-04 | UNDERSTANDING_THREAD_DELTA_INCOMPLETE | Understanding judge marked document-change gaps/thread-delta incomplete. | UNDERSTANDING_THREAD_DELTA_INCOMPLETE |
| CTX-03 | KNOWN_FACT_REASK_BLOCKED | Understanding passes; planner attempted missing_info for known heated_area_m2 and guard blocked. | KNOWN_FACT_REASK_BLOCKED |
| CTX-04 | NEW_POST_FIX05_CONTEXT_GAP | Budget false negative removed; current judge now BORDERLINE on missing critical fields / case-link uncertainty, not missing budget. | NEW_POST_FIX05_CONTEXT_GAP |

Non-capability integrity blockers:

| case | outcome | mechanical evidence |
| --- | --- | --- |
| FU-01 | DELIVERY | kalk-top niedostępny: [Errno 101] Network is unreachable |
| FU-06 | HARNESS | production_faithful_intake_invalid |
| DOC-02 | DELIVERY | kalk-top niedostępny: [Errno 101] Network is unreachable |
| MI-01 | HARNESS | production_faithful_intake_invalid |
| MI-02 | HARNESS | production_faithful_intake_invalid |
