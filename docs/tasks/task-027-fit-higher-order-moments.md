# Task 027: Expose fitted higher-order moment reports

## Status

Review Ready

## Source PRD

- `docs/prd/04-content-model.md`
- `docs/reproduction/PISA_BENCHMARK_CONTRACT.md`

## Goal

Expose observed and model third- and fourth-order moments in `FitResult` so
benchmark reports can compare the fitted model with the prepared sample without
recomputing internal statistics.

## Scope

- Add serializable observed/model higher-order moment mappings to `FitResult`.
- Populate them for exact KL/autodiff and moment-matching training paths.
- Preserve the mappings through save/load and dict/JSON export.
- Document their use with `compare_moment_orders`.

## Out of Scope

- Official PISA estimates, replicate weights, plausible values, or complex-survey variance.
- Higher orders beyond four.

## Domain Requirement

Observed moments describe the prepared binary sample; model moments describe the
fitted distribution and are approximate when the sampled calculation path is used.

## Acceptance Criteria

- A fitted result exposes matching third- and fourth-order observed/model keys.
- Exact and sampled paths populate the fields without breaking legacy artifacts.
- Save/load preserves the fields.
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

- Higher-order fit reports are implemented, tested, documented, committed, and pushed.
