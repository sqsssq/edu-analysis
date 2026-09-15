# Task 029: Make calculation-path selection explicit

## Status

Review Ready

## Source PRD

- `docs/prd/ROADMAP.md`
- `docs/prd/09-decision-log.md`

## Goal

Make automatic exact-versus-Monte-Carlo selection explicit and reproducible in
the public API and saved artifacts.

## Scope

- Add `calculation="auto"`, `"exact"`, or `"monte_carlo"` to `LearningModel`.
- Keep `auto` as the default and select from `max_exact_nodes`.
- Fail clearly when exact calculation is forced above the configured threshold.
- Persist the choice through model save/load and expose it in CLI configuration.

## Acceptance Criteria

- Automatic selection preserves current behavior.
- Both forced paths produce the requested calculation diagnostics.
- Saved models preserve the selected path.
- Standard package verification passes.

## Done When

- The path control is implemented, tested, documented, committed, and pushed.
