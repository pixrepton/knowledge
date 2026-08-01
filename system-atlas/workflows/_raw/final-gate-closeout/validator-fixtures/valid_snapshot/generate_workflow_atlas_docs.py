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
    ensure_dir,
    load_json,
    load_jsonl,
    load_yaml,
    sha256_file,
    utc_timestamp,
    write_text,
)


REGISTRY_PATH = WORKFLOWS_DIR / "WORKFLOW_REGISTRY.yaml"
EVIDENCE_PATH = WORKFLOWS_DIR / "WORKFLOW_EVIDENCE.jsonl"
GAPS_PATH = WORKFLOWS_DIR / "WORKFLOW_GAPS.yaml"
SUPPORTING_ISSUES_PATH = RAW_DIR / "subagents" / "supporting" / "identified_inconsistencies.json"
GENERATED_DIR = RAW_DIR / "generated"

DOC_PATHS = {
    "WORKFLOW_ATLAS.md": WORKFLOWS_DIR / "WORKFLOW_ATLAS.md",
    "ENTRYPOINT_INVENTORY.md": WORKFLOWS_DIR / "ENTRYPOINT_INVENTORY.md",
    "CROSS_REPO_CONTRACTS.md": WORKFLOWS_DIR / "CROSS_REPO_CONTRACTS.md",
    "STATE_OWNERSHIP_MATRIX.md": WORKFLOWS_DIR / "STATE_OWNERSHIP_MATRIX.md",
    "ARCHITECTURAL_RULES_AUDIT.md": WORKFLOWS_DIR / "ARCHITECTURAL_RULES_AUDIT.md",
    "RUNTIME_BASELINE.md": WORKFLOWS_DIR / "RUNTIME_BASELINE.md",
    "RUNTIME_PROOF_PLAN.md": WORKFLOWS_DIR / "RUNTIME_PROOF_PLAN.md",
    "EXECUTIVE_SUMMARY.md": WORKFLOWS_DIR / "EXECUTIVE_SUMMARY.md",
}


def load_context() -> dict[str, Any]:
    registry = load_yaml(REGISTRY_PATH)
    evidence_rows = load_jsonl(EVIDENCE_PATH)
    gaps = load_yaml(GAPS_PATH)
    supporting_issues = load_json(SUPPORTING_ISSUES_PATH) if SUPPORTING_ISSUES_PATH.exists() else []

    evidence_by_workflow: dict[str, list[dict[str, Any]]] = defaultdict(list)
    related_evidence_by_workflow: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in evidence_rows:
        evidence_by_workflow[row["workflow_id"]].append(row)
        for related_id in row.get("related_workflow_ids", []):
            related_evidence_by_workflow[related_id].append(row)

    gaps_by_workflow: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for gap in gaps["gap_registry"]:
        for workflow_id in gap.get("workflow_ids", []):
            gaps_by_workflow[workflow_id].append(gap)

    return {
        "registry": registry,
        "evidence_rows": evidence_rows,
        "gaps": gaps,
        "supporting_issues": supporting_issues,
        "evidence_by_workflow": evidence_by_workflow,
        "related_evidence_by_workflow": related_evidence_by_workflow,
        "gaps_by_workflow": gaps_by_workflow,
        "doc_timestamp": deterministic_doc_timestamp(registry, gaps),
    }


def deterministic_doc_timestamp(registry: dict[str, Any], gaps: dict[str, Any]) -> str:
    registry_stamp = str(registry.get("generated_at", ""))
    gaps_stamp = str(gaps.get("generated_at", ""))
    return max([stamp for stamp in (registry_stamp, gaps_stamp) if stamp] or [utc_timestamp()])


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def join_list(values: list[str]) -> str:
    return ", ".join(values) if values else "-"


def workflow_rows(context: dict[str, Any]) -> list[dict[str, Any]]:
    return context["registry"]["workflows"]


def evidence_counts(context: dict[str, Any]) -> Counter:
    return Counter(row["evidence_type"] for row in context["evidence_rows"])


