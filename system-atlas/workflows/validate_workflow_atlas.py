from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from workflow_tools_common import utc_timestamp


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_MANIFEST_NAME = "FINAL_MANIFEST.json"
EXPECTED_DOCS = [
    "WORKFLOW_ATLAS.md",
    "ENTRYPOINT_INVENTORY.md",
    "CROSS_REPO_CONTRACTS.md",
    "STATE_OWNERSHIP_MATRIX.md",
    "ARCHITECTURAL_RULES_AUDIT.md",
    "RUNTIME_BASELINE.md",
    "RUNTIME_PROOF_PLAN.md",
    "EXECUTIVE_SUMMARY.md",
    "PROGRESS.md",
]
ALLOWED_EVIDENCE_TYPES = {"CODE", "CONFIG", "RUNTIME", "TEST", "GRAPH", "ABSENCE_SEARCH", "SYNTHESIS"}
ALLOWED_CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}
ALLOWED_PATH_STATUSES = {"LIVE_PATH", "CONDITIONAL_PATH", "DORMANT_PATH", "LEGACY_PATH", "DEAD_PATH", "FALLBACK_PATH"}
ALLOWED_CONTRACT_STATUSES = {"BROKEN_CALL", "MISSING_PRODUCER", "MISSING_CONSUMER", "MISSING_EXECUTOR"}
ALLOWED_RUNTIME_CLASSIFICATIONS = {"CONFIRMED", "UNVERIFIED"}
ALLOWED_RUNTIME_SCOPES = {"FULL_WORKFLOW", "PARTIAL_WORKFLOW", "ENTRYPOINT_ONLY", "PATH_SELECTION_ONLY", "ENVIRONMENT_ONLY", "STATIC_ONLY"}
ALLOWED_TRIGGER_MODES = {"AUTOMATIC", "MANUAL_ONLY", "MIXED"}
ALLOWED_TEST_STATUSES = {"NO_DIRECT_TEST_FOUND", "SYNTHETIC_ONLY", "PROOF_ONLY", "UNIT_COVERED", "INTEGRATION_COVERED", "END_TO_END_COVERED", "CHAOS_COVERED"}
STALE_MARKERS = ["STALE", "regeneration pending", "next step is", "not yet enumerated line-by-line"]
REQUIRED_MANIFEST_ENTRIES = [
    "WORKFLOW_EVIDENCE.jsonl",
    "WORKFLOW_REGISTRY.yaml",
    "WORKFLOW_GAPS.yaml",
    "WORKFLOW_GAPS.md",
    "WORKFLOW_ATLAS.md",
    "ENTRYPOINT_INVENTORY.md",
    "CROSS_REPO_CONTRACTS.md",
    "STATE_OWNERSHIP_MATRIX.md",
    "ARCHITECTURAL_RULES_AUDIT.md",
    "RUNTIME_BASELINE.md",
    "RUNTIME_PROOF_PLAN.md",
    "EXECUTIVE_SUMMARY.md",
    "PROGRESS.md",
    "FINAL_CONSISTENCY_REPORT.md",
    "workflow_tools_common.py",
    "normalize_workflow_evidence.py",
    "normalize_workflow_registry.py",
    "normalize_workflow_gaps.py",
    "generate_workflow_atlas_docs.py",
    "generate_progress.py",
    "validate_workflow_atlas.py",
    "build_final_manifest.py",
    "run_validator_negative_tests.py",
]
REQUIRED_FINAL_FILES_OUTSIDE_MANIFEST = [
    "FINAL_MANIFEST.json",
]


@dataclass
class CheckResult:
    name: str
    status: str
    ok: bool
    details: list[str] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(read_text(path))


