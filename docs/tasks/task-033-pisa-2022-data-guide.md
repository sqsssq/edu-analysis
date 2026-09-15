# Task 033: Add the PISA 2022 local-data guide

## Status

Review Ready

## Source PRD

- `docs/reproduction/PISA_2022_DATA_GUIDE.md`
- `docs/prd/ROADMAP.md`

## Goal

Give users a safe, runnable PISA 2022 file-selection and mapping workflow
without downloading or redistributing restricted source data.

## Scope

- Document the official PISA 2022 data-file categories and supported formats.
- Show how to save and reuse a reviewed `PISAMapping` contract.
- State the local-only and non-official-estimate boundaries.

## Out of Scope

- Hard-coded variable names without codebook verification.
- Automatic downloading or raw-data packaging.

## Acceptance Criteria

- The guide links to the official source and gives an end-to-end local example.
- The example uses only aggregate outputs and reviewed mapping metadata.
- Harness verification and markdown-link checks pass.

## Done When

- The PISA 2022 guide is written, verified, documented in the README, committed, and pushed.
