from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from workflow_tools_common import (
    RAW_DIR,
    WORKFLOWS_DIR,
    dump_json,
    dump_jsonl,
    ensure_dir,
    load_json,
    load_jsonl,
    load_yaml,
    sha256_file,
    utc_timestamp,
)


EVIDENCE_PATH = WORKFLOWS_DIR / "WORKFLOW_EVIDENCE.jsonl"
REGISTRY_PATH = WORKFLOWS_DIR / "WORKFLOW_REGISTRY.yaml"
PREVIEW_PATH = RAW_DIR / "subagents" / "evidence" / "n1_full_rewrite_preview.jsonl"
UNATTACHED_PREVIEW_PATH = RAW_DIR / "n1_unattached_preview_seed.json"
PREVIEW_OUT_PATH = RAW_DIR / "n1_full_normalized_preview.jsonl"
REPORT_PATH = RAW_DIR / "n1_normalization_report.json"

ATLAS_GLOBAL = "ATLAS-GLOBAL"
VALID_EVIDENCE_TYPES = {
    "CODE",
    "CONFIG",
    "RUNTIME",
    "TEST",
    "GRAPH",
    "ABSENCE_SEARCH",
    "SYNTHESIS",
}
VALID_CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}

KNOWN_RAW_ARTIFACTS = {
    "EV-00139": "_raw/planner_tool_chain_cross_reference.md",
    "EV-00176": "_raw/proposal_type_creator_approver_executor_result_writer_cross_reference.md",
    "EV-00177": "_raw/tool_registry_cross_reference.md",
    "EV-00178": "_raw/event_type_emitter_handler_cross_reference.md",
    "EV-00179": "_raw/fact_key_producer_reader_supersession_invalidation_cross_reference.md",
    "EV-00180": "_raw/signal_source_kind_cross_reference.md",
    "EV-00181": "_raw/table_write_reader_cross_reference.md",
    "EV-00182": "_raw/status_value_writer_consumer_cross_reference.md",
    "EV-00183": "_raw/projection_field_backend_producer_frontend_reader_cross_reference.md",
    "EV-00184": "_raw/feature_flag_env_loader_branchpoint_live_value_cross_reference.md",
    "EV-00185": "_raw/scheduler_timer_cron_actual_caller_cross_reference.md",
    "EV-00186": "_raw/cross_repo_payload_validator_route_client_recovery_replay_cross_reference.md",
    "EV-00187": "_raw/test_evidence_mapping_cross_reference.md",
}


def load_registry_mappings() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    registry = load_yaml(REGISTRY_PATH)
    primary: dict[str, list[str]] = defaultdict(list)
    test_index: dict[str, list[str]] = defaultdict(list)
    for wf in registry.get("workflows", []):
        wid = wf["workflow_id"]
        for ev in wf.get("evidence_ids", []) or []:
            if wid not in primary[ev]:
                primary[ev].append(wid)
    for wid, meta in (registry.get("workflow_test_status") or {}).items():
        for ev in meta.get("evidence_ids", []) or []:
            if wid not in test_index[ev]:
                test_index[ev].append(wid)
    return primary, test_index


def load_full_preview() -> dict[str, dict[str, Any]]:
    if not PREVIEW_PATH.exists():
        return {}
    rows = load_jsonl(PREVIEW_PATH)
    return {row["id"]: row for row in rows}


def load_unattached_seed() -> dict[str, dict[str, Any]]:
    if not UNATTACHED_PREVIEW_PATH.exists():
        return {}
    return load_json(UNATTACHED_PREVIEW_PATH)


def infer_evidence_type(row: dict[str, Any]) -> str:
    existing = row.get("evidence_type")
    if existing in VALID_EVIDENCE_TYPES:
        return existing
    text = " ".join(str(row.get(key, "")) for key in ("claim", "summary", "file", "symbol"))
    lowered = text.lower()
    file_path = str(row.get("file", ""))
    if "runtime_confirmed" in lowered or "live worker" in lowered or "read live" in lowered:
        return "RUNTIME"
    if (
        "/tests/" in file_path.replace("\\", "/")
        or file_path.endswith((".spec.ts", ".test.js", ".regression.test.mjs"))
        or Path(file_path).name.startswith("test_")
        or "tests." in lowered
    ):
        return "TEST"
    if "gitnexus" in lowered or "codebase-memory" in lowered or "graph" in lowered:
        return "GRAPH"
    if any(token in lowered for token in ("zero callers", "absent", "no caller", "exhaustive grep", "not found", "project not found")):
        return "ABSENCE_SEARCH"
    if any(token in lowered for token in ("docker-compose", ".env", "config", "settings", "flag", "route enumeration")):
        return "CONFIG"
    return "CODE"


