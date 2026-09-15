# Task 041: Ship the PEP 561 package marker

## Status

Review Ready

## Source PRD

- `docs/prd/04-content-model.md`
- `docs/prd/06-acceptance-criteria.md`

## Goal

Make the package's inline annotations and public component protocols visible to
downstream type checkers after wheel installation.

## Scope

- Add `learning_energy_model/py.typed`.
- Include the marker in built distributions.
- Verify wheel contents.

## Out of Scope

- Claiming complete static typing for arbitrary user-provided components.
- Changing runtime behavior.

## Acceptance Criteria

- The built wheel contains `learning_energy_model/py.typed`.
- Existing tests and type checks remain green.
- Standard package verification passes.

## Done When

- The type marker is included, verified, documented, committed, and pushed.
