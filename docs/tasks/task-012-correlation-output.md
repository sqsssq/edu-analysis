# Task 012: Expose correlation outputs

## Status

Review Ready

## Source PRD

- `docs/prd/04-content-model.md`
- `docs/prd/06-acceptance-criteria.md`
- `docs/prd/ROADMAP.md`

## Goal

Expose the pairwise Pearson correlation matrix implied by the model moments.

## User Value

Researchers can inspect a familiar association scale alongside raw pairwise moments and learned interactions.

## Scope

- Bernoulli Pearson correlations derived from model means and pairwise moments.
- Stable zero-variance handling.
- Synthetic analysis and export coverage.

## Out of Scope

- Causal or partial-correlation interpretation.
- Correlation comparisons across unaligned datasets.

## Domain Requirement

Describe correlations as model associations and preserve the binary encoding assumptions.

## Harness Impact

Adds a feedback sensor for the documented correlation output contract.

## Acceptance Criteria

- Analysis returns a square correlation matrix aligned to node order.
- Non-degenerate diagonal entries are one and zero-variance pairs do not produce NaNs.
- Standard package verification passes.

## Verification Method

```bash
python -m pytest -q
python -m ruff check learning_energy_model tests examples
python -m mypy learning_energy_model
python -m build --wheel --no-isolation
bash scripts/verify.sh --strict-instance
```

## Done When

- Correlations are implemented, tested, and documented.
- The verified change is committed and pushed.
