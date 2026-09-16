# Methods

## Learning objective

The framework fits a binary pairwise maximum-entropy distribution. Given a
binary state `s`, the energy convention is:

```text
E(s) = h·s + Σ(i<j) J[i,j]s[i]s[j]
p(s) ∝ exp(-E(s))
```

Training minimizes the mismatch between empirical and model moments. The
gradient for a node field is the difference between observed and model means;
the gradient for an interaction is the difference between observed and model
pairwise moments.

## Binary normalization

Continuous input columns are converted to binary nodes using configured
thresholds. The default threshold is the median. Quantile thresholds and
explicit caller-supplied thresholds are also supported. Missing values are
handled according to `missing_strategy`.

For paper reproduction, record the exact threshold rule and apply it before
comparing parameters. The current PISA experiment uses the paper's
standard-deviation threshold rule through explicit thresholds.

## Exact enumeration

For `n` nodes, exact calculation enumerates `2**n` states. This is the reference
method for the 19-node paper-sized system and is deterministic at a fixed
configuration. `max_exact_nodes` controls the automatic switch point.

## Monte Carlo / Gibbs sampling

For larger systems, Gibbs sampling estimates model moments without enumerating
every state. The result includes R-hat, effective sample size, and MCSE. A
sampled result should not be interpreted until those diagnostics pass the
configured quality thresholds.

## Methods exposed by the API

| Method | Use |
| --- | --- |
| `moment_matching` | Iteratively match first- and second-order moments |
| `kl` | Exact explicit KL-gradient descent |
| `exact` calculation | Enumerate all states |
| `monte_carlo` calculation | Estimate moments with Gibbs sampling |
