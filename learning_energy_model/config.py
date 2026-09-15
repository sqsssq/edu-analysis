"""Configuration and preprocessing contracts."""

from dataclasses import dataclass, field, replace
from math import isfinite
from typing import Any


@dataclass
class DataConfig:
    """Rules for converting tabular inputs into binary model nodes.

    ``feature_names`` are required for named tabular data and recommended for
    arrays. Thresholds are learned from the training data by default and are
    stored with the fitted model.
    """

    feature_names: tuple[str, ...] = ()
    target_name: str = "target"
    thresholds: dict[str, float] | None = None
    target_threshold: float | None = None
    threshold_method: str = "median"
    quantile: float = 0.5
    missing_strategy: str = "error"
    metadata: dict[str, Any] = field(default_factory=dict)
    sample_weight_name: str | None = None

    def __post_init__(self) -> None:
        if any(not isinstance(name, str) or not name for name in self.feature_names):
            raise ValueError("feature_names must contain non-empty strings")
        if not isinstance(self.target_name, str) or not self.target_name:
            raise ValueError("target_name must be a non-empty string")
        if self.target_name in self.feature_names:
            raise ValueError("target_name must not also be a feature name")
        if self.sample_weight_name is not None and (
            not self.sample_weight_name
            or self.sample_weight_name in (*self.feature_names, self.target_name)
        ):
            raise ValueError("sample_weight_name must identify a separate non-empty column")
        if self.threshold_method not in {"median", "quantile"}:
            raise ValueError("threshold_method must be 'median' or 'quantile'")
        if not 0 < self.quantile < 1:
            raise ValueError("quantile must be between 0 and 1")
        if self.missing_strategy not in {"error", "median", "mean", "zero"}:
            raise ValueError("missing_strategy must be 'error', 'median', 'mean', or 'zero'")
        if len(set(self.feature_names)) != len(self.feature_names):
            raise ValueError("feature_names must be unique")
        if self.thresholds is not None and not all(
            isinstance(name, str) and isfinite(float(value))
            for name, value in self.thresholds.items()
        ):
            raise ValueError("thresholds must contain finite numeric values")
        if self.target_threshold is not None and not isfinite(float(self.target_threshold)):
            raise ValueError("target_threshold must be finite")

    def copy_with(self, **updates: Any) -> "DataConfig":
        return replace(self, **updates)
