# Task 022: Preserve named columns during inference

## Status

Review Ready

## Objective

Ensure prediction uses the fitted feature names when callers pass a mapping or named table.

## Acceptance criteria

- Reordered named columns produce the same predictions as the fitted array order.
- Extra named columns are ignored rather than silently changing feature positions.
- Missing fitted columns fail with an actionable error.
- Standard package verification passes.

## Handoff

Array inputs retain positional semantics; named tables use the recorded feature names.
