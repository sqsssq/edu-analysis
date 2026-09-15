# Stage 3: Product UI Harness

## Purpose

Stage 3 verifies the actual user-facing experience. It checks that the product UI exposes the MVP loop, key states, feedback, recovery paths, and basic accessibility in a way users can operate.

## Trigger Conditions

Start Stage 3 when:

- product UI exists,
- the primary user flow can be opened locally,
- there are visible states or interactions worth testing,
- Stage 1 or Stage 2 checks are no longer enough to prove behavior.

## Required Artifacts

- local run command,
- UI route or entry point,
- manual or automated UI verification steps,
- responsive viewport expectations,
- accessibility basics,
- screenshots or browser automation when useful,
- `scripts/verify.sh` integration when stable.

## Completion Checklist

- [ ] The primary user flow can be launched locally.
- [ ] Start, active, feedback/result, error, and completion states are visible where relevant.
- [ ] Responsive layout is checked for project-relevant viewports.
- [ ] Basic keyboard behavior is considered.
- [ ] Basic screen-reader labels or text alternatives are considered.
- [ ] Manual verification steps are documented.
- [ ] Automated UI checks exist when the flow is stable enough.
- [ ] `scripts/verify.sh` runs stable UI checks or documents why they remain manual.

## Verification Command

Run the project app as documented, then run:

```bash
bash scripts/verify.sh
```

## Do Not Start If

Do not claim Stage 3 completion before product UI exists. If only design docs or fixtures exist, use Stage 1 or Stage 2 instead.

## Example Task

```text
Task: Add Stage 3 UI harness for the primary MVP flow
Goal: Verify visible UI states and the primary user journey.
Verification: bash scripts/verify.sh plus documented manual UI checks
```
