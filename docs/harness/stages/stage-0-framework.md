# Stage 0: Framework Harness

## Purpose

Stage 0 establishes the project operating system before product code exists. It gives Codex and humans a shared structure for PRD-first planning, task execution, verification, review, and commit discipline.

## Trigger Conditions

Start Stage 0 when:

- a new project is being initialized,
- an existing project lacks a clear AI-assisted development workflow,
- Codex needs stable project guardrails before implementation,
- the team wants a reusable verification entry point before product code is added.

## Required Artifacts

- `AGENTS.md`
- `LICENSE`
- `README.md`
- `docs/prd/`
- `docs/tasks/README.md`
- `docs/tasks/TASK_TEMPLATE.md`
- `docs/meta/`
- `docs/harness/`
- `docs/domain/PROJECT_RULES.md`
- `docs/design.md`
- `config/init-project.example.env`
- `scripts/verify.sh`
- `scripts/init-project.sh`

## Completion Checklist

- [ ] Root `AGENTS.md` defines project-specific agent behavior.
- [ ] `LICENSE` defines public reuse terms.
- [ ] PRD files describe product direction and MVP boundaries.
- [ ] Task workflow defines status lifecycle and task template.
- [ ] Meta docs describe PRD generation, task breakdown, execution, change requests, verification, diff review, handoff, and commit.
- [ ] Harness docs define failure patterns, architecture rules, quality rules, stage checklists, and stage gates.
- [ ] Domain rules define project-specific guardrails.
- [ ] Design standards define how future UI or experience work should support the MVP loop.
- [ ] Initialization config example supports a repeatable setup path.
- [ ] `scripts/verify.sh` runs successfully.
- [ ] `bash scripts/verify.sh --instance` passes after customization.
- [ ] `bash scripts/verify.sh --strict-instance` passes before task execution.
- [ ] Markdown path references resolve to existing files or directories.
- [ ] No source-project-specific assumptions remain after customization.

## Verification Command

```bash
bash scripts/verify.sh
```

## Do Not Start If

Stage 0 should almost always be safe to start. If the project already has strong workflow docs, use this stage as an audit rather than replacing everything.

## Example Task

```text
Task: Initialize Stage 0 framework harness for Interpretable Learning Energy Model
Goal: Add PRD, task, meta, harness, domain, and verification scaffold without product code.
Verification: bash scripts/verify.sh
```
