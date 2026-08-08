"""Bounded live/deterministic planner fidelity proof (INT-01, INT-04) — no Fresh 38."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parents[2] / "gmail-agent" / "tools" / "gmail_audit"
# script lives in knowledge/eval/... → parents[3] is workspace
_HERE = Path(__file__).resolve()
for parent in _HERE.parents:
    candidate = parent / "gmail-agent" / "tools" / "gmail_audit"
    if candidate.is_dir():
        TOOL_DIR = candidate
        break
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from agent_runtime.constitution import load_constitution
from agent_runtime.effective_tools import compute_effective_available_tools
from agent_runtime.graph import AgentGraphEngine
from agent_runtime.settings import AgentRuntimeSettings, load_agent_runtime_settings
from agent_runtime.store import build_initial_snapshot
from agent_runtime.tool_context import ToolExecutionContext
from agent_runtime.tool_result import ToolCallPlan
from agent_runtime.tools_registry import AgentToolRegistry
from eval_planner_spine_handoff import (
    apply_hvac_seed_to_snapshot,
    build_production_faithful_planner_signal,
)


def _try_live_settings() -> AgentRuntimeSettings | None:
    try:
        settings = load_agent_runtime_settings()
    except Exception:
        return None
    if not str(getattr(settings, "openai_api_key", "") or "").strip():
        # Also accept AGENT_* keys via build_agent_planner_endpoints path
        if not any(
            os.getenv(k)
            for k in (
                "AGENT_OPENAI_API_KEY",
                "AGENT_OPENAI_NATIVE_API_KEY",
                "OPENAI_API_KEY",
                "GROQ_API_KEY",
            )
        ):
            return None
    return settings


def _intel(case_id: str, *, service: bool) -> dict:
    if service:
        return {
            "understanding_output": {
                "source_signal_id": f"{case_id}_msg",
                "operator_explanation": {
                    "essence_pl": "Awaria pompy ciepła — brak ogrzewania",
                    "why_pl": "Klient zgłasza usterkę",
                },
                "missing_critical_fields": ["objaw_szczegoly"],
                "next_best_action_recommendation": {
                    "title_pl": "Wymagana ręczna ocena",
                    "reason_pl": "escalate_internal",
                },
                "case_family": "awaria_naprawa",
            }
        }
    return {
        "understanding_output": {
            "source_signal_id": f"{case_id}_msg",
            "operator_explanation": {
                "essence_pl": "Lead wyceny PC 150 m2 pod Wrocławiem",
                "why_pl": "Nowe zapytanie ofertowe",
            },
            "missing_critical_fields": [],
            "next_best_action_recommendation": {
                "title_pl": "Wymagana ręczna ocena",
                "reason_pl": "escalate_internal",
            },
            "case_family": "wycena_oferta",
            "facts_explicit": {"heated_area_m2": 150, "city": "Wrocław"},
        }
    }


def run_case(case_id: str, *, service: bool, live: bool) -> dict:
    constitution = load_constitution()
    case_kind = "awaria_naprawa" if service else "wycena_oferta"
    body = (
        "Pompa nie grzeje od wczoraj, proszę o serwis"
        if service
        else "Proszę o wycenę pompy ciepła dla domu 150 m2 pod Wrocławiem, obecnie gaz."
    )
    extraction = None if service else {"heated_area_m2": 150, "city": "Wrocław"}
    handoff = build_production_faithful_planner_signal(
        case_id=f"case_{case_id}",
        signal_id=f"sig_{case_id}",
        message_id=f"{case_id}_msg",
        subject=case_id,
        body=body,
        case_intelligence_result=_intel(case_id, service=service),
        case_kind=case_kind,
        extraction=extraction,
        policy_required=True,
        harness_mode=False,
    )
    signal = handoff["signal_payload"]
    settings = _try_live_settings() if live else None
    use_live = settings is not None
    if settings is None:
        settings = AgentRuntimeSettings(
            enabled=True,
            mode="prep",
            model="gpt-4o-mini",
            model_fallback="",
            max_rounds=3,
            openai_api_key="test",
            openai_base_url="https://api.openai.com/v1",
            kalk_top_base_url="",
            kalk_top_agent_key="",
            kalk_top_timeout_sec=4,
            kalk_top_max_retries=1,
        )

    effective = compute_effective_available_tools(
        constitution.tool_allowlist,
        constitution=constitution,
        settings=settings,
    )

    snap = build_initial_snapshot(
        case_id=f"case_{case_id}",
        engagement_id=f"eng_{case_id}",
        trace_id=f"trace_{case_id}",
    )
    snap = snap.model_copy(update={"case_kind": case_kind})
    snap = apply_hvac_seed_to_snapshot(snap, signal)

    if use_live:
        from agent_runtime.openai_agent_client import OpenAIToolPlanner

        planner = OpenAIToolPlanner(settings=settings)
        mode = "live_llm"
    else:

        class DeterministicPlanner:
            def plan_next_tool(self, *, snapshot, available_tools, **_kwargs):
                if service:
                    # Attempt bad draft path to prove sanity gate
                    if "generate_draft_reply" in available_tools:
                        return ToolCallPlan(
                            tool_name="generate_draft_reply",
                            arguments={"intent": "missing_info"},
                        )
                if "generate_draft_reply" in available_tools:
                    return ToolCallPlan(
                        tool_name="generate_draft_reply",
                        arguments={"intent": "quote"},
                    )
                return ToolCallPlan(
                    tool_name="request_operator_clarification",
                    arguments={"ask_pl": "Operatorze, decyzja biznesowa?"},
                )

        planner = DeterministicPlanner()
        mode = "deterministic"

    engine = AgentGraphEngine(
        planner=planner,
        constitution=constitution,
        tool_registry=AgentToolRegistry(),
    )
    ctx = ToolExecutionContext.from_snapshot(
        snap, settings=settings, signal_payload=signal
    )
    result = engine.run(snap, context=ctx)
    env = result.snapshot.policy_action_envelope
    actions = [a.model_dump() for a in result.snapshot.actions]
    return {
        "case_id": case_id,
        "mode": mode,
        "envelope_presence": handoff["envelope_presence"],
        "policy_decision_id": getattr(env, "policy_decision_id", "") if env else "",
        "action_proposal_id": getattr(env, "action_proposal_id", "") if env else "",
        "envelope_freshness": getattr(env, "freshness", None) if env else None,
        "recommended_next_step_pl": (signal.get("case_understanding_projection") or {}).get(
            "recommended_next_step_pl"
        ),
        "kalk_offered": "call_kalk_top_quote" in effective.offered,
        "filtered_tools": list(effective.unavailable_notes),
        "first_tool": result.turns[0].tool_name if result.turns else None,
        "hitl_required": result.snapshot.hitl_gate.required,
        "hitl_reason": result.snapshot.hitl_gate.reason,
        "actions": actions,
        "planner_run_budget": result.planner_run_budget,
        "brain1_present": "case_understanding_projection" in signal,
    }


def main() -> int:
    live = "--live" in sys.argv
    out_dir = _HERE.parent
    payload = {
        "slice": "PLANNER-FIDELITY-CLOSEOUT-02",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "fresh38_rerun": False,
        "send_performed": False,
        "cases": {
            "INT-01": run_case("INT-01", service=False, live=live),
            "INT-04": run_case("INT-04", service=True, live=live),
        },
    }
    path = out_dir / "closeout_bounded_proof.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(path), "live": live}, ensure_ascii=False))
    # Hard asserts for fidelity closeout
    c1 = payload["cases"]["INT-01"]
    c4 = payload["cases"]["INT-04"]
    assert c1["envelope_freshness"] == "current", c1
    assert c1["policy_decision_id"] and c1["action_proposal_id"], c1
    assert c1["kalk_offered"] is False or c1["mode"] == "live_llm"
    assert c4["envelope_freshness"] == "current", c4
    assert c4["hitl_required"] is True, c4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
