# Task 054: Document the locked development environment

Status: Review Ready

## Goal

Give contributors and researchers a direct, reproducible installation path
that uses the committed dependency lock.

## Delivered

- Documented `uv sync --locked --extra dev` in the English and Chinese entry
  points.
- Added `.venv/` to the local-only ignore rules.
- Clarified that pip remains available for ordinary package installation.

## Verification

`uv lock --check`, locked sync dry-run, `pytest`, ruff, mypy, and
`bash scripts/verify.sh --strict-instance`.
