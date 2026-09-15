# Roadmap

## v0.1 - verified paper-scale core

- Define package layout and public API.
- Implement binary pairwise energy model.
- Implement exact state enumeration for 19 nodes.
- Implement weighted empirical moments and moment-matching trainer.
- Implement conditional target probability and structured diagnostics.
- Add synthetic recovery tests.
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

