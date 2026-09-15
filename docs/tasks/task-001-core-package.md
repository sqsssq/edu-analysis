# Task 001: Implement paper-scale package core

## Status

Review Ready

## Source PRD

- `docs/prd/00-product-brief.md`
- `docs/prd/01-mvp-scope.md`
- `docs/prd/04-content-model.md`
- `docs/domain/PROJECT_RULES.md`

## Goal

Provide an installable Python package with a binary pairwise energy model, exact enumeration, interpretable moment matching, conditional prediction, analysis, and serialization.

## User Value

Researchers and ML engineers can fit the paper-scale model to their own structured data through a stable high-level API and inspect the assumptions and learned interactions.

## Scope

- `DataConfig` and binary preprocessing with thresholds and median missing-value handling.
- Exact pairwise energy model with `h` and symmetric `J`.
- Weighted empirical moments and moment-matching training.
- Exact KL/autodiff training as a secondary cross-check path.
- Conditional target prediction and model-internal node-freezing analysis.
- Structured result objects and save/load support.
- Initial API tests and package build metadata.

## Out of Scope

- Full Monte Carlo convergence calibration and large-scale performance tuning.
- Continuous energy nodes.
- Causal inference or individual intervention recommendations.
- PISA raw data distribution and complex-survey inference.

## Domain Requirement

Keep the energy convention and binary preprocessing explicit. Label node freezing as a model-internal intervention rather than a causal effect, and preserve preprocessing metadata in saved artifacts.

## Harness Impact

Moves the project from Stage 0 toward Stage 2. Core behavior, deterministic exact-distribution recovery, and exact-vs-Monte-Carlo agreement are covered by tests; broader calibration remains a follow-up task.

## Acceptance Criteria

- `pip` can build a wheel from `pyproject.toml`.
- `LearningModel.fit`, `.predict`, `.analyze`, `.save`, and `.load` work on a small binary dataset.
- Weighted moment calculations and exact state enumeration are used by the trainer.
- Results expose named diagnostics and assumptions.
- Tests, lint, package build, and strict HarnessWeaver verification pass.

## Verification Method

```bash
python -m pytest -q
python -m ruff check learning_energy_model tests
python -m mypy learning_energy_model
python -m build --wheel --no-isolation
bash scripts/verify.sh --strict-instance
```

## Done When

- Implementation matches scope and domain rules.
- Acceptance criteria are satisfied.
- Verification has been run and recorded.
- Remaining numerical and sampling gaps are documented in the roadmap.