def load_json(path: Path) -> Any:
    return json.loads(read_text(path))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in read_text(path).splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_path(root: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate.resolve()


def path_escapes_root(root: Path, raw_path: str) -> bool:
    try:
        resolve_path(root, raw_path).relative_to(root.resolve())
    except ValueError:
        return True
    return False


def validate_evidence(root: Path) -> tuple[CheckResult, list[dict[str, Any]], set[str]]:
    path = root / "WORKFLOW_EVIDENCE.jsonl"
    rows = load_jsonl(path)
    issues: list[str] = []
    expected_ids = [f"EV-{index:05d}" for index in range(1, len(rows) + 1)]
    actual_ids = [row.get("id") for row in rows]
    if actual_ids != expected_ids:
        issues.append("evidence sequence is not contiguous")
    seen = set()
    for row in rows:
        for key in ("id", "workflow_id", "related_workflow_ids", "repo", "file", "symbol", "lines", "evidence_type", "claim", "confidence", "raw_artifact", "superseded_by"):
            if key not in row:
                issues.append(f"{row.get('id', 'UNKNOWN')} missing {key}")
        row_id = row.get("id")
        if row_id in seen:
            issues.append(f"duplicate evidence id {row_id}")
        seen.add(row_id)
        if row.get("evidence_type") not in ALLOWED_EVIDENCE_TYPES:
            issues.append(f"{row_id} invalid evidence_type {row.get('evidence_type')}")
        if row.get("confidence") not in ALLOWED_CONFIDENCE:
            issues.append(f"{row_id} invalid confidence {row.get('confidence')}")
        related = row.get("related_workflow_ids", [])
        if row.get("workflow_id") == "ATLAS-GLOBAL" and not related:
            issues.append(f"{row_id} uses ATLAS-GLOBAL without related workflows")
        if row.get("workflow_id") != "ATLAS-GLOBAL" and row.get("workflow_id") in related:
            issues.append(f"{row_id} repeats primary workflow_id in related_workflow_ids")
        raw_artifact = row.get("raw_artifact")
        if raw_artifact:
            raw_path = raw_artifact.split("#", 1)[0]
            artifact_path = resolve_path(root, raw_path)
            if not artifact_path.exists():
                issues.append(f"{row_id} raw_artifact missing: {raw_artifact}")
        superseded = row.get("superseded_by")
        if superseded and superseded not in actual_ids:
            issues.append(f"{row_id} superseded_by points to missing id {superseded}")
    workflow_ids = {row["workflow_id"] for row in rows if row["workflow_id"] != "ATLAS-GLOBAL"}
    return CheckResult("evidence", "PASS" if not issues else "FAIL", not issues, issues), rows, workflow_ids


def validate_registry(root: Path, evidence_rows: list[dict[str, Any]]) -> tuple[CheckResult, dict[str, Any], set[str]]:
    path = root / "WORKFLOW_REGISTRY.yaml"
    registry = load_yaml(path)
    issues: list[str] = []
    workflows = registry.get("workflows", [])
    workflow_ids = [workflow.get("workflow_id") for workflow in workflows]
    evidence_ids = {row["id"] for row in evidence_rows}
    if len(workflow_ids) != 17:
        issues.append(f"expected 17 workflows, found {len(workflow_ids)}")
    if len(set(workflow_ids)) != len(workflow_ids):
        issues.append("duplicate workflow_id in registry")
    if set(registry.get("workflow_test_status", {}).keys()) != set(workflow_ids):
        issues.append("workflow_test_status keys do not match workflow ids")
    scopes = registry.get("evidence_scopes", [])
    if not any(scope.get("scope_id") == "ATLAS-GLOBAL" for scope in scopes):
        issues.append("evidence_scopes missing ATLAS-GLOBAL")
    for workflow in workflows:
        wid = workflow["workflow_id"]
        for key in ("workflow_id", "domain", "owner", "path_statuses", "entrypoints", "evidence_ids", "runtime"):
            if key not in workflow:
                issues.append(f"{wid} missing {key}")
        for status in workflow.get("path_statuses", []):
            if status not in ALLOWED_PATH_STATUSES:
                issues.append(f"{wid} invalid path status {status}")
        for status in workflow.get("contract_statuses", []):
            if status not in ALLOWED_CONTRACT_STATUSES:
                issues.append(f"{wid} invalid contract status {status}")
        for evidence_id in workflow.get("evidence_ids", []):
            if evidence_id not in evidence_ids:
                issues.append(f"{wid} references missing evidence {evidence_id}")
        runtime = workflow.get("runtime", {})
        if runtime.get("classification") not in ALLOWED_RUNTIME_CLASSIFICATIONS:
            issues.append(f"{wid} invalid runtime classification")
        if runtime.get("evidence_scope") not in ALLOWED_RUNTIME_SCOPES:
            issues.append(f"{wid} invalid runtime evidence_scope")
        if runtime.get("trigger_mode") not in ALLOWED_TRIGGER_MODES:
            issues.append(f"{wid} invalid runtime trigger_mode")
        if not workflow.get("steps") and not workflow.get("uses"):
            issues.append(f"{wid} missing both steps and uses")
        if "status" in workflow:
            issues.append(f"{wid} contains legacy flat status field")
    for wid, node in registry.get("workflow_test_status", {}).items():
        for key in ("statuses", "evidence_ids"):
            if key not in node:
                issues.append(f"workflow_test_status {wid} missing {key}")
        for status in node.get("statuses", []):
            if status not in ALLOWED_TEST_STATUSES:
                issues.append(f"{wid} invalid test status {status}")
        for evidence_id in node.get("evidence_ids", []):
            if evidence_id not in evidence_ids:
                issues.append(f"{wid} workflow_test_status references missing evidence {evidence_id}")
    return CheckResult("registry", "PASS" if not issues else "FAIL", not issues, issues), registry, set(workflow_ids)


def validate_gaps(root: Path, registry_ids: set[str], evidence_rows: list[dict[str, Any]]) -> tuple[CheckResult, dict[str, Any]]:
    path = root / "WORKFLOW_GAPS.yaml"
    gaps = load_yaml(path)
    issues: list[str] = []
    evidence_ids = {row["id"] for row in evidence_rows}
    gap_registry = gaps.get("gap_registry", [])
    gap_ids = [gap.get("gap_id") for gap in gap_registry]
    if gaps.get("atomic_gap_count") != len(gap_registry):
        issues.append("atomic_gap_count does not match gap_registry size")
    if len(gap_ids) != len(set(gap_ids)):
        issues.append("duplicate gap_id in gap registry")
    mapped = sorted({gap_id for mapping in gaps.get("migration_map", []) for gap_id in mapping.get("gap_ids", [])})
    if sorted(gap_ids) != mapped:
        issues.append("migration_map coverage mismatch")
    for gap in gap_registry:
        gid = gap.get("gap_id", "UNKNOWN")
        for key in ("gap_id", "legacy_items", "priority", "workflow_ids", "evidence_ids", "producer", "consumer", "break_point", "technical_impact", "business_impact", "status"):
            if key not in gap:
                issues.append(f"{gid} missing {key}")
        for wid in gap.get("workflow_ids", []):
            if wid not in registry_ids:
                issues.append(f"{gid} references unknown workflow {wid}")
        for evidence_id in gap.get("evidence_ids", []):
            if evidence_id not in evidence_ids:
                issues.append(f"{gid} references unknown evidence {evidence_id}")
    return CheckResult("gaps", "PASS" if not issues else "FAIL", not issues, issues), gaps


def extract_table_row_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.startswith("| ") and not line.startswith("| ---"))


