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

- Publish `PreprocessorProtocol`, `SamplerProtocol`, `TrainerProtocol`, and `AnalyzerProtocol`.
- Allow compatible components for all four lifecycles to be injected into `LearningModel`.
- Preserve built-in components as the default.
- Test that caller-provided sampler, trainer, and analyzer components are actually used.

## Out of Scope

- Serializing arbitrary third-party component instances.
- Automatic serialization of arbitrary third-party component instances.

## Acceptance Criteria

- Existing default behavior is unchanged.
- Compatible custom sampler, trainer, and analyzer components can participate in the model lifecycle.
- The public protocols are importable from the package root.
- Standard package verification passes.

## Done When

- Component protocols are implemented, tested, documented, committed, and pushed.
