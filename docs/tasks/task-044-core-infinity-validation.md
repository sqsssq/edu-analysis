# Task 044: Reject infinity in core preprocessing

## Status

Review Ready

## Source PRD

- `docs/prd/06-acceptance-criteria.md`
- `docs/prd/04-content-model.md`

## Goal

Ensure direct Python API callers receive the same infinity validation as callers
who use the tabular quality report first.

## Scope

- Reject positive and negative infinity in core numeric input conversion.
- Preserve NaN handling through the configured missing-value strategy.
- Add a regression test and acceptance evidence.

## Out of Scope

- Automatically translating source-specific missing codes.
- Changing the configured NaN strategies.

## Acceptance Criteria

- Direct preprocessing fails clearly on infinity in features or target.
- Missing values remain handled by `error`, `median`, `mean`, or `zero`.
- Standard package verification passes.

## Done When

- Infinity validation is implemented, tested, documented, committed, and pushed.
