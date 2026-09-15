# Task 032: Add replaceable component protocols

## Status

Review Ready

## Source PRD

- `docs/prd/ROADMAP.md`
- `docs/prd/04-content-model.md`

## Goal

Allow callers to replace preprocessing and Monte Carlo sampling implementations
while retaining the stable `LearningModel` API and structured diagnostics.

## Scope

- Publish `PreprocessorProtocol` and `SamplerProtocol`.
- Allow compatible components to be injected into `LearningModel`.
- Preserve built-in components as the default.
- Test that a caller-provided sampler is actually used.

## Out of Scope

- Serializing arbitrary third-party component instances.
- Trainer and analyzer lifecycle hooks, which require a separate contract.

## Acceptance Criteria

- Existing default behavior is unchanged.
- A compatible custom sampler can participate in fitting and sampling.
- The public protocols are importable from the package root.
- Standard package verification passes.

## Done When

- Component protocols are implemented, tested, documented, committed, and pushed.
