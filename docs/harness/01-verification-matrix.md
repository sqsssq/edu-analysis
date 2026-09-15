# Verification Matrix

## Framework Documentation

| Requirement | Evidence |
| --- | --- |
| Required files exist | `bash scripts/verify.sh` |
| Paths are internally consistent | Markdown path reference check in `scripts/verify.sh` |
| Project agent entry point exists | root `AGENTS.md` |
| Open-source license exists | `LICENSE` is required by `bash scripts/verify.sh` |
| No source-project-specific terms remain | source-term search |
| Template placeholders are resolved | `--instance` rejects unresolved placeholders |
| Implementation readiness can be checked | `--strict-instance` rejects placeholders and unresolved TODO markers |
| No product code added during framework-only work | inspect new files and top-level directories |
| Verify script is executable | `test -x scripts/verify.sh` |
| Harness stage can be assessed | `docs/harness/05-stage-checklists.md` |
| Design standards exist | `docs/design.md` is required by `bash scripts/verify.sh` |
| Initialization provenance is recorded | `.harnessweaver-version` |

## Future Fixture or Content Checks

| Requirement | Future Sensor |
| --- | --- |
| Core entity has required fields | schema check |
| Review status is present when needed | schema check |
| Placeholder content is not marked final | quality check |
| Domain-specific quality rules are represented | domain check |
