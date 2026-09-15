# Neural Learning Model Package

This repository will turn the paper *A Neural Network Model for Learning - Application to PISA 2018 Data* into a reusable, interpretable Python package.

## Current status

The initial package core and an automatic Gibbs-sampling path are implemented. PISA preparation, reproduction notebooks, and final numerical calibration remain planned work.

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
model = LearningModel(config)
fit_result = model.fit(X, y)
prediction = model.predict(X_new)
analysis = model.analyze()
model.save("learning-model.pt")
```

For a runnable end-to-end example using generated data, run `python -m examples.fit_synthetic`.

The implementation uses exact enumeration up to the configured node threshold and automatically switches to multi-chain Gibbs sampling for larger models. Sampling diagnostics are returned with fit and analysis results and should be reviewed for large systems.

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
- `docs/harness/README.md` - HarnessWeaver workflow and verification contract.
- `docs/meta/WORKFLOW.md` - contribution and task workflow.
