# MVP Scope

## In Scope

- `PyTorch binary pairwise energy model with exact enumeration for small systems.`
- `Moment matching, KL/autodiff cross-checks, conditional prediction, and model-internal intervention analysis.`
- `Versioned serialization, sample weights, diagnostics, examples, and PyPI-ready documentation.`

## Out of Scope

- `Causal claims or individual student recommendations.`
- `Continuous energy nodes and full PISA complex-survey inference in v0.1.`
- `Bundling restricted raw PISA data or promising arbitrary high-dimensional speed.`

## MVP Boundary

The first implementation should prove this loop:

```text
Declare variables, target, metadata, and preprocessing rules.
-> Fit the energy model with interpretable moment matching.
-> Validate moments, convergence, and sampler diagnostics.
-> Predict, analyze interventions, save, and reload the model.
```
