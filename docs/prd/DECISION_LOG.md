# Decision Log

## Confirmed decisions

| Area | Decision |
| --- | --- |
| Fidelity | Faithful implementation with engineering improvements |
| Users | Researchers and ML engineers |
| Backend | PyTorch; validate whether GPU acceleration is beneficial per algorithm path |
| Data | Simple inputs plus configurable preprocessing and advanced dataset hooks later |
| Model customization | Fixed architecture first; configurable components later |
| Nodes | Binary by default; automatic or user-defined thresholds |
| Targets | Conditional prediction over a target node; one target model at a time |
| Scale | Exact enumeration for small models; automatic Monte Carlo for larger models |
| Training | Primarily interpretable moment matching; KL/autodiff as a second path |
| Sampling | Multiple chains, convergence checks, burn-in, effective sample diagnostics |
| Results | Structured result objects with optional DataFrame export |
| Interventions | Node-freezing/model-internal interventions, explicitly not causal effects |
| Missingness | Package-level strategies plus optional sample weights; no promise of full PISA survey inference |
| Testing | Synthetic recovery, exact-vs-Monte-Carlo comparison, and PISA first- through fourth-order reproduction benchmarks |
| Performance | Target approximately one minute for a paper-sized model on a normal laptop |
| Documentation | Quick start plus separate theory/reproduction guidance |
| Distribution | GitHub and PyPI with changelog; Apache-2.0 target license |
| Naming | Deferred until the implementation shape is clearer |

## Interpretation of “use other data”

The package must support both:

1. fitting a fresh model on a user's own dataset; and
2. loading a previously trained model for direct prediction and analysis.

It must not assume that another dataset has PISA's variable meanings. Variable names and metadata are required for traceability, while semantic equivalence is required before cross-dataset parameter comparisons.

