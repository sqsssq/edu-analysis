# Task 020: Add a multi-domain model manager

## Status

Review Ready

## Objective

Support several independent target models in one project without coupling their parameters or preprocessing state.

## Scope

- Add `MultiDomainManager` with per-domain `fit`, `predict`, and `analyze`.
- Save and load a directory of independent model artifacts with a JSON manifest.
- Preserve each domain's existing `LearningModel` serialization and diagnostics.

## Out of scope

- Joint multi-task training or shared parameters.
- Cross-domain causal comparisons.
- Automatic domain discovery.

## Acceptance criteria

- Domains can be fitted independently and retain independent reports.
- Unknown and duplicate domains fail with actionable errors.
- Manager save/load preserves domain names and predictions.
- Standard package verification passes.

## Handoff

Future multi-task research can build on the manager without changing the single-target model contract.
