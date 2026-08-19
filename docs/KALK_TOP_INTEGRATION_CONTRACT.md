# Kalk-top integration contract

Status: canonical contract for the `call_kalk_top_quote` integration path.
Source: `P1_KALK_TOP_CLOSEOUT = PASS` (2026-08-19), gmail-agent `bbf0006` + workspace `ed490a2`.
Re-verify against current source/runtime before using any fact here as live proof.

## Scope

The integration path is:

```text
call_kalk_top_quote
  -> handler
  -> kalk_top_client
  -> calculate-offer endpoint
```

Owner of domain logic: `kalk-top`. Owner of the route/config overlay in the local
stack: the workspace local runtime, not `kalk-top`.

## Canonical route

- Production contract: `POST {base}/wp-json/topinstal/v1/calculate-offer`.
- `index.php?rest_route=...` is an equivalent WP REST form used by health/e2e
  candidates, but is **not** the canonical production route.
- `ROUTE_OWNER = LOCAL_RUNTIME_ROUTER`; `ROUTE_FIX_FINAL = YES`.
- The final fix lives in the workspace local overlay
  (`scripts/kalk-top-local/_router.php` mapping `/wp-json/*` plus a volume in
  `docker-compose.kalk-top-local.yml`), not inside `kalk-top`.

## Auth configuration chain

Names/status only, never secret values:

```text
KALK_TOP_AGENT_KEY (env file) -> compose host interpolation
  -> env_file -> container KALK_TOP_AGENT_KEY
  -> PID1 alias KALKTOP_AGENT_KEY
  -> configure-runtime-wp.php -> WP option
  -> SecretStore precedence: constant -> env TOPINSTAL_CALC_AGENT_API_KEY -> option
```

`AUTH_CONFIG_PARITY = PASS`. The prior `AGENT_KEY_INVALID` failure was caused by a
stale container plus an empty host `KALKTOP_AGENT_KEY`; recreate alone was not
enough without the PID1 alias.

## Business eligibility vs technical readiness

These are two separate gates and must stay separate:

- **Business eligibility** — is the case allowed to attempt a quote now? Uses
  authoritative journey/case state, quote intent, Brain1 readiness, next action,
  and blocking contradictions.
- **Technical readiness** — are all true-required technical inputs present as real
  case facts?

Do not use Fresh38 fixture fields (`phone`, `address`, `OZC`) as universal required
inputs. For the current client path the only true-required technical input is
`heated_area_m2 > 0`; OZC/city/phone are not technical-required.

## No-fabrication

`KALK_TOP_NO_FABRICATION = PASS`. Do not silently substitute:

- `dhw.persons = 4`
- `building_type = single_family`

unless an existing, explicitly proven domain-default contract allows it and can
distinguish customer fact vs document-derived fact vs system/domain default.

## Enforcement points

- **Primary (pre-planner):** an ineligible case is not offered to the planner.
- **Secondary (handler, fail-closed):** direct/unexpected invocation requires valid
  case identity, true-required inputs, no fabricated facts, and a valid payload,
  otherwise it returns an attributable `ToolResult`/structured rejection with no
  HTTP call.

## Causal separation

Two independent problems were proven and must not be merged:

- Five residual cases (`INT-05`, `DOC-02`, `NEW-03`, `INT-01`, `CTX-03`):
  `FIRST_DIVERGENCE = upstream eligibility / planner availability`. Their endpoint
  call was not allowed.
- Historical `8/8 calls, 0 valid responses`: a separate downstream integration
  anomaly, not the reason those five cases failed.

## Live integration result

- `KALK_TOP_LIVE_INTEGRATION = PASS`
- `BUSINESS_SCHEMA_SUCCESS = PASS`
- `TOOL_RESULT_CONSUMPTION = PASS`
- `LIVE_CALL_COUNT = 3` (max allowed 4):
  - Call 1: route diagnosis -> `HTTP 200 text/html`, not JSON (`ROUTE_MISMATCH`).
  - Call 2: `rest_route` -> `HTTP 403 JSON AGENT_KEY_INVALID` (`AUTH/CONFIGURATION`).
  - Call 3: final route + auth parity -> `HTTP 200 application/json` offer.
- Success keys observed: `schemaVersion`, `traceId`, `engineering`, `pricing`,
  `warnings`, `assumptions`, `engineMeta`; no `errorCode`; `pricing.totals` present.

## Gate A

`GATE_A = PASS` (gmail-agent): `2541 passed / 0 failed` at P1 closeout.

## Proven debt not fixed

See `knowledge/docs/PROVEN_DEBT.md` for OfferDTO/offer_snapshot convergence,
EV-00140/select_sub_agent scope, quote-intent model limitation, and the local
`entrypoint-local.sh` fallback.
