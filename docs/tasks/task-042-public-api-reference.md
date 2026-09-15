# Task 042: Add a public API reference

## Status

Review Ready

## Source PRD

- `docs/API.md`
- `docs/prd/01-mvp-scope.md`

## Goal

Give downstream users one durable reference for training, inference, aggregate
reports, PISA preparation, and extension points.

## Scope

- Document public classes and their primary methods.
- Document calculation paths, result diagnostics, serialization, and limitations.
- Link the reference from the README.

## Out of Scope

- Promising complete sklearn compatibility.
- Claiming official PISA estimates or causal interpretations.

## Acceptance Criteria

- Every documented example uses an exported public symbol.
- Important interpretation and serialization boundaries are explicit.
- Markdown links and standard repository verification pass.

## Done When

- The API reference is written, verified, linked, committed, and pushed.
