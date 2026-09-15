# Interpretable Learning Energy Model

**See the structure behind learning data.**

Interpretable Learning Energy Model is a Python package for fitting binary
pairwise maximum-entropy energy models, inspecting interactions, and building
auditable reproduction workflows.

!!! tip "The short version"
    Declare your data contract, fit a model, inspect `h` and `J`, and export
    aggregate results with their assumptions and diagnostics.

## Why this package

| Goal | What the package provides |
| --- | --- |
| Fit | Exact moment matching and a Monte Carlo path for larger models |
| Explain | Signed fields `h`, interactions `J`, moments, and correlations |
| Reproduce | Explicit thresholds, missingness, weights, and provenance |
| Extend | Replaceable preprocessing, sampler, trainer, and analyzer protocols |

## Install

```bash
pip install interpretable-learning-energy-model
```

For PISA readers and plots:

```bash
pip install 'interpretable-learning-energy-model[pisa,visualization]'
```

## A first model

```python
from learning_energy_model import DataConfig, LearningModel

config = DataConfig(
    feature_names=("home_resources", "teacher_support"),
    target_name="outcome",
)
model = LearningModel(config, seed=7)
fit = model.fit_table(table)
analysis = model.analyze()
```

Read [Getting Started](getting-started.md) for a complete example.

## Model convention

```text
E(s) = h·s + Σ(i<j) J[i,j] s[i]s[j]
p(s) ∝ exp(-E(s))
```

`h` is the node field and `J` is the symmetric pairwise interaction matrix.
Node-freezing comparisons are model-internal structural contributions, not
causal effects or individualized recommendations.

!!! warning "Research boundary"
    Ordinary row weights are supported. PISA replicate weights, plausible-value
    aggregation, complex-survey variance estimation, and official PISA estimates
    are not implemented in the current release.
