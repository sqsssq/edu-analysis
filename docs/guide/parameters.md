# Parameters

## Data configuration

| Parameter | Meaning | Default |
| --- | --- | --- |
| `feature_names` | Ordered names of input nodes | `()` |
| `target_name` | Name of the target node | `"target"` |
| `threshold_method` | `"median"` or `"quantile"` | `"median"` |
| `quantile` | Quantile used with the quantile method | `0.5` |
| `thresholds` | Explicit feature thresholds | `None` |
| `target_threshold` | Explicit target threshold | `None` |
| `missing_strategy` | `error`, `median`, `mean`, or `zero` | `error` |
| `sample_weight_name` | Ordinary row-weight column | `None` |
| `metadata` | Provenance and caller-defined context | `{}` |

## Training configuration

| Parameter | Meaning | Default |
| --- | --- | --- |
| `learning_rate` | Moment update step size | `0.05` |
| `max_epochs` | Maximum training iterations | `2000` |
| `min_epochs` | Minimum iterations before convergence | `25` |
| `tolerance` | Maximum accepted moment error | `1e-3` |
| `calculation` | `auto`, `exact`, or `monte_carlo` | `auto` |
| `max_exact_nodes` | Largest exact model in automatic mode | `20` |
| `seed` | Reproducibility seed | `0` |

## Monte Carlo quality configuration

| Parameter | Meaning | Default |
| --- | --- | --- |
| `mc_samples` | Samples per chain | `2000` |
| `mc_burn_in` | Burn-in draws | `500` |
| `mc_thinning` | Sampling interval | `1` |
| `mc_chains` | Number of chains | `4` |
| `mc_max_rhat` | Maximum accepted R-hat | `1.1` |
| `mc_min_effective_sample_size` | Minimum accepted ESS | `100` |
| `mc_max_mcse` | Maximum accepted MCSE | `0.05` |

## Interpretation of `h` and `J`

`h[i]` is the fitted field for node `i`. `J[i, j]` is the fitted pairwise
interaction under the package's energy sign convention. These values describe
the fitted distribution; they are not automatically causal effects.
