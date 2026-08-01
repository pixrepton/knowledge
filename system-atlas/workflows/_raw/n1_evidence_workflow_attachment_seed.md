# N1 Evidence Workflow Attachment Seed

- timestamp: `2026-07-30 21:46:00 +02:00`
- working_directory: `C:\Users\compg\Desktop\top-code workspace`
- scope:
  - derive the first-pass evidence-to-workflow attachment map from the current registry only
  - quantify unattached evidence and multi-workflow evidence before rewriting `WORKFLOW_EVIDENCE.jsonl`

## Exact Command

```powershell
@'
import json
from collections import defaultdict, Counter
from pathlib import Path
import yaml
reg = Path(r'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\WORKFLOW_REGISTRY.yaml')
data = yaml.safe_load(reg.read_text(encoding='utf-8'))
wf_map = defaultdict(list)
for wf in data.get('workflows', []):
    wid = wf['workflow_id']
    for ev in wf.get('evidence_ids', []) or []:
        wf_map[ev].append(wid)
for wid, meta in (data.get('workflow_test_status') or {}).items():
    for ev in meta.get('evidence_ids', []) or []:
        if wid not in wf_map[ev]:
            wf_map[ev].append(wid)
counts = Counter(len(v) for v in wf_map.values())
attached = sorted(wf_map)
all_ids = [f'EV-{i:05d}' for i in range(1, 188)]
unattached = [ev for ev in all_ids if ev not in wf_map]
multi = {ev: v for ev, v in sorted(wf_map.items()) if len(v) > 1}
print(json.dumps({
    'attached_count': len(attached),
    'unattached_count': len(unattached),
    'association_cardinality': dict(sorted(counts.items())),
    'first_unattached': unattached[:40],
    'sample_multi': {k: multi[k] for k in list(multi)[:20]},
}, ensure_ascii=False, indent=2))
'@ | python -
```

- exit_code: `0`

## First-Pass Attachment Totals

- evidence attached by current registry/test-status index: `154/187`
- evidence still unattached after registry-only derivation: `33/187`
- attachment cardinality:
  - `1 workflow`: `144`
  - `2 workflows`: `6`
  - `3 workflows`: `1`
  - `6 workflows`: `1`
  - `8 workflows`: `1`
  - `17 workflows`: `1` (`EV-00187`, intentionally cross-workflow)

## Unattached Evidence IDs

- `EV-00042`
- `EV-00043`
- `EV-00066`
- `EV-00067`
- `EV-00068`
- `EV-00069`
- `EV-00070`
- `EV-00071`
- `EV-00105`
- `EV-00112`
- `EV-00113`
- `EV-00114`
- `EV-00115`
- `EV-00118`
- `EV-00121`
- `EV-00122`
- `EV-00123`
- `EV-00124`
- `EV-00125`
- `EV-00126`
- `EV-00127`
- `EV-00132`
- `EV-00133`
- `EV-00134`
- `EV-00135`
- `EV-00136`
- `EV-00155`
- `EV-00156`
- `EV-00163`
- `EV-00173`
- `EV-00174`
- `EV-00175`
- `EV-00178`

## Multi-Workflow Evidence Samples

- `EV-00044` -> `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`, `CALENDAR-TWO-WORLDS-OF-VISITS`
- `EV-00045` -> `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`, `CALENDAR-TWO-WORLDS-OF-VISITS`
- `EV-00046` -> `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`, `CALENDAR-TWO-WORLDS-OF-VISITS`
- `EV-00130` -> `CALENDAR-TWO-WORLDS-OF-VISITS`, `SLA-WATCHER-DECISION-ESCALATION`
- `EV-00182` -> `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`, `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`, `LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY`, `HITL-PROPOSAL-APPROVAL-DUAL-PATH`, `CALENDAR-TWO-WORLDS-OF-VISITS`, `DASZEK-COMMAND-OUTBOX-DRAIN`
- `EV-00183` -> `HITL-PROPOSAL-APPROVAL-DUAL-PATH`, `DASZEK-FEED-PUSH-NO-RETRY`
- `EV-00184` -> `CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF`, `DASZEK-FEED-PUSH-NO-RETRY`
- `EV-00185` -> `GMAIL-SIGNAL-WORKER-LOOP`, `DASZEK-COMMAND-OUTBOX-DRAIN`, `DASZEK-FEED-PUSH-NO-RETRY`
- `EV-00186` -> `FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH`, `KALK-TOP-CALCULATE-OFFER-PIPELINE`, `TOP-INSTAL-GENERATOR-OFFER-DOCUMENT`, `CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL`, `GMAIL-SIGNAL-WORKER-LOOP`, `DASZEK-COMMAND-OUTBOX-DRAIN`, `DASZEK-FEED-PUSH-NO-RETRY`, `RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE`
- `EV-00187` -> all `17` canonical workflows by design of the test-status index

## Immediate N1 Implications

- Registry-derived attachment is already sufficient to auto-populate a majority of rows.
- The remaining `33` evidence items require manual primary/related workflow classification before the JSONL rewrite.
- The highest-risk normalization rows are the high-fanout evidence items (`EV-00182`, `EV-00186`, `EV-00187`) because they must become one `workflow_id` plus explicit `related_workflow_ids`, not a duplicated record set.
