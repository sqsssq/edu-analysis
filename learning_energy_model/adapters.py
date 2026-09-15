"""Small framework adapters for the public learning energy model."""

from typing import Any

import numpy as np

from .config import DataConfig
from .model import LearningModel
from .results import FitResult, PredictionResult


class LearningEnergyClassifier:
    """A lightweight sklearn-style wrapper around :class:`LearningModel`.

    The adapter deliberately does not import or require scikit-learn. It follows
    the common estimator methods needed by callers and simple sklearn pipelines,
    while retaining the package's binary-node and interpretability contract.
    """

    def __init__(self, config: DataConfig | None = None, **model_kwargs: Any) -> None:
        self.config = config
        self.model_kwargs = dict(model_kwargs)
        self.model_: LearningModel | None = None
        self.fit_result_: FitResult | None = None
        self.classes_: np.ndarray = np.array([0.0, 1.0])

    def get_params(self, deep: bool = True) -> dict[str, Any]:
        """Return constructor parameters using the sklearn estimator convention."""
        del deep
        return {"config": self.config, "model_kwargs": dict(self.model_kwargs)}

    def set_params(self, **params: Any) -> "LearningEnergyClassifier":
        """Set constructor parameters and return this estimator."""
        unknown = set(params) - {"config", "model_kwargs"}
        if unknown:
            raise ValueError(f"unknown parameter(s): {', '.join(sorted(unknown))}")
        if "config" in params:
            self.config = params["config"]
        if "model_kwargs" in params:
            self.model_kwargs = dict(params["model_kwargs"])
        self.model_ = None
        self.fit_result_ = None
        return self

    def fit(
        self, X: Any, y: Any, sample_weight: Any | None = None
    ) -> "LearningEnergyClassifier":
        """Fit the wrapped model and return the estimator."""
        self.model_ = LearningModel(self.config, **self.model_kwargs)
        self.fit_result_ = self.model_.fit(X, y, sample_weight=sample_weight)
        return self

    def predict_proba(self, X: Any) -> np.ndarray:
        """Return two-column probabilities ordered as ``classes_``."""
        prediction = self._predict_result(X)
        positive = prediction.probabilities
        return np.column_stack([1.0 - positive, positive])

    def predict(self, X: Any) -> np.ndarray:
        """Return binary predictions using a 0.5 positive-probability cutoff."""
        return (self._predict_result(X).probabilities >= 0.5).astype(float)

    def _predict_result(self, X: Any) -> PredictionResult:
        if self.model_ is None:
            raise RuntimeError("fit the estimator before calling predict")
        return self.model_.predict(X)

    def analyze(self) -> Any:
        """Expose the wrapped model's structured interpretability report."""
        if self.model_ is None:
            raise RuntimeError("fit the estimator before calling analyze")
        return self.model_.analyze()
