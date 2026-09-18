# Task 056: Add original-style Monte Carlo Adam training

## Status

Review Ready

## Source PRD

- `docs/prd/ROADMAP.md`
- `docs/prd/09-decision-log.md`
- `docs/domain/PROJECT_RULES.md`

## Goal

Provide an explicit, optional training path that is closer to the public
original implementation: sampled model moments followed by Adam updates.

## Scope

- Add `LearningModel.fit(..., method="adam")` for Monte Carlo training.
- Preserve the package's documented `{0, 1}` state and energy convention.
- Reuse the package sampler and expose R-hat, ESS, MCSE, and optimizer settings.
- Persist Adam hyperparameters in `.pt` settings and keep legacy artifacts loadable.
- Expose the method through the CLI and document its relationship to the
  original C++/HDF5 implementation.

## Out of scope

- Replacing exact KL-gradient training.
- Implementing continuous-node models.
- Claiming bit-for-bit equivalence with the original C++ Metropolis executable.

## Acceptance criteria

- `method="adam"` requires the Monte Carlo calculation path and returns a
  structured `FitResult`.
- The result records `training_method="adam"`, optimizer settings, and MC
  diagnostics.
- Existing methods, defaults, save/load behavior, and tests remain compatible.
- CLI and method documentation show how to select the compatibility path.
- `pytest` (65 passed), ruff, mypy, wheel verification, and
  `bash scripts/verify.sh --strict-instance` pass.