def validate_docs(root: Path, registry: dict[str, Any], evidence_rows: list[dict[str, Any]], gaps: dict[str, Any]) -> CheckResult:
    issues: list[str] = []
    doc_contents: dict[str, str] = {}
    for name in EXPECTED_DOCS:
        path = root / name
        if not path.exists():
            issues.append(f"{name} missing")
            doc_contents[name] = ""
            continue
        doc_contents[name] = read_text(path)
    for name, text in doc_contents.items():
        if not text.strip():
            issues.append(f"{name} is empty")
        for marker in STALE_MARKERS:
            if marker.lower() in text.lower():
                issues.append(f"{name} contains stale marker: {marker}")
    workflow_count = len(registry["workflows"])
    evidence_count = len(evidence_rows)
    gap_count = gaps["atomic_gap_count"]
    summary = doc_contents["EXECUTIVE_SUMMARY.md"]
    if f"Evidence: {evidence_count}" not in summary and f"Evidence rows: `{evidence_count}`" not in summary:
        issues.append("EXECUTIVE_SUMMARY missing evidence count")
    if f"Workflows: {workflow_count}" not in summary and f"Workflows: `{workflow_count}`" not in summary:
        issues.append("EXECUTIVE_SUMMARY missing workflow count")
    if f"Atomic gaps: {gap_count}" not in summary and f"Atomic gaps: `{gap_count}`" not in summary:
        issues.append("EXECUTIVE_SUMMARY missing atomic gap count")
    if "Target status: COMPLETE" not in summary and "Target status on core artifacts before final validator pass: `PARTIAL`" in summary:
        issues.append("EXECUTIVE_SUMMARY still carries stale PARTIAL header")
    atlas = doc_contents["WORKFLOW_ATLAS.md"]
    if f"Workflows: `{workflow_count}`" not in atlas:
        issues.append("WORKFLOW_ATLAS missing workflow count")
    if f"Evidence rows: `{evidence_count}`" not in atlas:
        issues.append("WORKFLOW_ATLAS missing evidence count")
    if f"Atomic gaps: `{gap_count}`" not in atlas:
        issues.append("WORKFLOW_ATLAS missing atomic gap count")
    contract_rows = sum(len(workflow.get("external_calls", [])) for workflow in registry["workflows"])
    if extract_table_row_count(doc_contents["CROSS_REPO_CONTRACTS.md"]) - 1 != contract_rows:
        issues.append("CROSS_REPO_CONTRACTS row count mismatch")
    confirmed = sum(1 for workflow in registry["workflows"] if workflow["runtime"]["classification"] == "CONFIRMED")
    unverified = sum(1 for workflow in registry["workflows"] if workflow["runtime"]["classification"] == "UNVERIFIED")
    baseline = doc_contents["RUNTIME_BASELINE.md"]
    if f"- CONFIRMED workflows: `{confirmed}`" not in baseline:
        issues.append("RUNTIME_BASELINE confirmed count mismatch")
    if f"- UNVERIFIED workflows: `{unverified}`" not in baseline:
        issues.append("RUNTIME_BASELINE unverified count mismatch")
    return CheckResult("docs", "PASS" if not issues else "FAIL", not issues, issues)


