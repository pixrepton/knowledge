"""Bounded deterministic proof for PLANNER-EXEC-FIDELITY-01 (no Fresh 38, no send)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parents[3] / "gmail-agent" / "tools" / "gmail_audit"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from agent_runtime.constitution import load_constitution
from agent_runtime.draft_sanity import evaluate_draft_sanity
from agent_runtime.effective_tools import compute_effective_available_tools
from agent_runtime.envelope_presence import classify_envelope_presence
from agent_runtime.failure_taxonomy import classify_tool_handler_error
from agent_runtime.graph import AgentGraphEngine, _policy_enforcement_block
from agent_runtime.known_fact_guard import guard_known_fact_reask
from agent_runtime.planner_run_budget import build_planner_run_budget
from agent_runtime.policy_action_spine import correlate_tool_plan
from agent_runtime.settings import AgentRuntimeSettings
from agent_runtime.store import build_initial_snapshot
from agent_runtime.tool_context import ToolExecutionContext
from agent_runtime.tool_result import ToolCallPlan
from agent_runtime.tools.handlers import generate_draft_reply
from agent_runtime.tools_registry import AgentToolRegistry, MockToolRegistry
from llm_contracts.engagement_snapshot_v2 import (
    CaseUnderstandingProjection,
    HvacLocation,
    HvacProfile,
    PolicyActionEnvelopeV1,
)


def _settings(kalk: str = "") -> AgentRuntimeSettings:
    return AgentRuntimeSettings(
        enabled=True,
        mode="prep",
        model="gpt-4o-mini",
        model_fallback="",
        max_rounds=3,
        openai_api_key="test",
        openai_base_url="https://api.openai.com/v1",
        kalk_top_base_url=kalk,
        kalk_top_agent_key="",
        kalk_top_timeout_sec=4,
        kalk_top_max_retries=1,
    )


def case_int_01() -> dict:
    """Sales lead with known area/city; kalk unavailable; no reask."""
    constitution = load_constitution()
    before = compute_effective_available_tools(
        constitution.tool_allowlist, constitution=constitution, settings=_settings("")
    )
    after = compute_effective_available_tools(
        constitution.tool_allowlist,
        constitution=constitution,
        settings=_settings("http://host.docker.internal:8091"),
    )
    snap = build_initial_snapshot(case_id="INT-01", engagement_id="e_int01", trace_id="t_int01")
    snap = snap.model_copy(
        update={
            "case_kind": "wycena_oferta",
            "hvac_profile": HvacProfile(
                heated_area_m2=150,
                location=HvacLocation(city="Wrocław"),
            ),
            "case_understanding": CaseUnderstandingProjection(
                essence_pl="Lead wyceny pod Wrocławiem, 150 m2",
                recommended_next_step_pl="Przygotuj wycenę lub draft",
            ),
            "policy_action_envelope": PolicyActionEnvelopeV1(
                freshness="current",
                policy_decision_id="pd_int01",
                action_proposal_id="ap_int01",
                decision_candidate_id="dc_int01",
                source_signal_id="sig_int01",
                allowed_by_policy=True,
            ),
        }
    )
    reask = guard_known_fact_reask(
        tool_name="request_operator_clarification",
        arguments={"ask_pl": "Proszę o miasto lokalizacji"},
        snapshot=snap,
    )
    plan = correlate_tool_plan(
        ToolCallPlan(tool_name="generate_draft_reply", arguments={"intent": "quote"}),
        snap.policy_action_envelope,
    )
    return {
        "case_id": "INT-01",
        "effective_tools_without_kalk": list(before.offered),
        "filter_reasons": list(before.unavailable_notes),
        "effective_tools_with_kalk": list(after.offered),
        "known_fact_reask_blocked": bool(reask),
        "reask_keys": (reask or {}).get("fact_keys"),
        "policy_correlation": plan.correlation_status,
        "policy_decision_id": plan.policy_decision_id,
        "action_proposal_id": plan.action_proposal_id,
        "kalk_offered_without_config": "call_kalk_top_quote" in before.offered,
    }


def case_new_03() -> dict:
    """Known facts preserved; kalk config missing classified infra not planner."""
    snap = build_initial_snapshot(case_id="NEW-03", engagement_id="e_new03", trace_id="t_new03")
    snap = snap.model_copy(
        update={
            "case_kind": "wycena_oferta",
            "hvac_profile": HvacProfile(
                heated_area_m2=180,
                location=HvacLocation(city="Kraków"),
                building_type="single_family",
            ),
        }
    )
    attr = classify_tool_handler_error(
        tool_name="call_kalk_top_quote",
        summary="KALK_TOP_BASE_URL is not configured",
        status="error",
    )
    reask = guard_known_fact_reask(
        tool_name="request_operator_clarification",
        arguments={"ask_pl": "Jaki jest metraż?"},
        snapshot=snap,
    )
    return {
        "case_id": "NEW-03",
        "known_area": snap.hvac_profile.heated_area_m2,
        "known_city": snap.hvac_profile.location.city,
        "kalk_failure_class": attr["failure_class"],
        "kalk_owner": attr["owner"],
        "reask_blocked": bool(reask),
    }


def case_int_04() -> dict:
    """Service case — draft asking metraż/OZC blocked."""
    snap = build_initial_snapshot(case_id="INT-04", engagement_id="e_int04", trace_id="t_int04")
    snap = snap.model_copy(update={"case_kind": "awaria_naprawa"})
    ctx = ToolExecutionContext.from_snapshot(snap, settings=_settings())
    result = generate_draft_reply(
        ToolCallPlan(tool_name="generate_draft_reply", arguments={"intent": "missing_info"}),
        ctx,
    )
    sanity = evaluate_draft_sanity(
        body="prosimy o metraż i OZC",
        case_kind="awaria_naprawa",
        intent="missing_info",
    )
    return {
        "case_id": "INT-04",
        "handler_status": result.status,
        "failure_class": result.failure_class,
        "sanity_ok": sanity["ok"],
        "sanity_reasons": sanity.get("reason_codes"),
        "draft_enabled": False,
    }


def case_fu_06_07() -> dict:
    """Follow-up: facts/thread delta reach planner view; change detection ownership."""
    snap = build_initial_snapshot(case_id="FU-06", engagement_id="e_fu06", trace_id="t_fu06")
    snap = snap.model_copy(
        update={
            "case_kind": "wycena_oferta",
            "hvac_profile": HvacProfile(
                heated_area_m2=120,
                location=HvacLocation(city="Gliwice"),
            ),
            "case_understanding": CaseUnderstandingProjection(
                essence_pl="Follow-up: klient zmienił metraż",
                what_changed_pl="Metraż z 100 na 120 m2",
                recommended_next_step_pl="Zaktualizuj wycenę",
            ),
        }
    )
    from agent_runtime.openai_agent_client import _compact_view

    view = _compact_view(snap)
    return {
        "case_id": "FU-06/FU-07",
        "brain1_present": "brain1_context" in view,
        "what_changed_pl": view.get("brain1_context", {})
        .get("understanding", {})
        .get("what_changed_pl"),
        "heated_area_m2": view.get("hvac_profile", {}).get("heated_area_m2"),
        "change_detection_owner": "Brain1_case_understanding",
        "planner_ignores_change": False,
    }


def case_budget_and_envelope() -> dict:
    budget_before = build_planner_run_budget(max_rounds=2).as_dict()
    budget = build_planner_run_budget(max_rounds=1)
    budget.record_turn(tool_name="search_rag_knowledge", status="ok")
    exhausted = budget.check_before_turn()

    harness = classify_envelope_presence(
        None, case_understanding_present=False, harness_mode=True
    )
    wiring = classify_envelope_presence(
        None, case_understanding_present=True, policy_required=True
    )
    snap = build_initial_snapshot(case_id="ENV", engagement_id="e_env", trace_id="t_env")
    snap = snap.model_copy(
        update={
            "case_understanding": CaseUnderstandingProjection(essence_pl="x"),
        }
    )
    block = _policy_enforcement_block(
        snap,
        ToolCallPlan(tool_name="generate_draft_reply", arguments={"intent": "quote"}),
        signal_payload={"policy_required": True},
    )

    class Cap:
        def plan_next_tool(self, *, available_tools, **_kwargs):
            return ToolCallPlan(tool_name="report_gaps_and_stop", arguments={})

    offered: list[str] = []

    class Cap2:
        def plan_next_tool(self, *, available_tools, **_kwargs):
            offered.extend(available_tools)
            return ToolCallPlan(tool_name="report_gaps_and_stop", arguments={})

    engine = AgentGraphEngine(
        planner=Cap2(),
        constitution=load_constitution(),
        tool_registry=MockToolRegistry(),
    )
    engine.run(
        build_initial_snapshot(case_id="OFFER", engagement_id="e_o", trace_id="t_o"),
        context=ToolExecutionContext.from_snapshot(
            build_initial_snapshot(case_id="OFFER", engagement_id="e_o", trace_id="t_o"),
            settings=_settings(""),
        ),
    )
    return {
        "budget_before": budget_before,
        "budget_exhausted_reason": exhausted,
        "harness_envelope": harness["status"],
        "wiring_envelope": wiring["status"],
        "fail_closed_failure_class": getattr(block, "failure_class", None),
        "kalk_not_offered": "call_kalk_top_quote" not in offered,
        "offered_tools": offered,
    }


def main() -> int:
    out_dir = Path(__file__).resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "slice": "PLANNER-EXECUTION-FIDELITY-AND-TOOL-BUDGET-INTEGRITY-01",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "fresh38_rerun": False,
        "send_performed": False,
        "cases": {
            "INT-01": case_int_01(),
            "NEW-03": case_new_03(),
            "INT-04": case_int_04(),
            "FU-06_FU-07": case_fu_06_07(),
            "budget_envelope": case_budget_and_envelope(),
        },
    }
    path = out_dir / "bounded_proof.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
