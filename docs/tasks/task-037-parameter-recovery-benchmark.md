# Task 037: Add a repeatable parameter-recovery benchmark

## Status

Review Ready

## Source PRD

- `docs/prd/ROADMAP.md`
- `docs/prd/06-acceptance-criteria.md`

## Goal

Provide inspectable synthetic evidence for parameter recovery and moment
agreement before running any real PISA reproduction.

## Scope

- Add a deterministic known-distribution benchmark script.
- Report aggregate `h/J` errors and moment-order comparison results.
- Add a test and command-line usage documentation.

## Out of Scope

- Claiming agreement with the paper or official PISA estimates.
- Committing raw observations or generated benchmark rows.

## Acceptance Criteria

- The benchmark is deterministic and uses exact calculation.
- The aggregate report records calculation diagnostics, moment comparison, and parameter errors.
- Standard package verification passes.

## Done When

- The benchmark is implemented, tested, documented, committed, and pushed.
