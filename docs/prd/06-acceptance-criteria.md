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
- Initial model source modules, public API, and Gibbs sampler exist; sampler calibration and plugin components remain.
- The public model can draw joint binary states with exact or Gibbs sampling according to model size.
- Initial `tests/` coverage exists; exact parameter recovery and full numerical acceptance thresholds remain.
- A PISA local-data guide, generic tabular preparation helper, and runnable synthetic workflow exist; PISA-specific mappings and reproduction notebooks remain.
- PyTorch dependency policy is encoded in `pyproject.toml`; lock files and CI installation verification remain.
