"""Dependency-light binary preprocessing for arrays and tabular adapters."""

from collections.abc import Mapping
from typing import Any

import numpy as np

from .config import DataConfig


def _as_array(data: Any) -> np.ndarray:
    if hasattr(data, "to_numpy"):
        data = data.to_numpy()
    array = np.asarray(data, dtype=float)
    if array.ndim == 1:
        array = array.reshape(-1, 1)
    if array.ndim != 2:
        raise ValueError("data must be a two-dimensional array or table")
    return array


def _select_named_features(data: Any, names: tuple[str, ...]) -> Any:
    """Select fitted feature columns when a named table is supplied."""
    if isinstance(data, Mapping):
        missing = set(names) - set(data)
        if missing:
            raise ValueError(f"X is missing fitted feature columns: {sorted(missing)}")
        return np.column_stack([data[name] for name in names])
    if hasattr(data, "columns") and hasattr(data, "loc"):
        missing = set(names) - set(data.columns)
        if missing:
            raise ValueError(f"X is missing fitted feature columns: {sorted(missing)}")
        return data.loc[:, list(names)]
    return data


class BinaryPreprocessor:
    def __init__(self, config: DataConfig) -> None:
        self.config = config
        self.feature_names: tuple[str, ...] = config.feature_names
        self.thresholds: dict[str, float] = {}
        self.target_threshold: float | None = config.target_threshold
        self.feature_medians: np.ndarray | None = None
        self.target_median: float | None = None
        self._fitted = False

    def _names_for_features(self, n_features: int) -> tuple[str, ...]:
        if self.feature_names:
            if len(self.feature_names) != n_features:
                raise ValueError("feature_names length does not match X columns")
            return self.feature_names
        return tuple(f"x{i}" for i in range(n_features))

    def _fill_missing(self, array: np.ndarray, medians: np.ndarray | None = None) -> np.ndarray:
        if not np.isnan(array).any():
            return array
        if self.config.missing_strategy == "error":
            raise ValueError("missing values found; choose missing_strategy='median' to impute")
        if medians is None:
            medians = np.nanmedian(array, axis=0)
        if np.isnan(medians).any():
            raise ValueError("a column contains only missing values")
        result = array.copy()
        rows, cols = np.where(np.isnan(result))
        result[rows, cols] = medians[cols]
        return result

    @staticmethod
    def _binarize(values: np.ndarray, threshold: float) -> np.ndarray:
        """Preserve native 0/1 columns instead of thresholding at a zero median."""
        observed = values[~np.isnan(values)]
        if observed.size and np.isin(observed, (0.0, 1.0)).all():
            return values.astype(np.float64, copy=True)
        return (values >= threshold).astype(np.float64)

    def fit(self, X: Any, y: Any) -> "BinaryPreprocessor":
        features = _as_array(X)
        target_values = _as_array(y).reshape(-1)
        if len(features) != len(target_values):
            raise ValueError("X and y must have the same number of rows")
        self.feature_names = self._names_for_features(features.shape[1])
        self.feature_medians = np.nanmedian(features, axis=0)
        self.target_median = float(np.nanmedian(target_values))
        features = self._fill_missing(features, self.feature_medians)
        target_values = self._fill_missing(
            target_values.reshape(-1, 1), np.array([self.target_median])
        ).reshape(-1)

        if self.config.thresholds is not None:
            missing = set(self.feature_names) - set(self.config.thresholds)
            if missing:
                raise ValueError(f"thresholds missing feature names: {sorted(missing)}")
            self.thresholds = {name: float(self.config.thresholds[name]) for name in self.feature_names}
        else:
            quantile = self.config.quantile if self.config.threshold_method == "quantile" else 0.5
            self.thresholds = {
                name: float(np.quantile(features[:, i], quantile))
                for i, name in enumerate(self.feature_names)
            }
        if self.target_threshold is None:
            quantile = self.config.quantile if self.config.threshold_method == "quantile" else 0.5
            self.target_threshold = float(np.quantile(target_values, quantile))
        self._fitted = True
        return self

    def transform_features(self, X: Any) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("preprocessor must be fitted before transform")
        features = _as_array(_select_named_features(X, self.feature_names))
        if features.shape[1] != len(self.feature_names):
            raise ValueError("X has a different number of columns from the fitted data")
        features = self._fill_missing(features, self.feature_medians)
        threshold_array = np.array([self.thresholds[name] for name in self.feature_names])
        return np.column_stack(
            [self._binarize(features[:, i], threshold_array[i]) for i in range(features.shape[1])]
        )

    def transform_target(self, y: Any) -> np.ndarray:
        if not self._fitted or self.target_threshold is None:
            raise RuntimeError("preprocessor must be fitted before transform")
        target_matrix = _as_array(y).reshape(-1, 1)
        target_values = self._fill_missing(
            target_matrix, np.array([self.target_median])
        ).reshape(-1)
        return self._binarize(target_values, self.target_threshold)

    def transform(self, X: Any, y: Any) -> tuple[np.ndarray, np.ndarray]:
        return self.transform_features(X), self.transform_target(y)
