# Task 009: Include fit moment reports

## Status

Review Ready

## Source PRD

- `docs/prd/04-content-model.md`
- `docs/prd/06-acceptance-criteria.md`
- `docs/design.md`

## Goal

Make the fit result self-contained for numerical inspection by including the observed and fitted moments through fourth order.

## User Value

Researchers can inspect whether a training run matched the data without rerunning internal preprocessing or sampler code.

## Scope

- Add observed/model moment arrays to `FitResult` for first through fourth order.
- Populate them for moment matching and exact explicit KL-gradient training.
- Preserve them through dict/JSON export and saved model metadata.

## Out of Scope

- PISA official estimates or complex-survey variance.

## Domain Requirement

Keep the arrays tied to the recorded binary preprocessing and report sampled moments as approximate through diagnostics.

## Harness Impact

Adds a feedback sensor for moment-matching quality and reproducibility.

## Acceptance Criteria

- Both supported training methods return observed and model first- through fourth-order moments.
- The result export includes these arrays.
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

- Fit reports are populated, tested, and documented.
- The verified change is committed and pushed.
