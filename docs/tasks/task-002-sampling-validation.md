# Task 002: Validate exact and Monte Carlo computation paths

## Status

Review Ready

## Source PRD

- `docs/prd/ROADMAP.md`
- `docs/prd/06-acceptance-criteria.md`
- `docs/domain/PROJECT_RULES.md`

## Goal

Provide deterministic synthetic evidence that Gibbs sampling approximates the exact distribution on small systems and that the public model switches computation paths without changing its documented semantics.

## User Value

Researchers can distinguish a numerical implementation failure from ordinary Monte Carlo error before fitting a larger educational network.

## Scope

- Compare exact state probabilities and Gibbs-sampled moments on a small known energy model.
- Verify that the large-model path returns sampling diagnostics and the requested public sample shape.
- Document the remaining calibration work rather than presenting initial diagnostics as production-grade guarantees.

## Out of Scope

- PISA data access or redistribution.
- Full asymptotic effective-sample-size estimation.
- Benchmarking arbitrary high-dimensional models.

## Domain Requirement

Keep the energy sign convention explicit and describe Monte Carlo estimates as approximate. Do not interpret node freezing as a causal intervention.

## Harness Impact

Adds feedback sensors for the exact/Monte Carlo boundary and basic sampler agreement.

## Acceptance Criteria

- A small known model has sampled first- and second-order moments close to exact moments within a declared tolerance.
- Moment matching recovers a small known model within a declared parameter tolerance.
- A model above `max_exact_nodes` reports `calculation=monte_carlo` and exposes diagnostics.
- Existing pytest, ruff, mypy, wheel build, and strict HarnessWeaver verification pass.

## Verification Method

```bash
python -m pytest -q
python -m ruff check learning_energy_model tests
python -m mypy learning_energy_model
python -m build --wheel --no-isolation
bash scripts/verify.sh --strict-instance
```

## Done When

- Synthetic agreement and path-switch tests pass.
- Public documentation matches the implemented computation paths.
- Remaining sampler calibration limitations are recorded in the roadmap.
