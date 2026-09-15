# Task 038: Add a local-only PISA reproduction notebook

## Status

Review Ready

## Source PRD

- `docs/prd/ROADMAP.md`
- `docs/prd/06-acceptance-criteria.md`

## Goal

Provide an inspectable notebook template for running reviewed PISA mappings and
comparing aggregate moments without bundling raw observations.

## Scope

- Run deterministic synthetic smoke mode by default.
- Accept local PISA input and a reviewed mapping contract through environment variables.
- Fit, compare moments, assert finite aggregate results, and optionally export JSON.
- Document the local-only and non-official-estimate boundaries.

## Out of Scope

- Downloading or embedding PISA data.
- Claiming a paper reproduction without caller-supplied codebook-aligned data.

## Acceptance Criteria

- The notebook executes top-to-bottom without local PISA files.
- The rendered HTML contains visible aggregate checks and the caveat boundary.
- Standard repository verification passes.

## Done When

- The notebook is executed, visually checked, documented, committed, and pushed.