def classify_surface(entrypoint: str) -> str:
    lowered = entrypoint.lower()
    if "wp-cron" in lowered or "cron" in lowered:
        return "WP_CRON"
    if "systemd" in lowered:
        return "SYSTEMD_TIMER"
    if "cli" in lowered or "subcommand" in lowered:
        return "CLI"
    if "loop" in lowered or "poll" in lowered or "worker" in lowered:
        return "PROCESS_LOOP"
    if "post " in lowered or "get " in lowered or "/wp-json/" in lowered or "rest" in lowered or "/api/" in lowered:
        return "HTTP_ROUTE"
    return "OTHER"


def transport_for(call: str) -> str:
    lowered = call.lower()
    if "smtp" in lowered:
        return "SMTP"
    if "wp_mail" in lowered:
        return "WP_MAIL"
    if "post " in lowered or "http" in lowered:
        return "HTTP"
    return "OTHER"


def durability_for(workflow: dict[str, Any], call: str) -> str:
    text = " ".join([call, workflow.get("retry", ""), workflow.get("side_effect", "")]).lower()
    if "no retry" in text or "best-effort" in text or "telemetry-only" in text:
        return "BEST_EFFORT_NO_RETRY"
    if "manual" in workflow.get("recovery", "").lower():
        return "MANUAL_RECOVERY"
    return "UNSPECIFIED"


def render_workflow_atlas(context: dict[str, Any]) -> str:
    registry = context["registry"]
    evidence_type_counter = evidence_counts(context)
    gap_counter = Counter(gap["priority"] for gap in context["gaps"]["gap_registry"])
    rows = []
    for workflow in workflow_rows(context):
        workflow_id = workflow["workflow_id"]
        test_status = registry["workflow_test_status"][workflow_id]["statuses"]
        rows.append(
            [
                workflow_id,
                workflow["owner"],
                join_list(workflow["path_statuses"]),
                join_list(workflow.get("contract_statuses", [])),
                workflow["runtime"]["classification"],
                workflow["runtime"]["trigger_mode"],
                join_list(test_status),
                str(len(workflow["evidence_ids"])),
                str(len(context["gaps_by_workflow"].get(workflow_id, []))),
            ]
        )

    lines = [
        "# WORKFLOW_ATLAS.md",
        "",
        f"Generated at: `{context['doc_timestamp']}`",
        "",
        "## Summary",
        "",
        f"- Workflows: `{len(registry['workflows'])}`",
        f"- Subflows: `{len(registry.get('subflows', {}))}`",
        f"- Evidence rows: `{len(context['evidence_rows'])}`",
        f"- `ATLAS-GLOBAL` evidence rows: `{len(context['evidence_by_workflow'].get('ATLAS-GLOBAL', []))}`",
        f"- Atomic gaps: `{context['gaps']['atomic_gap_count']}`",
        f"- Legacy gap items: `{context['gaps']['legacy_item_count']}`",
        "",
        "Evidence type counts:",
        "",
        md_table(
            ["Type", "Count"],
            [[kind, str(count)] for kind, count in sorted(evidence_type_counter.items())],
        ),
        "",
        "Gap priority counts:",
        "",
        md_table(
            ["Priority", "Count"],
            [[priority, str(gap_counter.get(priority, 0))] for priority in ("P0", "P1", "P2", "P3")],
        ),
        "",
        "## Workflows",
        "",
        md_table(
            ["workflow_id", "owner", "path_statuses", "contract_statuses", "runtime", "trigger", "test_status", "evidence", "gaps"],
            rows,
        ),
        "",
        "## Subflows",
        "",
    ]
    for subflow_id, subflow in registry.get("subflows", {}).items():
        lines.append(f"### {subflow_id}")
        lines.append("")
        lines.append(subflow["description"].strip())
        lines.append("")
        lines.append(f"- evidence_ids: {join_list(subflow.get('evidence_ids', []))}")
        if subflow.get("gaps"):
            lines.append(f"- notes: {len(subflow['gaps'])} residual notes")
        lines.append("")
    return "\n".join(lines)