def infer_confidence(row: dict[str, Any], evidence_type: str) -> str:
    existing = row.get("confidence")
    if existing in VALID_CONFIDENCE:
        return existing
    text = " ".join(str(row.get(key, "")) for key in ("claim", "summary"))
    lowered = text.lower()
    if "decisive" in lowered or "confirmed" in lowered or "exhaustive" in lowered:
        return "HIGH"
    if evidence_type in {"RUNTIME", "TEST"}:
        return "HIGH"
    if evidence_type in {"GRAPH", "ABSENCE_SEARCH", "CONFIG"}:
        return "MEDIUM"
    return "HIGH"


def normalize_claim(row: dict[str, Any]) -> str:
    claim = row.get("claim") or row.get("summary") or ""
    return " ".join(str(claim).split())


def infer_workflow_attachment(
    row_id: str,
    primary_map: dict[str, list[str]],
    test_map: dict[str, list[str]],
    unattached_seed: dict[str, dict[str, Any]],
) -> tuple[str, list[str]]:
    if row_id in unattached_seed:
        seed = unattached_seed[row_id]
        workflow_id = seed["workflow_id"]
        related = list(seed.get("related_workflow_ids", []))
        return workflow_id, related

    attached = list(dict.fromkeys(primary_map.get(row_id, []) + test_map.get(row_id, [])))
    if not attached:
        return ATLAS_GLOBAL, []
    if len(attached) == 1:
        return attached[0], []
    if row_id == "EV-00187":
        return ATLAS_GLOBAL, attached
    return ATLAS_GLOBAL, attached


