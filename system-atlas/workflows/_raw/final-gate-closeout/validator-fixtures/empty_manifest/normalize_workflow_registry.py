from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from workflow_tools_common import (
    RAW_DIR,
    WORKFLOWS_DIR,
    dump_json,
    dump_yaml,
    ensure_dir,
    load_jsonl,
    load_yaml,
    sha256_file,
    utc_timestamp,
)


REGISTRY_PATH = WORKFLOWS_DIR / "WORKFLOW_REGISTRY.yaml"
EVIDENCE_PATH = WORKFLOWS_DIR / "WORKFLOW_EVIDENCE.jsonl"
EVIDENCE_PREVIEW_PATH = RAW_DIR / "n1_full_normalized_preview.jsonl"
PLAN_PATH = RAW_DIR / "subagents" / "registry" / "registry_normalization_plan.yaml"
PREVIEW_PATH = RAW_DIR / "registry_normalized_preview.yaml"
REPORT_PATH = RAW_DIR / "registry_normalization_report.json"

PATH_STATUSES = [
    "LIVE_PATH",
    "CONDITIONAL_PATH",
    "DORMANT_PATH",
    "LEGACY_PATH",
    "DEAD_PATH",
    "FALLBACK_PATH",
]
CONTRACT_STATUSES = [
    "BROKEN_CALL",
    "MISSING_PRODUCER",
    "MISSING_CONSUMER",
    "MISSING_EXECUTOR",
]
RUNTIME_CLASSIFICATIONS = ["CONFIRMED", "UNVERIFIED"]
RUNTIME_EVIDENCE_SCOPES = [
    "FULL_WORKFLOW",
    "PARTIAL_WORKFLOW",
    "ENTRYPOINT_ONLY",
    "PATH_SELECTION_ONLY",
    "ENVIRONMENT_ONLY",
    "STATIC_ONLY",
]
RUNTIME_TRIGGER_MODES = ["AUTOMATIC", "MANUAL_ONLY", "MIXED"]
TEST_STATUSES = [
    "NO_DIRECT_TEST_FOUND",
    "SYNTHETIC_ONLY",
    "PROOF_ONLY",
    "UNIT_COVERED",
    "INTEGRATION_COVERED",
    "END_TO_END_COVERED",
    "CHAOS_COVERED",
]

WORKFLOW_OVERRIDES: dict[str, dict[str, str]] = {
    "FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH": {
        "trigger_mode": "AUTOMATIC",
        "evidence_scope": "STATIC_ONLY",
    },
    "KALK-TOP-CALCULATE-OFFER-PIPELINE": {
        "trigger_mode": "AUTOMATIC",
        "evidence_scope": "STATIC_ONLY",
    },
    "TOP-INSTAL-GENERATOR-OFFER-DOCUMENT": {
        "trigger_mode": "AUTOMATIC",
        "evidence_scope": "STATIC_ONLY",
    },
    "CIEPLO-ORCHESTRATOR-INTAKE-TO-REVIEW-EMAIL": {
        "trigger_mode": "MANUAL_ONLY",
        "evidence_scope": "STATIC_ONLY",
    },
    "LEARNING-LOOP-DIVERGENCE-TO-CANDIDATE-EVIDENCE-ONLY": {
        "trigger_mode": "AUTOMATIC",
        "evidence_scope": "STATIC_ONLY",
    },
    "GMAIL-SIGNAL-WORKER-LOOP": {
        "trigger_mode": "AUTOMATIC",
        "evidence_scope": "ENTRYPOINT_ONLY",
    },
    "GMAIL-RECONCILE-MODE-DISPATCH": {
        "trigger_mode": "AUTOMATIC",
        "evidence_scope": "PATH_SELECTION_ONLY",
    },
    "CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF": {
        "trigger_mode": "AUTOMATIC",
        "evidence_scope": "PARTIAL_WORKFLOW",
    },
    "AGENT-GRAPH-EXECUTE-RUN": {
        "trigger_mode": "AUTOMATIC",
        "evidence_scope": "PARTIAL_WORKFLOW",
    },
    "AGENT-GRAPH-TURN-LOOP": {
        "trigger_mode": "AUTOMATIC",
        "evidence_scope": "PARTIAL_WORKFLOW",
    },
    "HITL-PROPOSAL-APPROVAL-DUAL-PATH": {
        "trigger_mode": "MANUAL_ONLY",
        "evidence_scope": "ENTRYPOINT_ONLY",
    },
    "CASE-SCOPED-RAG-VS-GLOBAL-RAG-GAP": {
        "trigger_mode": "AUTOMATIC",
        "evidence_scope": "ENVIRONMENT_ONLY",
    },
    "CALENDAR-TWO-WORLDS-OF-VISITS": {
        "trigger_mode": "MIXED",
        "evidence_scope": "STATIC_ONLY",
    },
    "DASZEK-COMMAND-OUTBOX-DRAIN": {
        "trigger_mode": "AUTOMATIC",
        "evidence_scope": "STATIC_ONLY",
    },
    "DASZEK-FEED-PUSH-NO-RETRY": {
        "trigger_mode": "MANUAL_ONLY",
        "evidence_scope": "PARTIAL_WORKFLOW",
    },
    "RAG-CHAT-ASYSTENT-QUERY-AND-INGEST-PIPELINE": {
        "trigger_mode": "AUTOMATIC",
        "evidence_scope": "STATIC_ONLY",
    },
    "SLA-WATCHER-DECISION-ESCALATION": {
        "trigger_mode": "MANUAL_ONLY",
        "evidence_scope": "STATIC_ONLY",
    },
}


