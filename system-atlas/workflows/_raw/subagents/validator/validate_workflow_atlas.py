#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"fatal: PyYAML import failed: {exc}", file=sys.stderr)
    sys.exit(2)


ALLOWED_EVIDENCE_TYPES = {
    "CODE",
    "CONFIG",
    "RUNTIME",
    "TEST",
    "GRAPH",
    "ABSENCE_SEARCH",
    "SYNTHESIS",
}
ALLOWED_CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}
ALLOWED_PATH_STATUSES = {
    "LIVE_PATH",
    "CONDITIONAL_PATH",
    "DORMANT_PATH",
    "LEGACY_PATH",
    "DEAD_PATH",
    "FALLBACK_PATH",
}
ALLOWED_CONTRACT_STATUSES = {
    "BROKEN_CALL",
    "MISSING_PRODUCER",
    "MISSING_CONSUMER",
    "MISSING_EXECUTOR",
}
ALLOWED_RUNTIME_CLASSIFICATION = {"CONFIRMED", "UNVERIFIED"}
ALLOWED_RUNTIME_EVIDENCE_SCOPE = {
    "FULL_WORKFLOW",
    "PARTIAL_WORKFLOW",
    "ENTRYPOINT_ONLY",
    "PATH_SELECTION_ONLY",
    "ENVIRONMENT_ONLY",
    "STATIC_ONLY",
}
ALLOWED_RUNTIME_TRIGGER_MODE = {"AUTOMATIC", "MANUAL_ONLY", "MIXED"}
ALLOWED_TEST_STATUSES = {
    "NO_DIRECT_TEST_FOUND",
    "SYNTHETIC_ONLY",
    "PROOF_ONLY",
    "UNIT_COVERED",
    "INTEGRATION_COVERED",
    "END_TO_END_COVERED",
    "CHAOS_COVERED",
}
ALLOWED_GAP_STATUSES = {
    "confirmed_inconsistency",
    "confirmed_open",
    "confirmed_risk",
    "needs_adjudication",
    "observation_only",
    "test_broken",
    "test_gap",
}
STALE_MARKERS = [
    "STALE",
    "regeneration pending",
    "next step is",
]
REQUIRED_DOCS = [
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
DOC_MARKER_RULES = {
    "WORKFLOW_ATLAS.md": ["workflow_id"],
    "ENTRYPOINT_INVENTORY.md": ["entrypoint_id", "surface_type", "route_count"],
    "CROSS_REPO_CONTRACTS.md": ["contract_id"],
    "STATE_OWNERSHIP_MATRIX.md": ["state_id", "source_of_truth"],
    "ARCHITECTURAL_RULES_AUDIT.md": ["rule_id"],
    "RUNTIME_BASELINE.md": ["RUNTIME_UNVERIFIED"],
    "RUNTIME_PROOF_PLAN.md": ["RUNTIME_UNVERIFIED"],
}
REQUIRED_FINAL_REPORT = "FINAL_CONSISTENCY_REPORT.md"
DEFAULT_MANIFEST = "FINAL_MANIFEST.json"
EVIDENCE_ID_RE = re.compile(r"^EV-(\d{5})$")
GAP_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]+$")


@dataclass
class Issue:
    level: str
    code: str
    message: str
    path: str | None = None

    def render(self) -> str:
        where = f" [{self.path}]" if self.path else ""
        return f"{self.level} {self.code}{where}: {self.message}"


