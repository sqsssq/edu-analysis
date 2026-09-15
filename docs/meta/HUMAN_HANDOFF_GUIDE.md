# Human Handoff Guide

Use this guide when a task is ready for human review.

## Handoff Goals

The handoff should help the reviewer answer:

1. What changed?
2. Why was it changed?
3. Which PRD or task does it satisfy?
4. How was it verified?
5. What domain-specific decision was made?
6. What should happen next?

## Handoff Template

```md
# Human Handoff

## Task

Task ID and title.

## Status

Ready for review / Needs human decision / Blocked

## What Changed

Brief summary.

## Files Changed

- `path` - reason

## PRD Coverage

- `docs/prd/...`

## Domain Impact

Explain how this supports `docs/domain/PROJECT_RULES.md`.

## Harness Impact

State feedforward rules or feedback sensors affected.

## Verification Performed

- `bash scripts/verify.sh` - passed/failed/unavailable

## Known Limitations

None, or list clearly.

## Recommended Next Step

Approve and commit / request changes / update PRD / create follow-up task.
```
