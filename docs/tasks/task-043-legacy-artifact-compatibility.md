# Task 043: Preserve legacy artifact loading

## Status

Review Ready

## Source PRD

- `docs/prd/04-content-model.md`
- `docs/prd/06-acceptance-criteria.md`

## Goal

Keep saved models loadable when new calculation and Monte Carlo quality settings
are introduced in later package versions.

## Scope

- Backfill defaults for settings absent from older artifacts.
- Add a regression test that simulates an artifact from before those settings existed.

## Out of Scope

- Migrating arbitrary future schema changes automatically.
- Serializing custom third-party components.

## Acceptance Criteria

- Legacy artifacts without the new settings load with documented defaults.
- Current save/load behavior remains unchanged.
- Standard package verification passes.

## Done When

- Legacy loading is implemented, tested, documented, committed, and pushed.
