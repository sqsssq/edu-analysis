# Task 016: Add a lightweight estimator adapter

## Status

Review Ready

## Objective

Make the interpretable energy model easy to call from estimator-oriented Python workflows without making scikit-learn a core dependency.

## Scope

- Add `LearningEnergyClassifier` with `fit`, `predict_proba`, `predict`, `get_params`, and `set_params`.
- Preserve access to the wrapped structured `analyze()` result.
- Keep binary classes, energy-derived probabilities, and the existing preprocessing contract explicit.

## Out of scope

- Full scikit-learn compatibility or mandatory scikit-learn installation.
- Automatic hyperparameter search or causal interpretation.

## Acceptance criteria

- The adapter returns two-column probabilities ordered by `classes_`.
- The adapter returns binary predictions using a documented 0.5 cutoff.
- Parameters can be inspected and changed before refitting.
- Existing package tests, lint, type checks, wheel build, and strict HarnessWeaver verification pass.

## Handoff

The adapter is intentionally small; future pipeline integration can add optional scikit-learn tests once the dependency policy is decided.
