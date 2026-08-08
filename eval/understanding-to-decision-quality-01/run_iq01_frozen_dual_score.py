"""IQ-01 frozen dual-score runner against pinned Fresh38 capture.

Verifies sha256 of ``fresh-full38-results.json`` against fixture-manifest,
extracts Understanding blobs (up to available count), scores baseline
(pre-sharpen raw NBA) vs sharpened classifier, and writes artifacts under
session scratch — never into the git tree by default.

Labeling: machine_proposed only. Does not claim human-adjudicated Fresh38
labels for the full cohort.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
TOOL_DIR = ROOT / "gmail-agent" / "tools" / "gmail_audit"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from agent_runtime.recommended_next_step_quality import (  # noqa: E402
    DECISION_STATES,
    classify_decision_state,
    evaluate_understanding_to_decision_quality,
    is_meaningful_follow_up_delta,
    is_vague_next_step,
    separate_gaps_vs_risks,
)

HERE = Path(__file__).resolve().parent
FIXTURE_DIR = (
    ROOT
    / "gmail-agent"
    / "tools"
    / "gmail_audit"
    / "tests"
    / "fixtures"
    / "measurement_contract_v1"
)
CAPTURE_NAME = "fresh-full38-results.json"
MANIFEST_NAME = "fixture-manifest.json"
EXPECTED_SHA256 = "c04f295293e750856548ac35b4a9126d5946da4e74b6b5df4efebaea33bf736c"
DEFAULT_SCRATCH_ROOT = Path(r"C:\top-code-session-scratch")

# Baseline composition uses the same exported primitives as sharpened scoring.
BASELINE_API_SUPPORTED = True


def default_out_dir() -> Path:
    scratch = os.environ.get("TOP_CODE_SESSION_SCRATCH", "").strip()
    root = Path(scratch) if scratch else DEFAULT_SCRATCH_ROOT
    return root / "iq01-eval"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest_expected_sha(manifest_path: Path) -> str:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    files = manifest.get("files") if isinstance(manifest.get("files"), dict) else {}
    entry = files.get(CAPTURE_NAME) if isinstance(files.get(CAPTURE_NAME), dict) else {}
    sha = str(entry.get("sha256") or "").strip().lower()
    if not sha:
        raise ValueError(f"manifest missing sha256 for {CAPTURE_NAME}")
    return sha


def verify_capture(capture_path: Path, manifest_path: Path) -> dict[str, Any]:
    expected = load_manifest_expected_sha(manifest_path)
    actual = file_sha256(capture_path)
    if expected != EXPECTED_SHA256:
        raise ValueError(
            "protocol pin mismatch: PROTOCOL/EXPECTED_SHA256 "
            f"{EXPECTED_SHA256} != manifest {expected}"
        )
    ok = actual == expected
    return {
        "capture_path": str(capture_path.as_posix()),
        "manifest_path": str(manifest_path.as_posix()),
        "expected_sha256": expected,
        "actual_sha256": actual,
        "bytes": capture_path.stat().st_size,
        "verified": ok,
    }


def extract_understanding_rows(capture: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in list(capture.get("cases") or []):
        if not isinstance(case, dict):
            continue
        case_id = str(case.get("id") or case.get("case_id") or "").strip()
        understanding = case.get("understanding")
        if not isinstance(understanding, dict):
            rows.append(
                {
                    "case_id": case_id or "unknown",
                    "extracted": False,
                    "skip_reason": "missing_understanding",
                    "understanding": None,
                    "categories": list(case.get("categories") or []),
                }
            )
            continue
        ss = understanding.get("situation_summary")
        ss = ss if isinstance(ss, dict) else {}
        rows.append(
            {
                "case_id": case_id or str(understanding.get("case_id") or "unknown"),
                "extracted": True,
                "skip_reason": None,
                "understanding": understanding,
                "categories": list(case.get("categories") or []),
                "case_kind": str(
                    ss.get("case_family")
                    or understanding.get("case_family")
                    or ""
                ),
                "business_area": str(ss.get("business_area") or ""),
            }
        )
    return rows


def _raw_next_step_text(understanding: dict[str, Any]) -> tuple[str, str, str]:
    nba = understanding.get("next_best_action_recommendation")
    nba = nba if isinstance(nba, dict) else {}
    title = str(nba.get("title_pl") or "")
    reason = str(nba.get("reason_pl") or "")
    action = str(nba.get("action_type") or nba.get("recommended_action") or "")
    return title, reason, action


def score_baseline(understanding: dict[str, Any], *, case_id: str, case_kind: str, business_area: str) -> dict[str, Any]:
    """Pre-sharpen score using exported primitives (no gold expected)."""
    uo = dict(understanding)
    title, reason, action = _raw_next_step_text(uo)
    raw_text = f"{title} {reason}".strip() or action
    missing = [str(x) for x in (uo.get("missing_critical_fields") or []) if str(x).strip()]
    risks = list(uo.get("risks") or [])
    open_loops = list(uo.get("open_loops") or [])
    delta = uo.get("thread_delta") if isinstance(uo.get("thread_delta"), dict) else {}
    ss = uo.get("situation_summary") if isinstance(uo.get("situation_summary"), dict) else {}
    family = str(case_kind or ss.get("case_family") or uo.get("case_family") or "")
    area = str(business_area or ss.get("business_area") or "")

    decision_state = classify_decision_state(
        sharpened_pl=raw_text,
        action_type=action,
        case_kind=family or area,
        missing_critical_fields=missing,
        risks=risks,
        open_loops=open_loops,
    )
    gaps_vs_risks = separate_gaps_vs_risks(
        missing_critical_fields=missing,
        risks=risks,
        open_loops=open_loops,
    )
    meaningful_delta = is_meaningful_follow_up_delta(
        what_changed_pl=str(delta.get("operator_visible_delta_summary") or ""),
        thread_delta=delta,
        risks=risks,
        open_loops=open_loops,
    )
    next_step_ok = bool(raw_text) and not is_vague_next_step(raw_text)
    state_ok = decision_state in DECISION_STATES
    gaps_ok = bool(gaps_vs_risks.get("separated"))
    follow_up_ok = True
    if meaningful_delta:
        follow_up_ok = next_step_ok and decision_state in DECISION_STATES
    checks = {
        "recommended_next_step_not_vague": next_step_ok,
        "decision_state_clear": state_ok,
        "gaps_vs_risks_separated": gaps_ok,
        "follow_up_delta": follow_up_ok,
    }
    failed = [name for name, ok in checks.items() if not ok]
    return {
        "case_id": case_id,
        "score_kind": "baseline",
        "verdict": "PASS" if not failed else "FAIL",
        "decision_state": decision_state,
        "expected_decision_state": None,
        "raw_next_step_was_vague": is_vague_next_step(raw_text),
        "raw_next_step_len": len(raw_text),
        "meaningful_follow_up_delta": meaningful_delta,
        "gaps_vs_risks": {
            "separated": gaps_ok,
            "gap_count": len(gaps_vs_risks["gaps"]),
            "risk_count": len(gaps_vs_risks["risks"]),
            "overlap_count": len(gaps_vs_risks["overlap"]),
            "questionish_gap_count": len(gaps_vs_risks["questionish_gaps"]),
        },
        "checks": checks,
        "failed_checks": failed,
    }


def score_sharpened(understanding: dict[str, Any], *, case_id: str, case_kind: str, business_area: str) -> dict[str, Any]:
    result = evaluate_understanding_to_decision_quality(
        understanding,
        case_id=case_id,
        case_kind=case_kind,
        business_area=business_area,
        expected_decision_state="",  # frozen: no adjudicated gold
    )
    result["score_kind"] = "sharpened"
    result["expected_decision_state"] = None
    result["sharpened_next_step_len"] = len(str(result.pop("sharpened_next_step_pl", "") or ""))
    return result


def build_cohort_manifest(
    *,
    integrity: dict[str, Any],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    extracted = [r for r in rows if r.get("extracted")]
    skipped = [r for r in rows if not r.get("extracted")]
    cases = []
    for r in extracted:
        cases.append(
            {
                "case_id": r["case_id"],
                "labeling_status": "machine_proposed",
                "expected_decision_state": None,
                "adjudicated": False,
                "categories": r.get("categories") or [],
                "case_kind": r.get("case_kind") or "",
                "business_area": r.get("business_area") or "",
            }
        )
    return {
        "program": "UNDERSTANDING-TO-DECISION-QUALITY-01",
        "roadmap_id": "IQ-01",
        "schema_version": "iq01-frozen-cohort-manifest.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "cohort_kind": "frozen_fresh38_capture",
        "labeling_status": "machine_proposed",
        "adjudicated_label_count": 0,
        "adjudicated_complete": False,
        "honesty_note": (
            "No human-adjudicated decision-state labels for all extracted cases. "
            "machine_proposed states come from the current classifier and must not "
            "be treated as gold expected."
        ),
        "integrity": integrity,
        "capture_case_count": len(rows),
        "extracted_understanding_count": len(extracted),
        "skipped_case_ids": [r["case_id"] for r in skipped],
        "cases": cases,
    }


def dual_score(
    rows: list[dict[str, Any]],
    *,
    baseline_supported: bool = BASELINE_API_SUPPORTED,
) -> dict[str, Any]:
    extracted = [r for r in rows if r.get("extracted") and isinstance(r.get("understanding"), dict)]
    baseline_results: list[dict[str, Any]] = []
    sharpened_results: list[dict[str, Any]] = []
    paired: list[dict[str, Any]] = []

    for r in extracted:
        understanding = r["understanding"]
        case_id = str(r["case_id"])
        case_kind = str(r.get("case_kind") or "")
        business_area = str(r.get("business_area") or "")
        sharp = score_sharpened(
            understanding,
            case_id=case_id,
            case_kind=case_kind,
            business_area=business_area,
        )
        sharpened_results.append(sharp)
        machine_proposed = str(sharp.get("decision_state") or "")
        entry: dict[str, Any] = {
            "case_id": case_id,
            "labeling_status": "machine_proposed",
            "expected_decision_state": None,
            "machine_proposed_decision_state": machine_proposed,
            "sharpened": {
                "verdict": sharp.get("verdict"),
                "decision_state": sharp.get("decision_state"),
                "checks": sharp.get("checks"),
                "failed_checks": sharp.get("failed_checks"),
                "raw_next_step_was_vague": sharp.get("raw_next_step_was_vague"),
            },
        }
        if baseline_supported:
            base = score_baseline(
                understanding,
                case_id=case_id,
                case_kind=case_kind,
                business_area=business_area,
            )
            baseline_results.append(base)
            entry["baseline"] = {
                "verdict": base.get("verdict"),
                "decision_state": base.get("decision_state"),
                "checks": base.get("checks"),
                "failed_checks": base.get("failed_checks"),
                "raw_next_step_was_vague": base.get("raw_next_step_was_vague"),
            }
            entry["state_changed_by_sharpen"] = base.get("decision_state") != sharp.get(
                "decision_state"
            )
            # Raw was vague AND sharpened metric "recommended_next_step_not_vague" passed.
            entry["vagueness_cleared_by_sharpen"] = bool(
                base.get("raw_next_step_was_vague")
            ) and bool((sharp.get("checks") or {}).get("recommended_next_step_not_vague"))
        paired.append(entry)

    def _counts(results: list[dict[str, Any]], key: str = "decision_state") -> dict[str, int]:
        c: Counter[str] = Counter()
        for row in results:
            c[str(row.get(key) or "")] += 1
        return dict(sorted(c.items()))

    sharpened_pass = sum(1 for r in sharpened_results if r.get("verdict") == "PASS")
    baseline_pass = sum(1 for r in baseline_results if r.get("verdict") == "PASS") if baseline_supported else None

    return {
        "program": "UNDERSTANDING-TO-DECISION-QUALITY-01",
        "roadmap_id": "IQ-01",
        "schema_version": "iq01-dual-score-summary.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "cohort_kind": "frozen_fresh38_capture",
        "labeling_status": "machine_proposed",
        "adjudicated_label_count": 0,
        "adjudicated_complete": False,
        "baseline_api_supported": baseline_supported,
        "baseline_gap": not baseline_supported,
        "baseline_gap_note": None
        if baseline_supported
        else (
            "Baseline pre-sharpen scoring unavailable; sharpened-only. "
            "See PROTOCOL.md dual-score definition."
        ),
        "extracted_understanding_count": len(extracted),
        "sharpened": {
            "scored": len(sharpened_results),
            "passed_metric_bundle": sharpened_pass,
            "failed_metric_bundle": len(sharpened_results) - sharpened_pass,
            "decision_state_distribution": _counts(sharpened_results),
            "note": (
                "PASS/FAIL here is metric-bundle self-consistency without gold expected; "
                "not Fresh38 adjudicated accuracy."
            ),
        },
        "baseline": None
        if not baseline_supported
        else {
            "scored": len(baseline_results),
            "passed_metric_bundle": baseline_pass,
            "failed_metric_bundle": len(baseline_results) - int(baseline_pass or 0),
            "decision_state_distribution": _counts(baseline_results),
            "vague_raw_count": sum(
                1 for r in baseline_results if r.get("raw_next_step_was_vague")
            ),
            "note": "Pre-sharpen raw recommended_next_step scoring via exported primitives.",
        },
        "machine_proposed_decision_state_distribution": _counts(
            [{"decision_state": p.get("machine_proposed_decision_state")} for p in paired]
        ),
        "state_changed_by_sharpen_count": sum(
            1 for p in paired if p.get("state_changed_by_sharpen")
        )
        if baseline_supported
        else None,
        "vagueness_cleared_by_sharpen_count": sum(
            1 for p in paired if p.get("vagueness_cleared_by_sharpen")
        )
        if baseline_supported
        else None,
        "cases": paired,
        "honesty_notes": [
            "Frozen capture is the pre-run baseline artifact (sha256 pinned).",
            "Labeling is machine_proposed only — not human-adjudicated for all 36.",
            "Do not treat metric-bundle PASS as Fresh38 gold accuracy.",
        ],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="IQ-01 frozen dual-score eval")
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory (default: session scratch iq01-eval)",
    )
    p.add_argument(
        "--capture",
        type=Path,
        default=FIXTURE_DIR / CAPTURE_NAME,
        help="Path to fresh-full38-results.json",
    )
    p.add_argument(
        "--manifest",
        type=Path,
        default=FIXTURE_DIR / MANIFEST_NAME,
        help="Path to fixture-manifest.json",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Verify sha256 + extract counts; print summary JSON; skip artifact files",
    )
    p.add_argument(
        "--sharpened-only",
        action="store_true",
        help="Force baseline_gap=true (document baseline gap; score sharpened only)",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    capture_path = Path(args.capture)
    manifest_path = Path(args.manifest)
    if not capture_path.is_file():
        print(f"ERROR: capture missing: {capture_path}", file=sys.stderr)
        return 2
    if not manifest_path.is_file():
        print(f"ERROR: manifest missing: {manifest_path}", file=sys.stderr)
        return 2

    integrity = verify_capture(capture_path, manifest_path)
    if not integrity["verified"]:
        print(
            json.dumps({"error": "sha256_mismatch", "integrity": integrity}, indent=2),
            file=sys.stderr,
        )
        return 3

    capture = json.loads(capture_path.read_text(encoding="utf-8-sig"))
    rows = extract_understanding_rows(capture)
    extracted_n = sum(1 for r in rows if r.get("extracted"))
    manifest = build_cohort_manifest(integrity=integrity, rows=rows)
    baseline_supported = BASELINE_API_SUPPORTED and not args.sharpened_only
    summary = dual_score(rows, baseline_supported=baseline_supported)
    summary["integrity"] = integrity

    preview = {
        "verified": integrity["verified"],
        "sha256": integrity["actual_sha256"],
        "capture_case_count": len(rows),
        "extracted_understanding_count": extracted_n,
        "labeling_status": "machine_proposed",
        "adjudicated_complete": False,
        "baseline_gap": summary.get("baseline_gap"),
        "machine_proposed_decision_state_distribution": summary.get(
            "machine_proposed_decision_state_distribution"
        ),
        "sharpened_passed_metric_bundle": (summary.get("sharpened") or {}).get(
            "passed_metric_bundle"
        ),
        "baseline_passed_metric_bundle": (summary.get("baseline") or {}).get(
            "passed_metric_bundle"
        )
        if summary.get("baseline")
        else None,
    }
    print(json.dumps(preview, ensure_ascii=False, indent=2))

    if args.dry_run:
        print("dry-run: no artifact files written")
        return 0

    out_dir = Path(args.out) if args.out is not None else default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path_out = out_dir / "cohort-manifest.json"
    summary_path_out = out_dir / "dual-score-summary.json"
    manifest["artifact_path"] = str(manifest_path_out.as_posix())
    summary["artifact_path"] = str(summary_path_out.as_posix())
    summary["cohort_manifest_path"] = str(manifest_path_out.as_posix())
    manifest_path_out.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    summary_path_out.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {manifest_path_out}")
    print(f"wrote {summary_path_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
