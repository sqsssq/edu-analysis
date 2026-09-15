# Task 015: Add a runnable synthetic workflow notebook

## Status

Review Ready

## Objective

Provide a reproducible, user-facing notebook that demonstrates the public package workflow without bundling or requiring restricted PISA data.

## Scope

- Add `examples/synthetic_workflow.ipynb` with deterministic synthetic data.
- Demonstrate named-column preparation, fitting, analysis, moment comparison, and artifact save/load.
- Include an interpretable correlation heatmap and explicit next steps for a locally obtained PISA file.
- Keep the notebook runnable from a repository checkout and free of raw data.

## Out of scope

- PISA reproduction claims or PISA raw-data distribution.
- Country-specific mappings and survey-design inference.
- A production notebook execution service.

## Acceptance criteria

- The notebook executes top-to-bottom with the project dependency environment.
- No code cell raises an exception or depends on a local raw-data file.
- The notebook exercises the public `learning_energy_model` API through save/load.
- The task index, roadmap, README, and acceptance criteria describe the notebook accurately.

## Verification

- `jupyter nbconvert --execute --to notebook --inplace examples/synthetic_workflow.ipynb`
- `jupyter nbconvert --to html examples/synthetic_workflow.ipynb`
- Inspect the executed notebook for five successful code-cell outputs and no error outputs.
- Run the repository verification suite before commit.

## Handoff

The notebook is a synthetic companion and is intentionally separate from the PISA 2018 local-data guide. A future task can add a codebook-backed reproduction notebook once the exact variables and permitted local files are selected.
