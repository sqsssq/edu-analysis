# Task Execution Guide

Use this guide when implementing one approved task from `docs/tasks/`.

## Required Inputs

Before editing files, read:

- the selected task file,
- all PRD files referenced by the task,
- `docs/domain/PROJECT_RULES.md`,
- relevant harness files under `docs/harness/`,
- `AGENTS.md`.

## Execution Brief

Before changing files, summarize:

- task file,
- source PRD files,
- scope,
- out of scope,
- files likely to change,
- domain rule impact,
- harness impact,
- blockers or open questions.

## Scope Control

Do not silently expand a task.

Do not:

- add broad infrastructure unless explicitly scoped,
- add dependencies without clear need,
- implement unrelated UI or product code,
- bypass domain-specific quality rules,
- skip verification.

## Handoff

After implementation:

1. Run verification.
2. Review the diff.
3. Update the task file if appropriate.
4. Provide human handoff.
5. Stop before commit unless the user approves committing.
