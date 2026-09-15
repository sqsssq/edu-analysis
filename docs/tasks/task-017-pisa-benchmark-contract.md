# Task 017: Define the PISA reproduction benchmark contract

## Status

Review Ready

## Objective

Define an inspectable, aggregate-only contract for future PISA reproduction runs.

## Scope

- Record source, codebook mapping, preprocessing, weights, seeds, and computation path.
- Require first- through fourth-order moment outputs and parameter conventions.
- Define exact-versus-Monte-Carlo reporting and the current survey-inference boundary.

## Out of scope

- Downloading, storing, or redistributing PISA files.
- Claiming reproduction without aligned local data.
- Implementing replicate weights or plausible-value aggregation.

## Acceptance criteria

- A future run has a concrete provenance and preprocessing checklist.
- Aggregate comparison uses `compare_moment_orders` with declared tolerances.
- The contract explicitly prevents official-estimate and causal overclaims.
- Strict HarnessWeaver verification passes.

## Handoff

The next PISA task can use a legitimately obtained local PISA 2018 file and a
codebook-backed mapping to produce the first benchmark report.
