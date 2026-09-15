# Stage 4: Continuous Harness

## Purpose

Stage 4 makes the harness repeatable across handoffs, commits, pull requests, and releases. It aligns local verification with CI or an equivalent automated check.

## Trigger Conditions

Start Stage 4 when:

- project tooling exists,
- lint, typecheck, tests, build, fixture validation, or logic checks are stable enough to run repeatedly,
- the project has collaborators or automated review needs,
- manual verification alone is becoming too fragile.

## Required Artifacts

- stable local verification entry point,
- CI or equivalent automation,
- documented required checks,
- clear failure reporting,
- project-specific exceptions or skipped checks documented.

## Completion Checklist

- [ ] `scripts/verify.sh` runs available lint, typecheck, test, build, fixture validation, and logic checks.
- [ ] CI or equivalent automation calls the same verification entry point.
- [ ] Required checks are documented.
- [ ] Missing optional checks are reported as unavailable, not silently ignored.
- [ ] Failure output is clear enough for Codex and humans to act on.
- [ ] Handoff summaries report verification evidence.
- [ ] Commit or merge process expects verification before approval.

## Verification Command

```bash
bash scripts/verify.sh
```

CI should call the same command when possible.

## Do Not Start If

Do not overbuild CI before the project has stable commands. Stage 4 should consolidate real checks, not invent noisy automation.

## Example Task

```text
Task: Add Stage 4 continuous harness
Goal: Run local verification in CI and document required checks.
Verification: CI passes and bash scripts/verify.sh passes locally
```
