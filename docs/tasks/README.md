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
| `task-004-pisa-local-adapter.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/reproduction/PISA_2018_DATA_GUIDE.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-005-synthetic-example.md` | Review Ready | `docs/prd/PRODUCT_BRIEF.md`, `docs/prd/ROADMAP.md` | synthetic smoke test, `pytest`, `ruff`, mypy, and `bash scripts/verify.sh --strict-instance` |
| `task-006-result-export.md` | Review Ready | `docs/prd/PRODUCT_BRIEF.md`, `docs/prd/04-content-model.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-007-kl-training.md` | Review Ready | `docs/prd/PRODUCT_BRIEF.md`, `docs/prd/ROADMAP.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-008-higher-order-moments.md` | Review Ready | `docs/prd/00-product-brief.md`, `docs/prd/04-content-model.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-009-fit-moment-report.md` | Review Ready | `docs/prd/04-content-model.md`, `docs/prd/06-acceptance-criteria.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-010-sampler-diagnostics.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/prd/06-acceptance-criteria.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-011-versioned-artifacts.md` | Review Ready | `docs/prd/04-content-model.md`, `docs/prd/06-acceptance-criteria.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-012-correlation-output.md` | Review Ready | `docs/prd/04-content-model.md`, `docs/prd/06-acceptance-criteria.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-013-weight-validation.md` | Review Ready | `docs/domain/PROJECT_RULES.md`, `docs/prd/06-acceptance-criteria.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-014-moment-comparison.md` | Review Ready | `docs/prd/00-product-brief.md`, `docs/prd/ROADMAP.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-015-notebook-companion.md` | Review Ready | `docs/prd/PRODUCT_BRIEF.md`, `docs/prd/ROADMAP.md` | executed notebook, rendered HTML, repository verification suite |
| `task-016-estimator-adapter.md` | Review Ready | `docs/prd/PRODUCT_BRIEF.md`, `docs/prd/ROADMAP.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
