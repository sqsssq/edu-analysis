# Project Rules

## Scientific rules

- Treat the model as a joint binary energy model, not as a conventional feed-forward neural network.
- Keep `h`, `J`, temperature/scaling conventions, and sign conventions explicit in code and reports.
- Record every normalization, threshold, missing-value, weighting, and sampler choice.
- Never compare parameters across datasets unless coding, preprocessing, variable definitions, and sampling assumptions are aligned.
- Make exact enumeration the reference implementation for the paper-sized model whenever feasible.

## Interpretation rules

- Label node-freezing results as model-internal interventions or structural contributions.
- Do not call them causal effects or individualized recommendations.
- Report uncertainty and convergence diagnostics for Monte Carlo-derived quantities.
- Distinguish predictive association from educational mechanism.

## Data rules

- Do not redistribute restricted PISA raw data.
- Provide field mappings and preparation instructions instead.
- Keep raw user data out of serialized model artifacts by default.
- Validate variable names, dimensionality, binary encodings, missingness, and sample weights before training.

## Product rules

- Prefer explainability and numerical stability over opaque speed optimizations.
- Keep the high-level API small and stable; put experimental features behind explicit adapters or flags.
- Every public analysis result must include assumptions and known limitations.

