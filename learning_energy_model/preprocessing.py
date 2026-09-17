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
    if np.isinf(array).any():
        raise ValueError("data must not contain positive or negative infinity")
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
        self.feature_means: np.ndarray | None = None
        self.feature_scales: np.ndarray | None = None
        self.target_mean: float = 0.0
        self.target_scale: float = 1.0
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
            raise ValueError(
                "missing values found; choose missing_strategy='median', 'mean', or 'zero' to impute"
            )
        if medians is None:
            if self.config.missing_strategy == "mean":
                medians = np.nanmean(array, axis=0)
            elif self.config.missing_strategy == "zero":
                medians = np.zeros(array.shape[1], dtype=float)
            else:
                medians = np.nanmedian(array, axis=0)
        if np.isnan(medians).any():
            raise ValueError("a column contains only missing values")
        result = array.copy()
        rows, cols = np.where(np.isnan(result))
        result[rows, cols] = medians[cols]
        return result

    def _imputation_values(self, array: np.ndarray) -> np.ndarray:
        if self.config.missing_strategy == "mean":
            return np.nanmean(array, axis=0)
        if self.config.missing_strategy == "zero":
            return np.zeros(array.shape[1], dtype=float)
        return np.nanmedian(array, axis=0)

    @staticmethod
    def _binarize(
        values: np.ndarray, threshold: float, *, strict: bool = False
    ) -> np.ndarray:
        """Binarize values while preserving native binary columns.

        ``strict=True`` reproduces the paper convention ``f > theta``;
        package-native thresholding retains its historical ``f >= theta``
        behavior.
        """
        observed = values[~np.isnan(values)]
        if observed.size and np.isin(observed, (0.0, 1.0)).all():
            return values.astype(np.float64, copy=True)
        if strict:
            return (values > threshold).astype(np.float64)
        return (values >= threshold).astype(np.float64)

    def fit(self, X: Any, y: Any) -> "BinaryPreprocessor":
        features = _as_array(X)
        target_values = _as_array(y).reshape(-1)
        if len(features) != len(target_values):
            raise ValueError("X and y must have the same number of rows")
        self.feature_names = self._names_for_features(features.shape[1])
        self.feature_medians = self._imputation_values(features)
        target_fill = self._imputation_values(target_values.reshape(-1, 1))
        self.target_median = float(target_fill[0])
        self.target_median = float(np.nanmedian(target_values))
        features = self._fill_missing(features, self.feature_medians)
        target_values = self._fill_missing(
            target_values.reshape(-1, 1), np.array([self.target_median])
        ).reshape(-1)

        self.feature_means, self.feature_scales = self._normalization_parameters(features)
        features = self._normalize(features, self.feature_means, self.feature_scales)
        target_mean, target_scale = self._normalization_parameters(target_values.reshape(-1, 1))
        self.target_mean = float(target_mean[0])
        self.target_scale = float(target_scale[0])
        target_values = self._normalize(
            target_values.reshape(-1, 1), target_mean, target_scale
        ).reshape(-1)

        if self.config.thresholds is not None:
            missing = set(self.feature_names) - set(self.config.thresholds)
            if missing:
                raise ValueError(f"thresholds missing feature names: {sorted(missing)}")
            self.thresholds = {name: float(self.config.thresholds[name]) for name in self.feature_names}
        elif self.config.threshold_method == "paper_std":
            self.thresholds = {
                name: float(np.std(features[:, i], ddof=0))
                for i, name in enumerate(self.feature_names)
            }
        else:
            quantile = self.config.quantile if self.config.threshold_method == "quantile" else 0.5
            self.thresholds = {
                name: float(np.quantile(features[:, i], quantile))
                for i, name in enumerate(self.feature_names)
            }
        if self.target_threshold is None and self.config.threshold_method == "paper_std":
            self.target_threshold = float(np.std(target_values, ddof=0))
        elif self.target_threshold is None:
            quantile = self.config.quantile if self.config.threshold_method == "quantile" else 0.5
            self.target_threshold = float(np.quantile(target_values, quantile))
        self._fitted = True
        return self

    def _normalization_parameters(self, array: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        if self.config.normalization == "none":
            return np.zeros(array.shape[1], dtype=float), np.ones(array.shape[1], dtype=float)
        means = np.zeros(array.shape[1], dtype=float)
        scales = np.ones(array.shape[1], dtype=float)
        for index in range(array.shape[1]):
            values = array[:, index]
            if np.isin(values, (0.0, 1.0)).all():
                continue
            means[index] = float(np.mean(values))
            scale = float(np.std(values, ddof=0))
            if not np.isfinite(scale) or scale == 0:
                raise ValueError("zscore normalization requires non-constant columns")
            scales[index] = scale
        return means, scales

    @staticmethod
    def _normalize(
        array: np.ndarray, means: np.ndarray, scales: np.ndarray
    ) -> np.ndarray:
        return (array - means) / scales

    def transform_features(self, X: Any) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("preprocessor must be fitted before transform")
        features = _as_array(_select_named_features(X, self.feature_names))
        if features.shape[1] != len(self.feature_names):
            raise ValueError("X has a different number of columns from the fitted data")
        features = self._fill_missing(features, self.feature_medians)
        if self.feature_means is None or self.feature_scales is None:
            raise RuntimeError("normalization parameters are unavailable")
        features = self._normalize(features, self.feature_means, self.feature_scales)
        threshold_array = np.array([self.thresholds[name] for name in self.feature_names])
        strict = self.config.threshold_method == "paper_std"
        return np.column_stack(
            [
                self._binarize(features[:, i], threshold_array[i], strict=strict)
                for i in range(features.shape[1])
            ]
        )

    def transform_target(self, y: Any) -> np.ndarray:
        if not self._fitted or self.target_threshold is None:
            raise RuntimeError("preprocessor must be fitted before transform")
        target_matrix = _as_array(y).reshape(-1, 1)
        target_values = self._fill_missing(
            target_matrix, np.array([self.target_median])
        ).reshape(-1)
        target_values = self._normalize(
            target_values.reshape(-1, 1),
            np.array([self.target_mean]),
            np.array([self.target_scale]),
        ).reshape(-1)
        return self._binarize(
            target_values,
            self.target_threshold,
            strict=self.config.threshold_method == "paper_std",
        )

    def transform(self, X: Any, y: Any) -> tuple[np.ndarray, np.ndarray]:
        return self.transform_features(X), self.transform_target(y)