def normalize_row(
    source_row: dict[str, Any],
    preview_row: dict[str, Any] | None,
    primary_map: dict[str, list[str]],
    test_map: dict[str, list[str]],
    unattached_seed: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    row_id = source_row["id"]
    if preview_row is not None:
        workflow_id = preview_row["workflow_id"]
        related = list(preview_row.get("related_workflow_ids", []))
        evidence_type = preview_row["evidence_type"]
        confidence = preview_row["confidence"]
        raw_artifact = preview_row.get("raw_artifact")
        superseded_by = preview_row.get("superseded_by")
    else:
        workflow_id, related = infer_workflow_attachment(row_id, primary_map, test_map, unattached_seed)
        evidence_type = infer_evidence_type(source_row)
        confidence = infer_confidence(source_row, evidence_type)
        raw_artifact = source_row.get("raw_artifact") or KNOWN_RAW_ARTIFACTS.get(row_id)
        superseded_by = None

    related = [item for item in dict.fromkeys(related) if item and item != workflow_id]
    normalized = {
        "id": row_id,
        "workflow_id": workflow_id,
        "related_workflow_ids": related,
        "repo": source_row.get("repo", ""),
        "file": source_row.get("file", ""),
        "symbol": source_row.get("symbol", ""),
        "lines": source_row.get("lines", ""),
        "evidence_type": evidence_type if evidence_type in VALID_EVIDENCE_TYPES else "CODE",
        "claim": normalize_claim(source_row),
        "confidence": confidence if confidence in VALID_CONFIDENCE else "MEDIUM",
        "raw_artifact": raw_artifact,
        "superseded_by": superseded_by,
    }
    return normalized


def build_preview() -> list[dict[str, Any]]:
    source_rows = load_jsonl(EVIDENCE_PATH)
    preview_rows = load_full_preview()
    unattached_seed = load_unattached_seed()
    primary_map, test_map = load_registry_mappings()
    normalized = [
        normalize_row(row, preview_rows.get(row["id"]), primary_map, test_map, unattached_seed)
        for row in source_rows
    ]
    normalized.sort(key=lambda row: int(row["id"].split("-")[1]))
    return normalized


def validate_rows(rows: list[dict[str, Any]], original_rows: list[dict[str, Any]]) -> dict[str, Any]:
    issues: list[str] = []
    original_by_id = {row["id"]: row for row in original_rows}
    ids = [row["id"] for row in rows]
    expected = [f"EV-{index:05d}" for index in range(1, len(rows) + 1)]
    if ids != expected:
        issues.append("evidence sequence mismatch")
    for row in rows:
        missing = [key for key in ("id", "workflow_id", "related_workflow_ids", "repo", "file", "symbol", "lines", "evidence_type", "claim", "confidence", "raw_artifact", "superseded_by") if key not in row]
        if missing:
            issues.append(f"{row['id']} missing keys: {missing}")
        if row["evidence_type"] not in VALID_EVIDENCE_TYPES:
            issues.append(f"{row['id']} invalid evidence_type {row['evidence_type']}")
        if row["confidence"] not in VALID_CONFIDENCE:
            issues.append(f"{row['id']} invalid confidence {row['confidence']}")
        original_claim = " ".join(str((original_by_id[row["id"]].get("claim") or original_by_id[row["id"]].get("summary") or "")).split())
        if row["claim"] != original_claim:
            issues.append(f"{row['id']} claim mismatch")
    scope_counts = Counter(row["workflow_id"] for row in rows)
    return {
        "ok": not issues,
        "issues": issues,
        "count": len(rows),
        "atlas_global_count": scope_counts.get(ATLAS_GLOBAL, 0),
        "evidence_type_counts": Counter(row["evidence_type"] for row in rows),
        "confidence_counts": Counter(row["confidence"] for row in rows),
    }


def write_report(rows: list[dict[str, Any]], validation: dict[str, Any], mode: str) -> None:
    report = {
        "timestamp": utc_timestamp(),
        "mode": mode,
        "source_path": str(EVIDENCE_PATH),
        "preview_path": str(PREVIEW_OUT_PATH),
        "source_sha256": sha256_file(EVIDENCE_PATH),
        "source_count": len(load_jsonl(EVIDENCE_PATH)),
        "normalized_count": len(rows),
        "validation": {
            "ok": validation["ok"],
            "issue_count": len(validation["issues"]),
            "issues": validation["issues"],
            "atlas_global_count": validation["atlas_global_count"],
            "evidence_type_counts": dict(validation["evidence_type_counts"]),
            "confidence_counts": dict(validation["confidence_counts"]),
        },
    }
    dump_json(REPORT_PATH, report)


def preview_mode() -> int:
    rows = build_preview()
    original_rows = load_jsonl(EVIDENCE_PATH)
    validation = validate_rows(rows, original_rows)
    dump_jsonl(PREVIEW_OUT_PATH, rows)
    write_report(rows, validation, "preview")
    print(json.dumps({"preview_path": str(PREVIEW_OUT_PATH), "report_path": str(REPORT_PATH), "ok": validation["ok"], "issues": validation["issues"]}, ensure_ascii=False, indent=2))
    return 0 if validation["ok"] else 1


def apply_mode() -> int:
    rows = build_preview()
    original_rows = load_jsonl(EVIDENCE_PATH)
    validation = validate_rows(rows, original_rows)
    dump_jsonl(PREVIEW_OUT_PATH, rows)
    write_report(rows, validation, "apply-preflight")
    if not validation["ok"]:
        print(json.dumps({"ok": False, "issues": validation["issues"]}, ensure_ascii=False, indent=2))
        return 1

    ensure_dir(RAW_DIR / "backups")
    backup_path = RAW_DIR / "backups" / f"WORKFLOW_EVIDENCE.{utc_timestamp().replace(':', '').replace('-', '')}.jsonl"
    shutil.copy2(EVIDENCE_PATH, backup_path)
    temp_path = EVIDENCE_PATH.with_suffix(".jsonl.tmp")
    dump_jsonl(temp_path, rows)
    temp_path.replace(EVIDENCE_PATH)
    write_report(rows, validation, "apply")
    print(json.dumps({"ok": True, "backup_path": str(backup_path), "applied_sha256": sha256_file(EVIDENCE_PATH)}, ensure_ascii=False, indent=2))
    return 0


def verify_mode() -> int:
    rows = load_jsonl(EVIDENCE_PATH)
    original_rows = load_jsonl(PREVIEW_OUT_PATH if PREVIEW_OUT_PATH.exists() else EVIDENCE_PATH)
    validation = validate_rows(rows, original_rows)
    write_report(rows, validation, "verify")
    print(json.dumps({"ok": validation["ok"], "issues": validation["issues"], "sha256": sha256_file(EVIDENCE_PATH)}, ensure_ascii=False, indent=2))
    return 0 if validation["ok"] else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    selected = sum(int(flag) for flag in (args.preview, args.apply, args.verify))
    if selected != 1:
        parser.error("choose exactly one of --preview, --apply, --verify")
    if args.preview:
        return preview_mode()
    if args.apply:
        return apply_mode()
    return verify_mode()


if __name__ == "__main__":
    raise SystemExit(main())
