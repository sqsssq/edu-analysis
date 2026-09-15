# Task 034: Align release metadata and changelog

## Status

Review Ready

## Source PRD

- `docs/prd/DECISION_LOG.md`
- `docs/prd/06-acceptance-criteria.md`

## Goal

Make the installable package's declared license and release history agree with
the project's documented distribution decision.

## Scope

- Align `LICENSE` with the Apache-2.0 declaration in `pyproject.toml`.
- Summarize implemented package capabilities in `CHANGELOG.md`.
- Keep new work under the `Unreleased` heading.

## Acceptance Criteria

- The repository contains the Apache-2.0 license text and copyright notice.
- `pyproject.toml`, decision docs, and `LICENSE` agree.
- The changelog identifies the current unreleased implementation scope.
- Standard package verification passes.

## Done When

- Release metadata is aligned, verified, committed, and pushed.
