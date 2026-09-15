# Task 018: Add pre-training tabular quality evidence

## Status

Review Ready

## Objective

Give callers an aggregate quality report before binary preprocessing changes or rejects a local dataset.

## Scope

- Add `validate_tabular_data` and `TabularQualityReport`.
- Report row count, required columns, missingness, infinite values, shape problems, and weight validity.
- Keep missing values reportable rather than automatically treating them as errors; the configured preprocessor owns imputation policy.

## Out of scope

- Dataset-specific sentinel-code inference.
- Duplicate-key or complex survey validation.
- Retaining raw rows in results or artifacts.

## Acceptance criteria

- Valid tables with missing values can be reviewed before fitting.
- Invalid required columns, row shapes, infinite values, and weights produce explicit issues.
- The report exports through the existing aggregate result interface.
- Standard package verification passes.

## Handoff

PISA mappings should replace source-specific missing codes before calling this helper, using the matching OECD codebook.
