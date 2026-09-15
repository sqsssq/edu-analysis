# Task 011: Version serialized artifacts

## Status

Review Ready

## Source PRD

- `docs/prd/04-content-model.md`
- `docs/prd/06-acceptance-criteria.md`
- `docs/prd/ROADMAP.md`

## Goal

Make saved models traceable and forward-compatible by recording artifact/package versions, caller metadata, random state, sampler settings, and fit logs.

## User Value

Researchers can reproduce and audit a saved model without embedding the original dataset.

## Scope

- Versioned artifact metadata with backward-compatible loading.
- `DataConfig.metadata` for variable/source descriptions.
- Torch and NumPy random state capture.
- Round-trip tests.

## Out of Scope

- Embedding raw observations or restricted PISA data.
- Guaranteeing compatibility across arbitrary future artifact formats.

## Domain Requirement

Preserve preprocessing assumptions and data provenance metadata while excluding raw records.

## Harness Impact

Adds a feedback sensor for serialization traceability.

## Acceptance Criteria

- Saved artifacts record format/package version and caller metadata.
- Saved artifacts record random state and fit logs.
- Existing artifacts without the new metadata remain loadable.
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

- Artifact metadata is implemented, tested, and documented.
- The verified change is committed and pushed.
