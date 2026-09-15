# Package, Notebook, and Report States

The first release is primarily a Python package, so these states apply to API results, notebooks, and any future UI.

## Required States

- start state,
- active work state,
- success state,
- empty state,
- loading state,
- error state,
- invalid action state,
- completion state.
- converged-with-warning state;
- sampling-not-converged state;
- unsupported-interpretation state.

## Placeholder or Review State

If the product presents placeholder or unreviewed content, the UI or fixture should preserve that status.

## State Semantics

- `start`: configuration accepted, no fit performed.
- `active`: training or sampling is running.
- `success`: fit completed and diagnostics are available.
- `converged-with-warning`: fit completed, but assumptions or diagnostics need review.
- `sampling-not-converged`: results must not be presented as reliable without further sampling.
- `unsupported-interpretation`: causal or individual-decision requests are rejected or clearly reframed.
