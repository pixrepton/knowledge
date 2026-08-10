#!/usr/bin/env python3
"""Mechanically verify the PRE-FIX Fresh38 first-attempt baseline has not been rewritten.

This directory is an immutable measurement record: 32/38 = 84.21% first-attempt reliability
against the SUT frozen in FROZEN_SUT_MANIFEST.json, before the AIOS-RUNTIME-RELIABILITY-01
runtime repair. Nothing here may be regenerated, retried, or corrected in place -- any
post-fix number belongs in a new directory under a new manifest.

Run from anywhere:

    python knowledge/eval/fresh38-canonical-clean-20260810T011858Z/verify_pre_fix_lock.py

Exit code 0 = baseline intact. Non-zero = the preserved record has drifted.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCK_PATH = HERE / "PRE_FIX_BASELINE_LOCK.json"

EXPECTED_TOTAL = 38
EXPECTED_VALID = 32
EXPECTED_FAILURES = 6
EXPECTED_FAILED_CASES = ["INT-05", "NEW-04", "FU-06", "SVC-04", "CTX-01", "NEW-01"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_preserved_hashes(lock: dict) -> list[str]:
    """Every file the lock recorded must still exist with the same bytes."""
    failures = []
    for rel, meta in lock["preserved_in_repo"]["files"].items():
        path = HERE / rel
        if not path.is_file():
            failures.append(f"MISSING preserved file: {rel}")
            continue
        actual = sha256(path)
        if actual != meta["sha256"]:
            failures.append(f"MUTATED preserved file: {rel}\n    locked  {meta['sha256']}\n    actual  {actual}")
    return failures


def check_headline(lock: dict) -> list[str]:
    """The headline reliability numbers are the whole point of the record."""
    failures = []
    head = lock["headline"]
    for key, expected in (
        ("FIRST_ATTEMPT_TOTAL", EXPECTED_TOTAL),
        ("FIRST_ATTEMPT_VALID", EXPECTED_VALID),
        ("FIRST_ATTEMPT_FAILURES", EXPECTED_FAILURES),
    ):
        if head.get(key) != expected:
            failures.append(f"headline {key}: locked {head.get(key)!r}, expected {expected!r}")
    if head.get("failed_case_ids") != EXPECTED_FAILED_CASES:
        failures.append(f"headline failed_case_ids drifted: {head.get('failed_case_ids')!r}")
    if head.get("PRE_FIX_FIRST_ATTEMPT_RELIABILITY") != "32/38 = 84.21%":
        failures.append(
            f"headline PRE_FIX_FIRST_ATTEMPT_RELIABILITY drifted: "
            f"{head.get('PRE_FIX_FIRST_ATTEMPT_RELIABILITY')!r}"
        )
    return failures


def check_ledger_agrees() -> list[str]:
    """The CSV ledger must independently reproduce the same 32/6 split and the same failures."""
    failures = []
    rows = list(csv.DictReader((HERE / "FIRST_ATTEMPT_LEDGER.csv").read_text(encoding="utf-8").splitlines()))
    if len(rows) != EXPECTED_TOTAL:
        failures.append(f"ledger row count {len(rows)}, expected {EXPECTED_TOTAL}")

    first_attempt = [r for r in rows if r["attempt_class"] == "FIRST_ATTEMPT"]
    if len(first_attempt) != len(rows):
        failures.append(
            f"ledger contains non-FIRST_ATTEMPT rows: first-attempt evidence must never be "
            f"mixed with recovery attempts ({len(rows) - len(first_attempt)} foreign rows)"
        )

    valid = [r for r in rows if r["valid_capture"] == "True"]
    failed = [r["case_id"] for r in rows if r["valid_capture"] != "True"]
    if len(valid) != EXPECTED_VALID:
        failures.append(f"ledger valid_capture count {len(valid)}, expected {EXPECTED_VALID}")
    if failed != EXPECTED_FAILED_CASES:
        failures.append(f"ledger failed cases {failed}, expected {EXPECTED_FAILED_CASES}")

    for row in rows:
        if row["valid_capture"] != "True" and row["failure_class"] != "PRODUCT_RUNTIME":
            failures.append(f"{row['case_id']}: failure_class {row['failure_class']!r}, expected PRODUCT_RUNTIME")
    return failures


def main() -> int:
    if not LOCK_PATH.is_file():
        print(f"FAIL: lock file missing: {LOCK_PATH}", file=sys.stderr)
        return 2

    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    failures = check_headline(lock) + check_ledger_agrees() + check_preserved_hashes(lock)

    if failures:
        print("PRE_FIX_BASELINE_LOCK: FAIL", file=sys.stderr)
        for item in failures:
            print(f"  - {item}", file=sys.stderr)
        return 1

    preserved = len(lock["preserved_in_repo"]["files"])
    captured = len(lock["volatile_capture_out_dir"]["files"])
    print("PRE_FIX_BASELINE_LOCK: PASS")
    print(f"  PRE_FIX_FIRST_ATTEMPT_RELIABILITY = {lock['headline']['PRE_FIX_FIRST_ATTEMPT_RELIABILITY']}")
    print(f"  failed cases                      = {', '.join(EXPECTED_FAILED_CASES)}")
    print(f"  preserved files verified          = {preserved}")
    print(f"  volatile capture files hashed     = {captured}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
