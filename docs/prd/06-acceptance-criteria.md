# Acceptance Criteria

## Framework Acceptance Criteria

- Root `AGENTS.md` is the stable Codex entry point for maintaining `Interpretable Learning Energy Model`.
- `LICENSE` defines public reuse terms.
- `docs/prd/` describes product direction and MVP boundaries.
- `docs/meta/` describes reusable AI development workflow.
- `docs/harness/` describes harness maturity, sensors, and failure patterns.
- `docs/domain/` describes project-specific rules.
- `docs/design.md` describes project-specific design standards.
- `.harnessweaver-version` records the scaffold version used to initialize the project.
- `config/init-project.example.env` documents repeatable project configuration.
- `docs/tasks/TASK_TEMPLATE.md` enforces small scope, acceptance criteria, verification, and handoff.
- `scripts/verify.sh` runs successfully.
- `.github/workflows/ci.yml` runs strict harness verification on pushes and pull requests.

## Future Product Acceptance Criteria

- The task supports the MVP loop.
- Domain-specific quality rules are preserved.
- Harness implications are documented.
- Verification was run or unavailable checks were clearly documented.

## Current Gap Register

- `pyproject.toml` and an initial installable package now exist; dependency locking and release metadata remain.
- Initial model source modules and public API exist; Monte Carlo and plugin components remain.
- Initial `tests/` coverage exists; exact parameter recovery and full numerical acceptance thresholds remain.
- No synthetic fixtures, PISA preparation scripts, or reproduction notebooks exist yet.
- PyTorch dependency policy is encoded in `pyproject.toml`; lock files and CI installation verification remain.
