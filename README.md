# Neural Learning Model Package

This repository will turn the paper *A Neural Network Model for Learning - Application to PISA 2018 Data* into a reusable, interpretable Python package.

## Current status

This is the design and verification stage. The repository currently contains the source paper and a HarnessWeaver-compatible project scaffold. Model implementation is intentionally deferred until the package contract and acceptance criteria are reviewed.

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

GitHub Actions runs the strict harness check on pushes and pull requests. The Python matrix is ready for package tests and builds once package metadata and source code are added.

## Documentation map

- `docs/prd/PRODUCT_BRIEF.md` - product scope and user-facing contract.
- `docs/prd/DECISION_LOG.md` - decisions made during requirements grilling.
- `docs/prd/ROADMAP.md` - staged implementation plan.
- `docs/domain/PROJECT_RULES.md` - scientific and safety guardrails.
- `docs/harness/README.md` - HarnessWeaver workflow and verification contract.
- `docs/meta/WORKFLOW.md` - contribution and task workflow.
