# Task 005: Add a runnable synthetic workflow

## Status

Review Ready

## Source PRD

- `docs/prd/PRODUCT_BRIEF.md`
- `docs/prd/ROADMAP.md`
- `docs/design.md`

## Goal

Provide a no-data, no-network example that exercises the public training, analysis, and serialization workflow.

## User Value

New users can validate their installation and understand the package contract before handling their own or restricted research data.

## Scope

- Deterministic synthetic-data example under `examples/`.
- README quickstart instructions and Chinese-language pointer.
- Documentation status update.

## Out of Scope

- PISA-derived data or claims about paper reproduction.
- A production benchmark or a stable scientific result.
- A command-line interface for arbitrary datasets.

## Domain Requirement

Clearly label generated data as synthetic and retain the model’s interpretability and non-causal language.

## Harness Impact

Adds a user-facing smoke-test path that can be run without external data or credentials.

## Acceptance Criteria

- The example runs from a clean checkout with core dependencies and writes only the requested model artifact.
- The example exercises `fit`, `analyze`, and `save` and reports convergence-path metadata.
- Standard package verification passes.

## Verification Method

```bash
python -m examples.fit_synthetic /tmp/learning-energy-model-example.pt
python -m pytest -q
python -m ruff check learning_energy_model tests examples
python -m mypy learning_energy_model
bash scripts/verify.sh --strict-instance
```

## Done When

- The example is runnable and documented.
- The verified change is committed and pushed.
