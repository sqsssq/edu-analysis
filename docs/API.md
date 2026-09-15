# Public API reference

The package exposes an interpretable binary pairwise maximum-entropy model. The
energy convention is

```text
E(s) = h·s + sum(i<j) J[i,j] s[i] s[j]
p(s) ∝ exp(-E(s))
```

All result objects provide `to_dict()` and `to_json()` aggregate exports. They
do not retain raw input rows.

## `DataConfig`

Use `DataConfig` to record feature names, target name, thresholding, missing
value policy, ordinary row-weight provenance, and caller metadata.

```python
config = DataConfig(
    feature_names=("home_resources", "teacher_support"),
    target_name="outcome",
    threshold_method="quantile",
    quantile=0.5,
    missing_strategy="median",  # error, median, mean, or zero
    sample_weight_name="W_FSTUWT",
)
```

## `LearningModel`

```python
model = LearningModel(config, calculation="auto", seed=7)
fit = model.fit(X, y, sample_weight=weights, method="moment_matching")
prediction = model.predict(X_new)
analysis = model.analyze()
model.save("model.pt")
reloaded = LearningModel.load("model.pt")
```

For named mappings or DataFrames, `fit_table()` combines aggregate quality
validation, column selection, optional ordinary weights, and fitting:

```python
model = LearningModel(DataConfig(target_name="outcome"))
fit = model.fit_table(
    table,
    feature_names=("home_resources", "teacher_support"),
    target_name="outcome",
    weight_name="W_FSTUWT",
)
```

The aggregate validation evidence is available as `model.last_quality_report`
and is retained in the saved artifact. It contains row count, required column
names, missingness, infinite-value counts, and issues only; raw table rows are
never stored.

`calculation="auto"` uses exact enumeration through `max_exact_nodes` and
Gibbs sampling above it. Use `"exact"` or `"monte_carlo"` to force a path.
`method="kl"` is an exact-only autodiff cross-check.

`FitResult` contains convergence information, sampler quality checks, observed
and modeled moments through fourth order, and warnings. For sampled fits,
review `quality_passed`, `quality_checks`, `quality_thresholds`, R-hat, ESS, and
MCSE before interpreting results.

`PredictionResult.probabilities` contains the conditional probability of the
target node being one. `AnalysisResult` contains `h`, symmetric `J`, moments,
binary Pearson correlations, higher-order model moments, and model-internal
node-freezing comparisons. A node-freezing comparison is not a causal effect.

## Estimator and multi-domain interfaces

`LearningEnergyClassifier` provides `fit`, `predict`, `predict_proba`,
`get_params`, `set_params`, and `analyze` for estimator-oriented callers.
It also provides `fit_table()` for named mappings or DataFrames and exposes the
wrapped model's `last_quality_report` through `estimator.model_`.
`MultiDomainManager` keeps independent `LearningModel` instances per domain:

```python
manager = MultiDomainManager(model_kwargs={"seed": 7})
manager.fit("math", X, y_math)
manager.fit("reading", X, y_reading)
report = manager.analyze("math")
```

## PISA local adapter

`PISAMapping` requires explicit, codebook-reviewed source column names and can
be saved as a row-free JSON contract:

```python
mapping = PISAMapping.load("pisa2022-reviewed.json")
prepared = prepare_pisa_file("data/raw/pisa2022-student.zip", mapping)
model = LearningModel(
    DataConfig(
        feature_names=prepared.feature_names,
        target_name=prepared.target_name,
        sample_weight_name=mapping.weight_name,
        metadata=mapping.metadata,
    )
)
fit = model.fit(prepared.X, prepared.y, sample_weight=prepared.sample_weight)
```

PISA raw files remain local. The adapter supports ordinary row weights but does
not implement replicate weights, plausible-value aggregation, or complex-survey
variance estimation. Results must therefore be described as estimates on the
prepared sample, not official PISA estimates.

## Replaceable components

`LearningModel` accepts protocol-compatible `preprocessor=`, `sampler=`,
`trainer=`, and `analyzer=` components. The public protocols are exported from
the package root. Custom components run at runtime and are not automatically
serialized; save their configuration or contract separately.
