from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

from workflow_tools_common import (
    RAW_DIR,
    WORKFLOWS_DIR,
    dump_json,
    dump_yaml,
    ensure_dir,
    load_yaml,
    read_text,
    sha256_file,
    utc_timestamp,
    write_text,
)


GAPS_MD_PATH = WORKFLOWS_DIR / "WORKFLOW_GAPS.md"
GAPS_YAML_PATH = WORKFLOWS_DIR / "WORKFLOW_GAPS.yaml"
PREVIEW_YAML_PATH = RAW_DIR / "gap_registry_preview.generated.yaml"
PREVIEW_MD_PATH = RAW_DIR / "gap_registry_preview.generated.md"
REPORT_PATH = RAW_DIR / "gap_registry_normalization_report.json"
SUBAGENT_PREVIEW_PATH = RAW_DIR / "subagents" / "gaps" / "gap_registry_preview.yaml"

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "UNCLASSIFIED": 4}


def slugify(text: str) -> str:
    lowered = text.lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    lowered = lowered.strip("-")
    return lowered[:72] or "gap"


def parse_legacy_items(text: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    current_priority = "UNCLASSIFIED"
    current_section = "UNCLASSIFIED"
    for line in text.splitlines():
        if line.startswith("## "):
            current_section = line[3:].strip()
            current_priority = next((code for code in PRIORITY_ORDER if current_section.startswith(code)), "UNCLASSIFIED")
            continue
        match = re.match(r"^(\d+)\.\s+(.*)$", line)
        if not match:
            continue
        legacy_number = int(match.group(1))
        title = match.group(2).strip()
        title = re.sub(r"^\*\*(.+?)\*\*$", r"\1", title)
        title = title.replace("**", "").strip()
        items.append(
            {
                "legacy_item_number": legacy_number,
                "legacy_section": current_section,
                "priority": current_priority,
                "title": title,
            }
        )
    return items


def build_fallback_preview() -> dict[str, Any]:
    legacy_items = parse_legacy_items(read_text(GAPS_MD_PATH))
    gap_registry: list[dict[str, Any]] = []
    for item in legacy_items:
        gap_id = f"gap.legacy.{item['legacy_item_number']:03d}.{slugify(item['title'])}"
        gap_registry.append(
            {
                "gap_id": gap_id,
                "legacy_items": [item["legacy_item_number"]],
                "priority": item["priority"],
                "workflow_ids": [],
                "evidence_ids": [],
                "producer": None,
                "consumer": None,
                "break_point": item["title"],
                "technical_impact": item["title"],
                "business_impact": None,
                "status": "legacy_unatomized",
            }
        )
    migration_map = [
        {
            "legacy_item_number": item["legacy_item_number"],
            "legacy_section": item["legacy_section"],
            "priority": item["priority"],
            "gap_ids": [f"gap.legacy.{item['legacy_item_number']:03d}.{slugify(item['title'])}"],
        }
        for item in legacy_items
    ]
    return {
        "schema_version": 2,
        "generated_at": utc_timestamp(),
        "legacy_item_count": len(legacy_items),
        "atomic_gap_count": len(gap_registry),
        "gap_registry": gap_registry,
        "migration_map": migration_map,
        "source": "fallback-parser",
    }


def load_subagent_preview() -> dict[str, Any] | None:
    if not SUBAGENT_PREVIEW_PATH.exists():
        return None
    raw = load_yaml(SUBAGENT_PREVIEW_PATH)
    if not raw or "atomic_gaps" not in raw:
        return None
    legacy_items = parse_legacy_items(read_text(GAPS_MD_PATH))
    legacy_by_number = {item["legacy_item_number"]: item for item in legacy_items}
    migration_index: dict[int, list[str]] = defaultdict(list)
    for entry in raw["atomic_gaps"]:
        for legacy_item in entry.get("legacy_items", []):
            migration_index[legacy_item].append(entry["gap_id"])
    migration_map = []
    for legacy_number in sorted(migration_index):
        meta = legacy_by_number.get(
            legacy_number,
            {"legacy_section": "UNKNOWN", "priority": "UNCLASSIFIED"},
        )
        migration_map.append(
            {
                "legacy_item_number": legacy_number,
                "legacy_section": meta["legacy_section"],
                "priority": meta["priority"],
                "gap_ids": migration_index[legacy_number],
            }
        )
    return {
        "schema_version": 2,
        "generated_at": raw.get("generated_at", utc_timestamp()),
        "legacy_item_count": raw.get("legacy_item_count", len(legacy_items)),
        "atomic_gap_count": raw.get("atomic_gap_count", len(raw["atomic_gaps"])),
        "gap_registry": raw["atomic_gaps"],
        "migration_map": migration_map,
        "source": "subagent-preview",
        "subagent_scope": raw.get("scope"),
        "repo_sha": raw.get("repo_sha"),
    }


def build_preview() -> dict[str, Any]:
    return load_subagent_preview() or build_fallback_preview()


def render_markdown(preview: dict[str, Any]) -> str:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in preview["gap_registry"]:
        grouped[entry["priority"]].append(entry)

    lines = [
        "# WORKFLOW_GAPS.md",
        "",
        f"Canonical atomic gap count: `{preview['atomic_gap_count']}`",
        f"Legacy item count: `{preview['legacy_item_count']}`",
        "",
    ]

    for priority, _sort_key in sorted(PRIORITY_ORDER.items(), key=lambda item: item[1]):
        items = sorted(grouped.get(priority, []), key=lambda item: item["gap_id"])
        if not items:
            continue
        lines.append(f"## {priority}")
        lines.append("")
        for index, item in enumerate(items, start=1):
            lines.append(f"{index}. **{item['gap_id']}**")
            lines.append(f"    `status`: `{item.get('status', 'unknown')}`")
            lines.append(
                "    `legacy_items`: "
                + ", ".join(f"`{value}`" for value in item.get("legacy_items", []))
            )
            if item.get("workflow_ids"):
                lines.append(
                    "    `workflow_ids`: "
                    + ", ".join(f"`{value}`" for value in item["workflow_ids"])
                )
            if item.get("evidence_ids"):
                lines.append(
                    "    `evidence_ids`: "
                    + ", ".join(f"`{value}`" for value in item["evidence_ids"])
                )
            if item.get("producer"):
                lines.append(f"    `producer`: {item['producer']}")
            if item.get("consumer"):
                lines.append(f"    `consumer`: {item['consumer']}")
            if item.get("break_point"):
                lines.append(f"    `break_point`: {item['break_point']}")
            lines.append(f"    {item.get('technical_impact', '')}")
            if item.get("business_impact"):
                lines.append(f"    Business impact: {item['business_impact']}")
            lines.append("")

    lines.append("## Migration Map")
    lines.append("")
    for mapping in preview["migration_map"]:
        lines.append(
            "- legacy item "
            + f"`{mapping['legacy_item_number']}` "
            + f"({mapping['legacy_section']}) -> "
            + ", ".join(f"`{gap_id}`" for gap_id in mapping["gap_ids"])
        )
    lines.append("")
    return "\n".join(lines)


def validate_preview(preview: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    registry = preview.get("gap_registry", [])
    migration_map = preview.get("migration_map", [])
    gap_ids = [entry.get("gap_id") for entry in registry]
    if len(gap_ids) != len(set(gap_ids)):
        issues.append("duplicate gap_id")
    if preview.get("atomic_gap_count") != len(registry):
        issues.append("atomic_gap_count does not match registry length")
    for entry in registry:
        for key in (
            "gap_id",
            "legacy_items",
            "priority",
            "workflow_ids",
            "evidence_ids",
            "producer",
            "consumer",
            "break_point",
            "technical_impact",
            "business_impact",
            "status",
        ):
            if key not in entry:
                issues.append(f"{entry.get('gap_id', 'UNKNOWN')} missing {key}")
        if entry.get("priority") not in PRIORITY_ORDER:
            issues.append(f"{entry.get('gap_id', 'UNKNOWN')} invalid priority {entry.get('priority')}")
    mapped_legacy = sorted({item for mapping in migration_map for item in mapping.get("gap_ids", [])})
    if sorted(gap_ids) != mapped_legacy:
        issues.append("migration map does not cover exactly the gap registry ids")
    return {"ok": not issues, "issues": issues, "count": len(registry)}


def write_report(preview: dict[str, Any], validation: dict[str, Any], mode: str) -> None:
    report = {
        "timestamp": utc_timestamp(),
        "mode": mode,
        "source_sha256": sha256_file(GAPS_MD_PATH),
        "source": preview.get("source"),
        "legacy_item_count": preview.get("legacy_item_count"),
        "atomic_gap_count": preview.get("atomic_gap_count"),
        "count": validation["count"],
        "ok": validation["ok"],
        "issues": validation["issues"],
    }
    dump_json(REPORT_PATH, report)


def preview_mode() -> int:
    preview = build_preview()
    validation = validate_preview(preview)
    dump_yaml(PREVIEW_YAML_PATH, preview)
    write_text(PREVIEW_MD_PATH, render_markdown(preview))
    write_report(preview, validation, "preview")
    print(
        json.dumps(
            {
                "ok": validation["ok"],
                "issues": validation["issues"],
                "preview_yaml": str(PREVIEW_YAML_PATH),
                "preview_md": str(PREVIEW_MD_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if validation["ok"] else 1


def apply_mode() -> int:
    preview = build_preview()
    validation = validate_preview(preview)
    dump_yaml(PREVIEW_YAML_PATH, preview)
    write_text(PREVIEW_MD_PATH, render_markdown(preview))
    write_report(preview, validation, "apply-preflight")
    if not validation["ok"]:
        return 1
    ensure_dir(RAW_DIR / "backups")
    yaml_backup = RAW_DIR / "backups" / f"WORKFLOW_GAPS.{utc_timestamp().replace(':', '').replace('-', '')}.yaml.bak"
    md_backup = RAW_DIR / "backups" / f"WORKFLOW_GAPS.{utc_timestamp().replace(':', '').replace('-', '')}.md.bak"
    if GAPS_YAML_PATH.exists():
        shutil.copy2(GAPS_YAML_PATH, yaml_backup)
    shutil.copy2(GAPS_MD_PATH, md_backup)
    temp_yaml = GAPS_YAML_PATH.with_suffix(".yaml.tmp")
    temp_md = GAPS_MD_PATH.with_suffix(".md.tmp")
    dump_yaml(temp_yaml, preview)
    write_text(temp_md, render_markdown(preview))
    temp_yaml.replace(GAPS_YAML_PATH)
    temp_md.replace(GAPS_MD_PATH)
    write_report(preview, validation, "apply")
    print(
        json.dumps(
            {"ok": True, "yaml_sha256": sha256_file(GAPS_YAML_PATH), "md_sha256": sha256_file(GAPS_MD_PATH)},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def verify_mode() -> int:
    preview = load_yaml(GAPS_YAML_PATH)
    validation = validate_preview(preview)
    rendered = render_markdown(preview)
    if read_text(GAPS_MD_PATH) != rendered:
        validation["ok"] = False
        validation["issues"].append("markdown out of sync with yaml")
    write_report(preview, validation, "verify")
    print(
        json.dumps(
            {"ok": validation["ok"], "issues": validation["issues"], "yaml_sha256": sha256_file(GAPS_YAML_PATH), "md_sha256": sha256_file(GAPS_MD_PATH)},
            ensure_ascii=False,
            indent=2,
        )
    )
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
