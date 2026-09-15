# Task 050: Verify wheel training in CI

Status: Review Ready

## Goal

Exercise the installed distribution's public training and prediction path in
CI, not only its importability.

## Delivered

- Extended the temporary wheel installation smoke test with a four-row
  synthetic `LearningModel.fit_table()` fit.
- Verified prediction output shape through the installed package path.
- Kept the smoke data synthetic and ephemeral.

## Verification

GitHub Actions runs the wheel training smoke after building the wheel; local
tests, lint, typing, package build, and strict HarnessWeaver verification also
pass.
