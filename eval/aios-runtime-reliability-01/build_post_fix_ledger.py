#!/usr/bin/env python3
"""Build the POST-FIX first-attempt ledger from a Fresh38 capture out-dir.

Deliberately mirrors the pre-fix ledger's columns so the two numbers can be compared without
anyone having to re-derive what either one measured.

The only question this answers is FIRST_ATTEMPT_RELIABILITY: did the system get through a case
correctly on real first contact? It says nothing about capability, and it refuses to look at
recovery attempts at all -- a retry lives under recovery-attempt-N/ and is excluded by
construction, so it cannot quietly improve a first-attempt number.

    python build_post_fix_ledger.py <capture-out-dir> [--out <dir>]
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

CASE_ORDER = [
    "INT-01", "INT-02", "INT-03", "INT-04", "INT-05", "INT-06",
    "NEW-02", "NEW-03", "NEW-04", "NEW-05",
    "FU-01", "FU-02", "FU-03", "FU-04", "FU-05", "FU-06", "FU-07",
    "SVC-01", "SVC-02", "SVC-03", "SVC-04", "SVC-05",
    "DOC-01", "DOC-02", "DOC-03", "DOC-04",
    "CTX-01", "CTX-02", "CTX-03", "CTX-04", "CTX-05",
    "MI-01", "MI-02", "MI-03", "MI-04",
    "DEC-01", "DEC-02", "NEW-01",
]

COLUMNS = [
    "case_id", "artifact_hash", "attempt_class", "completed", "valid_capture",
    "parity_error", "stage_reached", "failure_class", "production_would_fail",
    "experiment_manifest_hash",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path):
    # PowerShell's Set-Content -Encoding UTF8 writes a BOM; utf-8-sig handles both.
    return json.loads(path.read_text(encoding="utf-8-sig"))


def classify(parity_error: str, stderr_text: str) -> str:
    """Mechanical failure class, matching the pre-fix ledger's taxonomy."""
    if not parity_error:
        return ""
    if "INTAKE_LLM_TIMEOUT" in stderr_text or "stage_deadline_exhausted" in stderr_text:
        return "PRODUCT_RUNTIME"
    if "LLM_STAGE_BUDGET_FAILURE" in stderr_text:
        return "PRODUCT_RUNTIME"
    if "All LLM providers exhausted" in stderr_text:
        return "PROVIDER_AVAILABILITY"
    return "UNKNOWN"


def build(out_dir: Path, dest: Path) -> int:
    manifest_path = out_dir / "experiment-manifest.json"
    if not manifest_path.is_file():
        print(f"FAIL: no experiment-manifest.json in {out_dir}", file=sys.stderr)
        return 2
    manifest = load_json(manifest_path)
    experiment_hash = manifest["experiment_manifest_hash"]

    if manifest.get("attempt_type") != "FIRST_ATTEMPT":
        print(f"FAIL: capture is {manifest.get('attempt_type')}, not FIRST_ATTEMPT", file=sys.stderr)
        return 2

    rows = []
    problems = []
    for case_id in CASE_ORDER:
        artifact = out_dir / f"one-{case_id}.json"
        sidecar = out_dir / f"one-{case_id}.manifest.json"
        if not artifact.is_file():
            problems.append(f"{case_id}: no artifact")
            rows.append({
                "case_id": case_id, "artifact_hash": "", "attempt_class": "FIRST_ATTEMPT",
                "completed": False, "valid_capture": False, "parity_error": "no_artifact",
                "stage_reached": "", "failure_class": "HARNESS_ONLY",
                "production_would_fail": False, "experiment_manifest_hash": "",
            })
            continue

        # Provenance first: an artifact not bound to this experiment is not evidence about it.
        if not sidecar.is_file():
            problems.append(f"{case_id}: missing manifest sidecar")
            bound = ""
        else:
            bound = load_json(sidecar).get("experiment_manifest_hash", "")
            if bound != experiment_hash:
                problems.append(f"{case_id}: sidecar hash {bound[:12]} != experiment {experiment_hash[:12]}")
            if load_json(sidecar).get("attempt_type") != "FIRST_ATTEMPT":
                problems.append(f"{case_id}: sidecar attempt_type is not FIRST_ATTEMPT")

        payload = load_json(artifact)
        case = (payload.get("cases") or [{}])[0]
        parity_error = str(case.get("parity_error") or "")
        stderr_path = out_dir / f"one-{case_id}-stderr.txt"
        stderr_text = stderr_path.read_text(encoding="utf-8", errors="replace") if stderr_path.is_file() else ""

        rows.append({
            "case_id": case_id,
            "artifact_hash": sha256(artifact),
            "attempt_class": "FIRST_ATTEMPT",
            "completed": True,
            "valid_capture": not parity_error,
            "parity_error": parity_error,
            "stage_reached": str(case.get("stage_reached") or case.get("stage") or ""),
            "failure_class": classify(parity_error, stderr_text),
            "production_would_fail": bool(parity_error),
            "experiment_manifest_hash": bound,
        })

    total = len(rows)
    valid = sum(1 for r in rows if r["valid_capture"])
    failures = total - valid
    failed_ids = [r["case_id"] for r in rows if not r["valid_capture"]]

    ledger = {
        "measurement": "POST_FIX_FIRST_ATTEMPT_RELIABILITY",
        "task": "AIOS-RUNTIME-RELIABILITY-01",
        "experiment_manifest_hash": experiment_hash,
        "attempt_type": "FIRST_ATTEMPT",
        "capture_out_dir": str(out_dir),
        "FIRST_ATTEMPT_TOTAL": total,
        "FIRST_ATTEMPT_VALID": valid,
        "FIRST_ATTEMPT_FAILURES": failures,
        "FIRST_ATTEMPT_RELIABILITY": f"{valid}/{total} = {valid / total * 100:.2f}%",
        "failed_case_ids": failed_ids,
        "provenance_problems": problems,
        "comparison": {
            "PRE_FIX_FIRST_ATTEMPT_RELIABILITY": "32/38 = 84.21%",
            "PRE_FIX_failed_case_ids": ["INT-05", "NEW-04", "FU-06", "SVC-04", "CTX-01", "NEW-01"],
            "note": "Neither number may be altered by a retry. Both are first-attempt only.",
        },
        "cases": rows,
    }

    dest.mkdir(parents=True, exist_ok=True)
    (dest / "POST_FIX_FIRST_ATTEMPT_LEDGER.json").write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with open(dest / "POST_FIX_FIRST_ATTEMPT_LEDGER.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"POST_FIX_FIRST_ATTEMPT_RELIABILITY = {ledger['FIRST_ATTEMPT_RELIABILITY']}")
    print(f"failures: {failed_ids or 'none'}")
    if problems:
        print("PROVENANCE PROBLEMS:", file=sys.stderr)
        for item in problems:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print("provenance: every artifact bound to this experiment manifest, all FIRST_ATTEMPT")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    return build(args.out_dir, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
