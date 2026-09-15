# Harness Overview

## Purpose

The harness is a planning and verification layer for AI-assisted development. It should help agents build the right thing before implementation and detect problems after changes.

## Feedforward Guides

- `AGENTS.md`
- `CHANGELOG.md`
- `LICENSE`
- `docs/prd/`
- `docs/meta/`
- `docs/domain/PROJECT_RULES.md`
- `docs/design.md`
- `docs/harness/03-architecture-fitness-rules.md`
- `docs/harness/04-quality-rules.md`
- `docs/harness/05-stage-checklists.md`
- `docs/harness/stages/`
- `config/init-project.example.env`
- `docs/meta/UPGRADE_GUIDE.md`

## Feedback Sensors

Initial sensor categories:

- file path consistency,
- absence of template placeholder leakage when customized,
- strict instance readiness before task execution,
- no product code during framework-only work,
- domain-specific quality rule coverage,
- MVP loop completeness,
- generic app drift,
- architecture scope creep.

## Harness Maturity Stages

- Stage 0: Framework Harness
- Stage 1: Fixture or Schema Harness
- Stage 2: Logic Harness
- Stage 3: Product UI Harness
- Stage 4: Continuous Harness

Detailed gates live in `docs/harness/stages/`. Each stage document defines purpose, trigger conditions, required artifacts, completion checklist, verification command, when not to start, and an example task.
