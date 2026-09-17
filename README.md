# Neural Learning Model Package

This repository will turn the paper *A Neural Network Model for Learning - Application to PISA 2018 Data* into a reusable, interpretable Python package.

## Current status

The package core, automatic Gibbs-sampling path, and runnable synthetic workflows
are implemented. The paper-specific PISA reproduction runner is also available
for a locally obtained, codebook-reviewed file; the full 240-run numerical
calibration remains an explicit local experiment and is not bundled in Git.

## Quick start

For a reproducible development environment, install [uv](https://docs.astral.sh/uv/)
and run `uv sync --locked --extra dev`. The lock file covers the supported
Python matrix and the optional PISA extra; ordinary users can continue to use
the pip commands from the package metadata.

```python
from learnenergy import DataConfig, LearningModel

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
from learnenergy import LearningEnergyClassifier

estimator = LearningEnergyClassifier(config=config, model_kwargs={"seed": 7})
estimator.fit(X, y)
probabilities = estimator.predict_proba(X_new)
report = estimator.analyze()
```

For independent targets or domains, use `MultiDomainManager`; each domain keeps its own preprocessing rules and parameters:

```python
from learnenergy import MultiDomainManager

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

For a deterministic parameter-recovery check with an aggregate JSON report, run
`python examples/parameter_recovery_benchmark.py --output recovery.json`.

For an inspectable notebook version of the same workflow, open `examples/synthetic_workflow.ipynb`. It uses generated data only and does not require a PISA download.

Optional Matplotlib visualizations are available for fitted results:

```bash
pip install 'learnenergy[visualization]'
```

```python
from learning_energy_model.visualization import plot_correlations, plot_interactions

analysis = model.analyze()
plot_interactions(analysis)
plot_correlations(analysis)
```

For a local-only PISA reproduction template (synthetic smoke mode by default), open `examples/pisa_reproduction_workflow.ipynb`. Set `PISA_INPUT` and `PISA_MAPPING` to run against a reviewed local mapping contract.

### Paper reproduction protocol

The paper runner in `examples/pisa_paper_reproduction.py` uses the explicit
protocol below:

- 1,200 rows sampled without replacement and repeated 16 times per economy/outcome;
- `paper_std` binarization with `f > population standard deviation`;
- thresholds computed independently for each sampled repeat (`per_sample_repeat`);
- 19-node exact enumeration with explicit KL-gradient descent and no Adam;
- Monte Carlo effective interactions with chain diagnostics;
- exact covariance critical-state response derivatives.

Python callers can use `effective_interaction_report(calculation="monte_carlo")`
to retrieve the effective interactions together with their sampling diagnostics.

To export the paper-style Figures 3–12 from a completed aggregate report, run:

```bash
python examples/pisa_paper_figures_4_12.py \
  --report data/prepared/pisa2018-paper-reproduction-report.json \
  --output-dir data/prepared/pisa2018-paper-figures-4-12
```

This produces ten PNGs: Figures 3–5, 6–10, 11, and Appendix Figure A.12.
Figures 3 and 4 use the same economy color mapping for their scatter points.
Figure A.12 plots threshold `theta` against Pearson correlation between the
original and binarized data, using only aggregate report fields.

The runner writes only aggregate parameters, moments, convergence information,
Monte Carlo diagnostics, and provenance. It never writes raw PISA rows to the
repository. See `docs/reproduction/PISA_BENCHMARK_CONTRACT.md` for the complete
interpretation boundary and known differences from official PISA inference.
By default it also writes 15 selected PyTorch `.pt` model artifacts under
`data/prepared/pisa2018-paper-reproduction-models/`; each is reloadable with
`LearningModel.load()` and is selected from the 16 validation repeats.

The visual landing page is [`docs/landing.html`](docs/landing.html). The full searchable documentation is built from [`docs/`](docs/) with MkDocs Material and is available under `/docs/` on GitHub Pages.

Before fitting a local table, callers can inspect input quality without changing the data:

```python
from learnenergy import validate_tabular_data

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

Advanced callers can inject compatible preprocessing, sampling, training, or
analysis components via `preprocessor=`, `sampler=`, `trainer=`, and
`analyzer=`; the built-in implementations remain the default. Custom components
are runtime-only and must be serialized separately if needed.

Missing values can be handled with `missing_strategy="error"`, `"median"`, `"mean"`, or `"zero"`; the latter three impute without dropping rows. PISA-specific nonresponse codes must be recoded before fitting.

When passing a named mapping or DataFrame to `predict`, the fitted feature names are used, so column order and extra columns do not silently change the model input.

## Intended first release

- PyTorch implementation of a pairwise maximum-entropy energy model.
- Binary nodes by default, with recorded preprocessing and threshold rules.
- Exact enumeration for small models, automatic Monte Carlo for larger models.
- Interpretable moment matching as the default training path, with an explicit KL-gradient path for cross-checking.
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
- `docs/API.md` - public classes, methods, result contracts, and extension boundaries.
- `docs/prd/DECISION_LOG.md` - decisions made during requirements grilling.
- `docs/prd/ROADMAP.md` - staged implementation plan.
- `docs/domain/PROJECT_RULES.md` - scientific and safety guardrails.
- `docs/reproduction/PISA_2018_DATA_GUIDE.md` - official PISA source, local-only data workflow, and reproduction boundary.
- `docs/reproduction/PISA_2022_DATA_GUIDE.md` - PISA 2022 file selection, reviewed mapping contracts, and local-only workflow.
- `docs/reproduction/PISA_BENCHMARK_CONTRACT.md` - provenance, moment, tolerance, and interpretation requirements for future PISA runs.
- `docs/harness/README.md` - HarnessWeaver workflow and verification contract.
- `docs/meta/WORKFLOW.md` - contribution and task workflow.