class AtlasValidator:
    def __init__(self, root: Path, mode: str, manifest_path: Path | None) -> None:
        self.root = root
        self.mode = mode
        self.manifest_path = manifest_path or (self.root / DEFAULT_MANIFEST)
        self.issues: list[Issue] = []
        self.workflow_ids: set[str] = set()
        self.evidence_ids: set[str] = set()
        self.referenced_evidence_ids: set[str] = set()

    def add(self, level: str, code: str, message: str, path: Path | str | None = None) -> None:
        rendered_path = None
        if path is not None:
            rendered_path = str(path)
        self.issues.append(Issue(level=level, code=code, message=message, path=rendered_path))

    def read_text(self, path: Path) -> str:
        return path.read_text(encoding="utf-8", errors="replace")

    def load_yaml(self, path: Path) -> Any:
        return yaml.safe_load(self.read_text(path))

    def load_json(self, path: Path) -> Any:
        return json.loads(self.read_text(path))

    def sha256(self, path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def file_error(self, path: Path, code: str, message: str) -> bool:
        if not path.exists():
            self.add("ERROR", code, message, path)
            return True
        return False

    def validate(self) -> int:
        evidence_rows = self.validate_evidence()
        registry = self.validate_registry()
        self.validate_gap_registry()
        self.validate_supporting_docs()
        self.validate_manifest()
        self.validate_evidence_references(evidence_rows, registry)
        return self.render_summary()

    def validate_evidence(self) -> list[dict[str, Any]]:
        path = self.root / "WORKFLOW_EVIDENCE.jsonl"
        if self.file_error(path, "MISSING_EVIDENCE", "WORKFLOW_EVIDENCE.jsonl not found"):
            return []
        rows: list[dict[str, Any]] = []
        seen_ids: list[str] = []
        for line_number, raw_line in enumerate(self.read_text(path).splitlines(), start=1):
            if not raw_line.strip():
                self.add("ERROR", "EVIDENCE_BLANK_LINE", "blank line in JSONL evidence", f"{path}:{line_number}")
                continue
            try:
                row = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                self.add("ERROR", "EVIDENCE_JSON_DECODE", f"{exc}", f"{path}:{line_number}")
                continue
            rows.append(row)
        required = {
            "id",
            "workflow_id",
            "related_workflow_ids",
            "repo",
            "file",
            "symbol",
            "lines",
            "evidence_type",
            "claim",
            "confidence",
            "raw_artifact",
            "superseded_by",
        }
        for index, row in enumerate(rows, start=1):
            row_id = row.get("id")
            seen_ids.append(row_id)
            expected_id = f"EV-{index:05d}"
            if row_id != expected_id:
                self.add("ERROR", "EVIDENCE_SEQUENCE", f"expected {expected_id}, got {row_id}", path)
            missing = sorted(required - set(row))
            if missing:
                self.add("ERROR", "EVIDENCE_FIELDS", f"{row_id} missing fields: {missing}", path)
                continue
            extra = sorted(set(row) - required)
            if extra:
                self.add("WARN", "EVIDENCE_EXTRA_FIELDS", f"{row_id} has extra fields: {extra}", path)
            match = EVIDENCE_ID_RE.match(str(row_id))
            if not match:
                self.add("ERROR", "EVIDENCE_ID_FORMAT", f"invalid evidence id: {row_id}", path)
            if row_id in self.evidence_ids:
                self.add("ERROR", "EVIDENCE_DUPLICATE_ID", f"duplicate evidence id: {row_id}", path)
            self.evidence_ids.add(str(row_id))
            workflow_id = row.get("workflow_id")
            related = row.get("related_workflow_ids")
            if not isinstance(related, list):
                self.add("ERROR", "EVIDENCE_RELATED_TYPE", f"{row_id} related_workflow_ids must be a list", path)
            if workflow_id == "ATLAS-GLOBAL" and not related:
                self.add("ERROR", "EVIDENCE_ATLAS_SCOPE", f"{row_id} ATLAS-GLOBAL requires non-empty related_workflow_ids", path)
            if workflow_id != "ATLAS-GLOBAL" and isinstance(related, list) and workflow_id in related:
                self.add("ERROR", "EVIDENCE_RELATED_SELF", f"{row_id} repeats its primary workflow_id in related_workflow_ids", path)
            if row.get("evidence_type") not in ALLOWED_EVIDENCE_TYPES:
                self.add("ERROR", "EVIDENCE_TYPE", f"{row_id} invalid evidence_type {row.get('evidence_type')}", path)
            if row.get("confidence") not in ALLOWED_CONFIDENCE:
                self.add("ERROR", "EVIDENCE_CONFIDENCE", f"{row_id} invalid confidence {row.get('confidence')}", path)
            for field_name in ("repo", "file", "symbol", "lines"):
                value = row.get(field_name)
                if not isinstance(value, str):
                    self.add("ERROR", "EVIDENCE_FIELD_VALUE", f"{row_id} invalid {field_name}", path)
                elif not value:
                    level = "ERROR" if self.mode == "final" else "WARN"
                    self.add(level, "EVIDENCE_LOCATOR_EMPTY", f"{row_id} empty {field_name}", path)
            claim = row.get("claim")
            if not isinstance(claim, str) or not claim:
                self.add("ERROR", "EVIDENCE_FIELD_VALUE", f"{row_id} invalid claim", path)
            raw_artifact = row.get("raw_artifact")
            if raw_artifact is not None:
                if not isinstance(raw_artifact, str) or not raw_artifact.startswith("_raw/"):
                    self.add("ERROR", "EVIDENCE_RAW_ARTIFACT_FORMAT", f"{row_id} raw_artifact must point under _raw/: {raw_artifact}", path)
                else:
                    artifact_rel = raw_artifact.split("#", 1)[0]
                    artifact_path = self.root / artifact_rel
                    if not artifact_path.exists():
                        self.add("ERROR", "EVIDENCE_RAW_ARTIFACT_MISSING", f"{row_id} raw artifact not found: {artifact_rel}", path)
            superseded_by = row.get("superseded_by")
            if superseded_by is not None and (not isinstance(superseded_by, str) or not EVIDENCE_ID_RE.match(superseded_by)):
                self.add("ERROR", "EVIDENCE_SUPERSEDED_FORMAT", f"{row_id} invalid superseded_by {superseded_by}", path)
        if seen_ids:
            last_expected = f"EV-{len(seen_ids):05d}"
            if seen_ids[-1] != last_expected:
                self.add("ERROR", "EVIDENCE_LAST_ID", f"final evidence id should be {last_expected}, got {seen_ids[-1]}", path)
        for row in rows:
            superseded_by = row.get("superseded_by")
            row_id = row.get("id")
            if superseded_by is not None:
                if superseded_by == row_id:
                    self.add("ERROR", "EVIDENCE_SUPERSEDED_SELF", f"{row_id} supersedes itself", path)
                if superseded_by not in self.evidence_ids:
                    self.add("ERROR", "EVIDENCE_SUPERSEDED_TARGET", f"{row_id} points to missing superseded_by {superseded_by}", path)
        return rows

    def validate_registry(self) -> dict[str, Any]:
        path = self.root / "WORKFLOW_REGISTRY.yaml"
        if self.file_error(path, "MISSING_REGISTRY", "WORKFLOW_REGISTRY.yaml not found"):
            return {}
        registry = self.load_yaml(path)
        if not isinstance(registry, dict):
            self.add("ERROR", "REGISTRY_TYPE", "registry root must be a mapping", path)
            return {}
        for key in ("schema_version", "generated_at", "evidence_scopes", "status_taxonomy", "subflows", "workflows", "workflow_test_status"):
            if key not in registry:
                self.add("ERROR", "REGISTRY_FIELDS", f"missing top-level key {key}", path)
        scopes = registry.get("evidence_scopes") or []
        if not isinstance(scopes, list):
            self.add("ERROR", "REGISTRY_SCOPES_TYPE", "evidence_scopes must be a list", path)
        else:
            scope_ids = set()
            has_atlas_global = False
            for scope in scopes:
                if not isinstance(scope, dict):
                    self.add("ERROR", "REGISTRY_SCOPE_NODE", "scope entry must be a mapping", path)
                    continue
                scope_id = scope.get("scope_id")
                if scope_id in scope_ids:
                    self.add("ERROR", "REGISTRY_SCOPE_DUPLICATE", f"duplicate evidence scope {scope_id}", path)
                scope_ids.add(scope_id)
                if scope_id == "ATLAS-GLOBAL":
                    has_atlas_global = True
            if not has_atlas_global:
                self.add("ERROR", "REGISTRY_SCOPE_ATLAS", "ATLAS-GLOBAL scope missing", path)
        taxonomy = registry.get("status_taxonomy") or {}
        self.expect_taxonomy(taxonomy, path)
        subflows = registry.get("subflows") or {}
        if not isinstance(subflows, dict):
            self.add("ERROR", "REGISTRY_SUBFLOWS_TYPE", "subflows must be a mapping", path)
            subflows = {}
        for subflow_id, node in subflows.items():
            if not isinstance(node, dict):
                self.add("ERROR", "REGISTRY_SUBFLOW_NODE", f"{subflow_id} must be a mapping", path)
                continue
            if "description" not in node or "evidence_ids" not in node:
                self.add("ERROR", "REGISTRY_SUBFLOW_FIELDS", f"{subflow_id} missing description or evidence_ids", path)
            self.capture_evidence_refs(node.get("evidence_ids"), f"subflow {subflow_id}", path)
            if "confidence" in node:
                self.add("ERROR", "REGISTRY_FORBIDDEN_CONFIDENCE", f"{subflow_id} contains forbidden confidence", path)
        workflows_raw = registry.get("workflows") or {}
        workflow_items: list[tuple[str, dict[str, Any]]] = []
        if isinstance(workflows_raw, dict):
            workflow_items = [(key, value) for key, value in workflows_raw.items()]
        elif isinstance(workflows_raw, list):
            for item in workflows_raw:
                if not isinstance(item, dict):
                    self.add("ERROR", "REGISTRY_WORKFLOW_NODE", "workflow list item must be a mapping", path)
                    continue
                workflow_key = item.get("workflow_id")
                workflow_items.append((workflow_key, item))
        else:
            self.add("ERROR", "REGISTRY_WORKFLOWS_TYPE", "workflows must be a mapping or list", path)
        self.workflow_ids = {key for key, _ in workflow_items if isinstance(key, str)}
        for workflow_key, node in workflow_items:
            if not isinstance(node, dict):
                self.add("ERROR", "REGISTRY_WORKFLOW_NODE", f"{workflow_key} must be a mapping", path)
                continue
            if node.get("workflow_id") != workflow_key:
                self.add("ERROR", "REGISTRY_WORKFLOW_ID", f"{workflow_key} workflow_id mismatch", path)
            for required in ("workflow_id", "domain", "owner", "path_statuses", "entrypoints", "evidence_ids", "runtime"):
                if required not in node:
                    self.add("ERROR", "REGISTRY_WORKFLOW_FIELDS", f"{workflow_key} missing {required}", path)
            if "status" in node:
                self.add("ERROR", "REGISTRY_LEGACY_STATUS", f"{workflow_key} still uses legacy status field", path)
            if "confidence" in node:
                self.add("ERROR", "REGISTRY_FORBIDDEN_CONFIDENCE", f"{workflow_key} contains forbidden confidence", path)
            path_statuses = node.get("path_statuses")
            if not isinstance(path_statuses, list) or not path_statuses:
                self.add("ERROR", "REGISTRY_PATH_STATUSES", f"{workflow_key} path_statuses must be a non-empty list", path)
            else:
                invalid = [status for status in path_statuses if status not in ALLOWED_PATH_STATUSES]
                if invalid:
                    self.add("ERROR", "REGISTRY_PATH_STATUS_VALUE", f"{workflow_key} invalid path_statuses {invalid}", path)
            contract_statuses = node.get("contract_statuses")
            if contract_statuses is not None:
                if not isinstance(contract_statuses, list):
                    self.add("ERROR", "REGISTRY_CONTRACT_STATUSES", f"{workflow_key} contract_statuses must be a list", path)
                else:
                    invalid = [status for status in contract_statuses if status not in ALLOWED_CONTRACT_STATUSES]
                    if invalid:
                        self.add("ERROR", "REGISTRY_CONTRACT_STATUS_VALUE", f"{workflow_key} invalid contract_statuses {invalid}", path)
            runtime = node.get("runtime")
            if not isinstance(runtime, dict):
                self.add("ERROR", "REGISTRY_RUNTIME_TYPE", f"{workflow_key} runtime must be a mapping", path)
            else:
                for required in ("classification", "evidence_scope", "trigger_mode", "note"):
                    if required not in runtime:
                        self.add("ERROR", "REGISTRY_RUNTIME_FIELDS", f"{workflow_key} runtime missing {required}", path)
                if runtime.get("classification") not in ALLOWED_RUNTIME_CLASSIFICATION:
                    self.add("ERROR", "REGISTRY_RUNTIME_CLASSIFICATION", f"{workflow_key} invalid runtime classification {runtime.get('classification')}", path)
                if runtime.get("evidence_scope") not in ALLOWED_RUNTIME_EVIDENCE_SCOPE:
                    self.add("ERROR", "REGISTRY_RUNTIME_SCOPE", f"{workflow_key} invalid runtime evidence_scope {runtime.get('evidence_scope')}", path)
                if runtime.get("trigger_mode") not in ALLOWED_RUNTIME_TRIGGER_MODE:
                    self.add("ERROR", "REGISTRY_RUNTIME_TRIGGER", f"{workflow_key} invalid runtime trigger_mode {runtime.get('trigger_mode')}", path)
                if runtime.get("classification") == "CONFIRMED" and runtime.get("evidence_scope") == "STATIC_ONLY":
                    self.add("ERROR", "REGISTRY_RUNTIME_CONTRADICTION", f"{workflow_key} cannot be CONFIRMED with STATIC_ONLY scope", path)
                if "confidence" in runtime:
                    self.add("ERROR", "REGISTRY_FORBIDDEN_CONFIDENCE", f"{workflow_key} runtime contains forbidden confidence", path)
                self.capture_evidence_refs(runtime.get("evidence_ids"), f"runtime {workflow_key}", path, required=False)
            entrypoints = node.get("entrypoints")
            if not isinstance(entrypoints, list) or not entrypoints:
                self.add("ERROR", "REGISTRY_ENTRYPOINTS", f"{workflow_key} entrypoints must be a non-empty list", path)
            self.capture_evidence_refs(node.get("evidence_ids"), f"workflow {workflow_key}", path)
            if not node.get("steps") and not node.get("uses"):
                self.add("ERROR", "REGISTRY_FLOW_BODY", f"{workflow_key} needs at least one of steps or uses", path)
        test_status = registry.get("workflow_test_status") or {}
        if not isinstance(test_status, dict):
            self.add("ERROR", "REGISTRY_TEST_STATUS_TYPE", "workflow_test_status must be a mapping", path)
            test_status = {}
        if set(test_status) != self.workflow_ids:
            missing = sorted(self.workflow_ids - set(test_status))
            extra = sorted(set(test_status) - self.workflow_ids)
            self.add("ERROR", "REGISTRY_TEST_STATUS_KEYS", f"workflow_test_status mismatch missing={missing} extra={extra}", path)
        for workflow_id, node in test_status.items():
            if not isinstance(node, dict):
                self.add("ERROR", "REGISTRY_TEST_STATUS_NODE", f"{workflow_id} workflow_test_status must be a mapping", path)
                continue
            for required in ("statuses", "evidence_ids"):
                if required not in node:
                    self.add("ERROR", "REGISTRY_TEST_STATUS_FIELDS", f"{workflow_id} test status missing {required}", path)
            statuses = node.get("statuses")
            if not isinstance(statuses, list) or not statuses:
                self.add("ERROR", "REGISTRY_TEST_STATUS_VALUES", f"{workflow_id} statuses must be a non-empty list", path)
            else:
                invalid = [status for status in statuses if status not in ALLOWED_TEST_STATUSES]
                if invalid:
                    self.add("ERROR", "REGISTRY_TEST_STATUS_INVALID", f"{workflow_id} invalid test statuses {invalid}", path)
            self.capture_evidence_refs(node.get("evidence_ids"), f"workflow_test_status {workflow_id}", path)
            if "confidence" in node:
                self.add("ERROR", "REGISTRY_FORBIDDEN_CONFIDENCE", f"{workflow_id} workflow_test_status contains forbidden confidence", path)
        return registry

    def expect_taxonomy(self, taxonomy: dict[str, Any], path: Path) -> None:
        expected = {
            "path_statuses": ALLOWED_PATH_STATUSES,
            "contract_statuses": ALLOWED_CONTRACT_STATUSES,
            "runtime_classification": ALLOWED_RUNTIME_CLASSIFICATION,
            "runtime_evidence_scope": ALLOWED_RUNTIME_EVIDENCE_SCOPE,
            "runtime_trigger_mode": ALLOWED_RUNTIME_TRIGGER_MODE,
            "workflow_test_statuses": ALLOWED_TEST_STATUSES,
        }
        for key, allowed in expected.items():
            values = taxonomy.get(key)
            if not isinstance(values, list):
                self.add("ERROR", "REGISTRY_TAXONOMY", f"status_taxonomy.{key} must be a list", path)
                continue
            if set(values) != set(allowed):
                self.add("ERROR", "REGISTRY_TAXONOMY_VALUES", f"status_taxonomy.{key} mismatch", path)

    def capture_evidence_refs(self, evidence_ids: Any, label: str, path: Path, required: bool = True) -> None:
        if evidence_ids is None and not required:
            return
        if not isinstance(evidence_ids, list) or (required and not evidence_ids):
            self.add("ERROR", "EVIDENCE_ASSOCIATION_TYPE", f"{label} requires non-empty evidence_ids list", path)
            return
        for ev_id in evidence_ids:
            if not isinstance(ev_id, str) or not EVIDENCE_ID_RE.match(ev_id):
                self.add("ERROR", "EVIDENCE_ASSOCIATION_ID", f"{label} references invalid evidence id {ev_id}", path)
                continue
            self.referenced_evidence_ids.add(ev_id)

    def validate_gap_registry(self) -> None:
        path = self.root / "WORKFLOW_GAPS.yaml"
        if self.file_error(path, "MISSING_GAPS", "WORKFLOW_GAPS.yaml not found"):
            return
        data = self.load_yaml(path)
        if not isinstance(data, dict):
            self.add("ERROR", "GAPS_TYPE", "gap registry root must be a mapping", path)
            return
        for key in ("schema_version", "generated_at", "legacy_item_count", "atomic_gap_count", "gap_registry"):
            if key not in data:
                self.add("ERROR", "GAPS_FIELDS", f"missing top-level key {key}", path)
        gap_registry = data.get("gap_registry") or []
        if not isinstance(gap_registry, list):
            self.add("ERROR", "GAPS_LIST", "gap_registry must be a list", path)
            return
        if data.get("atomic_gap_count") != len(gap_registry):
            self.add("ERROR", "GAPS_COUNT", f"atomic_gap_count={data.get('atomic_gap_count')} but rows={len(gap_registry)}", path)
        seen_gap_ids = set()
        for row in gap_registry:
            if not isinstance(row, dict):
                self.add("ERROR", "GAPS_NODE", "gap entry must be a mapping", path)
                continue
            gap_id = row.get("gap_id")
            if not isinstance(gap_id, str) or not GAP_ID_RE.match(gap_id):
                self.add("ERROR", "GAPS_ID_FORMAT", f"invalid gap_id {gap_id}", path)
            if gap_id in seen_gap_ids:
                self.add("ERROR", "GAPS_DUPLICATE_ID", f"duplicate gap_id {gap_id}", path)
            seen_gap_ids.add(gap_id)
            if row.get("status") not in ALLOWED_GAP_STATUSES:
                self.add("ERROR", "GAPS_STATUS", f"{gap_id} invalid status {row.get('status')}", path)
            workflow_ids = row.get("workflow_ids")
            if not isinstance(workflow_ids, list) or not workflow_ids:
                level = "ERROR" if self.mode == "final" else "WARN"
                self.add(level, "GAPS_WORKFLOW_IDS", f"{gap_id} workflow_ids must be a non-empty list", path)
            else:
                for workflow_id in workflow_ids:
                    if workflow_id not in self.workflow_ids:
                        self.add("ERROR", "GAPS_WORKFLOW_REF", f"{gap_id} references unknown workflow_id {workflow_id}", path)
            evidence_ids = row.get("evidence_ids")
            if not isinstance(evidence_ids, list) or not evidence_ids:
                self.add("ERROR", "GAPS_EVIDENCE_IDS", f"{gap_id} evidence_ids must be a non-empty list", path)
            else:
                for ev_id in evidence_ids:
                    if ev_id not in self.evidence_ids:
                        self.add("ERROR", "GAPS_EVIDENCE_REF", f"{gap_id} references unknown evidence id {ev_id}", path)
            for field_name in ("producer", "consumer", "break_point", "technical_impact", "business_impact"):
                if not isinstance(row.get(field_name), str) or not row.get(field_name):
                    self.add("ERROR", "GAPS_FIELD_VALUE", f"{gap_id} invalid {field_name}", path)

    def validate_supporting_docs(self) -> None:
        required_docs = list(REQUIRED_DOCS)
        if self.mode == "final":
            required_docs.append(REQUIRED_FINAL_REPORT)
        for doc_name in required_docs:
            path = self.root / doc_name
            level = "ERROR" if self.mode == "final" else "WARN"
            if not path.exists():
                self.add(level, "DOC_MISSING", f"{doc_name} is missing", path)
                continue
            text = self.read_text(path)
            for marker in STALE_MARKERS:
                if marker in text:
                    issue_level = "ERROR" if self.mode == "final" else "WARN"
                    self.add(issue_level, "DOC_STALE_MARKER", f"{doc_name} contains stale marker '{marker}'", path)
            expected_markers = DOC_MARKER_RULES.get(doc_name)
            if expected_markers:
                if not any(marker in text for marker in expected_markers):
                    issue_level = "ERROR" if self.mode == "final" else "WARN"
                    self.add(issue_level, "DOC_NORMALIZATION_MARKER", f"{doc_name} missing any of markers {expected_markers}", path)

    def validate_manifest(self) -> None:
        path = self.manifest_path
        if not path.exists():
            level = "ERROR" if self.mode == "final" else "WARN"
            self.add(level, "MANIFEST_MISSING", f"manifest not found at {path.name}", path)
            return
        try:
            manifest = self.load_json(path)
        except json.JSONDecodeError as exc:
            self.add("ERROR", "MANIFEST_JSON_DECODE", f"{exc}", path)
            return
        if isinstance(manifest, dict):
            files = manifest.get("files")
        else:
            files = manifest
        if not isinstance(files, list):
            self.add("ERROR", "MANIFEST_FILES", "manifest must be a list or contain a files list", path)
            return
        recorded_paths = set()
        for entry in files:
            if not isinstance(entry, dict):
                self.add("ERROR", "MANIFEST_ENTRY_TYPE", "manifest entry must be a mapping", path)
                continue
            for required in ("path", "size", "sha256", "modified_at"):
                if required not in entry:
                    self.add("ERROR", "MANIFEST_ENTRY_FIELDS", f"manifest entry missing {required}", path)
            rel = entry.get("path")
            if not isinstance(rel, str) or not rel or Path(rel).is_absolute():
                self.add("ERROR", "MANIFEST_PATH", f"manifest path must be relative: {rel}", path)
                continue
            recorded_paths.add(rel)
            target = self.root / rel
            if not target.exists():
                self.add("ERROR", "MANIFEST_TARGET_MISSING", f"manifest target missing: {rel}", path)
                continue
            if entry.get("size") != target.stat().st_size:
                self.add("ERROR", "MANIFEST_SIZE", f"size mismatch for {rel}", path)
            if entry.get("sha256") != self.sha256(target):
                self.add("ERROR", "MANIFEST_SHA256", f"sha256 mismatch for {rel}", path)
            if not isinstance(entry.get("modified_at"), str) or not entry.get("modified_at"):
                self.add("ERROR", "MANIFEST_MODIFIED_AT", f"modified_at missing for {rel}", path)
        if self.mode == "final":
            expected_paths = set(REQUIRED_DOCS + [REQUIRED_FINAL_REPORT, "WORKFLOW_EVIDENCE.jsonl", "WORKFLOW_REGISTRY.yaml", "WORKFLOW_GAPS.yaml"])
            missing = sorted(expected_paths - recorded_paths)
            if missing:
                self.add("ERROR", "MANIFEST_COVERAGE", f"manifest missing expected paths: {missing}", path)

    def validate_evidence_references(self, evidence_rows: list[dict[str, Any]], registry: dict[str, Any]) -> None:
        if not evidence_rows or not registry:
            return
        for row in evidence_rows:
            workflow_id = row.get("workflow_id")
            related = row.get("related_workflow_ids") or []
            row_id = row.get("id")
            if workflow_id != "ATLAS-GLOBAL" and workflow_id not in self.workflow_ids:
                self.add("ERROR", "EVIDENCE_WORKFLOW_REF", f"{row_id} references unknown workflow_id {workflow_id}")
            for related_id in related:
                if related_id not in self.workflow_ids:
                    self.add("ERROR", "EVIDENCE_RELATED_WORKFLOW_REF", f"{row_id} references unknown related_workflow_id {related_id}")
        missing_refs = sorted(self.evidence_ids - self.referenced_evidence_ids)
        if missing_refs:
            level = "ERROR" if self.mode == "final" else "WARN"
            self.add(level, "EVIDENCE_UNATTACHED", f"evidence ids not referenced by registry/test/subflow nodes: {missing_refs[:20]}{'...' if len(missing_refs) > 20 else ''}")

    def render_summary(self) -> int:
        errors = [issue for issue in self.issues if issue.level == "ERROR"]
        warns = [issue for issue in self.issues if issue.level == "WARN"]
        print(f"root={self.root}")
        print(f"mode={self.mode}")
        print(f"errors={len(errors)} warnings={len(warns)}")
        for issue in self.issues:
            print(issue.render())
        print("status=PASS" if not errors else "status=FAIL")
        return 0 if not errors else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Draft validator for the workflow atlas artifacts.")
    parser.add_argument("--root", default="knowledge/system-atlas/workflows", help="Atlas root directory.")
    parser.add_argument("--mode", choices=["draft", "final"], default="final", help="draft = softer doc/manifest checks, final = hard gate.")
    parser.add_argument("--manifest", default=None, help="Optional manifest path. Defaults to <root>/FINAL_MANIFEST.json.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    manifest = Path(args.manifest).resolve() if args.manifest else None
    validator = AtlasValidator(root=root, mode=args.mode, manifest_path=manifest)
    return validator.validate()


if __name__ == "__main__":
    raise SystemExit(main())