def validate_progress(root: Path, registry: dict[str, Any], evidence_rows: list[dict[str, Any]], gaps: dict[str, Any]) -> CheckResult:
    text = read_text(root / "PROGRESS.md")
    issues: list[str] = []
    required = [
        "AI-OS-WORKFLOW-RECONSTRUCTION-AND-REGISTRY-01",
        f"Evidence rows: `{len(evidence_rows)}`",
        f"Workflows: `{len(registry['workflows'])}`",
        f"Atomic gaps: `{gaps['atomic_gap_count']}`",
        "FINAL-GATE-CLOSEOUT COMPLETE",
    ]
    for token in required:
        if token not in text:
            issues.append(f"PROGRESS missing token: {token}")
    for marker in STALE_MARKERS:
        if marker.lower() in text.lower():
            issues.append(f"PROGRESS contains stale marker: {marker}")
    return CheckResult("progress", "PASS" if not issues else "FAIL", not issues, issues)


def validate_manifest(root: Path, manifest_path: Path | None, final_mode: bool) -> CheckResult:
    if not final_mode:
        return CheckResult(
            "manifest",
            "NOT_APPLICABLE_PRE_MANIFEST",
            True,
            [],
            {
                "manifest_required": False,
                "manifest_path": None if manifest_path is None else str(manifest_path),
                "files_checked": 0,
                "missing_files": [],
                "hash_mismatches": [],
                "size_mismatches": [],
                "required_entry_missing": [],
            },
        )

    assert manifest_path is not None
    issues: list[str] = []
    missing_files: list[str] = []
    hash_mismatches: list[str] = []
    size_mismatches: list[str] = []
    required_entry_missing: list[str] = []
    files_checked = 0

    if not manifest_path.exists():
        return CheckResult(
            "manifest",
            "FAIL",
            False,
            [f"manifest not found: {manifest_path.name}"],
            {
                "manifest_required": True,
                "manifest_path": str(manifest_path),
                "files_checked": 0,
                "missing_files": [manifest_path.name],
                "hash_mismatches": [],
                "size_mismatches": [],
                "required_entry_missing": REQUIRED_MANIFEST_ENTRIES.copy(),
            },
        )
    try:
        manifest = load_json(manifest_path)
    except json.JSONDecodeError as exc:
        return CheckResult(
            "manifest",
            "FAIL",
            False,
            [f"manifest JSON invalid: {exc}"],
            {
                "manifest_required": True,
                "manifest_path": str(manifest_path),
                "files_checked": 0,
                "missing_files": [],
                "hash_mismatches": [],
                "size_mismatches": [],
                "required_entry_missing": REQUIRED_MANIFEST_ENTRIES.copy(),
            },
        )

    schema_version = manifest.get("schema_version")
    if schema_version is not None and schema_version != 1:
        issues.append(f"manifest schema_version unsupported: {schema_version}")

    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        issues.append("manifest files must be a non-empty list")
        entries = []

    entry_by_path: dict[str, dict[str, Any]] = {}
    for entry in entries:
        files_checked += 1
        if not isinstance(entry, dict):
            issues.append("manifest entry is not an object")
            continue
        raw_path = entry.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            issues.append("manifest entry missing path")
            continue
        path_obj = Path(raw_path)
        if path_obj.is_absolute():
            issues.append(f"manifest path is absolute: {raw_path}")
            continue
        if ".." in path_obj.parts:
            issues.append(f"manifest path contains parent traversal: {raw_path}")
            continue
        if path_escapes_root(root, raw_path):
            issues.append(f"manifest path escapes workflow root: {raw_path}")
            continue
        if raw_path in entry_by_path:
            issues.append(f"duplicate manifest path: {raw_path}")
            continue
        entry_by_path[raw_path] = entry

    for required in REQUIRED_MANIFEST_ENTRIES:
        if required not in entry_by_path:
            required_entry_missing.append(required)
            issues.append(f"manifest missing required entry: {required}")
    for required in REQUIRED_FINAL_FILES_OUTSIDE_MANIFEST:
        required_path = root / required
        if not required_path.exists():
            missing_files.append(required)
            issues.append(f"required final file missing: {required}")

    for raw_path, entry in entry_by_path.items():
        full_path = resolve_path(root, raw_path)
        if not full_path.exists():
            missing_files.append(raw_path)
            issues.append(f"manifest target missing: {raw_path}")
            continue
        if "size" not in entry:
            issues.append(f"manifest entry missing size: {raw_path}")
        elif full_path.stat().st_size != entry["size"]:
            size_mismatches.append(raw_path)
            issues.append(f"manifest size mismatch: {raw_path}")
        if "sha256" not in entry:
            issues.append(f"manifest entry missing sha256: {raw_path}")
        elif sha256_file(full_path) != entry["sha256"]:
            hash_mismatches.append(raw_path)
            issues.append(f"manifest sha256 mismatch: {raw_path}")

    if "file_count" in manifest and manifest["file_count"] != len(entries):
        issues.append(f"manifest file_count mismatch: declared {manifest['file_count']} vs actual {len(entries)}")

    return CheckResult(
        "manifest",
        "PASS" if not issues else "FAIL",
        not issues,
        issues,
        {
            "manifest_required": True,
            "manifest_path": str(manifest_path),
            "files_checked": len(entries),
            "missing_files": sorted(set(missing_files)),
            "hash_mismatches": sorted(set(hash_mismatches)),
            "size_mismatches": sorted(set(size_mismatches)),
            "required_entry_missing": sorted(set(required_entry_missing)),
        },
    )


