# Diff Review Guide

Use this guide after implementation and verification, before human handoff.

## Review Questions

1. Does the diff implement the requested task?
2. Does it match the relevant PRD files?
3. Does it preserve MVP scope?
4. Does it avoid product code or infrastructure outside the task?
5. Does it preserve domain-specific quality rules?
6. Were verification steps run or documented?
7. Are file paths internally consistent?

## Severity

- Critical: blocks approval because the task is wrong, unsafe, or unverifiable.
- Major: needs changes before approval.
- Minor: can be fixed quickly or tracked as follow-up.
- Note: useful context that does not block approval.
