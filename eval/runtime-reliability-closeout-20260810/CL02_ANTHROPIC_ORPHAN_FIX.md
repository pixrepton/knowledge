# CL-02 — Anthropic orphan-work defect: FIXED

## Status

```text
PREVIOUS : PROVEN_OPEN (deferred because the path is config-gated)
NOW      : FIXED
```

The path is unreachable in this deployment (`anthropic_api_key` UNSET). That is not a reason to
leave a proven defect in the tree, so it is repaired rather than annotated.

## What was actually wrong — sharper than previously recorded

The earlier note said "`future.cancel()` may leave a running Anthropic request". True, but
incomplete. The full mechanism:

```python
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    future = executor.submit(fn)
    result = future.result(timeout=hard_timeout)       # hard_timeout = client_timeout + 30 = 60
    ...
    except concurrent.futures.TimeoutError:
        future.cancel()                                # no-op on an already-running task
```

Verified mechanically:

```text
concurrent.futures.Executor.__exit__:
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return False
```

So after the timeout fired and `cancel()` failed, the `with` block **waited for the abandoned
work anyway**. The "hard timeout" therefore bounded *nothing at all*: it only changed which
exception was recorded, while spending a thread per attempt. The call's real duration was
whatever the underlying HTTP request took.

And underneath it there was a second retry loop:

```text
_call_with_retry   max_retries = 3            -> up to 4 attempts
TopInstalLLMClient max_retries = min(3, 4)=3  -> up to 3 HTTP attempts each
                                              -> up to 12 HTTP requests per logical call
```

with nothing observing the multiplication.

## Repair

| change | effect |
|---|---|
| `_call_with_retry` calls `fn()` directly; executor removed; `hard_timeout` parameter deleted | nothing can be abandoned; a parameter that guaranteed nothing no longer implies a guarantee |
| `_anthropic_client(..., max_retries=1)` by default | one visible retry layer instead of two multiplying ones |
| `_call_anthropic_raw_text` derives `timeout_sec` from `attempt_timeout_sec(settings.http_timeout)` | the per-attempt bound comes from the layer that can actually enforce it — the HTTP client — and is clamped by the stage budget |
| budget exhaustion raises a structured `LLMTimeoutError` with `terminal_failure_reason` | previously it fell through to `LLMError("LLM call failed (unknown reason)")`, erasing the one fact that explained the failure |

The last row was found by the tests below, not by inspection: when the loop stopped on budget
exhaustion *before any attempt ran*, `last_exc` was `None`.

## Why not simply move the executor elsewhere

`_call_with_retry` cannot enforce a per-attempt bound at all: `fn` is a blocking HTTP call, and
only the callee's own socket timeout can stop it. Any wrapper that claims otherwise is decoration.
So ownership was moved to the layer that genuinely controls the request, matching the router path,
where `requests.post(timeout=...)` is likewise the real bound.

## Tests

`tools/gmail_audit/tests/test_anthropic_path_deadline.py` — 11 tests:

| requirement | test |
|---|---|
| structural: no executor, no `submit`, no `cancel` (AST-checked) | `test_call_with_retry_no_longer_uses_an_executor` |
| the hollow parameter is gone | `test_hard_timeout_parameter_is_gone` |
| single visible retry layer | `test_anthropic_client_does_not_run_a_second_retry_loop` |
| fast success | `test_fast_success_returns_without_retrying` |
| fast provider failure then success | `test_retryable_failure_is_retried_then_succeeds` |
| permanent error is not retried | `test_non_retryable_llm_error_propagates_immediately` |
| timeout → bounded terminal failure | `test_timeout_is_retried_and_then_fails_terminally` |
| deadline exhaustion → structured terminal result | `test_retries_stop_when_the_budget_cannot_fund_an_attempt` |
| attempt refuses to start with no budget | `test_anthropic_attempt_refuses_to_start_with_no_budget` |
| no abandoned work | `test_no_orphan_work_survives_the_call` |
| the concurrency semaphore is not leaked on failure | `test_provider_semaphore_is_released_on_failure` |

No provider is contacted; all failure modes are injected.

## Live proof

Deliberately not attempted. `anthropic_api_key` is UNSET, so there is no Anthropic credential to
prove anything against, and manufacturing one would be theatre. The path's inactivity is itself
verified: `anthropic_configured(settings)` is False in the running container, so
`run_central_structured_stage` takes the router branch. Determinism plus that configuration check
is the honest bound of what can be proven here.
