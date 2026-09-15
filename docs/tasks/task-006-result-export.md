# Task 006: Add dependency-light result export

## Status

Review Ready

## Source PRD

- `docs/prd/PRODUCT_BRIEF.md`
- `docs/prd/04-content-model.md`
- `docs/design.md`

## Goal

Allow callers to persist aggregate fit, prediction, and analysis outputs without requiring pandas or serializing raw input data.

## User Value

Researchers can archive parameters, diagnostics, assumptions, and limitations as ordinary JSON for reports and pipelines.

## Scope

- `to_dict()` and `to_json()` on all public result objects.
- Recursive conversion of NumPy arrays and scalars.
- Round-trip test and API documentation.

## Out of Scope

- Automatic report generation.
- DataFrame-specific formatting.
- Exporting raw observations or user data.

## Domain Requirement

Keep assumptions, limitations, and sampler diagnostics in exported analysis results; export is aggregate-only.

## Harness Impact

Adds a feedback sensor for stable, JSON-compatible result serialization.

## Acceptance Criteria

- Every public result object produces a JSON-compatible dictionary and valid JSON.
- Export includes structured diagnostics and analysis guardrails.
- Core dependencies remain unchanged.
- Standard package verification passes.

## Verification Method

```bash
python -m pytest -q
python -m ruff check learning_energy_model tests examples
python -m mypy learning_energy_model
python -m build --wheel --no-isolation
bash scripts/verify.sh --strict-instance
```

## Done When

- Export methods are tested and documented.
- The verified change is committed and pushed.
