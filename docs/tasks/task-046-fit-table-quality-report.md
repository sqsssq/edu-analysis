# Task 046: Retain named-table quality evidence

Status: Review Ready

## Goal

Make the aggregate validation performed by `LearningModel.fit_table()`
auditable after fitting and after artifact reload, without retaining raw table
rows.

## Delivered

- Expose the latest successful `TabularQualityReport` as
  `LearningModel.last_quality_report`.
- Serialize and restore the report with the model artifact.
- Add regression coverage for report contents and round-tripping.
- Document the report fields and the raw-data retention boundary.

## Verification

`pytest`, `ruff`, mypy, wheel build, and
`bash scripts/verify.sh --strict-instance`.
