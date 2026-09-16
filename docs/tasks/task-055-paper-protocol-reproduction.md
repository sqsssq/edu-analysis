# Task 055: Reproduce the paper protocol

## Status

In Progress

## Scope

- Add the paper's strict standard-deviation binary threshold (`f > sigma`).
- Provide a local-only reproduction runner using 1,200 rows sampled 16 times
  per economy and outcome.
- Use exact 19-node explicit KL-gradient training and export first- through fourth-order
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
- The public analysis surface exposes paper-style effective interactions,
  mean±SD classifications, threshold sensitivity, and exact temperature
  response diagnostics; the reproduction runner forces Monte Carlo for the
  effective interaction calculation and records its chain diagnostics.
- `examples/pisa_paper_figures.py` exports aggregate PNGs for effective
  interactions, temperature response, and `Jij` distributions from a report.
- Existing package defaults remain backward compatible.
- `pytest`, lint/type checks when available, and strict harness verification
  are run before handoff.
