from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import yaml


BASE_DIR = Path(__file__).resolve().parent


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-status", required=True)
    parser.add_argument("--phase-c-status", required=True)
    parser.add_argument("--validator-status", required=True)
    parser.add_argument("--manifest-status", required=True)
    parser.add_argument("--pass1-status", required=True)
    parser.add_argument("--pass2-status", required=True)
    args = parser.parse_args()

    evidence_rows = load_jsonl(BASE_DIR / "WORKFLOW_EVIDENCE.jsonl")
    registry = yaml.safe_load((BASE_DIR / "WORKFLOW_REGISTRY.yaml").read_text(encoding="utf-8"))
    gaps = yaml.safe_load((BASE_DIR / "WORKFLOW_GAPS.yaml").read_text(encoding="utf-8"))

    evidence_types = Counter(row["evidence_type"] for row in evidence_rows)
    runtime_counts = Counter(workflow["runtime"]["classification"] for workflow in registry["workflows"])
    gap_counts = Counter(gap["priority"] for gap in gaps["gap_registry"])

    content = "\n".join(
        [
            "# PROGRESS.md",
            "",
            "## Target",
            "",
            "- Target: `AI-OS-WORKFLOW-RECONSTRUCTION-AND-REGISTRY-01`",
            f"- Status: `{args.target_status}`",
            "",
            "## Current Canonical State",
            "",
            f"- Evidence rows: `{len(evidence_rows)}`",
            f"- Workflows: `{len(registry['workflows'])}`",
            f"- Subflows: `{len(registry.get('subflows', {}))}`",
            f"- Atomic gaps: `{gaps['atomic_gap_count']}`",
            f"- Legacy gap items: `{gaps['legacy_item_count']}`",
            f"- Runtime confirmed workflows: `{runtime_counts.get('CONFIRMED', 0)}`",
            f"- Runtime unverified workflows: `{runtime_counts.get('UNVERIFIED', 0)}`",
            "",
            "## Phase Status",
            "",
            "- Reverse audit: `COMPLETE (12/12)`",
            "- Test-evidence mapping: `COMPLETE`",
            f"- Phase C normalization: `{args.phase_c_status}`",
            f"- Validator: `{args.validator_status}`",
            f"- Manifest: `{args.manifest_status}`",
            f"- First pass: `{args.pass1_status}`",
            f"- Second pass: `{args.pass2_status}`",
            "",
            "## Evidence Type Counts",
            "",
            *(f"- {key}: `{value}`" for key, value in sorted(evidence_types.items())),
            "",
            "## Gap Priority Counts",
            "",
            *(f"- {key}: `{gap_counts.get(key, 0)}`" for key in ("P0", "P1", "P2", "P3")),
            "",
            "## Notes",
            "",
            "- Canonical files are generated from normalized core artifacts, not preserved historical prose.",
            "- `ATLAS-GLOBAL` remains an evidence scope sentinel, not an eighteenth workflow.",
            "",
        ]
    )
    (BASE_DIR / "PROGRESS.md").write_text(content + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"ok": True, "path": str(BASE_DIR / 'PROGRESS.md')}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
