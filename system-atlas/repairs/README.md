# Repairs

Status: `WAVE_01_COMPLETE / WAVE_02_CLOSED`

Scope: repair-program overlay for the immutable Workflow Registry v1 baseline in `knowledge/system-atlas/workflows/`.

This directory is the active repair-program overlay for execution. It still does **not** create a Capability Registry.

Canonical textual entrypoint:

- `REPAIR_PROGRAM_SUPERPLAN.md` - synthesized master plan combining the atlas-coupled plan and the external executable plan.

## Files

- `REPAIR_PROGRAM_SUPERPLAN.md` - canonical synthesized repair plan and execution model.
- `WAVE_02_PROBLEM_ANALYSIS.md` - current problem analysis for the Wave 2 packages and their real blockers.
- `WAVE_02_IMPLEMENTATION_PLAN.md` - canonical Wave 2 execution model: `prove -> decide -> implement`, with defer allowed only for proof-backed large migrations.
- `validate_repairs_overlay.py` - local validator for overlay consistency, references and Workflow Registry v1 coherence checks.
- `EXECUTION_MODEL_VALIDATION.md` - latest validation report for the repair overlay.
- `REPAIR_PROGRAM_PLAN.md` - executable repair plan, capability layers, repair lanes, lifecycle, proof model and completion contract.
- `GAP_DISPOSITIONS.yaml` - disposition for all `78/78` atomic gaps with reachability, future mechanism, capability impact, cluster, lane and proof level.
- `ROOT_CAUSE_CLUSTERS.yaml` - root-cause grouping used to avoid one-fix-per-gap fragmentation.
- `EARLY_DECISION_QUEUE.md` - decisions that must be resolved before decision-dependent repairs can move to `READY`.
- `REPAIR_DAG.yaml` - dependency graph for repair execution, including blocking decisions, file-conflict surfaces, migration needs and proof readiness.
- `_raw/wave-02/rp-06/EXECUTION.md` - current execution record for durable Daszek transport.
- `_raw/wave-02/rp-12/EXECUTION.md` - current execution record for mailbox intake ownership.
- `_raw/wave-02/rp-15/EXECUTION.md` - current execution record for temporal trigger ownership.
- `_raw/wave-02/rp-01/EXECUTION.md` - current execution record for retiring the generic retrieval aggregator.
- `_raw/wave-02/rp-14/EXECUTION.md` - current execution record for the document readiness contract.
- `_raw/wave-02/rp-20/EXECUTION.md` - current execution record for removing dormant GraphRAG enrichment.
- `_raw/wave-02/rp-07/EXECUTION.md` - current execution record for the Calendar read-only lifecycle.
- `_raw/wave-02/exit-gate/` - final Wave 2 test, runtime, parity and validator proof logs.
## Current Summary

- Gaps covered: `78`
- Root-cause clusters: `17`
- Early decisions in synthesized superplan: `17`
- Repair lanes: `5`

Disposition totals:

- `FIX`: `23`
- `CONSOLIDATE`: `19`
- `REPLACE`: `16`
- `DEFER`: `6`
- `REMOVE`: `7`
- `PROVE_AT_RUNTIME`: `1`
- `ACCEPT_RISK`: `2`
- `NO_ACTION`: `4`

Lane totals:

- `FAST`: `15`
- `INTEGRITY`: `22`
- `DECISION_DEPENDENT`: `20`
- `ARCHITECTURAL`: `12`
- `CONSOLIDATION`: `9`

## Baseline Rules

- Workflow Registry v1 remains immutable.
- Repair execution must be append-only relative to that baseline.
- Capability status must be computed from repairs and proof, not handwritten.
- Workflow Registry v2 is a later snapshot created only after a repair wave closes.
- Wave 1 is complete.
- Wave 2 is closed locally.
- Packages closed locally in Wave 2: `RP-01`, `RP-06`, `RP-07`, `RP-12`, `RP-14`, `RP-15`, `RP-20`.
- Packages deferred with proof inside closed packages: automatic per-signal replay for `RP-12`; it requires later idempotency/recovery hardening before enablement.
- Packages with code mutation in Wave 2: `RP-01`, `RP-06`, `RP-07`, `RP-12`, `RP-14`, `RP-15`, `RP-20`.

## Use Order

1. Read `REPAIR_PROGRAM_SUPERPLAN.md`.
2. Read `WAVE_02_PROBLEM_ANALYSIS.md` for the current Wave 2 problem set and corrected decision assumptions.
3. Read `WAVE_02_IMPLEMENTATION_PLAN.md` for the operational Wave 2 proof and implementation sequence.
4. Use `GAP_DISPOSITIONS.yaml` as the canonical per-gap planning input.
5. Use `ROOT_CAUSE_CLUSTERS.yaml` and `REPAIR_DAG.yaml` as the machine execution backbone.
6. Resolve `EARLY_DECISION_QUEUE.md` with current proof before starting any Wave 2 code mutation.
7. Run `python validate_repairs_overlay.py` and inspect `EXECUTION_MODEL_VALIDATION.md` before Wave 2 execution.
8. Treat `REPAIR_PROGRAM_PLAN.md` as the earlier atlas-coupled source plan, now superseded textually by the superplan and the Wave 2 execution documents.
