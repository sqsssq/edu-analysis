# Stage 2: Logic Harness

## Purpose

Stage 2 checks behavior that can be simulated without a full user interface. It validates rules, state transitions, decision paths, scoring, routing, transformations, or other project logic.

## Trigger Conditions

Start Stage 2 when:

- fixtures describe paths, states, decisions, or outcomes,
- the project has rules that can be tested without UI,
- Codex is likely to implement plausible but incorrect behavior,
- important failure modes can be detected through simulation.

## Required Artifacts

- structured inputs or fixtures,
- expected outputs or state transitions,
- logic checker or test command,
- failure cases,
- `scripts/verify.sh` integration.

## Completion Checklist

- [ ] Logic rules are documented.
- [ ] Representative happy paths are covered.
- [ ] Representative edge paths are covered.
- [ ] Known failure modes have checks.
- [ ] The logic harness can run without the full UI.
- [ ] Results are deterministic enough for repeatable verification.
- [ ] `scripts/verify.sh` calls the logic harness.

## Verification Command

```bash
bash scripts/verify.sh
```

## Do Not Start If

Do not start Stage 2 before there is enough structured data or rules to simulate meaningful behavior. If the only available checks are file existence checks, remain at Stage 0 or Stage 1.

## Example Task

```text
Task: Add Stage 2 logic harness for core workflow paths
Goal: Validate expected state transitions and known failure cases from fixtures.
Verification: bash scripts/verify.sh
```