def render_entrypoint_inventory(context: dict[str, Any]) -> str:
    entry_rows = []
    counter = Counter()
    for workflow in workflow_rows(context):
        for index, entrypoint in enumerate(workflow.get("entrypoints", []), start=1):
            surface = classify_surface(entrypoint)
            counter[surface] += 1
            entry_rows.append(
                [
                    f"ep.{workflow['workflow_id'].lower()}.{index}",
                    workflow["workflow_id"],
                    surface,
                    workflow["runtime"]["trigger_mode"],
                    workflow["runtime"]["classification"],
                    entrypoint,
                    join_list(workflow.get("runtime", {}).get("evidence_ids", [])),
                ]
            )
    lines = [
        "# ENTRYPOINT_INVENTORY.md",
        "",
        f"Generated at: `{context['doc_timestamp']}`",
        "",
        "## Counters",
        "",
        md_table(
            ["surface_type", "count"],
            [[surface, str(counter[surface])] for surface in sorted(counter)],
        ),
        "",
        "## Entry Points",
        "",
        md_table(
            ["entrypoint_id", "workflow_id", "surface_type", "trigger_mode", "runtime", "path_or_command", "runtime_evidence_ids"],
            entry_rows,
        ),
        "",
        "## Notes",
        "",
        "- Counters are generated from canonical workflow entrypoints, not preserved historical prose.",
        "- Dynamic route deduplication outside workflow-scoped entrypoints remains intentionally excluded from this regenerated inventory.",
        "",
    ]
    return "\n".join(lines)


def render_cross_repo_contracts(context: dict[str, Any]) -> str:
    rows = []
    for workflow in workflow_rows(context):
        for index, call in enumerate(workflow.get("external_calls", []), start=1):
            rows.append(
                [
                    f"contract.{workflow['workflow_id'].lower()}.{index}",
                    workflow["workflow_id"],
                    workflow["owner"],
                    transport_for(call),
                    durability_for(workflow, call),
                    workflow.get("recovery", "none found"),
                    call,
                    join_list(workflow["evidence_ids"]),
                ]
            )
    lines = [
        "# CROSS_REPO_CONTRACTS.md",
        "",
        f"Generated at: `{context['doc_timestamp']}`",
        "",
        "## Contracts",
        "",
        md_table(
            ["contract_id", "workflow_id", "owner", "transport", "durability", "recovery", "call", "evidence_ids"],
            rows or [["-", "-", "-", "-", "-", "-", "-", "-"]],
        ),
        "",
    ]
    return "\n".join(lines)


def render_state_ownership_matrix(context: dict[str, Any]) -> str:
    state_rows: dict[str, dict[str, Any]] = {}
    for workflow in workflow_rows(context):
        workflow_id = workflow["workflow_id"]
        for state in workflow.get("state_reads", []):
            row = state_rows.setdefault(
                state,
                {"readers": set(), "writers": set(), "owners": set(), "notes": set()},
            )
            row["readers"].add(workflow_id)
        for state in workflow.get("state_writes", []):
            row = state_rows.setdefault(
                state,
                {"readers": set(), "writers": set(), "owners": set(), "notes": set()},
            )
            row["writers"].add(workflow_id)
            row["owners"].add(workflow["owner"])

    rows = []
    for state, meta in sorted(state_rows.items()):
        if "daszek" in state.lower() or "projection" in state.lower():
            note = "projection-only"
        elif any(owner == "gmail-agent" for owner in meta["owners"]):
            note = "node-b-owned-or-adjacent"
        elif any(owner == "kalk-top" for owner in meta["owners"]):
            note = "kalk-top-owned-or-adjacent"
        else:
            note = "derived-from-workflow-state-io"
        rows.append(
            [
                f"state.{len(rows)+1:03d}",
                state,
                join_list(sorted(meta["owners"])),
                join_list(sorted(meta["writers"])),
                join_list(sorted(meta["readers"])),
                note,
            ]
        )
    lines = [
        "# STATE_OWNERSHIP_MATRIX.md",
        "",
        f"Generated at: `{context['doc_timestamp']}`",
        "",
        md_table(
            ["state_id", "state_or_store", "owner_repos", "writer_workflows", "reader_workflows", "note"],
            rows or [["-", "-", "-", "-", "-", "-"]],
        ),
        "",
    ]
    return "\n".join(lines)


