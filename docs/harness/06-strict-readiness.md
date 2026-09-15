# Strict Instance Readiness

## Purpose

Strict instance readiness means the generated project has enough project-specific context to start task execution without unresolved placeholders or setup TODO markers.

Run:

```bash
bash scripts/verify.sh --strict-instance
```

## Fast Path

1. Copy `config/init-project.example.env` to `init-project.env`.
2. Fill every `HW_*` value in `init-project.env` with project-specific content.
3. Preview the initialization:

```bash
bash scripts/init-project.sh --config init-project.env --dry-run
```

4. Initialize the project:

```bash
bash scripts/init-project.sh --config init-project.env
```

5. Run:

```bash
bash scripts/verify.sh --instance
bash scripts/verify.sh --strict-instance
```

## Recommended Order

After running `scripts/init-project.sh`, complete these files first:

1. `AGENTS.md`
2. `docs/domain/PROJECT_RULES.md`
3. `docs/design.md`
4. `docs/prd/00-product-brief.md`
5. `docs/prd/01-mvp-scope.md`
6. `docs/prd/02-user-flows.md`
7. `docs/prd/03-feature-design.md`
8. `docs/prd/08-open-questions.md`

## Ready When

- Project identity, primary user, MVP focus, and non-goals are concrete.
- Domain rules describe what the project must and must not become.
- Design standards describe how future UI should support the MVP loop.
- Product brief, scope, flows, and feature principles are project-specific.
- Open questions are real questions, not placeholder prompts.
- `bash scripts/verify.sh --instance` passes.
- `bash scripts/verify.sh --strict-instance` passes.

## Common Friction

- `--instance` can pass while strict readiness still fails because setup TODO markers remain.
- Strict verification scans documentation too, so notes should avoid writing the exact setup marker syntax unless the note is meant to fail the gate.
- Long strict output should be treated as a checklist for the next editing pass.
