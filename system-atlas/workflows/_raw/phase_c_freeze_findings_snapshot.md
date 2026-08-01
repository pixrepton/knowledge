# Phase C Freeze Findings Snapshot

- timestamp: `2026-07-30 21:44:00 +02:00`
- working_directory: `C:\Users\compg\Desktop\top-code workspace`
- scope:
  - freeze the post-reverse-audit, post-N3 input state before normalization
  - capture file hashes, evidence sequence integrity, and current normalization backlog
- exclusions:
  - no normalization edits applied yet to `WORKFLOW_EVIDENCE.jsonl`
  - no registry schema rewrite yet
  - no gap-id migration yet

## Exact Commands

### Core file hashes

```powershell
@'
import hashlib
from pathlib import Path
files = [
    Path(r'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\WORKFLOW_EVIDENCE.jsonl'),
    Path(r'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\WORKFLOW_GAPS.md'),
    Path(r'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\WORKFLOW_REGISTRY.yaml'),
    Path(r'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\PROGRESS.md'),
]
for p in files:
    data = p.read_bytes()
    print(f'{p.name}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}')
'@ | python -
```

- exit_code: `0`

### Evidence-sequence integrity

```powershell
$p='C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\WORKFLOW_EVIDENCE.jsonl'; $ids = Get-Content $p | ForEach-Object { ($_ | ConvertFrom-Json).id }; $nums = $ids | ForEach-Object { [int]($_ -replace '^EV-','') }; $missing = Compare-Object -ReferenceObject (1..($nums | Measure-Object -Maximum).Maximum) -DifferenceObject $nums | Where-Object {$_.SideIndicator -eq '<='} | Select-Object -ExpandProperty InputObject; [pscustomobject]@{count=$nums.Count; max=($nums | Measure-Object -Maximum).Maximum; missing=@($missing).Count; dupes=($nums.Count - ($nums | Sort-Object -Unique).Count)} | ConvertTo-Json -Compress
```

- exit_code: `0`

### Evidence-schema drift snapshot

```powershell
@'
import json
from collections import Counter
from pathlib import Path
p = Path(r'C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\WORKFLOW_EVIDENCE.jsonl')
rows = [json.loads(line) for line in p.read_text(encoding='utf-8').splitlines() if line.strip()]
key_counter = Counter()
missing_workflow = []
missing_related = 0
missing_raw_artifact = 0
missing_evidence_type = 0
missing_confidence = 0
for row in rows:
    key_counter.update(row.keys())
    if 'workflow_id' not in row:
        missing_workflow.append(row['id'])
    if 'related_workflow_ids' not in row:
        missing_related += 1
    if 'raw_artifact' not in row:
        missing_raw_artifact += 1
    if 'evidence_type' not in row:
        missing_evidence_type += 1
    if 'confidence' not in row:
        missing_confidence += 1
print(json.dumps({
    'count': len(rows),
    'unique_keys': sorted(key_counter),
    'missing_workflow_id': len(missing_workflow),
    'missing_related_workflow_ids': missing_related,
    'missing_raw_artifact': missing_raw_artifact,
    'missing_evidence_type': missing_evidence_type,
    'missing_confidence': missing_confidence,
}, ensure_ascii=False, indent=2))
'@ | python -
```

- exit_code: `0`

## Frozen Checksums

| File | Bytes | SHA-256 |
|---|---:|---|
| `WORKFLOW_EVIDENCE.jsonl` | `251139` | `32e948afbe98f3d8d2d8f2ac456c290ee08e3cc8afaaa377696d7fbdf23b6436` |
| `WORKFLOW_GAPS.md` | `41487` | `7141db984c9ff5a51fa44b20992b192ee9ccc529eb07c17f9f8d1ff348706463` |
| `WORKFLOW_REGISTRY.yaml` | `110655` | `980f240b6178788b7814f53f0fac0e3a69195fe427c30e50f57fe635ab6dd52c` |
| `PROGRESS.md` | `51934` | `7f6e39552a6ab1c75b74cc5f8b25c5d098ed4f9700eef354bc82e9390e47d401` |

## Frozen Mechanical State

- evidence_sequence: `count=187`, `max=187`, `missing=0`, `dupes=0`
- `_raw` artifact files present: `13`
- registry test-status index present: `yes`
- reverse-audit status: `12/12 COMPLETE`
- current post-N3 ledger status: `PARTIAL`, first open step `Phase C step 1 - freeze findings`

## Evidence Normalization Backlog Snapshot

- unique keys currently in evidence rows:
  - `claim`
  - `confidence`
  - `evidence_type`
  - `file`
  - `id`
  - `lines`
  - `raw_artifact`
  - `repo`
  - `summary`
  - `symbol`
- missing `workflow_id`: `187/187`
- missing `related_workflow_ids`: `187/187`
- missing `raw_artifact`: `184/187`
- missing `evidence_type`: `137/187`
- missing `confidence`: `137/187`

## Interpretation

- Freeze complete: there is now a reproducible pre-normalization snapshot for the four core artifacts.
- `N1` remains fully open: no evidence row currently has `workflow_id`, so normalization cannot be treated as incremental cleanup.
- Registry already contains enough evidence references to seed attachment for a majority of rows; that seed is captured separately in `_raw/n1_evidence_workflow_attachment_seed.md`.