def build_report(results: list[CheckResult], validator_mode: str, manifest_result: CheckResult) -> str:
    overall_ok = all(result.ok for result in results)
    lines = [
        "# FINAL_CONSISTENCY_REPORT.md",
        "",
        f"Generated at: `{utc_timestamp()}`",
        "",
        f"- Validator mode: `{validator_mode}`",
        f"- Manifest required: `{str(manifest_result.meta.get('manifest_required', False)).lower()}`",
        f"- Manifest path: `{manifest_result.meta.get('manifest_path')}`",
        f"- Manifest files checked: `{manifest_result.meta.get('files_checked', 0)}`",
        f"- Hash mismatches: `{len(manifest_result.meta.get('hash_mismatches', []))}`",
        f"- Size mismatches: `{len(manifest_result.meta.get('size_mismatches', []))}`",
        f"- Missing files: `{len(manifest_result.meta.get('missing_files', [])) + len(manifest_result.meta.get('required_entry_missing', []))}`",
        f"- Final result: `{'PASS' if overall_ok else 'FAIL'}`",
        "",
    ]
    for result in results:
        lines.append(f"## {result.name}")
        lines.append("")
        lines.append(f"- status: `{result.status}`")
        if result.details:
            lines.append("- details:")
            for detail in result.details:
                lines.append(f"  - {detail}")
        else:
            lines.append("- details: none")
        if result.name == "manifest":
            lines.append(f"- files_checked: `{result.meta.get('files_checked', 0)}`")
            lines.append(f"- missing_files: `{len(result.meta.get('missing_files', []))}`")
            lines.append(f"- required_entry_missing: `{len(result.meta.get('required_entry_missing', []))}`")
            lines.append(f"- hash_mismatches: `{len(result.meta.get('hash_mismatches', []))}`")
            lines.append(f"- size_mismatches: `{len(result.meta.get('size_mismatches', []))}`")
        lines.append("")
    return "\n".join(lines)


