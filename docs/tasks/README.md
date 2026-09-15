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
| `task-017-pisa-benchmark-contract.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/reproduction/PISA_2018_DATA_GUIDE.md` | `bash scripts/verify.sh --strict-instance` and markdown-link validation |
| `task-018-tabular-quality-report.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/prd/04-content-model.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-019-config-validation.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/prd/04-content-model.md` | `pytest`, `ruff`, mypy, and `bash scripts/verify.sh --strict-instance` |
| `task-020-multi-domain-manager.md` | Review Ready | `docs/prd/PRODUCT_BRIEF.md`, `docs/prd/ROADMAP.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-021-cli-workflow.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/prd/PRODUCT_BRIEF.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-022-named-inference-columns.md` | Review Ready | `docs/prd/04-content-model.md`, `docs/prd/ROADMAP.md` | `pytest`, `ruff`, mypy, and `bash scripts/verify.sh --strict-instance` |
| `task-023-pisa-local-workflow.md` | Review Ready | `docs/reproduction/PISA_2018_DATA_GUIDE.md`, `docs/prd/ROADMAP.md` | `ruff`, mypy, and `bash scripts/verify.sh --strict-instance` |
| `task-024-weight-provenance.md` | Review Ready | `docs/prd/04-content-model.md`, `docs/prd/ROADMAP.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-025-pisa-provenance.md` | Review Ready | `docs/reproduction/PISA_BENCHMARK_CONTRACT.md`, `docs/prd/ROADMAP.md` | local synthetic workflow smoke test, `ruff`, mypy, and `bash scripts/verify.sh --strict-instance` |
| `task-026-monte-carlo-error-estimates.md` | Review Ready | `docs/tasks/task-010-sampler-diagnostics.md`, `docs/prd/ROADMAP.md` | `pytest`, `ruff`, mypy, and `bash scripts/verify.sh --strict-instance` |
| `task-027-fit-higher-order-moments.md` | Review Ready | `docs/prd/04-content-model.md`, `docs/reproduction/PISA_BENCHMARK_CONTRACT.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-028-missing-value-strategies.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/prd/06-acceptance-criteria.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-029-calculation-path-control.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/prd/09-decision-log.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-030-pisa-mapping-contract.md` | Review Ready | `docs/reproduction/PISA_BENCHMARK_CONTRACT.md`, `docs/prd/ROADMAP.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-031-monte-carlo-quality-thresholds.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/prd/06-acceptance-criteria.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-032-component-protocols.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/prd/04-content-model.md` | `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-033-pisa-2022-data-guide.md` | Review Ready | `docs/reproduction/PISA_2022_DATA_GUIDE.md`, `docs/prd/ROADMAP.md` | markdown-link validation and `bash scripts/verify.sh --strict-instance` |
| `task-034-release-metadata-alignment.md` | Review Ready | `docs/prd/DECISION_LOG.md`, `docs/prd/06-acceptance-criteria.md` | license consistency check, `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-035-pisa-workflow-mapping-cli.md` | Review Ready | `docs/reproduction/PISA_2022_DATA_GUIDE.md`, `docs/prd/ROADMAP.md` | synthetic local workflow smoke test, `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-036-strict-ci-dependencies.md` | Review Ready | `docs/prd/06-acceptance-criteria.md`, `docs/prd/ROADMAP.md` | workflow inspection, `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-037-parameter-recovery-benchmark.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/prd/06-acceptance-criteria.md` | benchmark test, `pytest`, `ruff`, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-038-pisa-reproduction-notebook.md` | Review Ready | `docs/prd/ROADMAP.md`, `docs/prd/06-acceptance-criteria.md` | executed synthetic notebook, rendered HTML inspection, and `bash scripts/verify.sh --strict-instance` |
| `task-039-pisa-extra-ci-smoke.md` | Review Ready | `docs/prd/06-acceptance-criteria.md`, `docs/prd/ROADMAP.md` | workflow inspection, optional dependency import smoke test, and `bash scripts/verify.sh --strict-instance` |
| `task-040-pypi-metadata.md` | Review Ready | `docs/prd/06-acceptance-criteria.md`, `docs/prd/DECISION_LOG.md` | TOML parse, wheel metadata inspection, and `bash scripts/verify.sh --strict-instance` |
| `task-041-typed-package-marker.md` | Review Ready | `docs/prd/04-content-model.md`, `docs/prd/06-acceptance-criteria.md` | wheel inspection, `pytest`, ruff, mypy, and `bash scripts/verify.sh --strict-instance` |
| `task-042-public-api-reference.md` | Review Ready | `docs/API.md`, `docs/prd/01-mvp-scope.md` | markdown-link validation, `pytest`, and `bash scripts/verify.sh --strict-instance` |
| `task-043-legacy-artifact-compatibility.md` | Review Ready | `docs/prd/04-content-model.md`, `docs/prd/06-acceptance-criteria.md` | legacy-load regression test, `pytest`, ruff, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-044-core-infinity-validation.md` | Review Ready | `docs/prd/06-acceptance-criteria.md`, `docs/prd/04-content-model.md` | regression test, `pytest`, ruff, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-045-fit-table-convenience-api.md` | Review Ready | `docs/API.md`, `docs/prd/01-mvp-scope.md` | `pytest`, ruff, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-046-fit-table-quality-report.md` | Review Ready | `docs/API.md`, `docs/prd/04-content-model.md` | `pytest`, ruff, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-047-chinese-user-guide.md` | Review Ready | `README.zh-CN.md`, `docs/API.md` | `pytest`, ruff, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
| `task-048-estimator-fit-table.md` | Review Ready | `docs/API.md`, `docs/prd/ROADMAP.md` | `pytest`, ruff, mypy, wheel build, and `bash scripts/verify.sh --strict-instance` |
