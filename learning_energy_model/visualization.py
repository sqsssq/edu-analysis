"""Optional Matplotlib visualizations for fitted model results.

The plotting helpers import Matplotlib lazily, so the core package does not
gain a plotting dependency. Each helper returns the ``(figure, axes)`` pair
and accepts an existing axes object for composition in notebooks or reports.
"""

from collections.abc import Sequence
from typing import Any

import numpy as np

from .results import AnalysisResult, FitResult


def _pyplot() -> Any:
    try:
        import matplotlib.pyplot as plt  # type: ignore[import-not-found]
    except ImportError as exc:
        raise ImportError(
            "visualization requires Matplotlib; install with "
            "`pip install interpretable-learning-energy-model[visualization]`"
        ) from exc
    return plt


def _labels(analysis: AnalysisResult, labels: Sequence[str] | None) -> list[str]:
    values = list(labels) if labels is not None else [
        *analysis.diagnostics.get("feature_names", []),
        analysis.diagnostics.get("target_name", "target"),
    ]
    if len(values) != len(analysis.h):
        return [f"node_{index}" for index in range(len(analysis.h))]
    return values


def _finish(fig: Any, ax: Any, title: str | None) -> tuple[Any, Any]:
    if title:
        ax.set_title(title)
    fig.tight_layout()
    return fig, ax


def plot_interactions(
    analysis: AnalysisResult,
    *,
    labels: Sequence[str] | None = None,
    ax: Any | None = None,
    title: str | None = "Pairwise interactions (J)",
    annotate: bool = False,
    cmap: str = "coolwarm",
) -> tuple[Any, Any]:
    """Plot the signed interaction matrix ``J`` as a heatmap."""
    plt = _pyplot()
    labels = _labels(analysis, labels)
    if ax is None:
        _, ax = plt.subplots(figsize=(max(5, len(labels) * 0.45), max(4, len(labels) * 0.4)))
    image = ax.imshow(analysis.J, cmap=cmap, aspect="auto")
    ax.figure.colorbar(image, ax=ax, label="J")
    ax.set_xticks(range(len(labels)), labels, rotation=90)
    ax.set_yticks(range(len(labels)), labels)
    if annotate and len(labels) <= 20:
        for i in range(len(labels)):
            for j in range(len(labels)):
                ax.text(j, i, f"{analysis.J[i, j]:.2f}", ha="center", va="center", fontsize=7)
    return _finish(ax.figure, ax, title)


def plot_correlations(
    analysis: AnalysisResult,
    *,
    labels: Sequence[str] | None = None,
    ax: Any | None = None,
    title: str | None = "Model correlations",
    cmap: str = "RdBu_r",
) -> tuple[Any, Any]:
    """Plot the model correlation matrix."""
    plt = _pyplot()
    labels = _labels(analysis, labels)
    if ax is None:
        _, ax = plt.subplots(figsize=(max(5, len(labels) * 0.45), max(4, len(labels) * 0.4)))
    image = ax.imshow(analysis.correlations, cmap=cmap, vmin=-1, vmax=1, aspect="auto")
    ax.figure.colorbar(image, ax=ax, label="correlation")
    ax.set_xticks(range(len(labels)), labels, rotation=90)
    ax.set_yticks(range(len(labels)), labels)
    return _finish(ax.figure, ax, title)


def plot_training_history(
    fit: FitResult,
    *,
    ax: Any | None = None,
    title: str | None = "Training objective",
) -> tuple[Any, Any]:
    """Plot the recorded training objective by epoch."""
    plt = _pyplot()
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 4))
    history = np.asarray(fit.objective_history, dtype=float)
    ax.plot(np.arange(1, len(history) + 1), history, linewidth=1.5)
    ax.set_xlabel("epoch")
    ax.set_ylabel("objective")
    ax.grid(alpha=0.25)
    return _finish(ax.figure, ax, title)


__all__ = ["plot_correlations", "plot_interactions", "plot_training_history"]
