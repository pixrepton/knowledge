# Raw inventory — reverse-audit category 4: planner tool schema ↔ allowlist ↔ handler ↔ executor

Generated 2026-07-30 during the Domain 3 pass. Evidence: `EV-00139` (+ `EV-00138`, `EV-00140`,
`EV-00141` for the surrounding mechanics).

## Commands used

```
grep -oE '^        "[A-Za-z0-9_]+": \{' agent_runtime/tool_schemas.py   # planner schemas
sed -n '/^HANDLERS/,/^}/p' agent_runtime/tools/handlers.py | grep -oE '^    "[A-Za-z0-9_]+":'
grep -n "MAIL_AGENT_TOOL_ALLOWLIST" -A 20 agent_runtime/constitution_mail.py
grep -n "CHAT_AGENT_TOOL_ALLOWLIST" -A 30 agent_runtime/constitution_chat.py
grep -n "_FORBIDDEN_TOOL_NAMES" -A 8 agent_runtime/policy_guardrails.py
comm -13 schemas.txt handlers.txt   # handlers with no schema
comm -23 schemas.txt handlers.txt   # schemas with no handler
docker exec ... python -m pytest tests/test_tool_reachability_contract.py -q
```

**Scope**: `gmail-agent/tools/gmail_audit/agent_runtime/`.
**Exclusions**: `tests/` excluded from the producer/consumer sets themselves (but the reachability
test IS the verification instrument, recorded separately). `_MOCK_HANDLERS` in
`tools_registry.py` excluded — explicitly test-only by its own docstring ("PR-B deterministic
mock — tests only").

**Methodology note**: a first pass used the regex `^        "[a-z_]*": \{`, which silently
excluded every tool name containing a digit (`check_cp2025_eligibility`) and produced a false
"2 handlers unreachable" result. Corrected to `[A-Za-z0-9_]+`. Recording this because it is
exactly the class of false positive the operator required be manually adjudicated rather than
trusted from raw `rg` output.

## Counts

| Set | Count |
|---|---|
| Planner-facing schemas (`tool_schemas.py` specs) | 23 |
| Registered handlers (`HANDLERS`) | 24 |
| `MAIL_AGENT_TOOL_ALLOWLIST` | 10 |
| `CHAT_AGENT_TOOL_ALLOWLIST` | 23 |
| `_FORBIDDEN_TOOL_NAMES` | 5 |

## Set differences

- **schemas − handlers = ∅** — no schema advertises a tool the runtime cannot execute.
- **handlers − schemas = `{request_human_handoff}`** — 1 item, and it is a *documented deliberate
  exception*, not an accident: it is in neither allowlist, and
  `test_tool_reachability_contract.py:30` names it in `_KNOWN_HANDLER_NOT_ALLOWLISTED` with the
  reason (escalation semantics already covered by the reachable `report_gaps_and_stop`).
  Classification: **INTENTIONAL_INACTIVE**, not `MISSING_PRODUCER`.

## Forbidden tools (never offered, blocked twice)

`send_email`, `auto_send`, `create_offerdto`, `archive_gmail`, `calendar_live_write` — subtracted
at offer time by `filter_planner_allowlist` AND re-checked at execution time by `guard_tool_plan`.
`test_no_forbidden_tool_is_ever_allowlisted` asserts none ever appears in either allowlist.

## Enforcement chain (3 independent layers, all confirmed in code)

1. **Offer time** — `filter_planner_allowlist(available_tools, constitution)` →
   `openai_tool_definitions(filtered)` (`return [specs[name] for name in allowlist if name in specs]`).
2. **Post-plan** — `graph.py:219`: `if plan.tool_name not in available_tools` → `ToolResult(status="error")`
   + `hitl_gate.required=True`, `reason=tool_not_offered:<name>`.
3. **Execution time** — `guard_tool_plan` (forbidden + allowlist re-check) → `HANDLERS.get(name)`
   → explicit `Nieznane narzędzie: <name>` error on miss.

## Test instrument (first TEST evidence in this reconstruction)

`tests/test_tool_reachability_contract.py` — 7 tests, **executed this pass, 7 passed in 1.49s**
inside the live worker container. Locks: allowlist⊆schemas (both allowlists), allowlist⊆handlers
(both), no-silent-drop in `openai_tool_definitions`, no forbidden tool allowlisted, and every
handler either allowlisted or in a named exception list.

The file's own header documents that this exact bug class already caused real production harm
(EVAL-1 RC-2: `generate_draft_reply` was allowlisted without a schema, crashing live planner
turns) — so this is a regression lock on a *proven* failure mode, not a speculative guard.

## Unresolved / open from this category

- Argument-**signature** conformance (schema `parameters` vs what each handler actually reads
  from `plan.arguments`) was NOT mechanically verified per-tool this pass — only the *name*
  chain was. A handler could still read a key the schema never declares. Flagged open.
- `_MOCK_HANDLERS` (2 entries) intentionally excluded as test-only; not cross-checked against
  the real `HANDLERS` for behavioral drift.
