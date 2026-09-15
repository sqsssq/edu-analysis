# Verification Guide

Use this guide before handoff for documentation, setup, and product tasks.

## Preferred Command

Run:

```bash
bash scripts/verify.sh
```

The script should only run checks that exist.

## Verification Levels

Use the levels that apply:

1. Static repository checks.
2. Documentation path checks.
3. Domain-specific checks.
4. Product build checks after product code exists.
5. Automated tests after tests exist.
6. Harness checks for fixtures, logic, or user flows.

## Missing Commands

If a command is unavailable because the project is not initialized, report it as unavailable, not failed.

## Failed Verification

Do not claim verification passed unless the relevant checks actually ran or were manually checked.
