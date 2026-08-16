# CAPABILITY-28 Diagnostic Proof Summary

## Result

PASS_DIAGNOSTIC

## Baseline Confirmed

- Source: `C:\Users\compg\Desktop\top-code workspace\knowledge\eval\fresh38-recapture-20260808`
- Frozen SUT run_id: `fresh38-recapture-20260808T045859`
- Frozen SUT git_head: `fea458f73dbfc43e8bc98f957cc61b303918f973` dirty_status=`clean`
- Measurement contract: `v2` manifest_sha256=`a8839f595df48d96dd50e77ee123840ab9a27ab1e948222385f08d0ba7c814c7`
- Capture hash: `fresh-full38-results.json` `3c83c9d89d3736a6fce6ecf772c4c197a8e5f325144565830022ee79053cd2ec`
- Judge hash: `fresh-understanding-judge.json` `437965b8ac6540108e19cf56820622fdd3831e5f9b313abbd7327a0060234fa3`
- Outcomes: CLEAN_PASS=10, CAPABILITY=28
- Integrity: capture_gap_cases=0, judge_error_cases=0, unsafe_non_escalation=0, scoring_complete=True

## Current State Checked

- gmail-agent HEAD: `a764fb0f6520a9cb2f04fb3ae880cc68b5071063`; status preserved as found.
- knowledge HEAD: `9d56ada206ffb5b43e637bc1b74bf05ac68f4dd7`; status preserved as found.
- GitNexus refresh: repo-scoped CLI fallback for gmail-agent and knowledge; current code used only as code-path evidence.
- Codebase Memory refresh: direct MCP unavailable; repo-scoped CLI fallback for gmail-agent and knowledge; Fresh38 artifacts read directly because CBM excludes large run artifacts.

## Cluster Counts

- CLUSTER-01:BRAIN1_POLICY_APV2_HANDOFF_MISSING: 9
- CLUSTER-02:CASE_LINK_CONTEXT_SIGNAL_NOT_TRUSTED: 8
- CLUSTER-03:OVERSTRICT_GAP_AND_REVIEW_GUIDANCE: 7
- CLUSTER-04:DRAFT_CONTEXT_BUDGET_OVERFLOW: 1
- CLUSTER-05:DRAFT_REPLY_GATE_AND_PROMISE_SEMANTICS: 2
- CLUSTER-06:EVAL_EXPECTATION_FALSE_NEGATIVE: 1

## Model Vs System

- system/context/draft/handoff product problems: 27/28
- eval expectation/scoring issue: 1/28
- actual model reasoning limitation after complete context and valid contracts: 0/28

## Infra Regression Check

NOT_INFRA_REGRESSION. The frozen source has 38/38 captures, 30/30 Understanding scored, 0 capture gaps, 0 judge errors, 0 unsafe_non_escalation. The 413 draft failures are case-level draft-input/context-budget failures, not a Fresh38 capture/delivery/capacity program regression in the v2 qualification summary.

## What Not To Fix First

- Do not patch planner wording for cases where Understanding/context already introduced bad gaps.
- Do not patch final draft text before fixing draft gate/context budget and upstream case-link truth.
- Do not reopen infrastructure cleanup or provider-delivery programs without a fresh current-HEAD regression proof.
- Do not tune the frozen scorer broadly; adjudicate CTX-04/NEW-03 as narrow expectation evidence only.
