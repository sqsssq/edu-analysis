# Task 021: Add a local CSV CLI workflow

## Status

Review Ready

## Objective

Provide a repeatable command-line path for callers who want to train and use a model without writing Python glue code.

## Scope

- Add `python -m learning_energy_model fit` for numeric CSV training.
- Add `python -m learning_energy_model predict` for saved-model probability output.
- Register the `learning-energy-model` console script.
- Emit aggregate fit/quality JSON only; never include raw rows in output.

## Out of scope

- Direct SAS/SPSS CLI parsing or automatic PISA variable mapping.
- Hyperparameter search and official survey inference.

## Acceptance criteria

- A clean numeric CSV can be trained into a versioned model artifact.
- Prediction output contains class probabilities and a binary cutoff prediction.
- Invalid input produces an actionable error through the quality checks.
- Standard package verification passes.

## Handoff

Use `PISAMapping` and the Python API for SAS/SPSS or codebook-backed PISA workflows; the CLI intentionally stays dependency-light.
