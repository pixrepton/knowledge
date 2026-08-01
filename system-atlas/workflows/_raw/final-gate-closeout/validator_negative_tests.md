# Validator Negative Tests

- Generated at: `2026-07-30T23:10:24Z`
- Total tests: `12`
- Passed: `12`
- Failed: `0`

| Test | Expected exit | Actual exit | Result | Note |
| --- | --- | --- | --- | --- |
| final without manifest flag and missing default manifest | `1` | `1` | `PASS` | must fail closed when default FINAL_MANIFEST.json is absent |
| final with explicit missing manifest path | `1` | `1` | `PASS` | must fail when explicit manifest path does not exist |
| empty manifest object | `1` | `1` | `PASS` | must fail for empty manifest object |
| invalid JSON manifest | `1` | `1` | `PASS` | must fail for malformed manifest JSON |
| hash mismatch after one-byte mutation | `1` | `1` | `PASS` | must fail when content changes without size change |
| size mismatch after append | `1` | `1` | `PASS` | must fail when file size changes |
| missing file referenced by manifest | `1` | `1` | `PASS` | must fail when a manifest target file is absent |
| duplicate path in manifest | `1` | `1` | `PASS` | must fail on duplicate manifest path |
| path traversal in manifest | `1` | `1` | `PASS` | must fail on manifest path escaping workflow root |
| pre-manifest without manifest | `0` | `0` | `PASS` | must pass and report manifest NOT_APPLICABLE_PRE_MANIFEST |
| valid final snapshot | `0` | `0` | `PASS` | must pass on a valid final snapshot |
| both modes at once | `2` | `2` | `PASS` | argparse should reject mutually exclusive modes |

## Commands

### final without manifest flag and missing default manifest

```text
python C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\validate_workflow_atlas.py --final --root C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\no_manifest
```

### final with explicit missing manifest path

```text
python C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\validate_workflow_atlas.py --final --root C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\no_manifest --manifest C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\no_manifest\missing.json
```

### empty manifest object

```text
python C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\validate_workflow_atlas.py --final --root C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\empty_manifest
```

### invalid JSON manifest

```text
python C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\validate_workflow_atlas.py --final --root C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\invalid_json_manifest
```

### hash mismatch after one-byte mutation

```text
python C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\validate_workflow_atlas.py --final --root C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\hash_mismatch
```

### size mismatch after append

```text
python C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\validate_workflow_atlas.py --final --root C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\size_mismatch
```

### missing file referenced by manifest

```text
python C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\validate_workflow_atlas.py --final --root C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\missing_file
```

### duplicate path in manifest

```text
python C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\validate_workflow_atlas.py --final --root C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\duplicate_path
```

### path traversal in manifest

```text
python C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\validate_workflow_atlas.py --final --root C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\path_escape
```

### pre-manifest without manifest

```text
python C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\validate_workflow_atlas.py --pre-manifest --root C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\no_manifest
```

### valid final snapshot

```text
python C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\validate_workflow_atlas.py --final --root C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\valid_snapshot
```

### both modes at once

```text
python C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\validate_workflow_atlas.py --pre-manifest --final --root C:\Users\compg\Desktop\top-code workspace\knowledge\system-atlas\workflows\_raw\final-gate-closeout\validator-fixtures\valid_snapshot
```

