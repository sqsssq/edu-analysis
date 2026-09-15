# Commit Guide

Use this guide only after human approval.

## Rules

- Do not commit before human approval.
- Run or document verification before committing.
- Stage only files related to the approved task.
- Do not stage unrelated local files.
- Do not include raw reference files, temporary outputs, or secrets.
- Use a clear commit message.
- After approval, push the approved commit to the current remote branch unless the user explicitly says not to push.
- If the user separates commit and push approval, follow the narrower approval.

## Pre-Commit Checklist

- [ ] Human approval was given.
- [ ] Task scope is satisfied.
- [ ] PRD and task docs are aligned.
- [ ] Harness impact is documented.
- [ ] Domain-specific quality rules are satisfied or exceptions are documented.
- [ ] Verification was run or documented.
- [ ] Diff review is complete.
- [ ] Only related files are staged.

## Suggested Commit Format

Use Conventional Commits when possible:

```text
docs(framework): add harness workflow
feat(core): add first MVP loop
test(content): add fixture validation
```
