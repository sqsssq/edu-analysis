# Visualizations

Install the optional plotting dependency:

```bash
pip install 'learnenergy[visualization]'
```

The helpers return `(figure, axes)` pairs and accept an existing Matplotlib axes
object for composing reports.

```python
from learnenergy.visualization import plot_correlations, plot_interactions, plot_training_history

analysis = model.analyze()
plot_interactions(analysis, annotate=True)
plot_correlations(analysis)
plot_training_history(model.fit_result)
```

`plot_interactions` shows signed `J` values. `plot_correlations` shows model-
implied binary Pearson correlations. `plot_training_history` shows the recorded
optimization objective by epoch.

The current helpers cover core diagnostics. The paper's complete multi-country
figure suite—higher-order comparison panels, `J` distributions, country panels,
and threshold-sensitivity plots—remains a separate reproduction task.
