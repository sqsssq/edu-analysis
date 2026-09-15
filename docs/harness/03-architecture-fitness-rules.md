# Architecture Fitness Rules

## Current Rule

Keep the repository documentation-first until a setup task explicitly initializes product code.

## Fitness Rules

- Keep the MVP loop narrow and explicit.
- Keep domain-specific rules in `docs/domain/PROJECT_RULES.md`.
- Prefer structured fixtures or schemas when future validation would benefit.
- Keep verification commands centralized through `scripts/verify.sh`.
- Do not add broad infrastructure without approved PRD and task coverage.
- Avoid large abstractions before the first MVP loop is proven.
- Keep files small enough for review.
