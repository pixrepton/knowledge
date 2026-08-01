from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from workflow_tools_common import utc_timestamp


BASE_DIR = Path(__file__).resolve().parent
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


@dataclass
class CheckResult:
    name: str
    ok: bool
    details: list[str]


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


def check_evidence() -> tuple[CheckResult, list[dict[str, Any]], set[str]]:
    path = BASE_DIR / "WORKFLOW_EVIDENCE.jsonl"
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
        if row["id"] in seen:
            issues.append(f"duplicate evidence id {row['id']}")
        seen.add(row["id"])
        if row["evidence_type"] not in ALLOWED_EVIDENCE_TYPES:
            issues.append(f"{row['id']} invalid evidence_type {row['evidence_type']}")
        if row["confidence"] not in ALLOWED_CONFIDENCE:
            issues.append(f"{row['id']} invalid confidence {row['confidence']}")
        if row["workflow_id"] == "ATLAS-GLOBAL" and not row["related_workflow_ids"]:
            issues.append(f"{row['id']} uses ATLAS-GLOBAL without related workflows")
        raw_artifact = row.get("raw_artifact")
        if raw_artifact:
            raw_path = raw_artifact.split("#", 1)[0]
            full = BASE_DIR / raw_path.replace("_raw/", "_raw/", 1) if raw_path.startswith("_raw/") else BASE_DIR / raw_path
            if not full.exists():
                issues.append(f"{row['id']} raw_artifact missing: {raw_artifact}")
        superseded = row.get("superseded_by")
        if superseded and superseded not in actual_ids:
            issues.append(f"{row['id']} superseded_by points to missing id {superseded}")
    workflow_ids = {row["workflow_id"] for row in rows if row["workflow_id"] != "ATLAS-GLOBAL"}
    return CheckResult("evidence", not issues, issues), rows, workflow_ids


def check_registry(evidence_rows: list[dict[str, Any]]) -> tuple[CheckResult, dict[str, Any], set[str]]:
    path = BASE_DIR / "WORKFLOW_REGISTRY.yaml"
    registry = load_yaml(path)
    issues: list[str] = []
    workflow_ids = [workflow.get("workflow_id") for workflow in registry.get("workflows", [])]
    evidence_ids = {row["id"] for row in evidence_rows}
    if len(workflow_ids) != 17:
        issues.append(f"expected 17 workflows, found {len(workflow_ids)}")
    if len(set(workflow_ids)) != len(workflow_ids):
        issues.append("duplicate workflow_id in registry")
    if set(registry.get("workflow_test_status", {}).keys()) != set(workflow_ids):
        issues.append("workflow_test_status keys do not match workflow ids")
    for workflow in registry.get("workflows", []):
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
    return CheckResult("registry", not issues, issues), registry, set(workflow_ids)


def check_gaps(registry_ids: set[str], evidence_rows: list[dict[str, Any]]) -> tuple[CheckResult, dict[str, Any]]:
    path = BASE_DIR / "WORKFLOW_GAPS.yaml"
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
    return CheckResult("gaps", not issues, issues), gaps


def extract_table_row_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.startswith("| ") and not line.startswith("| ---"))


def check_docs(registry: dict[str, Any], evidence_rows: list[dict[str, Any]], gaps: dict[str, Any]) -> CheckResult:
    issues: list[str] = []
    doc_contents = {name: read_text(BASE_DIR / name) for name in EXPECTED_DOCS}
    for name, text in doc_contents.items():
        if not text.strip():
            issues.append(f"{name} is empty")
        for marker in STALE_MARKERS:
            if marker.lower() in text.lower():
                issues.append(f"{name} contains stale marker: {marker}")
    workflow_count = len(registry["workflows"])
    evidence_count = len(evidence_rows)
    gap_count = gaps["atomic_gap_count"]
    if f"Workflows: `{workflow_count}`" not in doc_contents["WORKFLOW_ATLAS.md"]:
        issues.append("WORKFLOW_ATLAS missing workflow count")
    if f"Evidence rows: `{evidence_count}`" not in doc_contents["WORKFLOW_ATLAS.md"]:
        issues.append("WORKFLOW_ATLAS missing evidence count")
    if f"Atomic gaps: `{gap_count}`" not in doc_contents["WORKFLOW_ATLAS.md"]:
        issues.append("WORKFLOW_ATLAS missing atomic gap count")
    if f"Atomic gaps: `{gap_count}`" not in doc_contents["EXECUTIVE_SUMMARY.md"]:
        issues.append("EXECUTIVE_SUMMARY missing atomic gap count")
    contract_rows = sum(len(workflow.get("external_calls", [])) for workflow in registry["workflows"])
    if extract_table_row_count(doc_contents["CROSS_REPO_CONTRACTS.md"]) - 1 != contract_rows:
        issues.append("CROSS_REPO_CONTRACTS row count mismatch")
    confirmed = sum(1 for workflow in registry["workflows"] if workflow["runtime"]["classification"] == "CONFIRMED")
    unverified = sum(1 for workflow in registry["workflows"] if workflow["runtime"]["classification"] == "UNVERIFIED")
    if f"- CONFIRMED workflows: `{confirmed}`" not in doc_contents["RUNTIME_BASELINE.md"]:
        issues.append("RUNTIME_BASELINE confirmed count mismatch")
    if f"- UNVERIFIED workflows: `{unverified}`" not in doc_contents["RUNTIME_BASELINE.md"]:
        issues.append("RUNTIME_BASELINE unverified count mismatch")
    for workflow in registry["workflows"]:
        wid = workflow["workflow_id"]
        if wid not in doc_contents["WORKFLOW_ATLAS.md"]:
            issues.append(f"WORKFLOW_ATLAS missing workflow {wid}")
        if wid not in doc_contents["RUNTIME_BASELINE.md"]:
            issues.append(f"RUNTIME_BASELINE missing workflow {wid}")
    return CheckResult("docs", not issues, issues)


