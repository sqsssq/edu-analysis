# Quality Rules

## Purpose

These rules help keep project work domain-specific, reviewable, and compatible with future harness checks.

## Required Qualities

- support the MVP loop,
- preserve domain-specific rules,
- include clear acceptance criteria,
- include verification evidence,
- avoid known failure patterns,
- keep future automation possible through structured data where useful.

## Generic Drift Check

A change is at risk of generic drift if it ignores `docs/domain/PROJECT_RULES.md` or removes project-specific constraints in favor of broad abstractions.
