# Fit and inspect

## The main loop

```python
fit = model.fit(X, y)
prediction = model.predict(X_new)
samples = model.sample(1000)
analysis = model.analyze()
```

For DataFrames or named mappings, prefer `fit_table()` so feature order and
quality checks are explicit.

## Results

`FitResult` contains convergence, objective history, moment errors, warnings,
and observed/model moments through fourth order. `PredictionResult` contains
conditional target probabilities. `AnalysisResult` contains `h`, `J`, moments,
correlations, energy statistics, and structural comparisons.

All result objects support `to_dict()` and `to_json()` and do not retain raw rows.

## Replace components

Advanced callers can inject protocol-compatible preprocessors, samplers,
trainers, and analyzers. Custom components run at runtime and are not
automatically serialized.
