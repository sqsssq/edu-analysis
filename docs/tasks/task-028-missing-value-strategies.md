# Task 028: Add explicit missing-value strategies

## Status

Review Ready

## Source PRD

- `docs/prd/ROADMAP.md`
- `docs/prd/06-acceptance-criteria.md`

## Goal

Let callers choose a documented missing-value policy while keeping binary
preprocessing deterministic and inspectable.

## Scope

- Keep `error` as the fail-fast default.
- Add `median`, `mean`, and `zero` imputation strategies.
- Expose the same choices through the CLI.
- Preserve row count and record the selected strategy in `DataConfig`.

## Out of Scope

- Automatic interpretation of PISA nonresponse codes.
- Silent row dropping or complex-survey missing-data inference.

## Acceptance Criteria

- Each supported strategy gives deterministic output on missing numeric values.
- Invalid strategy names fail during `DataConfig` construction.
- CLI choices and public documentation agree with the implementation.
- Standard package verification passes.

## Done When

- The strategies are implemented, tested, documented, committed, and pushed.
