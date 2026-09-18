# Continuous models

The package includes an experimental `ContinuousEnergyModel` for numeric data
that should not be thresholded into binary nodes. It is separate from the
paper-reproduction `LearningModel`.

## Mathematical convention

The model fits a Gaussian maximum-entropy distribution:

```text
E(x) = 1/2 xᵀ K x - bᵀ x + const
p(x) ∝ exp(-E(x))
```

where `K` is the positive-definite precision matrix and `b = K μ`. The fitted
mean is `μ` and the covariance is `Σ = K⁻¹`. Off-diagonal precision terms
represent conditional dependence. They are not causal effects.

## Basic usage

```python
import numpy as np
from learnenergy import ContinuousEnergyModel

X = np.random.default_rng(7).normal(size=(500, 3))
model = ContinuousEnergyModel(
    feature_names=("home_resources", "teacher_support", "outcome_score"),
    ridge=1e-6,
    seed=7,
)
fit = model.fit(X)
analysis = model.analyze()

print(fit.model_mean)
print(analysis.covariance)
print(analysis.precision)
print(analysis.interactions)
```

The model also supports named table-like data:

```python
model = ContinuousEnergyModel(ridge=1e-6)
model.fit_table(table, feature_names=("feature_a", "feature_b"))
```

## Conditional mean and sampling

Pass one value per node and use `NaN` at the target position:

```python
conditional = model.conditional_mean(
    [np.nan, 0.4, -0.2],
    target_index=0,
)
samples = model.sample(1_000)
```

## Regularization and limitations

`ridge` adds `ridge * I` to the empirical covariance before inversion. This
keeps the precision matrix positive definite when variables are collinear, but
it also means the reported model covariance can differ slightly from the raw
empirical covariance.

This first continuous family assumes joint Gaussian structure. It does not yet
support nonlinear dependence, heavy-tailed distributions, mixed binary and
continuous nodes, or official PISA survey inference.

The original binary API remains unchanged:

```python
from learnenergy import DataConfig, LearningModel
```
