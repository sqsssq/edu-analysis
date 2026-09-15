# Task 007: Add exact KL/autodiff training

## Status

Review Ready

## Source PRD

- `docs/prd/PRODUCT_BRIEF.md`
- `docs/prd/ROADMAP.md`
- `docs/domain/PROJECT_RULES.md`

## Goal

Provide an exact negative-log-likelihood training path as a numerical cross-check for the default moment-matching trainer.

## User Value

Advanced users can compare the interpretable default optimizer against a standard autodiff likelihood objective on paper-scale models.

## Scope

- `LearningModel.fit(..., method="kl")` using exact partition-function evaluation.
- Explicit rejection above the exact-enumeration threshold.
- Diagnostics identifying the training method and synthetic tests.

## Out of Scope

- Approximate KL training for large models.
- Replacing moment matching as the default.
- Claims that either path establishes causal effects.

## Domain Requirement

Keep the energy sign convention and exact-vs-approximate boundary visible in diagnostics.

## Harness Impact

Adds a numerical cross-check sensor for the second training path.

## Acceptance Criteria

- Exact models accept `method="kl"` and return structured diagnostics.
- Large models reject exact KL with an actionable error.
- Synthetic API tests and standard package verification pass.

## Verification Method

```bash
python -m pytest -q
python -m ruff check learning_energy_model tests examples
python -m mypy learning_energy_model
python -m build --wheel --no-isolation
bash scripts/verify.sh --strict-instance
```

## Done When

- The secondary training path is tested and documented.
- The verified change is committed and pushed.
