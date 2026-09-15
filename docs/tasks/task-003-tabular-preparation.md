# Task 003: Add reusable tabular-data preparation

## Status

Review Ready

## Source PRD

- `docs/prd/ROADMAP.md`
- `docs/prd/04-content-model.md`
- `docs/domain/PROJECT_RULES.md`

## Goal

Provide a dependency-light helper that extracts named feature, target, and optional weight columns from user tables without bundling or retaining raw data.

## User Value

Users can prepare their own CSV-loaded or DataFrame-like data before calling the model, including survey-style sample weights.

## Scope

- Named-column extraction for mappings and table-like objects.
- Shape, duplicate-name, infinite-value, and sample-weight validation.
- A `PreparedData` result containing arrays and metadata.
- Tests and public exports.

## Out of Scope

- Downloading or redistributing PISA data.
- Dataset-specific PISA variable codes.
- Missing-value imputation and threshold learning, which remain governed by `DataConfig` and `BinaryPreprocessor`.

## Domain Requirement

Preserve raw-data boundaries and validate weights without claiming full complex-survey inference.

## Harness Impact

Adds deterministic feedback sensors for the user-data preparation boundary.

## Acceptance Criteria

- Named table columns can be converted to `X`, `y`, and optional `sample_weight`.
- Invalid columns and weights fail with actionable `ValueError`s.
- Raw input tables are not stored in `PreparedData` or model artifacts.
- Standard package verification passes.

## Verification Method

```bash
python -m pytest -q
python -m ruff check learning_energy_model tests
python -m mypy learning_energy_model
python -m build --wheel --no-isolation
bash scripts/verify.sh --strict-instance
```

## Done When

- The helper is exported and tested.
- Documentation and roadmap reflect the implemented boundary.
- The verified change is committed and pushed.
