---
name: harness-weaver
description: Initialize, validate, audit, or upgrade HarnessWeaver projects. Use for generating or rehearsing a HarnessWeaver project, preparing init-project.env, running init-project.sh, checking --template, --instance, or --strict-instance, and Chinese requests to 创建、初始化、复用、演练、验证、审计或升级 HarnessWeaver. Do not use for generic project scaffolding.
---

# HarnessWeaver

## Overview

Use this skill to initialize, validate, audit, or upgrade a project from the HarnessWeaver template. Keep the workflow focused on scaffold and harness operations; do not generate product code, create PRDs beyond the initialization config, or commit the target project unless the user explicitly asks.

For design rationale and scope boundaries, see `references/skill-brief.md` when planning or updating this skill.

## Required Inputs

Determine these before initializing:

- Source HarnessWeaver template path or repository.
- Target project path.
- Project name.
- Domain.
- Primary user.
- MVP focus.

If any required input is missing and cannot be inferred safely, ask a concise question before modifying files.

## Workflow

1. Locate the HarnessWeaver source template.
   - If the current working directory is a HarnessWeaver repo, use the current repo root.
   - If the user gives a path or repo URL, use that.
   - Otherwise ask for the source template location.
   - Do not assume or mention a hard-coded local path such as a specific user's `Projects/harness-weaver` directory unless the user provided it or the current workspace is exactly that repo.
2. Confirm the target path does not already contain unrelated work. If it exists and is non-empty, ask before overwriting or merging.
3. Create `init-project.env` in the HarnessWeaver source repository from `config/init-project.example.env`.
4. Fill or help the user fill the `HW_*` values. Keep values project-specific. The file is declarative data and must contain only supported `HW_*` assignments.
5. Generate the target project through `scripts/init-project.sh --target`. Do not copy the source repository manually; the generator excludes repository-only docs, branding, skills, and template source.
6. Run:

```bash
bash scripts/verify.sh --template
bash scripts/init-project.sh --target "$TARGET_PATH" --config init-project.env --dry-run
bash scripts/init-project.sh --target "$TARGET_PATH" --config init-project.env
cd "$TARGET_PATH"
bash scripts/verify.sh --instance
bash scripts/verify.sh --strict-instance
```

7. If strict verification fails, use the output as an edit checklist. Update only project-specific files needed for readiness.
8. Provide a handoff with commands run, pass/fail results, changed files, and remaining manual decisions.

## Guardrails

- Do not create product application code.
- Do not create a real task file in `docs/tasks/` during initialization.
- Do not commit or push the target project unless the user explicitly asks.
- Do not treat the example config values as product truth.
- Do not source or execute initialization config files.
- Do not hide failed verification. Report failed commands and the next concrete fix.

## Handoff Shape

Include:

- Target project path.
- Source template path or commit when available.
- Initialization method used, such as `--config`.
- Verification results for `--template`, `--instance`, and `--strict-instance`.
- Any files the user still needs to review, especially `docs/domain/PROJECT_RULES.md`, `docs/design.md`, and `docs/prd/`.
