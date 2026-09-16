# Task 055: Reproduce the paper protocol

## Status

In Progress

## Scope

- Add the paper's strict standard-deviation binary threshold (`f > sigma`).
- Provide a local-only reproduction runner using 1,200 rows sampled 16 times
  per economy and outcome.
- Use exact 19-node KL/autodiff training and export first- through fourth-order
  moment comparisons, convergence, parameter stability, and `J` distribution
  statistics.
- Use the paper's explicit KL gradients for the paper runner; adaptive Adam is
  not used in that reproduction path.
- Record the complete reproduction protocol and provenance without exporting
  raw PISA rows.

## Out of scope

- Downloading, redistributing, or committing PISA data.
- Claiming official PISA survey estimates.
- Inferring an unreviewed codebook mapping.

## Acceptance criteria

- `DataConfig(threshold_method="paper_std")` implements the paper's strict
  `f > population standard deviation` rule.
- The paper runner defaults to 1,200 samples, 16 repeats, exact calculation,
  and `method="kl"`.
- Reports include provenance, thresholds/protocol, moment orders 1-4,
  pass/fail comparisons, convergence, repeated-parameter correlations, and
  `J` distribution statistics.
- Existing package defaults remain backward compatible.
- `pytest`, lint/type checks when available, and strict harness verification
  are run before handoff.
