# Task 048: Add named-table fitting to the estimator adapter

Status: Review Ready

## Goal

Let estimator-oriented callers train directly from named mappings or DataFrames
while retaining the same quality and interpretability contract as
`LearningModel.fit_table()`.

## Delivered

- Added `LearningEnergyClassifier.fit_table()`.
- Preserved access to the wrapped model and its aggregate quality report.
- Added prediction and quality-report regression coverage.
- Documented the estimator table entry point.

## Verification

`pytest`, `ruff`, mypy, wheel build/install smoke test, and
`bash scripts/verify.sh --strict-instance`.