def load_subagent_plan() -> dict[str, Any]:
    if not PLAN_PATH.exists():
        return {}
    return load_yaml(PLAN_PATH)


def load_evidence_rows() -> list[dict[str, Any]]:
    rows = load_jsonl(EVIDENCE_PATH)
    if rows and "workflow_id" not in rows[0]:
        if not EVIDENCE_PREVIEW_PATH.exists():
            raise RuntimeError("normalized evidence preview missing; run normalize_workflow_evidence.py --preview first")
        return load_jsonl(EVIDENCE_PREVIEW_PATH)
    return rows


def load_evidence_index() -> tuple[dict[str, dict[str, Any]], dict[str, list[str]], dict[str, list[str]]]:
    rows = load_evidence_rows()
    by_id = {row["id"]: row for row in rows}
    primary: dict[str, list[str]] = defaultdict(list)
    related: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        workflow_id = row["workflow_id"]
        if workflow_id and workflow_id != "ATLAS-GLOBAL":
            primary[workflow_id].append(row["id"])
        for related_id in row.get("related_workflow_ids", []):
            related[related_id].append(row["id"])
    return by_id, primary, related


def extract_statuses(old_status: list[str]) -> tuple[list[str], list[str]]:
    path_statuses = [status for status in old_status if status in PATH_STATUSES]
    contract_statuses = [status for status in old_status if status in CONTRACT_STATUSES]
    if not path_statuses:
        path_statuses = ["LIVE_PATH"]
    return list(dict.fromkeys(path_statuses)), list(dict.fromkeys(contract_statuses))


def runtime_classification(old_status: list[str], runtime_note: str | None) -> str:
    if "RUNTIME_CONFIRMED" in old_status:
        return "CONFIRMED"
    if runtime_note and "RUNTIME_CONFIRMED" in runtime_note:
        return "CONFIRMED"
    return "UNVERIFIED"


def runtime_trigger_mode(workflow_id: str, old_status: list[str], entrypoints: list[str]) -> str:
    override = WORKFLOW_OVERRIDES.get(workflow_id, {}).get("trigger_mode")
    if override:
        return override
    if "MANUAL_TRIGGER_ONLY" in old_status:
        return "MANUAL_ONLY"
    joined = " ".join(entrypoints).lower()
    if "manual" in joined or "operator-triggered" in joined:
        return "MANUAL_ONLY"
    if "cli" in joined and "post " not in joined:
        return "MANUAL_ONLY"
    return "AUTOMATIC"


