# Deploy token tiers (P1-ID-2)

Production and local stacks use **three write identities** between Daszek (WordPress), Node B (`gmail-agent`), and RAG. Each tier has a distinct secret and allowed surface.

## Tier map

| Tier         | Env var (Node B)              | Env var (Daszek WP)                       | Who uses it                                   | Allowed writes                                                      |
| ------------ | ----------------------------- | ----------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------- |
| **Operator** | Session + CSRF in browser     | `daszek_check_csrf` + `daszek_check_auth` | Human in Biurko UI                            | All operator POST (tasks, proposals, merge, agent-chat proxy)       |
| **Bridge**   | `DASZEK_BRIDGE_TOKEN`         | `DASZEK_BRIDGE_TOKEN`                     | Legacy bridge queue drain, compat automations | Bridge queue complete, selected v2 ingress when service token unset |
| **Service**  | `DASZEK_NODE_B_SERVICE_TOKEN` | `DASZEK_NODE_B_SERVICE_TOKEN`             | Node B → WP snapshot push                     | `operational-feed`, `ingress-quality`, `system-health` POST only    |

Registry / internal API (Node B inbound):

| Tier             | Env var                                                      | Consumers                                                                                       |
| ---------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| **Registry**     | `NODE_B_REGISTRY_TOKEN`                                      | `cieplo-orchestrator`, RAG context pack fetch, Daszek → Node B proxy (`daszek_node_b_get_json`) |
| **Internal API** | `DASZEK_NODE_B_API_TOKEN` / `GMAIL_AGENT_INTERNAL_API_TOKEN` | Agent runtime authz (`agent_runtime/authz.py`)                                                  |

## Production procedure

1. Generate **distinct** random secrets per tier (do not reuse one token for all).
2. On **Node B VPS** (`/etc/topinstal/gmail-agent.env`):
   - `NODE_B_REGISTRY_TOKEN`
   - `DASZEK_BRIDGE_TOKEN`
   - `DASZEK_NODE_B_SERVICE_TOKEN`
   - `DASZEK_NODE_B_API_TOKEN` (optional; falls back to registry token in proxy)
3. On **Daszek WP** (`wp-config` or env plugin):
   - Mirror `DASZEK_BRIDGE_TOKEN`, `DASZEK_NODE_B_SERVICE_TOKEN`, and `node_b_api.api_token` (= registry or dedicated API token).
4. On **RAG VPS**: `GMAIL_AGENT_NODE_B_TOKEN` = `NODE_B_REGISTRY_TOKEN`.
5. On **Cieplo orchestrator**: `NODE_B_REGISTRY_TOKEN` match.

## Local dev mirror

`scripts/sync-local-stack-env.ps1` copies **one** `NODE_B_REGISTRY_TOKEN` from `.env.local-vps` into audit + Daszek local env for all three bridge/service slots — **convenience only**, not production policy.

```powershell
pwsh -File scripts/sync-local-stack-env.ps1
```

After sync, recreate Daszek WP + worker containers so env is picked up.

## Verification

```bash
# Node B health (registry token)
curl -s -H "Authorization: Bearer $NODE_B_REGISTRY_TOKEN" http://127.0.0.1:8766/health

# CSRF audit (operator POST gaps)
python daszek/scripts/audit_csrf_post_handlers.py
```

## Proof token

`DEPLOY_TOKEN_TIERS_DOC_OK` — this document + distinct prod secrets configured on VPS.
