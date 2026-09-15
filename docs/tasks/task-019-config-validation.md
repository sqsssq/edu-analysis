# Task 019: Validate model configuration early

## Status

Review Ready

## Objective

Reject invalid variable names and explicit threshold values when `DataConfig` is constructed.

## Acceptance criteria

- Empty names and target/feature collisions fail with actionable errors.
- Explicit feature and target thresholds must be finite numeric values.
- Existing tests, lint, type checks, and HarnessWeaver verification pass.

## Handoff

Data-dependent threshold checks remain part of the fitted preprocessor because they require observing the training table.
