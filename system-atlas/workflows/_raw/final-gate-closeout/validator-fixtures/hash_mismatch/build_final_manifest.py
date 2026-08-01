from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "FINAL_MANIFEST.json"
INCLUDED_FILES = [
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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest() -> dict:
    files = []
    for relative in INCLUDED_FILES:
        path = BASE_DIR / relative
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
    return {
        "schema_version": 1,
        "root": str(BASE_DIR),
        "file_count": len(files),
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    manifest = build_manifest()
    if args.write:
        MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"ok": True, "file_count": manifest["file_count"], "path": str(MANIFEST_PATH)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
