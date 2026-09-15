# Harness Stage Checklists

Detailed stage gates:

- `docs/harness/stages/stage-0-framework.md`
- `docs/harness/stages/stage-1-fixture-schema.md`
- `docs/harness/stages/stage-2-logic.md`
- `docs/harness/stages/stage-3-product-ui.md`
- `docs/harness/stages/stage-4-continuous.md`

## Stage 0: Framework Harness

Ready when:

- [ ] `AGENTS.md` exists and points to real docs.
- [ ] `docs/prd/` defines product direction and MVP boundaries.
- [ ] `docs/meta/` defines PRD-first, task-based workflow.
- [ ] `docs/tasks/TASK_TEMPLATE.md` enforces scope, acceptance criteria, verification, and handoff.
- [ ] `docs/domain/PROJECT_RULES.md` defines project-specific guardrails.
- [ ] `docs/design.md` defines project-specific design standards.
- [ ] `docs/harness/` defines failure patterns, architecture rules, and quality rules.
- [ ] `scripts/verify.sh` exists and runs successfully.

## Stage 1: Fixture or Schema Harness

Ready when:

- [ ] A structured fixture or schema format exists.
- [ ] Required fields are documented.
- [ ] Review status exists when needed.
- [ ] A validation command exists.
- [ ] `scripts/verify.sh` calls the validation command.

## Stage 2: Logic Harness

Ready when:

- [ ] Fixtures describe possible paths or state transitions.
- [ ] Expected outcomes are represented in structured data.
- [ ] Domain-specific failure modes can be detected.
- [ ] Simulated logic checks can run without a full UI.

## Stage 3: Product UI Harness

Ready when product UI exists and the primary user flow can be manually or automatically exercised.

## Stage 4: Continuous Harness

Ready when project tooling and CI run the same verification entry point.
