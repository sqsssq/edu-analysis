# Upgrade Guide

Use this guide when a generated project wants to absorb newer HarnessWeaver improvements.

## Principles

- Do not blindly overwrite project-specific PRD, domain, design, task, or decision files.
- Prefer copying reusable workflow and harness improvements first.
- Preserve local product decisions unless the project owner explicitly asks to update them.
- Run verification before and after the upgrade.

## Recommended Upgrade Flow

1. Review `CHANGELOG.md` in the source HarnessWeaver template.
2. Identify reusable files that changed, such as:
   - `scripts/verify.sh`
   - `scripts/init-project.sh`
   - generated-project `AGENTS.md` guidance
   - `docs/meta/`
   - `docs/harness/`
   - `config/init-project.example.env`
3. Identify project-specific files that need manual merge, such as:
   - root `AGENTS.md`
   - root `AGENTS.md`
   - `docs/domain/PROJECT_RULES.md`
   - `docs/design.md`
   - `docs/prd/`
   - `docs/tasks/`
4. Copy or merge the reusable changes.
5. Run:

```bash
bash scripts/verify.sh --instance
bash scripts/verify.sh --strict-instance
```

6. Record any project-specific upgrade decision in `docs/prd/09-decision-log.md`.

## Common Upgrade Cases

### Add Config-Based Initialization

Copy:

- `config/init-project.example.env`
- updated `scripts/init-project.sh`
- updated `.gitignore`

Then decide whether the existing project needs a local `init-project.env`. Do not commit local initialization files unless the project intentionally treats them as public examples.

### Add Design Standards

Copy `docs/design.md` only if the existing project does not already have a design standard file. If it does, merge the HarnessWeaver structure into the existing file instead of replacing it.

### Add Strict Readiness Guidance

Copy `docs/harness/06-strict-readiness.md` and update `scripts/verify.sh` if the project wants strict readiness checks.

## Verification Notes

- `--instance` confirms no unresolved template placeholder tokens remain.
- `--strict-instance` also rejects setup TODO markers.
- If strict verification fails because existing project notes intentionally mention setup markers, reword those notes or document why strict readiness is not yet required.
