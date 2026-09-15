# Agent Failure Patterns

## Generic App Drift

Failure: the agent builds a generic version of the app instead of the project-specific MVP loop.

Sensor: check task scope against `docs/domain/PROJECT_RULES.md`.

## Placeholder Becomes Product Truth

Failure: placeholder examples become treated as final product content.

Sensor: review status fields and handoff notes.

## Infrastructure Creep

Failure: the agent adds broad backend, auth, deployment, AI API, or platform architecture before an approved task needs it.

Sensor: inspect changed files and dependency changes.

## Missing Harness Impact

Failure: the agent changes content, data, or user flow without updating harness assumptions.

Sensor: task and handoff must include harness impact.

## Path Drift

Failure: docs refer to files that do not exist or old project paths.

Sensor: path consistency checks in verification.