def runtime_evidence_scope(workflow_id: str, classification: str, runtime_note: str | None) -> str:
    override = WORKFLOW_OVERRIDES.get(workflow_id, {}).get("evidence_scope")
    if override:
        return override
    if classification == "UNVERIFIED":
        return "STATIC_ONLY"
    note = (runtime_note or "").lower()
    if "container up" in note or "stack" in note or "healthy" in note:
        return "ENVIRONMENT_ONLY"
    if "route it's called from is live" in note or "route it is called from is live" in note:
        return "PARTIAL_WORKFLOW"
    if "mode=prep" in note or "selects the agent-runtime branch" in note:
        return "PATH_SELECTION_ONLY"
    if "worker command only" in note or "reachability" in note:
        return "ENTRYPOINT_ONLY"
    return "PARTIAL_WORKFLOW"


def evidence_by_type(evidence_by_id: dict[str, dict[str, Any]], all_ids: list[str]) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {
        "code_evidence_ids": [],
        "config_evidence_ids": [],
        "runtime_evidence_ids": [],
        "test_evidence_ids": [],
        "graph_evidence_ids": [],
        "absence_search_evidence_ids": [],
        "synthesis_evidence_ids": [],
    }
    mapping = {
        "CODE": "code_evidence_ids",
        "CONFIG": "config_evidence_ids",
        "RUNTIME": "runtime_evidence_ids",
        "TEST": "test_evidence_ids",
        "GRAPH": "graph_evidence_ids",
        "ABSENCE_SEARCH": "absence_search_evidence_ids",
        "SYNTHESIS": "synthesis_evidence_ids",
    }
    for evidence_id in all_ids:
        evidence = evidence_by_id.get(evidence_id)
        if evidence is None:
            continue
        buckets[mapping[evidence["evidence_type"]]].append(evidence_id)
    return buckets


def build_workflow_test_status(current: dict[str, Any], workflow_ids: list[str]) -> dict[str, Any]:
    current_status = current.get("workflow_test_status", {})
    normalized: dict[str, Any] = {}
    for workflow_id in workflow_ids:
        node = current_status.get(workflow_id) or {}
        statuses = list(dict.fromkeys(node.get("statuses", [])))
        if not statuses:
            statuses = ["NO_DIRECT_TEST_FOUND"]
        normalized[workflow_id] = {
            "statuses": statuses,
            "evidence_ids": list(dict.fromkeys(node.get("evidence_ids", []))),
        }
    return normalized


def infer_recovery(retry_text: str) -> str:
    lowered = (retry_text or "").lower()
    if any(token in lowered for token in ("retry", "replay", "re-drive", "manual")):
        return retry_text
    if "none" in lowered or "n/a" in lowered:
        return "none found"
    return retry_text or "none found"


def clean_runtime_note(runtime_note: str | None) -> str:
    if runtime_note is None:
        return "not_proven"
    return runtime_note.strip()