def build_json_payload(
    results: list[CheckResult],
    validator_mode: str,
    root: Path,
    manifest_path: Path | None,
) -> dict[str, Any]:
    manifest_result = next(result for result in results if result.name == "manifest")
    return {
        "ok": all(result.ok for result in results),
        "validator_mode": validator_mode,
        "root": str(root),
        "manifest_required": manifest_result.meta.get("manifest_required", False),
        "manifest_path": None if manifest_path is None else str(manifest_path),
        "results": [
            {
                "name": result.name,
                "status": result.status,
                "ok": result.ok,
                "details": result.details,
                "meta": result.meta,
            }
            for result in results
        ],
    }


def run_validation(root: Path, manifest_path: Path | None, final_mode: bool) -> tuple[list[CheckResult], dict[str, Any]]:
    evidence_result, evidence_rows, _ = validate_evidence(root)
    registry_result, registry, registry_ids = validate_registry(root, evidence_rows)
    gaps_result, gaps = validate_gaps(root, registry_ids, evidence_rows)
    docs_result = validate_docs(root, registry, evidence_rows, gaps)
    progress_result = validate_progress(root, registry, evidence_rows, gaps)
    manifest_result = validate_manifest(root, manifest_path, final_mode)
    results = [evidence_result, registry_result, gaps_result, docs_result, progress_result, manifest_result]
    return results, {
        "registry": registry,
        "evidence_rows": evidence_rows,
        "gaps": gaps,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--pre-manifest", action="store_true")
    mode_group.add_argument("--final", action="store_true")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--root", type=Path, default=SCRIPT_DIR)
    parser.add_argument("--report-md", type=Path)
    parser.add_argument("--report-json", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    final_mode = bool(args.final)
    validator_mode = "FINAL" if final_mode else "PRE_MANIFEST"
    manifest_path = None if not final_mode else (args.manifest.resolve() if args.manifest else (root / DEFAULT_MANIFEST_NAME))

    results, _ = run_validation(root, manifest_path, final_mode)
    manifest_result = next(result for result in results if result.name == "manifest")
    payload = build_json_payload(results, validator_mode, root, manifest_path)

    if args.report_md:
        args.report_md.write_text(build_report(results, validator_mode, manifest_result), encoding="utf-8", newline="\n")
    if args.report_json:
        args.report_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        json.dumps(
            {
                "ok": payload["ok"],
                "validator_mode": validator_mode,
                "manifest_required": payload["manifest_required"],
                "results": [
                    {
                        "name": result.name,
                        "status": result.status,
                        "ok": result.ok,
                        "detail_count": len(result.details),
                    }
                    for result in results
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
