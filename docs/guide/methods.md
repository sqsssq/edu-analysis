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

For paper reproduction, the continuous inputs are first standardized within
the fitted sample (population mean and standard deviation), then the paper's
strict standard-deviation rule is applied. In standardized units this is
`z > 1`. The fitted normalization statistics are stored with the model so that
reload and inference use the same transformation.

## Exact enumeration

For `n` nodes, exact calculation enumerates `2**n` states. This is the reference
method for the 19-node paper-sized system and is deterministic at a fixed
configuration. `max_exact_nodes` controls the automatic switch point.

## Monte Carlo / Gibbs sampling

For larger systems, Gibbs sampling estimates model moments without enumerating
every state. The result includes R-hat, effective sample size, and MCSE. A
sampled result should not be interpreted until those diagnostics pass the
configured quality thresholds.

The optional compatibility path uses those sampled moments with Adam:

```python
model = LearningModel(
    config,
    calculation="monte_carlo",
    learning_rate=0.001,
    mc_samples=2**20,
    mc_burn_in=1024,
)
fit = model.fit(X, y, method="adam")
```

This follows the original implementation's broad algorithmic pattern
(``sample moments -> Adam update``), but it keeps the package's `{0, 1}` state
encoding and uses the package Gibbs sampler. It is therefore a compatibility
path, not a bit-for-bit replacement for the original C++ spin/Metropolis code.

## Methods exposed by the API

| Method | Use |
| --- | --- |
| `moment_matching` | Iteratively match first- and second-order moments |
| `kl` | Exact explicit KL-gradient descent |
| `adam` | Monte Carlo moment estimates with Adam updates; use with `calculation="monte_carlo"` |
| `exact` calculation | Enumerate all states |
| `monte_carlo` calculation | Estimate moments with Gibbs sampling |
