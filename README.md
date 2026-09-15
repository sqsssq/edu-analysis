# Neural Learning Model Package

This repository will turn the paper *A Neural Network Model for Learning - Application to PISA 2018 Data* into a reusable, interpretable Python package.

## Current status

The initial package core, automatic Gibbs-sampling path, and a runnable synthetic workflow are implemented. PISA preparation is available through an explicit local adapter; reproduction notebooks and final numerical calibration remain planned work.

## Quick start

```python
from learning_energy_model import DataConfig, LearningModel

X = ...       # rows x feature values from your own dataset
y = ...       # one target value per row
X_new = ...   # rows with the same feature columns
config = DataConfig(
    feature_names=("home_resources", "teacher_support"),
    target_name="outcome",
)
model = LearningModel(config, calculation="auto")
fit_result = model.fit(X, y)
prediction = model.predict(X_new)
analysis = model.analyze()
model.save("learning-model.pt")
```

For estimator-style callers, the dependency-free `LearningEnergyClassifier` exposes `fit`, `predict_proba`, `predict`, and `analyze` while retaining the same interpretable model underneath:

```python
from learning_energy_model import LearningEnergyClassifier

estimator = LearningEnergyClassifier(config=config, model_kwargs={"seed": 7})
estimator.fit(X, y)
probabilities = estimator.predict_proba(X_new)
report = estimator.analyze()
```

For independent targets or domains, use `MultiDomainManager`; each domain keeps its own preprocessing rules and parameters:

```python
from learning_energy_model import MultiDomainManager

manager = MultiDomainManager(model_kwargs={"seed": 7})
manager.fit("math", X, y_math)
manager.fit("reading", X, y_reading)
math_report = manager.analyze("math")
```

For a numeric CSV, the same workflow is available from the command line:

```bash
python -m learning_energy_model fit \
  --input data.csv --features feature_a,feature_b --target outcome \
  --output model.pt --missing-strategy median
python -m learning_energy_model predict --model model.pt --input data.csv --output predictions.csv
python -m learning_energy_model analyze --model model.pt > analysis.json
```

For a runnable end-to-end example using generated data, run `python -m examples.fit_synthetic`.

For an inspectable notebook version of the same workflow, open `examples/synthetic_workflow.ipynb`. It uses generated data only and does not require a PISA download.

Before fitting a local table, callers can inspect input quality without changing the data:

```python
from learning_energy_model import validate_tabular_data

quality = validate_tabular_data(
    table,
    feature_names=("feature_a", "feature_b"),
    target_name="outcome",
    weight_name="W_FSTUWT",
)
if not quality.passed:
    raise ValueError(quality.issues)
```

The default `calculation="auto"` uses exact enumeration up to `max_exact_nodes` and switches to multi-chain Gibbs sampling for larger models. Use `calculation="exact"` or `"monte_carlo"` to force and record a path for reproducibility. Sampling diagnostics are returned with fit and analysis results and should be reviewed for large systems.

Sampled fits also report `quality_passed`, the individual R-hat/ESS/MCSE checks,
and the configured thresholds (`mc_max_rhat`,
`mc_min_effective_sample_size`, and `mc_max_mcse`). These are review guardrails,
not universal scientific cutoffs.

Missing values can be handled with `missing_strategy="error"`, `"median"`, `"mean"`, or `"zero"`; the latter three impute without dropping rows. PISA-specific nonresponse codes must be recoded before fitting.

When passing a named mapping or DataFrame to `predict`, the fitted feature names are used, so column order and extra columns do not silently change the model input.

## Intended first release

- PyTorch implementation of a pairwise maximum-entropy energy model.
- Binary nodes by default, with recorded preprocessing and threshold rules.
- Exact enumeration for small models, automatic Monte Carlo for larger models.
- Interpretable moment matching as the default training path, with a KL/autodiff path for cross-checking.
- Structured fit, prediction, intervention-analysis, save, and load results.
- PISA reproduction benchmarks without bundling restricted raw PISA data.

## Verification

Run the project harness check from the repository root:

```bash
bash scripts/verify.sh --instance
```

GitHub Actions runs the strict harness check, package tests, lint, type checks, and wheel builds on pushes and pull requests across Python 3.10–3.12.

## Documentation map

- `docs/prd/PRODUCT_BRIEF.md` - product scope and user-facing contract.
- `docs/prd/DECISION_LOG.md` - decisions made during requirements grilling.
- `docs/prd/ROADMAP.md` - staged implementation plan.
- `docs/domain/PROJECT_RULES.md` - scientific and safety guardrails.
- `docs/reproduction/PISA_2018_DATA_GUIDE.md` - official PISA source, local-only data workflow, and reproduction boundary.
- `docs/reproduction/PISA_BENCHMARK_CONTRACT.md` - provenance, moment, tolerance, and interpretation requirements for future PISA runs.
- `docs/harness/README.md` - HarnessWeaver workflow and verification contract.
- `docs/meta/WORKFLOW.md` - contribution and task workflow.
