# TOOL_AVAILABILITY_MATRIX

| Tool | Config gate | Before | After (no URL) | After (URL set) |
|---|---|---|---|---|
| `call_kalk_top_quote` | `KALK_TOP_BASE_URL` / `kalk_top_base_url` | offered on allowlist | **filtered** (`TOOL_CONFIGURATION_MISSING`) | offered |
| `propose_mutation` | mutation freeze (default on) | mail: not on allowlist | filtered if present | same |
| send tools | send freeze | forbidden | filtered | filtered |

Sources of truth consulted:

1. constitution allowlist (`constitution_mail` / `constitution_chat`)
2. `filter_planner_allowlist` forbidden set
3. runtime settings (`AgentRuntimeSettings`)
4. per-turn effective list in `graph._run` + `OpenAIToolPlanner.plan_next_tool`

No per-turn network health check — config presence only.
