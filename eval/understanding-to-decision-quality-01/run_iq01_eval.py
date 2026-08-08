"""Bounded IQ-01 eval: Understanding → one clear decision state.

Runs synthetic cohort fixtures (no live Gmail). Writes aggregate summary JSON
without secrets/PII.

Default artifacts go under session scratch (does not dirty the git tree).
Optional ``--write-repo-summary`` restores the legacy in-repo ``summary.json``.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL_DIR = ROOT / "gmail-agent" / "tools" / "gmail_audit"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from agent_runtime.recommended_next_step_quality import (  # noqa: E402
    DECISION_STATES,
    evaluate_understanding_to_decision_quality,
)

HERE = Path(__file__).resolve().parent
COHORT_PATH = HERE / "cohort.json"
REPO_SUMMARY_PATH = HERE / "summary.json"

DEFAULT_SCRATCH_ROOT = Path(r"C:\top-code-session-scratch")


def default_out_dir() -> Path:
    scratch = os.environ.get("TOP_CODE_SESSION_SCRATCH", "").strip()
    root = Path(scratch) if scratch else DEFAULT_SCRATCH_ROOT
    return root / "iq01-eval"


def build_summary(cases: list[dict], cohort: dict, *, out_path: Path) -> dict:
    results: list[dict] = []
    for row in cases:
        understanding = row.get("understanding") if isinstance(row.get("understanding"), dict) else {}
        result = evaluate_understanding_to_decision_quality(
            understanding,
            case_id=str(row.get("case_id") or ""),
            case_kind=str(row.get("case_kind") or ""),
            business_area=str(row.get("business_area") or ""),
            expected_decision_state=str(row.get("expected_decision_state") or ""),
            lifecycle_hint=str(row.get("lifecycle_hint") or ""),
            policy_allowed=row.get("policy_allowed"),
            hitl_required=row.get("hitl_required"),
            draft_ready=row.get("draft_ready"),
            require_follow_up_delta=bool(row.get("require_follow_up_delta")),
        )
        result["fresh38_ref"] = row.get("fresh38_ref")
        # Drop free-text next step from aggregate if it could carry customer phrasing —
        # keep a short, non-PII hash-like token length only.
        result["sharpened_next_step_len"] = len(str(result.pop("sharpened_next_step_pl", "") or ""))
        results.append(result)

    passed = sum(1 for r in results if r.get("verdict") == "PASS")
    failed = [r["case_id"] for r in results if r.get("verdict") != "PASS"]
    by_state: dict[str, int] = {}
    for r in results:
        st = str(r.get("decision_state") or "")
        by_state[st] = by_state.get(st, 0) + 1

    return {
        "program": "UNDERSTANDING-TO-DECISION-QUALITY-01",
        "roadmap_id": "IQ-01",
        "schema_version": "iq01-summary.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "cohort_path": str(COHORT_PATH.as_posix()),
        "cohort_kind": "synthetic",
        "labeling_status": "synthetic_fixture",
        "cases": len(results),
        "passed": passed,
        "failed": len(failed),
        "failed_case_ids": failed,
        "verdict": "PASS" if not failed and len(results) >= 10 else "FAIL",
        "decision_state_counts": by_state,
        "decision_states_covered": sorted(by_state),
        "all_roadmap_states_present": set(by_state.keys()) >= set(DECISION_STATES),
        "metrics": list(cohort.get("metrics") or []),
        "results": results,
        "artifact_path": str(out_path.as_posix()),
        "notes": [
            "Synthetic fixtures; Fresh38 refs are labels only.",
            "No live Gmail / no full Fresh 38.",
            "follow_up_guardian untouched (FG-02/03 isolation).",
            "Default artifact write is session scratch (see PROTOCOL.md).",
        ],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="IQ-01 synthetic cohort eval")
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory (default: %%TOP_CODE_SESSION_SCRATCH%%/iq01-eval or C:\\top-code-session-scratch\\iq01-eval)",
    )
    p.add_argument(
        "--write-repo-summary",
        action="store_true",
        help="Also write legacy knowledge/.../summary.json (dirty-write; off by default)",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    out_dir = Path(args.out) if args.out is not None else default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "synthetic-summary.json"

    cohort = json.loads(COHORT_PATH.read_text(encoding="utf-8"))
    cases = list(cohort.get("cases") or [])
    summary = build_summary(cases, cohort, out_path=out_path)

    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written = [out_path]
    if args.write_repo_summary:
        REPO_SUMMARY_PATH.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        written.append(REPO_SUMMARY_PATH)

    print(
        json.dumps(
            {
                k: summary[k]
                for k in (
                    "verdict",
                    "cases",
                    "passed",
                    "failed",
                    "failed_case_ids",
                    "decision_state_counts",
                    "all_roadmap_states_present",
                    "labeling_status",
                    "artifact_path",
                )
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    for path in written:
        print(f"wrote {path}")
    return 0 if summary["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
