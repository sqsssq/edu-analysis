"""Aggregate numerical comparison helpers for synthetic and reproduction checks."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np

from .results import ResultExportMixin


def _flatten_moments(value: Any) -> dict[str, float]:
    if isinstance(value, Mapping):
        return {str(key): float(item) for key, item in value.items()}
    array = np.asarray(value, dtype=float)
    if not np.isfinite(array).all():
        raise ValueError("moment values must be finite")
    return {str(index): float(item) for index, item in enumerate(array.reshape(-1))}


@dataclass(frozen=True)
class MomentComparison(ResultExportMixin):
    """Aggregate errors for matched moment orders."""

    max_absolute_error: dict[int, float]
    mean_absolute_error: dict[int, float]
    tolerances: dict[int, float]
    passed: bool


def compare_moment_orders(
    observed: Mapping[int, Any],
    modeled: Mapping[int, Any],
    *,
    tolerances: Mapping[int, float] | None = None,
) -> MomentComparison:
    """Compare matching first- through fourth-order moment collections.

    Orders may be NumPy arrays (for first/second order) or keyed mappings (for
    higher-order moments). Missing orders and mismatched keys fail loudly so a
    reproduction check cannot pass against an incomplete report.
    """
    if not observed:
        raise ValueError("observed moments must contain at least one order")
    if set(observed) != set(modeled):
        raise ValueError("observed and modeled moment orders must match")
    limits = {int(order): 0.0 for order in observed}
    if tolerances is not None:
        unknown = set(tolerances) - set(observed)
        if unknown:
            raise ValueError(f"tolerances contain unknown moment orders: {sorted(unknown)}")
        for order, tolerance in tolerances.items():
            if tolerance < 0 or not np.isfinite(tolerance):
                raise ValueError("moment tolerances must be finite and non-negative")
            limits[int(order)] = float(tolerance)
    max_errors: dict[int, float] = {}
    mean_errors: dict[int, float] = {}
    for order in observed:
        observed_values = _flatten_moments(observed[order])
        modeled_values = _flatten_moments(modeled[order])
        if set(observed_values) != set(modeled_values):
            raise ValueError(f"moment keys do not match for order {order}")
        differences = np.array(
            [abs(observed_values[key] - modeled_values[key]) for key in observed_values]
        )
        max_errors[int(order)] = float(differences.max())
        mean_errors[int(order)] = float(differences.mean())
    return MomentComparison(
        max_absolute_error=max_errors,
        mean_absolute_error=mean_errors,
        tolerances=limits,
        passed=all(max_errors[order] <= limits[order] for order in max_errors),
    )
