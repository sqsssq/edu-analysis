"""Configuration and preprocessing contracts."""

from dataclasses import dataclass, replace
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

    def __post_init__(self) -> None:
        if self.threshold_method not in {"median", "quantile"}:
            raise ValueError("threshold_method must be 'median' or 'quantile'")
        if not 0 < self.quantile < 1:
            raise ValueError("quantile must be between 0 and 1")
        if self.missing_strategy not in {"error", "median"}:
            raise ValueError("missing_strategy must be 'error' or 'median'")
        if len(set(self.feature_names)) != len(self.feature_names):
            raise ValueError("feature_names must be unique")

    def copy_with(self, **updates: Any) -> "DataConfig":
        return replace(self, **updates)
