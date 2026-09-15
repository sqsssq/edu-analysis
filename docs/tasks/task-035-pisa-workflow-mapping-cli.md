# Task 035: Connect the PISA workflow to mapping contracts

## Status

Review Ready

## Source PRD

- `docs/reproduction/PISA_2022_DATA_GUIDE.md`
- `docs/prd/ROADMAP.md`

## Goal

Make the local PISA workflow consume a reviewed mapping JSON directly and expose
the package's current calculation and sampling-quality controls.

## Scope

- Add `--mapping` support with provenance fallback from mapping metadata.
- Keep the existing explicit-column CLI form backward-compatible.
- Expose missing strategies, calculation selection, and MC quality thresholds.
- Smoke-test the workflow with a synthetic local archive.

## Out of Scope

- Downloading or inferring PISA variables.
- Treating ordinary row weights as complex-survey inference.

## Acceptance Criteria

- A reviewed mapping contract can drive the local workflow without repeating column names.
- Existing explicit arguments still work.
- Aggregate report and model output remain local-only.
- Standard package verification passes.

## Done When

- The workflow integration is implemented, tested, documented, committed, and pushed.
