from __future__ import annotations

import argparse
import copy
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from build_final_manifest import INCLUDED_FILES


WORKFLOWS_DIR = Path(__file__).resolve().parent
RAW_DIR = WORKFLOWS_DIR / "_raw" / "final-gate-closeout"
FIXTURES_DIR = RAW_DIR / "validator-fixtures"
REPORT_MD = RAW_DIR / "validator_negative_tests.md"
REPORT_LOG = RAW_DIR / "validator_negative_tests.log"
REPORT_JSON = RAW_DIR / "validator_negative_tests.json"
VALIDATOR_PATH = WORKFLOWS_DIR / "validate_workflow_atlas.py"


@dataclass
class TestResult:
    name: str
    command: list[str]
    expected_exit: int
    actual_exit: int
    passed: bool
    stdout: str
    stderr: str
    note: str


def sha256_file(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_manifest(root: Path) -> None:
    files = []
    for relative in INCLUDED_FILES:
        path = root / relative
        stat = path.stat()
        files.append(
            {
                "path": relative,
                "size": stat.st_size,
                "sha256": sha256_file(path),
                "modified_time_ns": stat.st_mtime_ns,
                "modified_time_utc": stat.st_mtime,
            }
        )
    manifest = {
        "schema_version": 1,
        "root": str(root),
        "file_count": len(files),
        "files": files,
    }
    (root / "FINAL_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def copy_baseline(target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    for relative in INCLUDED_FILES:
        src = WORKFLOWS_DIR / relative
        dst = target / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    shutil.copy2(WORKFLOWS_DIR / "FINAL_CONSISTENCY_REPORT.md", target / "FINAL_CONSISTENCY_REPORT.md")
    evidence_rows = [
        json.loads(line)
        for line in (WORKFLOWS_DIR / "WORKFLOW_EVIDENCE.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    raw_artifacts = sorted(
        {
            row["raw_artifact"].split("#", 1)[0]
            for row in evidence_rows
            if row.get("raw_artifact")
        }
    )
    for raw_artifact in raw_artifacts:
        src = WORKFLOWS_DIR / raw_artifact
        if not src.exists():
            continue
        dst = target / raw_artifact
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    write_manifest(target)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(command: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(command, cwd=WORKFLOWS_DIR, capture_output=True, text=True)
    return completed.returncode, completed.stdout, completed.stderr


def mutate_one_byte(path: Path) -> None:
    data = bytearray(path.read_bytes())
    data[0] = ord("X") if data[0] != ord("X") else ord("Y")
    path.write_bytes(bytes(data))


def build_fixtures() -> dict[str, Path]:
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    fixtures = {
        "valid_snapshot": FIXTURES_DIR / "valid_snapshot",
        "no_manifest": FIXTURES_DIR / "no_manifest",
        "empty_manifest": FIXTURES_DIR / "empty_manifest",
        "invalid_json_manifest": FIXTURES_DIR / "invalid_json_manifest",
        "hash_mismatch": FIXTURES_DIR / "hash_mismatch",
        "size_mismatch": FIXTURES_DIR / "size_mismatch",
        "missing_file": FIXTURES_DIR / "missing_file",
        "duplicate_path": FIXTURES_DIR / "duplicate_path",
        "path_escape": FIXTURES_DIR / "path_escape",
    }
    copy_baseline(fixtures["valid_snapshot"])

    copy_baseline(fixtures["no_manifest"])
    (fixtures["no_manifest"] / "FINAL_MANIFEST.json").unlink()

    copy_baseline(fixtures["empty_manifest"])
    (fixtures["empty_manifest"] / "FINAL_MANIFEST.json").write_text("{}\n", encoding="utf-8", newline="\n")

    copy_baseline(fixtures["invalid_json_manifest"])
    (fixtures["invalid_json_manifest"] / "FINAL_MANIFEST.json").write_text("{invalid json\n", encoding="utf-8", newline="\n")

    copy_baseline(fixtures["hash_mismatch"])
    mutate_one_byte(fixtures["hash_mismatch"] / "PROGRESS.md")

    copy_baseline(fixtures["size_mismatch"])
    with (fixtures["size_mismatch"] / "PROGRESS.md").open("a", encoding="utf-8", newline="\n") as handle:
        handle.write("\n")

    copy_baseline(fixtures["missing_file"])
    (fixtures["missing_file"] / "WORKFLOW_ATLAS.md").unlink()

    copy_baseline(fixtures["duplicate_path"])
    manifest = read_json(fixtures["duplicate_path"] / "FINAL_MANIFEST.json")
    manifest["files"].append(copy.deepcopy(manifest["files"][0]))
    manifest["file_count"] = len(manifest["files"])
    (fixtures["duplicate_path"] / "FINAL_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    copy_baseline(fixtures["path_escape"])
    manifest = read_json(fixtures["path_escape"] / "FINAL_MANIFEST.json")
    manifest["files"][0]["path"] = "../escape.txt"
    (fixtures["path_escape"] / "FINAL_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    return fixtures


def evaluate_manifest_status(stdout: str) -> str | None:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return None
    for result in payload.get("results", []):
        if result.get("name") == "manifest":
            return result.get("status")
    return None


def run_tests() -> list[TestResult]:
    fixtures = build_fixtures()
    tests: list[tuple[str, list[str], int, str, callable | None]] = [
        (
            "final without manifest flag and missing default manifest",
            ["python", str(VALIDATOR_PATH), "--final", "--root", str(fixtures["no_manifest"])],
            1,
            "must fail closed when default FINAL_MANIFEST.json is absent",
            None,
        ),
        (
            "final with explicit missing manifest path",
            ["python", str(VALIDATOR_PATH), "--final", "--root", str(fixtures["no_manifest"]), "--manifest", str(fixtures["no_manifest"] / "missing.json")],
            1,
            "must fail when explicit manifest path does not exist",
            None,
        ),
        (
            "empty manifest object",
            ["python", str(VALIDATOR_PATH), "--final", "--root", str(fixtures["empty_manifest"])],
            1,
            "must fail for empty manifest object",
            None,
        ),
        (
            "invalid JSON manifest",
            ["python", str(VALIDATOR_PATH), "--final", "--root", str(fixtures["invalid_json_manifest"])],
            1,
            "must fail for malformed manifest JSON",
            None,
        ),
        (
            "hash mismatch after one-byte mutation",
            ["python", str(VALIDATOR_PATH), "--final", "--root", str(fixtures["hash_mismatch"])],
            1,
            "must fail when content changes without size change",
            None,
        ),
        (
            "size mismatch after append",
            ["python", str(VALIDATOR_PATH), "--final", "--root", str(fixtures["size_mismatch"])],
            1,
            "must fail when file size changes",
            None,
        ),
        (
            "missing file referenced by manifest",
            ["python", str(VALIDATOR_PATH), "--final", "--root", str(fixtures["missing_file"])],
            1,
            "must fail when a manifest target file is absent",
            None,
        ),
        (
            "duplicate path in manifest",
            ["python", str(VALIDATOR_PATH), "--final", "--root", str(fixtures["duplicate_path"])],
            1,
            "must fail on duplicate manifest path",
            None,
        ),
        (
            "path traversal in manifest",
            ["python", str(VALIDATOR_PATH), "--final", "--root", str(fixtures["path_escape"])],
            1,
            "must fail on manifest path escaping workflow root",
            None,
        ),
        (
            "pre-manifest without manifest",
            ["python", str(VALIDATOR_PATH), "--pre-manifest", "--root", str(fixtures["no_manifest"])],
            0,
            "must pass and report manifest NOT_APPLICABLE_PRE_MANIFEST",
            lambda stdout: evaluate_manifest_status(stdout) == "NOT_APPLICABLE_PRE_MANIFEST",
        ),
        (
            "valid final snapshot",
            ["python", str(VALIDATOR_PATH), "--final", "--root", str(fixtures["valid_snapshot"])],
            0,
            "must pass on a valid final snapshot",
            None,
        ),
        (
            "both modes at once",
            ["python", str(VALIDATOR_PATH), "--pre-manifest", "--final", "--root", str(fixtures["valid_snapshot"])],
            2,
            "argparse should reject mutually exclusive modes",
            None,
        ),
    ]

    results: list[TestResult] = []
    for name, command, expected_exit, note, extra_check in tests:
        exit_code, stdout, stderr = run_command(command)
        passed = exit_code == expected_exit
        if passed and extra_check is not None:
            passed = bool(extra_check(stdout))
        results.append(
            TestResult(
                name=name,
                command=command,
                expected_exit=expected_exit,
                actual_exit=exit_code,
                passed=passed,
                stdout=stdout,
                stderr=stderr,
                note=note,
            )
        )
    return results


def write_reports(results: list[TestResult]) -> None:
    md_lines = [
        "# Validator Negative Tests",
        "",
        f"- Generated at: `{datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}`",
        f"- Total tests: `{len(results)}`",
        f"- Passed: `{sum(1 for result in results if result.passed)}`",
        f"- Failed: `{sum(1 for result in results if not result.passed)}`",
        "",
        "| Test | Expected exit | Actual exit | Result | Note |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in results:
        md_lines.append(
            f"| {result.name} | `{result.expected_exit}` | `{result.actual_exit}` | `{'PASS' if result.passed else 'FAIL'}` | {result.note} |"
        )
    md_lines.append("")
    md_lines.append("## Commands")
    md_lines.append("")
    for result in results:
        md_lines.append(f"### {result.name}")
        md_lines.append("")
        md_lines.append("```text")
        md_lines.append(" ".join(result.command))
        md_lines.append("```")
        md_lines.append("")
    REPORT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8", newline="\n")

    REPORT_LOG.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "name": result.name,
                        "command": result.command,
                        "expected_exit": result.expected_exit,
                        "actual_exit": result.actual_exit,
                        "passed": result.passed,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                    },
                    ensure_ascii=False,
                )
                for result in results
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    REPORT_JSON.write_text(
        json.dumps(
            {
                "ok": all(result.passed for result in results),
                "tests": [
                    {
                        "name": result.name,
                        "expected_exit": result.expected_exit,
                        "actual_exit": result.actual_exit,
                        "passed": result.passed,
                    }
                    for result in results
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    results = run_tests()
    write_reports(results)
    print(json.dumps({"ok": all(result.passed for result in results), "tests": len(results), "report": str(REPORT_MD)}, ensure_ascii=False, indent=2))
    return 0 if all(result.passed for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
