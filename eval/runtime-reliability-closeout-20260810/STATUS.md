# RUNTIME RELIABILITY CLOSEOUT 01 — status

```text
RUNTIME_RELIABILITY_CLOSEOUT     = BLOCKED_OPERATOR_ACTION
CAPABILITY_QUALIFICATION_READINESS = HOLD
```

## Why not PASS

Every engineering condition for `PASS` is met:

| condition | state |
|---|---|
| CL-01 mechanically resolved | yes — proven `FIX_REQUIRED`, then fixed |
| CL-02 fixed | yes |
| CL-03 reproducible | yes — tracked canonical `scripts/fresh38/` |
| CL-04 no manual SUT blind spot of the proven class | yes — derived 361-file subtree, blind-spot test passes |
| CL-05 pool fully understood, no hidden unknown credential state | yes — every slot classified; the product defect it exposed is fixed |
| CL-06 reconciled | yes — disjoint sets, overlap 0 |
| targeted tests green | yes — 124 passed, 0 failed |
| Gate A green | yes — 2474 passed, 15 skipped, 24 subtests, 0 failed |
| no unresolved proven product runtime defect in scope | yes — `PROVEN_OPEN = NONE` |

What remains is **not** a code or runtime defect. It is two credential/billing facts that cannot
be changed without operator-held secrets or billing access, and the closeout rule is explicit that
this case is `BLOCKED_OPERATOR_ACTION` rather than `PASS`.

## The blocker

```text
1. openai_chat (PRIMARY provider) has no credits
   slot    OPENAI_COMPAT_API_KEY   endpoint https://openrouter.ai/api/v1
   proof   HTTP 402 "Insufficient credits. This account never purchased credits."
   action  purchase credits for that account, OR repoint the primary at a funded provider
   effect  until then every stage spends one round-trip on a guaranteed 402 before falling back

2. GROQ_API_KEY slot 4 is rejected
   slot        GROQ_API_KEY_SLOT_4   fingerprint d8c3ee154fce   (value never disclosed)
   proof       HTTP 401 "Invalid API Key"
   action      remove that entry from the GROQ_API_KEY pool in .env.local-vps, or replace it
   effect      one wasted attempt per call that reaches it; no longer aborts the chain
```

Slots 1–3 and `deepseek` are healthy. `cerebras`, `nvidia`, `anthropic` are unconfigured by
design and correctly skipped.

Neither item was actioned: item 1 needs billing access, and item 2 is a live credential-file edit
that belongs to the operator. No configuration file was modified by this closeout.

## Measured state

```text
PRE_FIX        32/38 =  84.21%   fresh38-canonical-clean-20260810T011858Z
POST_FIX       38/38 = 100.00%   fresh38-postfix-20260810T064731Z
POST_CLOSEOUT  38/38 = 100.00%   fresh38-closeout-20260810T175305Z
```

Three separate frozen SUTs, zero artifact reuse, no external retry-to-green anywhere. The PRE-FIX
lock re-verified `PASS` after every subsequent run.

## Capability readiness

`HOLD`, per the closeout rule, because the status is not `PASS`.

The hold is on the *provider pool*, not on the runtime work. Capability qualification measures
answer quality, and running it against a chain whose primary is dead and whose fallback pool is
rate-limiting would measure the pool as much as the product. The two operator actions above are
what move this to `READY`.

`CAPABILITY-QUALIFICATION-20260809` remains `BLOCKED` with an open blocker. The Understanding
judge and v5 capability scoring were not run.

## Proven open defects

```text
PROVEN_OPEN = NONE
```

within this closeout's bounded scope (timeout ownership, executor cancellation, Fresh38 runner
identity, Fresh38 SUT fingerprint, provider credentials/capacity).

Known boundaries, recorded rather than hidden — none is a defect of the proven class:

- the SUT fingerprint is directory-based, not an import-graph closure (a runtime module living
  outside `tools/gmail_audit` would still be missed; nothing on the capture path does that);
- non-`.py` runtime inputs inside the tree (e.g. `config/agent_goals.yaml`) are not fingerprinted,
  but they are not hot-synced either, so they can only change via a rebuild — which changes the
  container image id that *is* in the fingerprint;
- the 180 s stage budget and 90 s planner budget are derived from the current chain shape and have
  not been validated against a sustained multi-provider outage in production traffic.
