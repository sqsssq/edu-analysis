# Task 014: Add moment-order comparison helper

## Status

Review Ready

## Source PRD

- `docs/prd/00-product-brief.md`
- `docs/prd/ROADMAP.md`
- `docs/domain/PROJECT_RULES.md`

## Goal

Provide a strict, aggregate-only comparison helper for first- through fourth-order moments.

## User Value

Researchers can quantify model-versus-reference agreement consistently for synthetic checks and future PISA reproduction runs.

## Scope

- Match moment orders and keys explicitly.
- Report maximum/mean absolute errors and declared tolerances.
- Support arrays and keyed higher-order moment mappings.
- Export the report through the existing result interface.

## Out of Scope

- Loading or distributing PISA data.
- Statistical significance or complex-survey variance.
- Passing incomplete comparisons silently.

## Domain Requirement

Keep comparisons aggregate and require aligned preprocessing/definitions before interpretation.

## Harness Impact

Adds a feedback sensor for the first- through fourth-order reproduction contract.

## Acceptance Criteria

- Mismatched orders or keys raise actionable errors.
- Reports expose per-order maximum and mean absolute errors and pass/fail status.
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

- The comparison helper is implemented, tested, and documented.
- The verified change is committed and pushed.
