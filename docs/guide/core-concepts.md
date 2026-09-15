# Core concepts

## Pairwise energy model

Each observation is represented as a binary state vector `s`:

```text
E(s) = h·s + Σ(i<j) J[i,j]s[i]s[j]
p(s) ∝ exp(-E(s))
```

The package stores `J` symmetrically with a zero diagonal. Always state this
sign convention when interpreting parameters.

## Binary preprocessing

`DataConfig` records names, threshold policy, missing-value strategy, optional
ordinary row weights, and metadata. The built-in threshold policies are median
and quantile. PISA nonresponse codes must be recoded using the matching codebook.

## Exact versus Monte Carlo

Exact enumeration is the reference path for small models. The Monte Carlo path
uses Gibbs sampling and reports R-hat, effective sample size, and MCSE.

## Interpretation boundary

`analyze()` reports association and model-internal interventions. Freezing a node
is not a causal intervention, and the package does not produce individual
educational recommendations.
