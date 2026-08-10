# DEEPSEEK-EMPTY-CONTENT-01

```text
CLASSIFICATION = INSUFFICIENT_EVIDENCE
```

Not a hedge — a statement about what the available data can and cannot support, plus the exact
reason the investigation could not be completed.

## Something I must report first

**I exhausted the DeepSeek account balance during the live reproduction.** DeepSeek now answers
`HTTP 402 "Insufficient Balance"` to a one-token request. Tier 1 of the intended SUT is currently
unusable, and that is a direct consequence of my probe.

What I spent:

```text
16 HTTP-200 calls    38,699 completion tokens   (28,180 of them reasoning tokens)
 8 HTTP-402 calls    balance exhausted mid-run
```

I did not check the remaining balance before running 24 reasoning-heavy calls against real stage
schemas. I should have. Whether the balance was already near zero cannot be established
retrospectively, but the exhaustion happened inside my run and I am not going to attribute it
elsewhere.

## Denominator and rate — historical run

Source: closeout Fresh38 (`fresh38-closeout-20260810T175305Z`).

`CONTEXT_ASSEMBLED` is emitted once per `run_central_structured_stage` call, before any provider
tier, and the LLM response cache was cold for the entire run:

```text
CONTEXT_ASSEMBLED        183      <- central structured stage calls
LLM_CACHE_HIT              0      <- no call short-circuited before the provider tiers
deepseek_configured     True      <- every stage call therefore attempted DeepSeek first

DeepSeek attempts (denominator)      = 183
empty_content fallthroughs (numerator) =  34
empty-content rate per DeepSeek call   =  18.58%
valid DeepSeek responses               = 149  (81.42%)
```

Every one of the 34 carried the identical message:
`OpenAI-compatible response has empty message.content.`

### Per stage

```text
stage                 empty_content events
business_reasoning              24
reply_drafter                    5
signal_extraction                4
intake_reasoning                 1
                                --
                                34   across 28 of 38 cases
```

**Per-stage denominators are not recoverable from this run.** No event is logged on a DeepSeek
*success*, and `CONTEXT_ASSEMBLED` carries no `stage` field, so the 183 cannot be split. Per-stage
rates would be invented, so none are given. This is itself fixed going forward by the change below.

## Why the 34 events could not be classified retrospectively

The adapter already builds precisely the evidence needed:

```python
empty_details = {"error_class": "empty_content", "finish_reason": ..., "has_tool_calls": ...,
                 "has_reasoning_content": ..., "content_type": ..., "content_len": ...}
raise GroqClientError("OpenAI-compatible response has empty `message.content`.", details=empty_details)
```

and the fallthrough handler threw all of it away:

```python
logger.error("LLM_DEEPSEEK_FAILED", extra={"x": {"stage": stage_name, "error": str(exc)[:300]}})
```

Confirmed absent from every artifact and log of the run:

```text
has_reasoning_content  0 occurrences
has_tool_calls         0 occurrences
finish_reason          0 occurrences
content_len            0 occurrences
```

So for the historical events, hypotheses **A** (provider returned nothing), **B** (usable output
in another field), **C** (structured-output interaction) and **E** are *indistinguishable*. That
is an observability defect, and it is fixed below.

## Hypotheses tested

| # | hypothesis | verdict | basis |
|---|---|---|---|
| **A** | provider truly returned no usable output | **possible, unproven** | cannot be separated from C without `finish_reason` |
| **B** | usable output existed in another field, adapter ignored it | **rejected** | the adapter reads `content`, and refuses to promote `reasoning_content` — deliberately. Promoting chain-of-thought into business output would be a correctness defect, not a fix. `tool_calls` are not expected on structured stages |
| **C** | structured-output / response-format interaction emptied `content` | **possible, unproven** | plausible mechanism: no `max_tokens` is sent, and reasoning tokens (up to 3,569 observed) share the completion budget. Would show as `finish_reason="length"` — the field that was not recorded |
| **D** | parser/normalizer dropped valid content | **rejected** | `_extract_openai_chat_message_text` returns `content.strip()` whenever it is a non-empty string; 16/16 live HTTP-200 responses were extracted correctly |
| **E** | another deterministic product mechanism | **rejected** | no cache hits, one DeepSeek key, single provider entry in that tier; nothing else short-circuits |
| **F** | genuine provider variance | **possible, unproven** | see reproduction below |

