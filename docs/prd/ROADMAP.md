# Roadmap

## v0.1 - verified paper-scale core

- Add GitHub Actions CI for strict harness verification and the supported Python matrix. **Implemented: CI now installs locked dependencies, smoke-tests the installed wheel and both CLI entry points, and cancels superseded runs per branch or pull request.**
- Define package layout and public API. **Implemented: the installable package and documented high-level API are present.**
- Implement binary pairwise energy model. **Implemented: the exact binary pairwise model is present and tested.**
- Implement exact state enumeration for 19 nodes. **Implemented: configurable exact enumeration supports the paper-scale boundary and is tested on small systems.**
- Implement weighted empirical moments and moment-matching trainer. **Implemented: weighted moments, default moment matching, and deterministic recovery checks are present.**
- Implement exact KL/autodiff training as a cross-check path. **Implemented: `fit(..., method="kl")` is available for exact models.**
- Implement conditional target probability and structured diagnostics. **Implemented: `predict` exposes the energy-derived conditional probability and diagnostics; the formula is regression-tested.**
- Add synthetic recovery tests. **Implemented: sampled and deterministic exact-distribution recovery plus a repeatable aggregate benchmark report are covered; domain-specific calibration remains.**
- Add exact-vs-Monte-Carlo agreement tests on small systems. **Implemented: known-model moment agreement and computation-path switching are covered; deterministic exact-distribution recovery is also tested.**
- Add PISA reproduction benchmark contracts and preparation instructions. **Implemented: the aggregate-only contract is documented in `docs/reproduction/PISA_BENCHMARK_CONTRACT.md`; reusable reviewed `PISAMapping` JSON contracts are supported, while local data and aligned mappings remain required.**
- Add PISA source and local-data instructions. **Implemented: official source, access boundary, and preparation checklist are documented.**
- Add an optional local PISA reader and explicit mapping adapter. **Implemented: `PISAMapping` and `prepare_pisa_file` are available with early contract validation; survey inference remains out of scope.**
- Support OECD compressed local files without project-directory extraction. **Implemented: `read_pisa_file` accepts ZIPs containing exactly one supported data file and extracts only to a temporary file.**
- Add a runnable synthetic end-to-end example. **Implemented: `examples/fit_synthetic.py` and `examples/synthetic_workflow.ipynb` cover preparation, fit, analysis, comparison, and save/load without restricted data.**
- Add aggregate result export. **Implemented: result objects expose JSON-compatible `to_dict()` and `to_json()`.**
- Add third- and fourth-order joint moment outputs for reproduction checks. **Implemented: `AnalysisResult.higher_order_moments` and observed/model higher-order fields in `FitResult` are available on exact and sampled paths.**
- Include observed/model moments in fit results. **Implemented: `FitResult` now carries first- and second-order moment arrays.**
- Add correlation outputs to analysis results. **Implemented: `AnalysisResult.correlations` uses stable Bernoulli Pearson correlations.**
- Add versioned artifact metadata and caller-supplied configuration metadata. **Implemented: saved artifacts include format/package metadata, random state, and `DataConfig.metadata`.**
- Add aggregate moment-order comparison for reproduction checks. **Implemented: `compare_moment_orders` reports per-order errors and pass/fail status.**
- Add a dependency-light named-column preparation helper. **Implemented: `PreparedData` and `prepare_tabular_data` are available.**
- Add pre-training tabular quality evidence. **Implemented: `validate_tabular_data` reports required-column, shape, missingness, infinity, and weight issues without transforming data.**
- Validate configuration names and thresholds early. **Implemented: `DataConfig` rejects collisions, empty names, and non-finite explicit thresholds.**
- Preserve named-column semantics during inference. **Implemented: fitted feature names select reordered mapping/DataFrame columns and reject missing columns.**
- Add a runnable local PISA workflow template. **Implemented: `examples/pisa_local_workflow.py` performs explicit mapping, quality checks, fit, provenance recording, and aggregate report export without downloading or bundling data.**
- Preserve ordinary weight-field provenance. **Implemented: `DataConfig.sample_weight_name` is validated and serialized with fitted artifacts and used by the local workflows.**

## v0.2 - robust computation

- Automatic Monte Carlo selection for larger systems. **Implemented: `calculation="auto"` selects exact enumeration or Gibbs sampling from `max_exact_nodes`, while `exact` and `monte_carlo` can be forced for reproducible runs.**
- Multiple chains, convergence diagnostics, burn-in, effective sample size, and error estimates. **Implemented: multi-chain R-hat, autocorrelation-based ESS, ESS-derived MCSE, configurable quality thresholds, and fit warnings are present; scientific threshold calibration remains domain-dependent.**
- More missing-value strategies and sample-weight handling. **Partially implemented: `error`, `median`, `mean`, and `zero` preserve rows; PISA-specific missing codes and row-dropping policy remain caller-owned.**
- Example pretrained model artifact only if its data and redistribution rights are clear.

## v0.3 - extensibility

- Pluggable trainer, sampler, analyzer, and preprocessor components. **Implemented: public protocols for all four lifecycles can be injected into `LearningModel`; arbitrary third-party components remain runtime-only and are not serialized automatically.**
- sklearn adapter. **Implemented: dependency-free `LearningEnergyClassifier` provides the common estimator methods while preserving the structured analysis API.**
- Multi-domain manager for independent target models. **Implemented: `MultiDomainManager` provides independent fit/predict/analyze/save/load operations per domain.**
- Better CLI and reporting exports. **Implemented: `python -m learning_energy_model fit/predict/analyze` and the `learning-energy-model` console entry point support numeric CSV workflows and aggregate interpretability export.**

## v1.0 - stable release

- Stable public API and serialization format.
- Supported Python/PyTorch matrix in CI.
- Complete user, theory, and reproduction documentation.
- PyPI release under the finalized project name and license.

## Current status

The repository is currently at Stage 2 for the paper-scale core. Package source, metadata, tests, CI, initial Gibbs sampling, generic named-column preparation, an optional local PISA adapter, and runnable synthetic workflows are present; real-data PISA reproduction runs and production release work remain.
