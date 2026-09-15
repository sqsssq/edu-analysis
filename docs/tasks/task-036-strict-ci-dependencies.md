# Task 036: Make CI dependency checks strict

## Status

Review Ready

## Source PRD

- `docs/prd/06-acceptance-criteria.md`
- `docs/prd/ROADMAP.md`

## Goal

Ensure CI cannot silently skip linting, typing, or package checks because the
development extra failed to install.

## Scope

- Remove the fallback from `.[dev]` installation to the base package.
- Keep the declared Python matrix and package checks unchanged.
- Correct acceptance documentation to reflect implemented lifecycle and result contracts.

## Acceptance Criteria

- A project with `pyproject.toml` must install `.[dev]` successfully or fail the job.
- CI still runs tests, lint, typing, build, and CLI smoke tests.
- Standard repository verification passes.

## Done When

- CI dependency installation is strict, documented, verified, committed, and pushed.
