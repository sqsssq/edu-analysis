# Roadmap

## v0.1 - verified paper-scale core

- Add GitHub Actions CI for strict harness verification and the supported Python matrix.
- Define package layout and public API. **In progress: initial package skeleton is present.**
- Implement binary pairwise energy model. **In progress: exact binary model is present.**
- Implement exact state enumeration for 19 nodes. **In progress: exact enumeration is present.**
- Implement weighted empirical moments and moment-matching trainer. **In progress: initial trainer is present.**
- Implement conditional target probability and structured diagnostics. **In progress: initial API is present.**
- Add synthetic recovery tests. **In progress: initial API tests are present; parameter-recovery coverage remains.**
- Add exact-vs-Monte-Carlo agreement tests on small systems.
- Add PISA reproduction benchmark contracts and preparation instructions.

## v0.2 - robust computation

- Automatic Monte Carlo selection for larger systems.
- Multiple chains, convergence diagnostics, burn-in, effective sample size, and error estimates.
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

The repository is currently at Stage 0. Harness documentation, project rules, and CI are present; package source code, package metadata, tests, notebooks, data preparation scripts, and reproduction benchmarks are not yet implemented.
