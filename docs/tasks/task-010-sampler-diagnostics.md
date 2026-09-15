# Task 010: Replace sampler ESS placeholder with diagnostics

## Status

Review Ready

## Source PRD

- `docs/prd/ROADMAP.md`
- `docs/prd/06-acceptance-criteria.md`
- `docs/domain/PROJECT_RULES.md`

## Goal

Make Monte Carlo diagnostics informative enough to support review of large-model results by estimating R-hat and effective sample size from the sampled chains.

## User Value

Users can identify nodes with poor mixing instead of interpreting the total number of draws as if it were the effective sample size.

## Scope

- Standard multi-chain R-hat calculation with degenerate-node handling.
- Initial-positive-sequence autocorrelation ESS estimate.
- Aggregate and per-node diagnostics in sampler, fit, and analysis results.

## Out of Scope

- Formal calibration thresholds for every model topology.
- Batch means, spectral estimators, or official survey uncertainty.

## Domain Requirement

Describe diagnostics as estimates and retain the requirement that Monte Carlo results be reviewed before interpretation.

## Harness Impact

Adds feedback sensors for sampler mixing and replaces a known placeholder metric.

## Acceptance Criteria

- ESS is not always equal to the raw draw count.
- R-hat and ESS are available per node and in aggregate.
- Uniform and model-based sampler tests pass with standard verification.

## Verification Method

```bash
python -m pytest -q
python -m ruff check learning_energy_model tests examples
python -m mypy learning_energy_model
python -m build --wheel --no-isolation
bash scripts/verify.sh --strict-instance
```

## Done When

- The placeholder is removed, diagnostics are tested, and limitations are documented.
- The verified change is committed and pushed.
