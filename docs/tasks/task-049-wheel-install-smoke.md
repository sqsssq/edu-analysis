# Task 049: Verify the built wheel in CI

Status: Review Ready

## Goal

Prove in CI that the built distribution can be imported independently of the
repository checkout, so downstream users are not relying on editable-install
behavior.

## Delivered

- Added a no-dependency wheel installation into a temporary target directory.
- Added an import smoke test from outside the checkout directory.
- Kept the existing package, CLI, test, lint, type, and HarnessWeaver checks.

## Verification

The GitHub Actions Python matrix runs the wheel-install smoke test after the
wheel build; local package tests and strict HarnessWeaver verification also
pass.
