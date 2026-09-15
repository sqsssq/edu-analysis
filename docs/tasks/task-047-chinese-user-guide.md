# Task 047: Complete the Chinese user guide

Status: Review Ready

## Goal

Make the Chinese repository entry point sufficient for a new user to install
the package, train a model on their own table, inspect results, and understand
the PISA data boundary.

## Delivered

- Added core and optional installation commands.
- Added direct-array and named-table training examples.
- Documented save/load, calculation paths, and sampling diagnostics.
- Documented PISA provenance and complex-survey limitations.

## Verification

`pytest`, `ruff`, mypy, wheel build, and
`bash scripts/verify.sh --strict-instance`.
