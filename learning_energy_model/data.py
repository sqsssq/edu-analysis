"""Input validation and tabular-data preparation helpers."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class PreparedData:
    """A validated, model-ready view of a tabular training dataset.

    The helper intentionally returns arrays rather than retaining the source
    table. This keeps raw data out of model artifacts and works with pandas,
    dictionaries of columns, and plain NumPy arrays.
    """

    X: np.ndarray
    y: np.ndarray
    feature_names: tuple[str, ...]
    target_name: str
    sample_weight: np.ndarray | None = None


def _column(data: Any, name: str) -> Any:
    if isinstance(data, Mapping):
        if name not in data:
            raise ValueError(f"column {name!r} is missing from the input table")
        return data[name]
    if hasattr(data, "columns") and name not in data.columns:
        raise ValueError(f"column {name!r} is missing from the input table")
    try:
        return data[name]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(f"could not select column {name!r} from the input table") from exc


def _as_vector(values: Any, *, name: str) -> np.ndarray:
    if hasattr(values, "to_numpy"):
        values = values.to_numpy()
    array = np.asarray(values, dtype=float).reshape(-1)
    if array.ndim != 1 or array.size == 0:
        raise ValueError(f"{name} must contain at least one value")
    if np.isinf(array).any():
        raise ValueError(f"{name} contains infinite values")
    return array


def prepare_tabular_data(
    table: Any,
    *,
    feature_names: tuple[str, ...] | list[str],
    target_name: str,
    weight_name: str | None = None,
) -> PreparedData:
    """Extract and validate named columns from a table-like input.

    Missing values are preserved for :class:`BinaryPreprocessor`, which can
    either reject or median-impute them according to ``DataConfig``. This
    function validates shape and infinities, but does not learn thresholds.
    """

    names = tuple(feature_names)
    if not names:
        raise ValueError("feature_names must contain at least one column")
    if len(set(names)) != len(names):
        raise ValueError("feature_names must be unique")
    if target_name in names:
        raise ValueError("target_name must not also be a feature name")
    features = np.column_stack([_as_vector(_column(table, name), name=name) for name in names])
    target = _as_vector(_column(table, target_name), name=target_name)
    if features.shape[0] != target.shape[0]:
        raise ValueError("feature and target columns must have the same number of rows")
    weights = None
    if weight_name is not None:
        if weight_name in names or weight_name == target_name:
            raise ValueError("weight_name must identify a separate column")
        weights = _as_vector(_column(table, weight_name), name=weight_name)
        if weights.shape[0] != target.shape[0]:
            raise ValueError("sample-weight column must have the same number of rows")
        if np.isnan(weights).any() or (weights < 0).any() or float(weights.sum()) <= 0:
            raise ValueError("sample weights must be finite, non-negative, and not all zero")
    return PreparedData(
        X=features,
        y=target,
        feature_names=names,
        target_name=target_name,
        sample_weight=weights,
    )
