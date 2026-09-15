# Task 026: Add Monte Carlo error estimates

## Status

Review Ready

## Objective

Expose sampling uncertainty for marginal node means alongside R-hat and ESS diagnostics.

## Acceptance criteria

- The sampler reports per-node and aggregate MC standard errors.
- Estimates use the observed marginal variance and effective sample size.
- Degenerate binary nodes remain finite and interpretable.
- Standard package verification passes.

## Handoff

MCSE is an approximate diagnostic, not official PISA sampling variance; calibration across topologies remains future work.
