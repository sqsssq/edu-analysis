# Package and Research Experience Standards

## Purpose

This file defines project-specific standards for the Python package, notebooks, generated reports, and any future UI. The primary product experience is a researcher moving from data preparation to a verified, interpretable model result.

Use this file for API ergonomics, notebook/report presentation, language, and future interface states. Keep reusable workflow rules in `docs/meta/`, harness rules in `docs/harness/`, and scientific guardrails in `docs/domain/PROJECT_RULES.md`.

## Primary Experience

- Primary user: `researchers and machine-learning engineers`
- MVP focus: `fit, inspect, and reproduce a binary maximum-entropy learning model`
- The design should support `declare data rules -> fit -> validate -> inspect -> save/reload`.
- The design must not become `an opaque black-box predictor or an irreproducible research script`.
- The simplest valid example should fit a small binary model without requiring users to understand internal sampler details.
- Advanced users must be able to inspect `h`, `J`, moments, correlations, convergence, and preprocessing metadata.

## API and Result Standards

- Prefer a small stable surface: `LearningModel`, `DataConfig`, `FitResult`, `PredictionResult`, and `AnalysisResult`.
- Return structured results with named fields and metadata; do not return unexplained positional arrays.
- Preserve the preprocessing contract in every saved model.
- Distinguish prediction, association, model-internal intervention, and causal inference in names and prose.
- Make exact enumeration and Monte Carlo choices visible in diagnostics.

## Notebook and Report Standards

- Start with the smallest complete MVP loop before adding secondary surfaces.
- Make core user actions visible, reversible where appropriate, and easy to verify.
- Include empty, loading, error, invalid action, success, and completion states when the UI exists.
- Preserve review or placeholder status when content is not final.
- Show assumptions, threshold rules, missing-value handling, sample weights, and sampler diagnostics beside results.
- Every paper-reproduction notebook must identify its data preparation path and any deviation from the paper.
- Tables and figures should label variables by stable names and explain the sign convention for `h` and `J`.

## Future UI Standards

- Prefer clear hierarchy, readable density, and domain-appropriate tone over decorative complexity.
- Use layout and labels that help the primary user decide what to do next.
- Avoid generic landing-page polish unless the PRD explicitly calls for a marketing surface.
- If a UI is added, prioritize data schema, training progress, diagnostics, and report export over decorative visualization.

## Accessibility Standards

- Keep keyboard access, visible focus, text alternatives, and readable contrast in scope for UI tasks.
- Document any accessibility limitation in the task handoff if it cannot be resolved in the current slice.

## Verification Questions

- Does the design support the MVP loop?
- Are required package, notebook, report, or UI states represented or intentionally deferred?
- Does the design preserve domain-specific rules from `docs/domain/PROJECT_RULES.md`?
- Is the experience specific to `Interpretable Learning Energy Model` rather than a generic app?
