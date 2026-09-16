"""Paper-specific aggregate diagnostics kept separate from core fitting."""

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np


def classify_effective_interactions(
    values: Mapping[str, float],
) -> dict[str, Any]:
    """Classify effective interactions using the paper's mean ± SD rule."""
    if not values:
        raise ValueError("effective interaction values must not be empty")
    names = list(values)
    array = np.asarray([values[name] for name in names], dtype=float)
    if not np.isfinite(array).all():
        raise ValueError("effective interaction values must be finite")
    mean = float(array.mean())
    std = float(array.std())
    lower, upper = mean - std, mean + std
    classification = {
        name: (
            "inhibitory" if values[name] > upper
            else "facilitative" if values[name] < lower
            else "neutral"
        )
        for name in names
    }
    return {
        "mean": mean,
        "std": std,
        "lower_benchmark": lower,
        "upper_benchmark": upper,
        "values": dict(values),
        "classification": classification,
    }


def threshold_sensitivity(
    data: Any,
    thresholds: Sequence[float],
    *,
    standardize: bool = True,
) -> dict[str, Any]:
    """Measure original-vs-binarized correlation across a threshold grid.

    This reproduces the Appendix A diagnostic without retaining raw rows in a
    report. When ``standardize`` is true, each column is centered and scaled
    using its population standard deviation before thresholding.
    """
    values = np.asarray(data, dtype=float)
    grid = np.asarray(thresholds, dtype=float).reshape(-1)
    if values.ndim != 2 or values.shape[0] < 2 or values.shape[1] < 2:
        raise ValueError("data must contain at least two rows and two columns")
    if grid.size == 0 or not np.isfinite(grid).all() or not np.isfinite(values).all():
        raise ValueError("data and thresholds must be finite and non-empty")
    transformed = values.copy()
    if standardize:
        scales = transformed.std(axis=0)
        if np.any(scales == 0):
            raise ValueError("cannot standardize a constant column")
        transformed = (transformed - transformed.mean(axis=0)) / scales
    original = np.corrcoef(transformed, rowvar=False)
    upper = np.triu_indices(values.shape[1], k=1)
    original_pairs = original[upper]
    correlations = []
    for threshold in grid:
        binary = (transformed > threshold).astype(float)
        binary_pairs = np.corrcoef(binary, rowvar=False)[upper]
        if np.std(binary_pairs) == 0 or np.std(original_pairs) == 0:
            correlation = None
        else:
            correlation = float(np.corrcoef(original_pairs, binary_pairs)[0, 1])
        correlations.append(correlation)
    finite = [value for value in correlations if value is not None]
    return {
        "thresholds": grid.tolist(),
        "correlations": correlations,
        "minimum_correlation": float(min(finite)) if finite else None,
        "maximum_correlation": float(max(finite)) if finite else None,
        "all_above_0_8": bool(finite) and min(finite) > 0.8,
        "standardized": standardize,
    }


__all__ = ["classify_effective_interactions", "threshold_sensitivity"]
