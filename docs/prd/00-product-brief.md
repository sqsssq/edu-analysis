# Product Brief

## Summary

`Interpretable Learning Energy Model` is a reusable PyTorch package for fitting and analyzing an interpretable pairwise maximum-entropy energy model.

## Product Context

- Domain: `research Python package for educational and structured-data energy modeling`
- Primary user: `researchers and machine-learning engineers`
- Primary user problem: `Researchers need a reproducible way to fit, inspect, validate, and reuse the paper's energy model on their own structured data.`
- MVP focus: `fit, inspect, and reproduce a binary maximum-entropy learning model`

## Product Promise

`The package exposes a simple fit/predict/save/load API while preserving the model's moments, interactions, diagnostics, and assumptions.`

## Success Criteria

The MVP succeeds when:

- `A user can fit a paper-sized binary model and obtain structured diagnostics.`
- `Synthetic recovery and exact-versus-Monte-Carlo tests pass.`
- `PISA reproduction benchmarks document first- through fourth-order correlation agreement and known gaps.`