def build_preview() -> dict[str, Any]:
    current = load_yaml(REGISTRY_PATH)
    _plan = load_subagent_plan()
    evidence_by_id, primary_ids, related_ids = load_evidence_index()
    workflow_test_status = build_workflow_test_status(
        current, [workflow["workflow_id"] for workflow in current["workflows"]]
    )

    normalized_workflows: list[dict[str, Any]] = []
    for workflow in current["workflows"]:
        workflow_id = workflow["workflow_id"]
        old_status = list(workflow.get("status", []))
        path_statuses, contract_statuses = extract_statuses(old_status)
        primary_evidence = list(dict.fromkeys(primary_ids.get(workflow_id, [])))
        related_evidence = list(dict.fromkeys(related_ids.get(workflow_id, [])))
        all_evidence = list(dict.fromkeys(workflow.get("evidence_ids", []) + primary_evidence + related_evidence))
        evidence_sets = evidence_by_type(evidence_by_id, all_evidence)
        classification = runtime_classification(old_status, workflow.get("runtime"))
        trigger_mode = runtime_trigger_mode(workflow_id, old_status, workflow.get("entrypoints", []))
        evidence_scope = runtime_evidence_scope(workflow_id, classification, workflow.get("runtime"))

        normalized: dict[str, Any] = {
            "workflow_id": workflow_id,
            "domain": workflow.get("domain", "unknown"),
            "owner": workflow.get("owner", "unknown"),
            "path_statuses": path_statuses,
            "entrypoints": workflow.get("entrypoints", []),
            "evidence_ids": all_evidence,
            "runtime": {
                "classification": classification,
                "evidence_scope": evidence_scope,
                "trigger_mode": trigger_mode,
                "note": clean_runtime_note(workflow.get("runtime")),
            },
            **evidence_sets,
        }

        if evidence_sets["runtime_evidence_ids"]:
            normalized["runtime"]["evidence_ids"] = evidence_sets["runtime_evidence_ids"]
        if contract_statuses:
            normalized["contract_statuses"] = contract_statuses
        if workflow.get("participating_repos"):
            normalized["participating_repos"] = workflow["participating_repos"]
        if workflow.get("uses"):
            normalized["uses"] = workflow["uses"]
        if workflow.get("steps"):
            normalized["steps"] = workflow["steps"]
        if workflow.get("state_reads"):
            normalized["state_reads"] = workflow["state_reads"]
        if workflow.get("state_writes"):
            normalized["state_writes"] = workflow["state_writes"]
        if workflow.get("external_calls"):
            normalized["external_calls"] = workflow["external_calls"]
        if workflow.get("side_effect"):
            normalized["side_effect"] = workflow["side_effect"]
        if workflow.get("policy"):
            normalized["policy"] = workflow["policy"]
        if workflow.get("approval"):
            normalized["approval"] = workflow["approval"]
        if workflow.get("terminal"):
            normalized["terminal"] = workflow["terminal"]
        if workflow.get("retry"):
            normalized["retry"] = workflow["retry"]
        normalized["recovery"] = infer_recovery(workflow.get("retry", ""))
        if workflow.get("consumers"):
            normalized["consumers"] = workflow["consumers"]
        normalized["primary_evidence_ids"] = primary_evidence
        normalized["related_evidence_ids"] = related_evidence
        if workflow.get("gaps"):
            normalized["gaps"] = workflow["gaps"]

        normalized_workflows.append(normalized)

    preview = {
        "schema_version": 2,
        "generated_at": utc_timestamp(),
        "evidence_scopes": [
            {
                "scope_id": "ATLAS-GLOBAL",
                "scope_type": "CROSS_WORKFLOW",
                "description": "Evidence concerning the whole atlas or multiple independent workflows.",
            }
        ],
        "status_taxonomy": {
            "path_statuses": PATH_STATUSES,
            "contract_statuses": CONTRACT_STATUSES,
            "runtime_classification": RUNTIME_CLASSIFICATIONS,
            "runtime_evidence_scope": RUNTIME_EVIDENCE_SCOPES,
            "runtime_trigger_mode": RUNTIME_TRIGGER_MODES,
            "workflow_test_statuses": TEST_STATUSES,
        },
        "subflows": current.get("subflows", {}),
        "workflows": normalized_workflows,
        "workflow_test_status": workflow_test_status,
    }
    return preview


