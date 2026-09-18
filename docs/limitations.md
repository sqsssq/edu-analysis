# Limitations and research status

This is a research-oriented implementation of a binary pairwise maximum-entropy
model. It is not a causal inference system and does not make individual
educational recommendations.

The current binary paper-reproduction path does not implement mixed continuous
nodes, PISA replicate-weight variance estimation, plausible-value aggregation,
complex-survey inference, or official PISA estimates. An experimental
Gaussian/quadratic continuous model is available separately; it does not yet
support nonlinear, heavy-tailed, or mixed-node energy models.

The paper's full figure and numerical reproduction remains an active benchmark.
Comparisons should record the source file, codebook mapping, complete-case rule,
threshold rule, sample size, seeds, calculation path, and convergence diagnostics.
