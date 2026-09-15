# Task Breakdown Guide

Use this guide to turn approved PRD direction into small, executable tasks.

## Required Inputs

Before creating tasks, read:

- `AGENTS.md`
- relevant files under `docs/prd/`
- `docs/domain/PROJECT_RULES.md`
- `docs/harness/05-stage-checklists.md`

## Task Size Rule

Each task should be small enough that an agent can understand it, modify a limited number of files, verify it locally, produce a reviewable diff, and stop cleanly after handoff.

## Task Requirements

Each task should state:

- source PRD files,
- scope and out-of-scope boundaries,
- domain requirement,
- harness impact,
- acceptance criteria,
- verification method.

## Output Location

Write task files under `docs/tasks/` using `docs/tasks/TASK_TEMPLATE.md`.
