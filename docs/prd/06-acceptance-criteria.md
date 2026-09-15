# Acceptance Criteria

## Framework Acceptance Criteria

- Root `AGENTS.md` is the stable Codex entry point for maintaining `Interpretable Learning Energy Model`.
- `LICENSE` defines public reuse terms.
- `docs/prd/` describes product direction and MVP boundaries.
- `docs/meta/` describes reusable AI development workflow.
- `docs/harness/` describes harness maturity, sensors, and failure patterns.
- `docs/domain/` describes project-specific rules.
- `docs/design.md` describes project-specific design standards.
- `.harnessweaver-version` records the scaffold version used to initialize the project.
- `config/init-project.example.env` documents repeatable project configuration.
- `docs/tasks/TASK_TEMPLATE.md` enforces small scope, acceptance criteria, verification, and handoff.
- `scripts/verify.sh` runs successfully.
- `.github/workflows/ci.yml` runs strict harness verification, package checks, and CLI entry-point smoke tests on pushes and pull requests.

## Future Product Acceptance Criteria

- The task supports the MVP loop.
- Domain-specific quality rules are preserved.
- Harness implications are documented.
- Verification was run or unavailable checks were clearly documented.

## Current Gap Register

- `pyproject.toml` and an initial installable package now exist; dependency locking and final release publication remain.
- Initial model source modules, public API, Gibbs sampler, and injectable lifecycle components exist.
- Configured missing-value strategies include fail-fast, median, mean, and zero imputation; PISA-specific missing codes remain an explicit preparation responsibility.
- Exact KL/autodiff training is available as a cross-check for models within the exact-enumeration threshold.
- Analysis results expose third- and fourth-order joint moments for reproducibility checks.
- Analysis results expose a stable binary-node correlation matrix.
- Fit results expose observed and model moments through fourth order.
- Sampling diagnostics include per-node R-hat and autocorrelation-based effective sample size estimates.
- Saved artifacts expose format/package version, caller metadata, random state, and training logs without raw observations.
- Training and tabular preparation reject non-finite sample weights before moment calculation.
- The public model can draw joint binary states with exact or Gibbs sampling according to model size.
- Initial `tests/` coverage includes deterministic exact-distribution parameter recovery and a repeatable aggregate benchmark; domain-specific numerical calibration remains.
- PISA 2018/2022 local-data guides, generic tabular preparation, reusable reviewed mappings, runnable local workflow, executed synthetic notebook, and local-only reproduction notebook template exist; real-data reproduction remains caller-run.
- A dependency-free sklearn-style adapter exposes `fit`, `predict`, `predict_proba`, and parameter access without changing the core model contract.
- A pre-training tabular quality report exposes aggregate missingness, shape, infinity, and sample-weight checks without retaining raw rows.
- Monte Carlo diagnostics expose per-node and aggregate MC standard error estimates in addition to R-hat and ESS.
- Monte Carlo fit reports evaluate configurable R-hat, ESS, and MCSE quality thresholds and emit a warning when a sampled run fails them.
- PyTorch dependency policy is encoded in `pyproject.toml`; lock files remain, while CI now strictly installs development dependencies and smoke-tests the optional PISA extra.
