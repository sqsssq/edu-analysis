# Task 057: Add an experimental continuous Gaussian energy model

## Status

Review Ready

## Source PRD

- `docs/prd/01-mvp-scope.md`
- `docs/prd/03-feature-design.md`
- `docs/domain/PROJECT_RULES.md`

## Goal

Provide a separate, non-binarizing continuous model for researchers who need
to fit jointly distributed numeric variables while preserving the binary
paper-reproduction API and its semantics.

## Scope

- Add a Gaussian/quadratic energy model with closed-form weighted fitting.
- Expose mean, covariance, precision, conditional interactions, sampling,
  conditional means, analysis, and save/load.
- Keep source rows out of serialized artifacts.
- Document this as an experimental continuous family, not as a replacement for
  the binary paper model.

## Out of Scope

- Mixed binary-continuous nodes.
- Nonlinear, non-Gaussian, or deep continuous energy models.
- PISA complex-survey inference or causal interpretation.
- Changing the existing `LearningModel` preprocessing or defaults.

## Domain Requirement

State the quadratic energy convention, positive-definite precision requirement,
ridge regularization, and non-causal interpretation of precision interactions.

## Harness Impact

Add import, fit, conditional-mean, sampling, serialization, and invalid-input
coverage to the standard verification suite.

## Acceptance Criteria

- Continuous inputs can be fit without binary thresholding.
- Analysis returns mean, covariance, precision, and conditional interactions.
- Sampling, named-table fitting, save/load, and aggregate diagnostics work.
- Existing binary tests and paper reproduction behavior remain unchanged.
- 68 tests passed, ruff, mypy, wheel verification, and
  `bash scripts/verify.sh --strict-instance` pass.

## Verification Method

```bash
python -m pytest -q
python -m ruff check learning_energy_model tests examples
python -m mypy learning_energy_model
python -m build --wheel --no-isolation
bash scripts/verify.sh --strict-instance
```