def check_progress(registry: dict[str, Any], evidence_rows: list[dict[str, Any]], gaps: dict[str, Any]) -> CheckResult:
    path = BASE_DIR / "PROGRESS.md"
    text = read_text(path)
    issues: list[str] = []
    required = [
        "AI-OS-WORKFLOW-RECONSTRUCTION-AND-REGISTRY-01",
        f"Evidence rows: `{len(evidence_rows)}`",
        f"Workflows: `{len(registry['workflows'])}`",
        f"Atomic gaps: `{gaps['atomic_gap_count']}`",
    ]
    for token in required:
        if token not in text:
            issues.append(f"PROGRESS missing token: {token}")
    for marker in STALE_MARKERS:
        if marker.lower() in text.lower():
            issues.append(f"PROGRESS contains stale marker: {marker}")
    return CheckResult("progress", not issues, issues)


def check_manifest(manifest_path: Path | None) -> CheckResult:
    if manifest_path is None or not manifest_path.exists():
        return CheckResult("manifest", True, [])
    manifest = load_json(manifest_path)
    issues: list[str] = []
    for entry in manifest.get("files", []):
        path = BASE_DIR / entry["path"]
        if not path.exists():
            issues.append(f"manifest path missing: {entry['path']}")
            continue
        if path.stat().st_size != entry["size"]:
            issues.append(f"manifest size mismatch: {entry['path']}")
        if sha256_file(path) != entry["sha256"]:
            issues.append(f"manifest sha256 mismatch: {entry['path']}")
        if path.stat().st_mtime_ns != entry["modified_time_ns"]:
            issues.append(f"manifest mtime mismatch: {entry['path']}")
    return CheckResult("manifest", not issues, issues)


def render_report(results: list[CheckResult]) -> str:
    lines = [
        "# FINAL_CONSISTENCY_REPORT.md",
        "",
        f"Generated at: `{utc_timestamp()}`",
        "",
    ]
    for result in results:
        lines.append(f"## {result.name}")
        lines.append("")
        lines.append(f"- status: `{'PASS' if result.ok else 'FAIL'}`")
        if result.details:
            lines.append("- details:")
            for detail in result.details:
                lines.append(f"  - {detail}")
        else:
            lines.append("- details: none")
        lines.append("")
    lines.append(f"Overall: `{'PASS' if all(result.ok for result in results) else 'FAIL'}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--report-md", type=Path)
    parser.add_argument("--report-json", type=Path)
    args = parser.parse_args()

    evidence_result, evidence_rows, _ = check_evidence()
    registry_result, registry, registry_ids = check_registry(evidence_rows)
    gaps_result, gaps = check_gaps(registry_ids, evidence_rows)
    docs_result = check_docs(registry, evidence_rows, gaps)
    progress_result = check_progress(registry, evidence_rows, gaps)
    manifest_result = check_manifest(args.manifest)
    results = [evidence_result, registry_result, gaps_result, docs_result, progress_result, manifest_result]

    if args.report_md:
        args.report_md.write_text(render_report(results), encoding="utf-8", newline="\n")
    if args.report_json:
        payload = {
            "ok": all(result.ok for result in results),
            "results": [{"name": result.name, "ok": result.ok, "details": result.details} for result in results],
        }
        args.report_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({"ok": all(result.ok for result in results), "results": [{"name": result.name, "ok": result.ok, "detail_count": len(result.details)} for result in results]}, ensure_ascii=False, indent=2))
    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
