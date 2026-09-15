# Roadmap

## v0.1 - verified paper-scale core

- Add GitHub Actions CI for strict harness verification and the supported Python matrix.
- Define package layout and public API. **In progress: initial package skeleton is present.**
- Implement binary pairwise energy model. **In progress: exact binary model is present.**
- Implement exact state enumeration for 19 nodes. **In progress: exact enumeration is present.**
- Implement weighted empirical moments and moment-matching trainer. **In progress: initial trainer is present.**
- Implement conditional target probability and structured diagnostics. **In progress: initial API is present.**
- Add synthetic recovery tests. **Implemented: small-model parameter recovery is covered; broader calibration remains.**
- Add exact-vs-Monte-Carlo agreement tests on small systems.
- Add PISA reproduction benchmark contracts and preparation instructions.
- Add PISA source and local-data instructions. **Implemented: official source, access boundary, and preparation checklist are documented.**
- Add an optional local PISA reader and explicit mapping adapter. **Implemented: `PISAMapping` and `prepare_pisa_file` are available; survey inference remains out of scope.**
- Add a dependency-light named-column preparation helper. **Implemented: `PreparedData` and `prepare_tabular_data` are available.**

## v0.2 - robust computation

- Automatic Monte Carlo selection for larger systems. **In progress: Gibbs sampling is present.**
- Multiple chains, convergence diagnostics, burn-in, effective sample size, and error estimates. **In progress: initial diagnostics are present.**
- More missing-value strategies and sample-weight handling.
- Example pretrained model artifact only if its data and redistribution rights are clear.

## v0.3 - extensibility

- Pluggable trainer, sampler, analyzer, and preprocessor components.
- sklearn adapter.
- Multi-domain manager for independent target models.
- Better CLI and reporting exports.

## v1.0 - stable release

- Stable public API and serialization format.
- Supported Python/PyTorch matrix in CI.
- Complete user, theory, and reproduction documentation.
- PyPI release under the finalized project name and license.

## Current status

The repository is currently at Stage 2 for the paper-scale core. Package source, metadata, tests, CI, initial Gibbs sampling, generic named-column preparation, and an optional local PISA adapter are present; country-specific mappings, reproduction notebooks, complete parameter-recovery benchmarks, and production release work remain.
