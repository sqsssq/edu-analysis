# Task 045: Add the named-table fitting API

## Status

Review Ready

## Source PRD

- `docs/API.md`
- `docs/prd/01-mvp-scope.md`

## Goal

Provide one high-level call for named-table quality validation, preparation,
ordinary row-weight extraction, and model fitting.

## Scope

- Add `LearningModel.fit_table()` for mappings and DataFrames.
- Reuse existing aggregate quality and tabular preparation contracts.
- Preserve selected feature and weight names in `DataConfig`.

## Out of Scope

- Automatic source-specific missing-code inference.
- Replacing the lower-level `fit()` API.

## Acceptance Criteria

- A named mapping can be fit with one public call.
- Invalid quality input fails before model fitting.
- Standard package verification passes.

## Done When

- The convenience API is implemented, tested, documented, committed, and pushed.