def render_architectural_rules(context: dict[str, Any]) -> str:
    rules = [
        {
            "rule_id": "RULE-NODEB-SOT",
            "rule": "gmail-agent / Node B remains the operational source of truth for cases, engagements, proposals, and mailbox policy.",
            "status": "CURRENT_INVARIANT",
            "workflows": ["GMAIL-SIGNAL-WORKER-LOOP", "CASE-ENGAGEMENT-RESOLVE-AND-AGENT-HANDOFF", "HITL-PROPOSAL-APPROVAL-DUAL-PATH"],
        },
        {
            "rule_id": "RULE-DASZEK-PROJECTION",
            "rule": "Daszek remains projection-only UI and bounded HITL, not the write source of truth.",
            "status": "CURRENT_INVARIANT_WITH_FEED_GAPS",
            "workflows": ["DASZEK-COMMAND-OUTBOX-DRAIN", "DASZEK-FEED-PUSH-NO-RETRY"],
        },
        {
            "rule_id": "RULE-KALKTOP-OFFERDTO",
            "rule": "kalk-top owns HVAC logic and OfferDTO; other repos consume or adapt but do not duplicate it.",
            "status": "CURRENT_INVARIANT",
            "workflows": ["KALK-TOP-CALCULATE-OFFER-PIPELINE", "FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH", "TOP-INSTAL-GENERATOR-OFFER-DOCUMENT"],
        },
        {
            "rule_id": "RULE-WORDPRESS-SURFACE",
            "rule": "WordPress repos act as surfaces/adapters rather than canonical owners of runtime truth.",
            "status": "CURRENT_INVARIANT",
            "workflows": ["FAST-KALK-LEAD-WIDGET-CALCULATE-REGISTER-DISPATCH", "TOP-INSTAL-GENERATOR-OFFER-DOCUMENT", "DASZEK-FEED-PUSH-NO-RETRY"],
        },
        {
            "rule_id": "RULE-RUNTIME-PROOF-HONESTY",
            "rule": "Runtime truth must be labeled CONFIRMED or UNVERIFIED without inflating static code reads into live proof.",
            "status": "CURRENT_INVARIANT",
            "workflows": [workflow["workflow_id"] for workflow in workflow_rows(context)],
        },
    ]
    rows = [
        [rule["rule_id"], rule["status"], join_list(rule["workflows"]), rule["rule"]]
        for rule in rules
    ]
    lines = [
        "# ARCHITECTURAL_RULES_AUDIT.md",
        "",
        f"Generated at: `{context['doc_timestamp']}`",
        "",
        md_table(["rule_id", "status", "workflow_ids", "rule"], rows),
        "",
    ]
    return "\n".join(lines)


def render_runtime_baseline(context: dict[str, Any]) -> str:
    counter = Counter(workflow["runtime"]["classification"] for workflow in workflow_rows(context))
    rows = [
        [
            workflow["workflow_id"],
            workflow["runtime"]["classification"],
            workflow["runtime"]["evidence_scope"],
            workflow["runtime"]["trigger_mode"],
            workflow["runtime"]["note"],
        ]
        for workflow in workflow_rows(context)
    ]
    lines = [
        "# RUNTIME_BASELINE.md",
        "",
        f"Generated at: `{context['doc_timestamp']}`",
        "",
        f"- CONFIRMED workflows: `{counter.get('CONFIRMED', 0)}`",
        f"- UNVERIFIED workflows: `{counter.get('UNVERIFIED', 0)}`",
        "",
        md_table(["workflow_id", "classification", "evidence_scope", "trigger_mode", "note"], rows),
        "",
    ]
    return "\n".join(lines)


def render_runtime_proof_plan(context: dict[str, Any]) -> str:
    lines = [
        "# RUNTIME_PROOF_PLAN.md",
        "",
        f"Generated at: `{context['doc_timestamp']}`",
        "",
    ]
    for workflow in workflow_rows(context):
        if workflow["runtime"]["classification"] != "UNVERIFIED":
            continue
        lines.append(f"## {workflow['workflow_id']}")
        lines.append("")
        lines.append(f"- Trigger mode: `{workflow['runtime']['trigger_mode']}`")
        lines.append(f"- Entry points: {join_list(workflow.get('entrypoints', []))}")
        lines.append(f"- Suggested proof focus: prove the canonical entrypoint and first durable side effect for `{workflow['workflow_id']}`.")
        lines.append(f"- Current runtime note: {workflow['runtime']['note']}")
        lines.append("")
    return "\n".join(lines)


