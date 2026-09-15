# Task 013: Harden sample-weight validation

## Status

Review Ready

## Source PRD

- `docs/domain/PROJECT_RULES.md`
- `docs/prd/06-acceptance-criteria.md`

## Goal

Reject invalid sample weights before they can contaminate empirical moments or serialized diagnostics.

## User Value

Researchers receive an actionable error instead of a numerically corrupted model when survey weights contain missing or infinite values.

## Scope

- Validate finite, non-negative, non-zero-sum weights in model fitting and table preparation.
- Regression tests for ordinary and PISA-style preparation paths.

## Out of Scope

- Reweighting or calibration of survey weights.
- Full PISA complex-survey inference.

## Domain Requirement

Validate sample weights before training and do not imply official survey estimates.

## Harness Impact

Adds a feedback sensor for a documented data-quality failure mode.

## Acceptance Criteria

- `NaN` and infinite weights are rejected with actionable errors.
- Negative and all-zero weights remain rejected.
- Standard package verification passes.

## Verification Method

```bash
python -m pytest -q
python -m ruff check learning_energy_model tests examples
python -m mypy learning_energy_model
python -m build --wheel --no-isolation
bash scripts/verify.sh --strict-instance
```

## Done When

- Weight validation is implemented, tested, and documented.
- The verified change is committed and pushed.
