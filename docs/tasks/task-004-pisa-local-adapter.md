# Task 004: Add an explicit local PISA adapter

## Status

Review Ready

## Source PRD

- `docs/prd/ROADMAP.md`
- `docs/reproduction/PISA_2018_DATA_GUIDE.md`
- `docs/domain/PROJECT_RULES.md`

## Goal

Allow a user who has legitimately obtained a PISA Public Use File to load it locally and apply an explicit codebook-backed column mapping without putting the data in the repository.

## User Value

The reproduction workflow becomes executable after the user obtains the data, while the core package remains free of a mandatory pandas/pyreadstat dependency.

## Scope

- Optional local readers for CSV/TSV, SAS, and SPSS files.
- `PISAMapping` for features, target, ordinary weight, and codebook-confirmed missing codes.
- Optional `pisa` dependencies and tests using synthetic in-memory data.

## Out of Scope

- Downloading data or accepting OECD registration on behalf of the user.
- Committing raw or derived PISA data.
- Full complex-survey variance, replicate weights, plausible-value aggregation, or official PISA estimates.

## Domain Requirement

Require explicit codebook-backed missing-value mappings and preserve the rule that local PISA files remain outside Git.

## Harness Impact

Adds a deterministic adapter boundary without introducing restricted data into tests or fixtures.

## Acceptance Criteria

- A user can call `prepare_pisa_file(path, PISAMapping(...))` after installing the optional dependencies.
- PISA-specific missing codes are explicit rather than silently guessed.
- Core installation does not require pandas or pyreadstat.
- Standard package verification passes.

## Verification Method

```bash
python -m pytest -q
python -m ruff check learning_energy_model tests
python -m mypy learning_energy_model
python -m build --wheel --no-isolation
bash scripts/verify.sh --strict-instance
```

## Done When

- The adapter is exported, tested with synthetic data, and documented.
- The verified change is committed and pushed.
