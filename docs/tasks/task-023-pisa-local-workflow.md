# Task 023: Add a runnable local PISA workflow template

## Status

Review Ready

## Objective

Provide a concrete executable template for fitting a locally obtained, codebook-mapped PISA file.

## Scope

- Read CSV/SAS/SPSS or a single-data-file ZIP through the package adapter.
- Apply explicit missing-code mapping, quality checks, training, and analysis.
- Write only the model artifact and aggregate JSON report requested by the caller.

## Out of scope

- Downloading or redistributing PISA data.
- Inferring variable semantics, missing codes, survey weights, or plausible values.
- Official PISA estimates.

## Acceptance criteria

- The script requires explicit feature, target, and missing-code choices.
- The output report contains quality, fit, and analysis aggregates without raw rows.
- The PISA guide documents how to invoke the template.
- Standard package verification passes.

## Handoff

The next research step is to select paper-aligned PISA 2018 variables and record their codebook mapping before running the template.
