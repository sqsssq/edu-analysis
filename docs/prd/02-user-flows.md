# User Flows

## Primary Flow

```text
Create a LearningModel with DataConfig.
-> Call fit(X, y, sample_weight=None) on user data.
-> Inspect PredictionResult and AnalysisResult diagnostics.
-> Save the artifact or export a reproducible report.
```

## Edge Flows

- `Input schema or binary encoding is invalid.`
- `Monte Carlo chains fail convergence checks.`
- `A user attempts an unsupported causal or cross-dataset interpretation.`
