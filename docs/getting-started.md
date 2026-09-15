# Getting started

## Install

```bash
python -m pip install interpretable-learning-energy-model
```

For local development:

```bash
git clone https://github.com/sqsssq/edu-analysis.git
cd edu-analysis
python -m pip install -e '.[dev,visualization]'
```

## Fit a named table

`fit_table` validates named columns, retains an aggregate quality report,
applies the configured binary thresholds, and fits the model.

```python
import pandas as pd
from learning_energy_model import DataConfig, LearningModel

table = pd.DataFrame({"support": [0.1, 0.8, 0.4, 0.9], "resources": [0.2, 0.7, 0.3, 0.95], "outcome": [0, 1, 0, 1]})
model = LearningModel(DataConfig(feature_names=("support", "resources"), target_name="outcome"), calculation="exact", seed=7)
fit = model.fit_table(table)
print(fit.converged, fit.mean_error, fit.correlation_error)
```

## Choose the calculation path

`calculation="auto"` uses exact enumeration through `max_exact_nodes` and
switches to Gibbs sampling above that threshold. Use `"exact"` for a reference
calculation or `"monte_carlo"` for larger models. Sampled results include
diagnostics that should be reviewed before interpretation.

## Inspect quality and assumptions

```python
quality = model.last_quality_report
analysis = model.analyze()
print(quality.to_dict())
print(analysis.h)
print(analysis.J)
print(analysis.assumptions)
```