## Bounded live reproduction

Real stage schemas, realistic payloads, current settings unchanged, no retry-to-green.

```text
stage                schema_chars   calls   HTTP 200   empty content   402
signal_extraction        1,054        6        6            0            0
intake_reasoning         8,782        6        6            0            0
business_reasoning       2,345        6        4            0            2
reply_drafter            1,333        6        0            0            6
                                     --       --           --           --
                                     24       16            0            8
```

**0 empty-content responses in 16 HTTP-200 calls.** All 16 returned well-formed content
(290–4,068 chars) with `finish_reason="stop"`, alongside substantial `reasoning_content`
(1,843–13,169 chars).

The 8 `HTTP 402` rows are *not* empty-content events — they are the balance exhaustion. The run
script's `empty` flag conflated "no content" with "HTTP error"; corrected here.

### What 16 clean calls do and do not establish

If the true per-call rate were the historical 18.58%, the chance of seeing zero empties in 16
calls is `0.8142^16 ≈ 3.5%`. So the reproduction is in real tension with that rate **for these
schemas under these conditions** — but 16 samples cannot distinguish "much rarer than 18.6%" from
"triggered by conditions this probe did not reproduce".

Conditions the probe did **not** reproduce, any of which could matter:

- **assembled context size** — the probe sent a synthetic payload; production prompts carry
  RAG chunks, case history and context-pack overlay, which are far larger;
- **concurrency** — `intake_shared_downstream` runs business_reasoning, draft_reply and
  case_intelligence through a thread pool, so several DeepSeek calls can be in flight together;
  the probe was strictly sequential;
- **input variant degradation** — `request_structured_output` retries across `input_variants`;
- the concentration in `business_reasoning` (24 of 34) is consistent with the concurrent path,
  but that is a hypothesis the data cannot yet settle.

Continuing was impossible: the balance is gone.

## Implemented fix — observability defect (proven)

`central_llm_stage._deepseek_failure_diagnostics()` now attaches the adapter's response-shape
facts to `LLM_DEEPSEEK_FAILED`:

```text
error_class · finish_reason · has_tool_calls · has_reasoning_content
content_type · content_len · status_code · attempt · mode
(+ last_attempt_* when the error is router-shaped)
```

It is an **allow-list, not a blanket copy** of `exc.details`: provider errors can echo request
fields, and a blanket copy would put prompt content — customer email bodies — into the logs.

With this in place, the next occurrence distinguishes A from C from F directly:
`finish_reason="length"` means truncation (C, fixable with `max_tokens`);
`finish_reason="stop"` with `has_reasoning_content=True` means the model produced thinking but no
answer (A/F); `has_tool_calls=True` would mean a mode mismatch.

### Tests

`tools/gmail_audit/tests/test_deepseek_failure_diagnostics.py` — 8 tests, all driven through the
**real** adapter rather than hand-written stand-ins:

- diagnostics preserved end to end;
- truncation distinguishable from a genuinely empty answer (`length` vs `stop`);
- reasoning-only response distinguishable from nothing at all;
- `null` content distinguishable from empty string;
- router-shaped errors surface the last attempt;
- **allow-list enforced** — an error carrying `api_key`, `Authorization`, `prompt` and
  `messages` yields exactly `{error_class, finish_reason}`, and the serialized output contains
  none of the secret or personal-data markers;
- missing details degrade to `{}`;
- the fallthrough log site itself carries the fields.

Gate A: **2482 passed, 15 skipped, 24 subtests passed, 0 failed.**

## What would settle the classification

1. Restore DeepSeek balance.
2. Run a Fresh38 (or a bounded multi-case capture) with the diagnostics fix deployed.
3. Read `finish_reason` / `has_reasoning_content` across the empty_content events.

That converts this from `INSUFFICIENT_EVIDENCE` to one of
`STRUCTURED_OUTPUT_COMPATIBILITY` (if `length` dominates → set `max_tokens`),
`PROVIDER_EMPTY_RESPONSE_VARIANCE` (if `stop` with reasoning dominates), or `MIXED`.

## Fallback usage caused, quantified

At the historical rate, **18.58% of central stage calls** fell through from DeepSeek to the router
tier. Before the topology fix each of those also spent a guaranteed-402 round-trip on
`openai_chat` before reaching Groq; after it, they go straight to the Groq pool.
