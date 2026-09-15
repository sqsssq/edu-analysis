# Task 030: Persist reviewed PISA mapping contracts

## Status

Review Ready

## Source PRD

- `docs/reproduction/PISA_BENCHMARK_CONTRACT.md`
- `docs/prd/ROADMAP.md`

## Goal

Make explicit PISA variable mappings reusable and auditable without storing raw
PISA observations in the repository or model artifacts.

## Scope

- Add provenance metadata to `PISAMapping`.
- Support JSON-compatible `to_dict`, `from_dict`, `save`, and `load` operations.
- Test a mapping round trip and document codebook review responsibility.

## Out of Scope

- Inferring variable names from a PISA file.
- Downloading, bundling, or redistributing OECD data.

## Acceptance Criteria

- A mapping contract round-trips without loss of selected columns, missing codes,
  weights, or provenance metadata.
- The contract contains no row-level data.
- Standard package verification passes.

## Done When

- The reusable mapping contract is implemented, tested, documented, committed, and pushed.