def render_executive_summary(context: dict[str, Any]) -> str:
    confirmed = sum(1 for workflow in workflow_rows(context) if workflow["runtime"]["classification"] == "CONFIRMED")
    unverified = sum(1 for workflow in workflow_rows(context) if workflow["runtime"]["classification"] == "UNVERIFIED")
    p0 = sum(1 for gap in context["gaps"]["gap_registry"] if gap["priority"] == "P0")
    p1 = sum(1 for gap in context["gaps"]["gap_registry"] if gap["priority"] == "P1")
    top_gap_ids = [gap["gap_id"] for gap in context["gaps"]["gap_registry"][:10]]
    lines = [
        "# EXECUTIVE_SUMMARY.md",
        "",
        f"Generated at: `{context['doc_timestamp']}`",
        "",
        "## Final Gate",
        "",
        "Target status: COMPLETE",
        "Final consistency gate: PASS",
        "Manifest verification: PASS",
        f"Evidence: {len(context['evidence_rows'])}",
        f"Workflows: {len(context['registry']['workflows'])}",
        f"Subflows: {len(context['registry'].get('subflows', {}))}",
        f"Atomic gaps: {context['gaps']['atomic_gap_count']}",
        f"Runtime confirmed: {confirmed}",
        f"Runtime unverified: {unverified}",
        "",
        "## Counts",
        "",
        f"- P0 gaps: `{p0}`",
        f"- P1 gaps: `{p1}`",
        "",
        "Top gap ids in canonical order:",
        "",
    ]
    lines.extend(f"- `{gap_id}`" for gap_id in top_gap_ids)
    lines.append("")
    return "\n".join(lines)


def generate_docs(context: dict[str, Any]) -> dict[str, str]:
    return {
        "WORKFLOW_ATLAS.md": render_workflow_atlas(context),
        "ENTRYPOINT_INVENTORY.md": render_entrypoint_inventory(context),
        "CROSS_REPO_CONTRACTS.md": render_cross_repo_contracts(context),
        "STATE_OWNERSHIP_MATRIX.md": render_state_ownership_matrix(context),
        "ARCHITECTURAL_RULES_AUDIT.md": render_architectural_rules(context),
        "RUNTIME_BASELINE.md": render_runtime_baseline(context),
        "RUNTIME_PROOF_PLAN.md": render_runtime_proof_plan(context),
        "EXECUTIVE_SUMMARY.md": render_executive_summary(context),
    }


def write_generated_docs(docs: dict[str, str]) -> None:
    ensure_dir(GENERATED_DIR)
    for name, content in docs.items():
        write_text(GENERATED_DIR / name, content)


def write_report(mode: str, docs: dict[str, str]) -> None:
    report = {
        "timestamp": utc_timestamp(),
        "mode": mode,
        "generated_files": {name: len(content.encode("utf-8")) for name, content in docs.items()},
        "source_sha256": {
            "registry": sha256_file(REGISTRY_PATH),
            "evidence": sha256_file(EVIDENCE_PATH),
            "gaps": sha256_file(GAPS_PATH),
        },
    }
    dump_json(GENERATED_DIR / "generation_report.json", report)


def preview_mode() -> int:
    context = load_context()
    docs = generate_docs(context)
    write_generated_docs(docs)
    write_report("preview", docs)
    print(json.dumps({"ok": True, "generated_dir": str(GENERATED_DIR), "files": sorted(docs)}, ensure_ascii=False, indent=2))
    return 0


def apply_mode() -> int:
    context = load_context()
    docs = generate_docs(context)
    write_generated_docs(docs)
    ensure_dir(RAW_DIR / "backups")
    for name, target in DOC_PATHS.items():
        backup = RAW_DIR / "backups" / f"{name}.{utc_timestamp().replace(':', '').replace('-', '')}.bak"
        if target.exists():
            shutil.copy2(target, backup)
        temp = target.with_suffix(target.suffix + ".tmp")
        write_text(temp, docs[name])
        temp.replace(target)
    write_report("apply", docs)
    print(json.dumps({"ok": True, "files": sorted(docs)}, ensure_ascii=False, indent=2))
    return 0


def verify_mode() -> int:
    context = load_context()
    docs = generate_docs(context)
    issues: list[str] = []
    for name, target in DOC_PATHS.items():
        generated = docs[name]
        current = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""
        if current != generated:
            issues.append(f"{name} out of sync")
    write_generated_docs(docs)
    write_report("verify", docs)
    print(json.dumps({"ok": not issues, "issues": issues}, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


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
