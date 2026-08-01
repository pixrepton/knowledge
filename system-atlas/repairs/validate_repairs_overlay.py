from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
WORKFLOWS = ROOT.parent / "workflows"

REQUIRED_FILES = [
    "README.md",
    "EARLY_DECISION_QUEUE.md",
    "GAP_DISPOSITIONS.yaml",
    "REPAIR_DAG.yaml",
    "REPAIR_PROGRAM_PLAN.md",
    "REPAIR_PROGRAM_SUPERPLAN.md",
    "REPAIR_REGISTRY.yaml",
    "ROOT_CAUSE_CLUSTERS.yaml",
    "WAVE_02_PROBLEM_ANALYSIS.md",
    "WAVE_02_IMPLEMENTATION_PLAN.md",
]

WAVE2_PACKAGES = {"RP-01", "RP-06", "RP-07", "RP-12", "RP-14", "RP-15", "RP-20"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def collect_ids(pattern: str, text: str) -> set[str]:
    return set(re.findall(pattern, text))


def main() -> int:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    errors: list[str] = []
    infos: list[str] = []

    for name in REQUIRED_FILES:
        if not (ROOT / name).exists():
            errors.append(f"missing required file: {name}")

    if errors:
        write_report(timestamp, errors, infos, None, None)
        return 1

    gap_dispositions = load_yaml(ROOT / "GAP_DISPOSITIONS.yaml")
    root_cause_clusters = load_yaml(ROOT / "ROOT_CAUSE_CLUSTERS.yaml")
    repair_registry = load_yaml(ROOT / "REPAIR_REGISTRY.yaml")

    gap_ids = {item["gap_id"] for item in gap_dispositions["gap_dispositions"]}
    cluster_ids = {item["cluster_id"] for item in root_cause_clusters["clusters"]}

    for item in gap_dispositions["gap_dispositions"]:
        cluster = item["root_cause_cluster"]
        if cluster not in cluster_ids:
            errors.append(f"gap {item['gap_id']} points to missing cluster {cluster}")

    for cluster in root_cause_clusters["clusters"]:
        for gap_id in cluster["targets_gaps"]:
            if gap_id not in gap_ids:
                errors.append(f"cluster {cluster['cluster_id']} points to missing gap {gap_id}")

    dq_text = read_text(ROOT / "EARLY_DECISION_QUEUE.md")
    dq_ids = collect_ids(r"DQ-\d{2}", dq_text)
    if not dq_ids:
        errors.append("no DQ ids found in EARLY_DECISION_QUEUE.md")

    referenced_dqs: set[str] = set()
    for item in gap_dispositions["gap_dispositions"]:
        if item.get("early_decision"):
            referenced_dqs.add(item["early_decision"])
    for cluster in root_cause_clusters["clusters"]:
        referenced_dqs.update(cluster.get("early_decisions", []))
    referenced_dqs.update(collect_ids(r"DQ-\d{2}", read_text(ROOT / "WAVE_02_IMPLEMENTATION_PLAN.md")))
    referenced_dqs.update(collect_ids(r"DQ-\d{2}", read_text(ROOT / "WAVE_02_PROBLEM_ANALYSIS.md")))

    for dq_id in sorted(referenced_dqs):
        if dq_id not in dq_ids:
            errors.append(f"referenced decision does not exist in EARLY_DECISION_QUEUE.md: {dq_id}")

    superplan_rps = collect_ids(r"RP-\d{2}", read_text(ROOT / "REPAIR_PROGRAM_SUPERPLAN.md"))
    registry_rps = {item["repair_id"] for item in repair_registry["repairs"]}
    for rp_id in sorted(WAVE2_PACKAGES):
        if rp_id not in superplan_rps:
            errors.append(f"Wave 2 package missing from superplan: {rp_id}")
        infos.append(
            f"Wave 2 package {rp_id}: present in superplan={'yes' if rp_id in superplan_rps else 'no'}, "
            f"present in repair registry={'yes' if rp_id in registry_rps else 'no'}"
        )

    readme_text = read_text(ROOT / "README.md")
    for filename in collect_ids(r"`([A-Za-z0-9_./-]+\.(?:md|yaml|py))`", readme_text):
        path = ROOT / filename
        if not path.exists():
            errors.append(f"README references missing file: {filename}")

    workflow_registry_path = WORKFLOWS / "WORKFLOW_REGISTRY.yaml"
    workflow_manifest_path = WORKFLOWS / "FINAL_MANIFEST.json"
    workflow_validation = subprocess.run(
        [sys.executable, "validate_workflow_atlas.py", "--final", "--manifest", "FINAL_MANIFEST.json"],
        cwd=WORKFLOWS,
        capture_output=True,
        text=True,
    )
    workflow_result = {
        "exit_code": workflow_validation.returncode,
        "stdout": workflow_validation.stdout.strip(),
        "stderr": workflow_validation.stderr.strip(),
    }
    if workflow_validation.returncode != 0:
        errors.append("Workflow Registry v1 final validator failed")

    workflow_hashes = {
        "WORKFLOW_REGISTRY.yaml": sha256(workflow_registry_path),
        "FINAL_MANIFEST.json": sha256(workflow_manifest_path),
    }

    write_report(timestamp, errors, infos, workflow_result, workflow_hashes)
    return 1 if errors else 0


def write_report(
    timestamp: str,
    errors: list[str],
    infos: list[str],
    workflow_result: dict | None,
    workflow_hashes: dict | None,
) -> None:
    status = "PASS" if not errors else "FAIL"
    report_lines = [
        "# EXECUTION_MODEL_VALIDATION.md",
        "",
        f"Timestamp UTC: `{timestamp}`",
        f"Result: `{status}`",
        "",
        "## Checks",
        "",
        "- required repairs files exist",
        "- YAML parse for gap dispositions, root-cause clusters and repair registry",
        "- cluster to gap references are valid",
        "- gap to cluster references are valid",
        "- all referenced `DQ-*` ids exist in `EARLY_DECISION_QUEUE.md`",
        "- Wave 2 package ids exist in the superplan",
        "- README file references resolve",
        "- Workflow Registry v1 final validator still passes",
        "",
        "## Findings",
        "",
    ]

    if errors:
        report_lines.extend([f"- FAIL: {item}" for item in errors])
    else:
        report_lines.append("- PASS: all overlay consistency checks passed")

    if infos:
        report_lines.extend(["", "## Notes", ""])
        report_lines.extend([f"- {item}" for item in infos])

    if workflow_hashes:
        report_lines.extend(["", "## Workflow Registry v1 hashes", ""])
        for name, digest in workflow_hashes.items():
            report_lines.append(f"- `{name}`: `{digest}`")

    if workflow_result is not None:
        report_lines.extend(["", "## Workflow validator result", ""])
        report_lines.append(f"- exit code: `{workflow_result['exit_code']}`")
        if workflow_result["stdout"]:
            report_lines.append("")
            report_lines.append("```text")
            report_lines.append(workflow_result["stdout"])
            report_lines.append("```")
        if workflow_result["stderr"]:
            report_lines.append("")
            report_lines.append("```text")
            report_lines.append(workflow_result["stderr"])
            report_lines.append("```")

    (ROOT / "EXECUTION_MODEL_VALIDATION.md").write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
