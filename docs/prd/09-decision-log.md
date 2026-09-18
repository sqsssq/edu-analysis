# Decision Log

## Accepted Decisions

### 2026-09-15: Adopt HarnessWeaver workflow

This project uses PRD-first planning, small task files, verification before handoff, diff review, and human approval before commit.

### 2026-09-15: Confirm package direction

The first release targets a PyTorch binary pairwise maximum-entropy energy model with exact enumeration at paper scale and automatic Monte Carlo at larger scale. It prioritizes interpretable moment matching, supports fresh user data and saved-model inference, and does not make causal or individual-decision claims.

### 2026-09-15: Add GitHub Actions CI

GitHub Actions is the project's CI system. It runs strict HarnessWeaver verification on pushes and pull requests and tests Python 3.10-3.12. Package tests, linting, typing, and builds become active automatically once the corresponding project metadata and tooling are added.

### 2026-09-18: Keep original-style Monte Carlo Adam as an explicit compatibility path

The package keeps exact enumeration plus explicit KL-gradient training as the
paper-aligned reference path, and adds a separate `method="adam"` with
`calculation="monte_carlo"` for compatibility with the public original
implementation. The compatibility path remains binary and uses the package's
documented `{0, 1}` energy convention; exact numerical equivalence with the
original C++ spin/Metropolis executable is not claimed.

### 2026-09-18: Add continuous Gaussian model as a separate experimental family

Continuous input support must not silently remove binary preprocessing from
`LearningModel`. The project adds a separate `ContinuousEnergyModel` with a
quadratic Gaussian energy, closed-form weighted fit, precision-based
conditional interactions, sampling, and artifact persistence. Mixed-node,
nonlinear, and non-Gaussian extensions remain separate future tasks.
