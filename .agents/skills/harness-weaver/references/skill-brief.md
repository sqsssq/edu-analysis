# HarnessWeaver Skill Brief

## Goal

Help Codex initialize, validate, audit, or upgrade a clean HarnessWeaver-based project from the template repo, using the config-based initialization path and strict verification gates.

## Target User

Project creators who want a PRD-first, task-based, harness-oriented starting point for a new project.

## Inputs

- Source HarnessWeaver template path or repository.
- Target project path.
- Project identity values for `init-project.env`.

## Outputs

- A clean generated project scaffold without HarnessWeaver repository-only files.
- A project-specific `init-project.env` kept local by `.gitignore`.
- Successful `--instance` and, when enough project-specific content is provided, `--strict-instance` verification.
- A concise handoff.

## Non-Goals

- Product code generation.
- Full PRD authoring.
- Automatic commits.
- Updating the source HarnessWeaver template.

## Compatibility

Designed for HarnessWeaver template version `0.2.x` style projects with:

- `config/init-project.example.env`
- `scripts/init-project.sh --config`
- `scripts/init-project.sh --target`
- `scripts/init-project.sh --dry-run`
- `scripts/verify.sh --instance`
- `scripts/verify.sh --strict-instance`
