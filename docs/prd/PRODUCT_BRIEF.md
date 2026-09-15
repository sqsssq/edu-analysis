# Product Brief

## Summary

Build a reusable Python package that implements the paper's maximum-entropy, pairwise Hopfield/Boltzmann-style learning model for educational and other structured datasets.

The package is an exploratory research tool. It models a joint distribution over binary variables, estimates local fields `h` and pairwise interactions `J`, and exposes model-internal analyses such as conditional prediction, correlations, energy/entropy diagnostics, and node-freezing interventions.

## Primary users

1. Researchers who need interpretable interaction models and paper-reproduction experiments.
2. ML engineers who need a callable `fit/predict/save/load` interface for their own datasets.

## In scope for v0.1

- PyTorch backend with CPU and NVIDIA GPU support where available.
- One target node per model; multiple domains are represented by a manager of independent models.
- `X` and `y` inputs from NumPy, tensors, and simple tabular adapters.
- `DataConfig` for variable names, binary conversion, thresholds, missing values, and metadata.
- Exact enumeration for the paper-sized model (19 nodes).
- Automatic sampler selection with Monte Carlo above the exact-enumeration threshold.
- Moment matching as the primary, interpretable trainer.
- KL-divergence/autodiff training as a secondary implementation and validation path.
- Optional sample weights.
- Structured result objects and DataFrame export.
- Model serialization including parameters, preprocessing, metadata, random state, sampler state, logs, and version information.
- Synthetic recovery tests and PISA reproduction benchmarks.

## Proposed public contract

```python
model = LearningModel(config)
fit_result = model.fit(X, y, sample_weight=None)
prediction = model.predict(X)
analysis = model.analyze()
model.save(path)
loaded = LearningModel.load(path)
```

The public surface remains simple; internal components may be split into `Trainer`, `Sampler`, `Analyzer`, and `Preprocessor`. A sklearn-style adapter may expose `fit`, `predict`, `get_params`, and `set_params` without claiming complete sklearn compatibility.

## Output semantics

`predict` returns target probability, energy-related diagnostics, and uncertainty or sampling intervals where applicable. Binary labels are not forced by the package; users choose thresholds.

Analysis reports include observed/model moments, pairwise and higher-order correlation diagnostics, learned `h`/`J`, node-freezing results, sampler diagnostics, assumptions, and limitations.

## Explicitly out of scope

- Causal inference.
- Individual student intervention recommendations.
- Continuous-node energy models in v0.1.
- Full replication of PISA's complex survey inference, replicate weights, or all plausible values.
- Guaranteed fast training for arbitrary high-dimensional models.
- Bundling restricted PISA raw data.

