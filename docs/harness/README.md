# Project Harness

This directory defines the local HarnessWeaver contract for this repository. It is a project workflow scaffold, not a Python runtime dependency.

## Purpose

HarnessWeaver keeps project intent, implementation stages, and verification connected. The first stage is documentation-only: no model code should be started until the package contract is reviewed.

## Required workflow

1. Read `docs/prd/PRODUCT_BRIEF.md` and `docs/domain/PROJECT_RULES.md`.
2. Restate the task scope and out-of-scope items in the task record.
3. Implement the smallest complete stage.
4. Run `bash scripts/verify.sh --instance`.
5. Before a release-ready task, run `bash scripts/verify.sh --strict-instance`.

## Current stage

**Stage 0: project brief and rules.** The required artifact is a reviewable design contract. Stages for schema/data fixtures, model logic, and package release are planned in `docs/prd/ROADMAP.md`.

## Verification modes

- `--instance` checks that the customized project scaffold is internally consistent.
- `--strict-instance` additionally fails on unresolved placeholders and incomplete readiness markers.