def validate_preview(preview: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    workflows = preview.get("workflows", [])
    workflow_ids = [workflow.get("workflow_id") for workflow in workflows]
    workflow_test_status = preview.get("workflow_test_status", {})

    if len(workflows) != 17:
        issues.append(f"expected 17 workflows, got {len(workflows)}")
    if set(workflow_test_status) != set(workflow_ids):
        issues.append("workflow_test_status keys do not match workflows")

    for workflow in workflows:
        for key in (
            "workflow_id",
            "domain",
            "owner",
            "path_statuses",
            "entrypoints",
            "evidence_ids",
            "runtime",
            "code_evidence_ids",
            "config_evidence_ids",
            "runtime_evidence_ids",
            "test_evidence_ids",
            "graph_evidence_ids",
            "absence_search_evidence_ids",
            "synthesis_evidence_ids",
            "primary_evidence_ids",
            "related_evidence_ids",
        ):
            if key not in workflow:
                issues.append(f"{workflow.get('workflow_id', 'UNKNOWN')} missing {key}")
        if "confidence" in workflow:
            issues.append(f"{workflow['workflow_id']} contains forbidden workflow-level confidence")
        if not workflow.get("steps") and not workflow.get("uses"):
            issues.append(f"{workflow['workflow_id']} missing both steps and uses")
        for status in workflow.get("path_statuses", []):
            if status not in PATH_STATUSES:
                issues.append(f"{workflow['workflow_id']} invalid path status {status}")
        for status in workflow.get("contract_statuses", []):
            if status not in CONTRACT_STATUSES:
                issues.append(f"{workflow['workflow_id']} invalid contract status {status}")
        runtime = workflow.get("runtime", {})
        if runtime.get("classification") not in RUNTIME_CLASSIFICATIONS:
            issues.append(f"{workflow['workflow_id']} invalid runtime classification")
        if runtime.get("evidence_scope") not in RUNTIME_EVIDENCE_SCOPES:
            issues.append(f"{workflow['workflow_id']} invalid runtime evidence_scope")
        if runtime.get("trigger_mode") not in RUNTIME_TRIGGER_MODES:
            issues.append(f"{workflow['workflow_id']} invalid runtime trigger_mode")
        if "confidence" in runtime:
            issues.append(f"{workflow['workflow_id']} runtime contains forbidden confidence")

    for workflow_id, node in workflow_test_status.items():
        if "statuses" not in node or "evidence_ids" not in node:
            issues.append(f"workflow_test_status missing fields for {workflow_id}")
            continue
        for status in node["statuses"]:
            if status not in TEST_STATUSES:
                issues.append(f"{workflow_id} invalid test status {status}")
        if "confidence" in node:
            issues.append(f"{workflow_id} workflow_test_status contains forbidden confidence")

    return {
        "ok": not issues,
        "issues": issues,
        "workflow_count": len(workflows),
        "path_status_counts": Counter(
            status for workflow in workflows for status in workflow.get("path_statuses", [])
        ),
        "contract_status_counts": Counter(
            status for workflow in workflows for status in workflow.get("contract_statuses", [])
        ),
        "runtime_classification_counts": Counter(
            workflow.get("runtime", {}).get("classification", "UNKNOWN") for workflow in workflows
        ),
    }


def write_report(preview: dict[str, Any], validation: dict[str, Any], mode: str) -> None:
    report = {
        "timestamp": utc_timestamp(),
        "mode": mode,
        "source_sha256": sha256_file(REGISTRY_PATH),
        "plan_path": str(PLAN_PATH),
        "plan_present": PLAN_PATH.exists(),
        "preview_path": str(PREVIEW_PATH),
        "workflow_count": len(preview["workflows"]),
        "validation": {
            "ok": validation["ok"],
            "issues": validation["issues"],
            "path_status_counts": dict(validation["path_status_counts"]),
            "contract_status_counts": dict(validation["contract_status_counts"]),
            "runtime_classification_counts": dict(validation["runtime_classification_counts"]),
        },
    }
    dump_json(REPORT_PATH, report)


def preview_mode() -> int:
    preview = build_preview()
    validation = validate_preview(preview)
    dump_yaml(PREVIEW_PATH, preview)
    write_report(preview, validation, "preview")
    print(
        json.dumps(
            {"ok": validation["ok"], "issues": validation["issues"], "preview_path": str(PREVIEW_PATH)},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if validation["ok"] else 1


def apply_mode() -> int:
    preview = build_preview()
    validation = validate_preview(preview)
    dump_yaml(PREVIEW_PATH, preview)
    write_report(preview, validation, "apply-preflight")
    if not validation["ok"]:
        return 1
    ensure_dir(RAW_DIR / "backups")
    backup = RAW_DIR / "backups" / f"WORKFLOW_REGISTRY.{utc_timestamp().replace(':', '').replace('-', '')}.yaml"
    shutil.copy2(REGISTRY_PATH, backup)
    temp_path = REGISTRY_PATH.with_suffix(".yaml.tmp")
    dump_yaml(temp_path, preview)
    temp_path.replace(REGISTRY_PATH)
    write_report(preview, validation, "apply")
    print(json.dumps({"ok": True, "backup_path": str(backup), "sha256": sha256_file(REGISTRY_PATH)}, ensure_ascii=False, indent=2))
    return 0


def verify_mode() -> int:
    preview = load_yaml(REGISTRY_PATH)
    validation = validate_preview(preview)
    write_report(preview, validation, "verify")
    print(json.dumps({"ok": validation["ok"], "issues": validation["issues"], "sha256": sha256_file(REGISTRY_PATH)}, ensure_ascii=False, indent=2))
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
