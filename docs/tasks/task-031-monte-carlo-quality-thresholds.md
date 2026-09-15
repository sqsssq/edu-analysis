# Task 031: Add Monte Carlo quality thresholds

## Status

Review Ready

## Source PRD

- `docs/prd/ROADMAP.md`
- `docs/prd/06-acceptance-criteria.md`

## Goal

Make sampled fit results self-auditing by evaluating R-hat, effective sample
size, and Monte Carlo standard error against caller-configured thresholds.

## Scope

- Add finite positive thresholds to `LearningModel`.
- Record threshold values and boolean checks in fit diagnostics.
- Add a warning when a sampled run fails a configured check.
- Persist thresholds and expose them through the CLI.

## Out of Scope

- Claiming universal scientific cutoffs; defaults are operational guardrails.
- Replacing domain-specific convergence review.

## Acceptance Criteria

- Exact fits are not incorrectly marked as sampled-quality failures.
- Monte Carlo fits expose quality checks, thresholds, and warnings when needed.
- Saved models preserve threshold settings.
- Standard package verification passes.

## Done When

- Quality thresholds are implemented, tested, documented, committed, and pushed.
