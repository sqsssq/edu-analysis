# Task 008: Add higher-order moment outputs

## Status

Review Ready

## Source PRD

- `docs/prd/00-product-brief.md`
- `docs/prd/04-content-model.md`
- `docs/prd/ROADMAP.md`

## Goal

Expose third- and fourth-order joint moments so paper-reproduction checks can compare more than pairwise associations.

## User Value

Researchers can inspect the higher-order structure used by the planned PISA reproduction benchmarks.

## Scope

- `AnalysisResult.higher_order_moments` for orders three and four.
- Exact computation for small models and sampled estimates for larger models.
- JSON/dict export coverage and synthetic tests.

## Out of Scope

- Claiming PISA reproduction without the official data and aligned preparation.
- Full survey variance estimation.
- Arbitrary orders beyond four.

## Domain Requirement

Label higher-order outputs as model moments and preserve exact-versus-sampled diagnostics.

## Harness Impact

Adds a feedback sensor for the high-order reproduction contract.

## Acceptance Criteria

- Exact analysis returns all valid third- and fourth-order node combinations.
- Large-model analysis returns sampled higher-order estimates and diagnostics.
- Standard package verification passes.

## Verification Method

```bash
python -m pytest -q
python -m ruff check learning_energy_model tests examples
python -m mypy learning_energy_model
python -m build --wheel --no-isolation
bash scripts/verify.sh --strict-instance
```

## Done When

- Higher-order moments are exposed, tested, and documented.
- The verified change is committed and pushed.
