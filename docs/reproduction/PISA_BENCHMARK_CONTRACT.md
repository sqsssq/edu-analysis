# PISA reproduction benchmark contract

This contract defines what a future PISA reproduction run must record before its
results can be compared with the paper or another implementation. It is an
aggregate reporting contract; it is not a claim that the package currently
reproduces the paper.

## Required provenance

Record the following in the run metadata and in the human-readable report. The
local workflow template accepts the cycle, scope, and codebook reference as
required arguments and stores them in `DataConfig.metadata`:

- assessment cycle, file name/version, country or economy scope, and respondent level;
- source codebook and the exact variable names used for every model node;
- recodes, valid response ranges, and source-specific missing-value codes;
- whether the data are SAS or SPSS and the reader version;
- the target definition, feature order, threshold method, missing-value strategy,
  and ordinary row-weight field;
- package version, model configuration, random seed, calculation path, and sampler
  diagnostics when Monte Carlo is used.

Raw files, row-level extracts, and artifacts containing raw observations must stay
outside Git and must not be included in a benchmark report.

## Paper-aligned protocol

The bundled paper's protocol is available through
`examples/pisa_paper_reproduction.py`. It uses the following explicit settings:

- 18 WLE features plus one outcome, for 19 binary nodes;
- `f > population standard deviation` for every binary threshold;
- thresholds are computed independently within each sampled 1,200-row repeat;
- first plausible values `PV1MATH`, `PV1SCIE`, and `PV1READ`;
- 1,200 rows sampled without replacement, repeated 16 times per economy/outcome;
- exact enumeration and explicit KL-gradient training;
- aggregate comparison at moment orders 1, 2, 3, and 4.

Effective interactions use the paper's Monte Carlo node-freezing calculation,
even though training and critical-state curves use exact enumeration at 19
nodes. The report records chain count, draws, R-hat, ESS, and MCSE for the
baseline and every frozen-node conditional sample. Critical-state derivatives
use the exact covariance identities for `d<E>/dT` and `dm/dT`.

The 16 repeats are retained for validation. The runner also saves one selected
PyTorch `.pt` artifact per economy/outcome (15 total) using the rule
"converged, then minimum KL; otherwise minimum moment error". These artifacts
contain model parameters and aggregate fit metadata, not raw PISA rows.

This mode is separate from the package default median threshold and ordinary
row-weight behavior. It still requires a locally obtained, codebook-reviewed
PISA file and does not implement official complex-survey inference.

The explicit `PISAMapping` contract can be saved as a small JSON file containing
only selected column names, missing codes, and provenance metadata. Review that
file against the matching OECD codebook before using it, and keep it separate
from the raw data file.

## Required numerical outputs

The report must include aggregate values for the same ordered node list:

1. first-order means for every node;
2. second-order joint moments and the derived binary Pearson correlations;
3. every valid third-order joint moment;
4. every valid fourth-order joint moment;
5. fitted `h` and symmetric `J` parameters, with the energy convention
   `E(s) = h·s + sum(i<j) J[i,j]s[i]s[j]` stated explicitly.

Use `compare_moment_orders` with `FitResult.observed_higher_order_moments` and
`FitResult.model_higher_order_moments` for observed-versus-modeled comparisons.
Declare a
non-negative tolerance for each reported order and include maximum and mean
absolute error plus the pass/fail result. Missing orders or mismatched node keys
must fail the comparison rather than be silently ignored.

## Computation and interpretation boundary

- Exact enumeration is preferred when the configured node threshold allows it.
- Monte Carlo results must include chain count, draws, R-hat, and effective sample
  size diagnostics and must be described as approximate.
- `sample_weight` is ordinary row weighting in the current release. PISA replicate
  weights, plausible-value aggregation, and complex-survey variance estimation are
  not implemented.
- A node-freezing result is a model-internal intervention, not a causal effect.
- Results must be described as estimates on the prepared sample, not official PISA
  estimates, until the missing survey methodology is implemented.

## Minimal report shape

```python
report = {
    "provenance": {"cycle": "PISA 2018", "scope": "..."},
    "nodes": ["FEATURE_A", "FEATURE_B", "TARGET"],
    "preprocessing": {"threshold_method": "median", "missing_strategy": "median"},
    "calculation": {"path": "exact", "seed": 7},
    "moment_comparison": comparison.to_dict(),
    "parameters": {"h": analysis.h.tolist(), "J": analysis.J.tolist()},
}
```

The provenance and preprocessing sections are mandatory even when only aggregate
model parameters are shared, because numerical agreement is not interpretable
without aligned variable definitions.
