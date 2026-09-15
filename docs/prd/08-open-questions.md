# Open Questions

## Product Questions

- Which exact names and fields should the first stable result objects expose?
- What is the minimum notebook that demonstrates fitting a fresh user dataset and reloading an artifact?
- Which report formats are needed before the PyPI release?

## Technical Questions

- What node-count threshold should trigger automatic Monte Carlo on supported hardware?
- Which convergence criteria and effective-sample-size thresholds are acceptable?
- Which PyTorch and Python versions should CI support in the first release?
- How should PISA weights and missingness be represented without claiming full complex-survey inference?

## Resolved Guardrails

- Model-internal interventions are not causal effects.
- Individual student recommendations are out of scope.
- PISA raw data is not redistributed.
- Cross-dataset parameter comparisons require aligned definitions and preprocessing.
