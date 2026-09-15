# Task Workflow

## Purpose

This folder holds small, reviewable implementation tasks. A task is the unit Codex should execute, verify, hand off, and commit.

Use `docs/tasks/TASK_TEMPLATE.md` for new task files.

## Task Status Lifecycle

```text
Draft
-> Ready
-> In Progress
-> Review Ready
-> Approved
-> Committed
-> Done
```

Do not use `Done` for work that is merely implemented but not verified, reviewed, or committed.

## Task Index Rule

When the task list grows beyond a few files, add a task index to this README:

```md
| Task | Status | Source PRD | Verification Evidence |
| --- | --- | --- | --- |
| `task-001-example.md` | Ready | `docs/prd/...` | planned: `bash scripts/verify.sh` |
```

## Current Tasks

| Task | Status | Source PRD | Verification Evidence |
| --- | --- | --- | --- |
| `task-001-core-package.md` | Review Ready | `docs/prd/00-product-brief.md`, `docs/prd/01-mvp-scope.md` | `pytest`, `ruff`, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-002-sampling-validation.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/prd/06-acceptance-criteria.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-003-tabular-preparation.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/prd/04-content-model.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
