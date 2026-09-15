# Task 039: Smoke-test the optional PISA extra in CI

## Status

Review Ready

## Source PRD

- `docs/prd/06-acceptance-criteria.md`
- `docs/prd/ROADMAP.md`

## Goal

Verify that the optional PISA reader dependencies advertised by the package can
be installed and imported on a supported Python version.

## Scope

- Install `.[pisa]` in the Python 3.12 CI job.
- Import pandas and pyreadstat as an installation smoke check.
- Keep the core dependency matrix unchanged.

## Out of Scope

- Downloading or parsing restricted PISA files in CI.
- Testing country-specific mappings without reviewed fixtures.

## Acceptance Criteria

- The optional PISA extra install/import check runs on CI.
- Existing tests and strict harness verification remain enabled.
- No raw PISA data is introduced.

## Done When

- The optional dependency smoke check is configured, documented, and verified in CI.
