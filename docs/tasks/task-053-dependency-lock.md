# Task 053: Lock project dependencies

Status: Review Ready

## Goal

Make development and optional PISA environments reproducible across the
supported Python matrix.

## Delivered

- Added `uv.lock` generated from the project metadata.
- Included platform and Python-version resolution markers and package hashes.
- Updated CI to verify the lock and install development/PISA dependencies from
  locked exports.
- Documented dependency-lock status in the roadmap and acceptance criteria.

## Verification

`uv lock --check`, locked dependency export/install, `pytest`, `ruff`, mypy,
wheel build, and `bash scripts/verify.sh --strict-instance`.
