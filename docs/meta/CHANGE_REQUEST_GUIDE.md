# Change Request Guide

Use this guide when the user changes scope after a PRD, task, or implementation direction already exists.

## Classification

Classify the request as one of:

- `Clarification`: makes the existing task clearer without changing scope.
- `Small extension`: adds a small related requirement that still fits the current task.
- `New task`: adds separable work that should be tracked independently.
- `PRD rewrite`: changes product direction, MVP boundaries, domain model, or architecture assumptions.

## Process

1. Restate the requested change.
2. Identify affected files.
3. Classify the change.
4. Decide whether the current task can safely absorb it.
5. Update docs before or alongside implementation.
6. Reconfirm acceptance criteria and verification.

## Output Template

```md
## Change Request Summary

- Requested change:
- Classification:
- Affected PRD files:
- Affected task:
- Scope decision:
- Verification impact:
- Recommended next step:
```
