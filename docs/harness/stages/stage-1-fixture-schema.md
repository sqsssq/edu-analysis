# Stage 1: Fixture or Schema Harness

## Purpose

Stage 1 turns project intent into structured fixtures, schemas, or data contracts that can be validated before a full app exists.

## Trigger Conditions

Start Stage 1 when:

- the project has content, workflows, examples, scenarios, data records, prompts, rules, or domain objects that should be structured,
- future implementation should consume repeatable fixtures,
- placeholder or reviewed content needs explicit status,
- Codex needs a machine-checkable way to avoid generic drift.

## Required Artifacts

Choose artifacts that fit the project:

- a fixture or schema folder,
- documented required fields,
- at least one valid example fixture,
- at least one invalid or edge-case example when useful,
- validation script,
- `scripts/verify.sh` integration.

## Completion Checklist

- [ ] Fixture or schema format is documented.
- [ ] Required fields are explicit.
- [ ] Review status exists when placeholder, generated, expert-reviewed, or user-facing content is involved.
- [ ] Domain-specific quality rules are represented in structured fields where useful.
- [ ] A validation command exists.
- [ ] `scripts/verify.sh` calls the validation command.
- [ ] Validation fails clearly when required fields are missing.
- [ ] Validation passes on at least one representative fixture.

## Verification Command

Use the project-specific validation command, then the repository entry point:

```bash
bash scripts/verify.sh
```

## Do Not Start If

Do not start Stage 1 if the project has no structured content, data, workflow, or fixture need yet. In that case, keep Stage 1 as a planned future task.

## Example Task

```text
Task: Define Stage 1 fixture schema for Interpretable Learning Energy Model
Goal: Add structured fixture format and validation without building product UI.
Verification: bash scripts/verify.sh
```
