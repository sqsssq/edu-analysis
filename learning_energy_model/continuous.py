"""Continuous Gaussian/quadratic energy model.

This module is intentionally separate from the binary model.  It fits the
maximum-entropy distribution with a prescribed continuous mean and covariance:

    E(x) = 1/2 x.T K x - b.T x + const
    p(x) proportional to exp(-E(x))

where ``K`` is the positive-definite precision matrix and ``b = K @ mean``.
Off-diagonal precision terms describe conditional dependence; they are not
causal effects.
"""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch

from .results import ResultExportMixin
from .version import __version__


@dataclass
class ContinuousFitResult(ResultExportMixin):
    """Aggregate evidence returned by :class:`ContinuousEnergyModel.fit`."""

    converged: bool
    epochs: int
    objective_history: list[float]
    mean_error: float
    covariance_error: float
    warnings: list[str]
    diagnostics: dict[str, Any]
    observed_mean: np.ndarray
    model_mean: np.ndarray
    observed_covariance: np.ndarray
    model_covariance: np.ndarray


@dataclass
class ContinuousAnalysisResult(ResultExportMixin):
    """Interpretable aggregate output for a fitted continuous model."""

    mean: np.ndarray
    covariance: np.ndarray
    precision: np.ndarray
    interactions: np.ndarray
    conditional_coefficients: np.ndarray
    assumptions: list[str]
    limitations: list[str]
    diagnostics: dict[str, Any]


class ContinuousEnergyModel:
    """Fit a continuous Gaussian maximum-entropy energy model.

    The fitted density is ``N(mean, covariance)``.  The energy convention is
    ``E(x)=0.5*x.T@precision@x - (precision@mean).T@x + const``.  The
    interaction matrix is ``-precision`` off the diagonal, matching the sign
    of the coefficient in a conditional Gaussian mean.
    """

    def __init__(
        self,
        feature_names: tuple[str, ...] = (),
        *,
        ridge: float = 1e-6,
        metadata: dict[str, Any] | None = None,
        seed: int = 0,
    ) -> None:
        if ridge < 0 or not np.isfinite(ridge):
            raise ValueError("ridge must be finite and non-negative")
        if len(set(feature_names)) != len(feature_names):
            raise ValueError("feature_names must be unique")
        if any(not isinstance(name, str) or not name for name in feature_names):
            raise ValueError("feature_names must contain non-empty strings")
        self.feature_names = tuple(feature_names)
        self.ridge = float(ridge)
        self.metadata = dict(metadata or {})
        self.seed = int(seed)
        self.mean: np.ndarray | None = None
        self.covariance: np.ndarray | None = None
        self.precision: np.ndarray | None = None
        self.fit_result: ContinuousFitResult | None = None
        self._fitted = False
        self.artifact_metadata = {
            "format_version": 1,
            "package": "interpretable-learning-energy-model",
            "package_version": __version__,
            "model_family": "continuous_gaussian_quadratic",
        }

    @property
    def n_nodes(self) -> int:
        if self.mean is None:
            raise RuntimeError("fit the model before accessing n_nodes")
        return int(self.mean.size)

    @staticmethod
    def _as_matrix(X: Any) -> np.ndarray:
        values = X.to_numpy() if hasattr(X, "to_numpy") else np.asarray(X)
        array = np.asarray(values, dtype=float)
        if array.ndim != 2 or array.shape[0] < 2 or array.shape[1] < 1:
            raise ValueError("X must be a two-dimensional matrix with at least two rows")
        if not np.isfinite(array).all():
            raise ValueError("X must contain only finite values")
        return array

    @staticmethod
    def _validate_weights(sample_weight: Any | None, n_rows: int) -> np.ndarray:
        if sample_weight is None:
            return np.ones(n_rows, dtype=float)
        values = sample_weight.to_numpy() if hasattr(sample_weight, "to_numpy") else sample_weight
        weights = np.asarray(values, dtype=float).reshape(-1)
        if (
            len(weights) != n_rows
            or not np.isfinite(weights).all()
            or (weights < 0).any()
            or float(weights.sum()) <= 0
        ):
            raise ValueError("sample_weight must be finite, non-negative, and not all zero")
        return weights

    def fit(self, X: Any, sample_weight: Any | None = None) -> ContinuousFitResult:
        """Fit mean and covariance directly from continuous observations."""
        data = self._as_matrix(X)
        weights = self._validate_weights(sample_weight, data.shape[0])
        if self.feature_names and len(self.feature_names) != data.shape[1]:
            raise ValueError("feature_names length must match the number of columns in X")
        if not self.feature_names:
            self.feature_names = tuple(f"x{i}" for i in range(data.shape[1]))

        normalised = weights / weights.sum()
        mean = np.sum(data * normalised[:, None], axis=0)
        centered = data - mean
        covariance = np.einsum("n,ni,nj->ij", normalised, centered, centered)
        regularized_covariance = covariance + self.ridge * np.eye(data.shape[1])
        try:
            precision = np.linalg.inv(regularized_covariance)
        except np.linalg.LinAlgError as exc:
            raise ValueError(
                "continuous covariance is singular; provide more observations or a positive ridge"
            ) from exc
        precision = (precision + precision.T) / 2.0

        self.mean = mean
        self.covariance = regularized_covariance
        self.precision = precision
        logdet = float(np.linalg.slogdet(regularized_covariance)[1])
        objective = 0.5 * (logdet + data.shape[1] * np.log(2.0 * np.pi) + data.shape[1])
        covariance_error = float(np.max(np.abs(regularized_covariance - covariance)))
        self._fitted = True
        self.fit_result = ContinuousFitResult(
            converged=True,
            epochs=1,
            objective_history=[objective],
            mean_error=0.0,
            covariance_error=covariance_error,
            warnings=[],
            diagnostics={
                "n_samples": int(data.shape[0]),
                "n_nodes": int(data.shape[1]),
                "model_family": "continuous_gaussian_quadratic",
                "estimator": "weighted_gaussian_mle_with_ridge",
                "ridge": self.ridge,
                "positive_definite": bool(np.all(np.linalg.eigvalsh(regularized_covariance) > 0)),
            },
            observed_mean=mean.copy(),
            model_mean=mean.copy(),
            observed_covariance=covariance.copy(),
            model_covariance=regularized_covariance.copy(),
        )
        return self.fit_result

    def fit_table(self, table: Any, *, feature_names: tuple[str, ...] | None = None) -> ContinuousFitResult:
        """Fit from named columns without retaining the source table."""
        names = tuple(feature_names or self.feature_names)
        if not names:
            columns = getattr(table, "columns", None)
            if columns is None:
                raise ValueError("feature_names are required for a named table")
            names = tuple(str(name) for name in columns)
        try:
            values = np.column_stack([np.asarray(table[name], dtype=float) for name in names])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("could not select the requested continuous columns") from exc
        self.feature_names = names
        return self.fit(values)

    def _require_fitted(self) -> None:
        if not self._fitted or self.mean is None or self.covariance is None or self.precision is None:
            raise RuntimeError("fit the model before calling this method")

    def analyze(self) -> ContinuousAnalysisResult:
        """Return covariance, precision, and conditional interaction matrices."""
        self._require_fitted()
        assert self.mean is not None and self.covariance is not None and self.precision is not None
        interactions = -self.precision.copy()
        np.fill_diagonal(interactions, 0.0)
        diagonal = np.diag(self.precision)
        conditional_coefficients = np.divide(
            interactions,
            diagonal[:, None],
            out=np.zeros_like(interactions),
            where=diagonal[:, None] > 0,
        )
        return ContinuousAnalysisResult(
            mean=self.mean.copy(),
            covariance=self.covariance.copy(),
            precision=self.precision.copy(),
            interactions=interactions,
            conditional_coefficients=conditional_coefficients,
            assumptions=[
                "Variables are continuous and jointly Gaussian after preparation.",
                "The energy is quadratic with a positive-definite precision matrix.",
                "Off-diagonal precision interactions describe conditional dependence, not causality.",
            ],
            limitations=[
                "The Gaussian family cannot represent nonlinear or heavy-tailed dependence without extensions.",
                "A ridge term changes the reported covariance when the empirical covariance is ill-conditioned.",
                "PISA complex-survey inference is not implemented.",
            ],
            diagnostics={
                "feature_names": list(self.feature_names),
                "ridge": self.ridge,
                "model_family": "continuous_gaussian_quadratic",
            },
        )

    def conditional_mean(self, values: Any, target_index: int) -> float:
        """Return a target's Gaussian conditional mean given the other nodes.

        ``values`` must contain one value per node; the target entry is ignored.
        """
        self._require_fitted()
        assert self.mean is not None and self.covariance is not None
        target = int(target_index)
        if not 0 <= target < self.n_nodes:
            raise ValueError("target_index is outside the model node range")
        observed = np.asarray(values, dtype=float).reshape(-1)
        if observed.size != self.n_nodes:
            raise ValueError("values length must match the number of model nodes")
        if np.isnan(observed[target]):
            pass
        elif not np.isfinite(observed[target]):
            raise ValueError("values must be finite except for an optional NaN target")
        indices = np.array([i for i in range(self.n_nodes) if i != target])
        if not np.isfinite(observed[indices]).all():
            raise ValueError("all non-target values must be finite")
        covariance_oo = self.covariance[np.ix_(indices, indices)]
        coefficients = self.covariance[target, indices] @ np.linalg.solve(covariance_oo, np.eye(indices.size))
        return float(self.mean[target] + coefficients @ (observed[indices] - self.mean[indices]))

    def sample(self, n_samples: int = 1_000) -> np.ndarray:
        """Draw continuous observations from the fitted joint distribution."""
        self._require_fitted()
        if n_samples <= 0:
            raise ValueError("n_samples must be positive")
        assert self.mean is not None and self.covariance is not None
        return np.random.default_rng(self.seed).multivariate_normal(
            self.mean, self.covariance, size=n_samples, check_valid="raise"
        )

    def save(self, path: str | Path) -> None:
        """Save parameters and metadata without source observations."""
        self._require_fitted()
        assert self.mean is not None and self.covariance is not None and self.precision is not None
        payload = {
            "artifact": self.artifact_metadata,
            "feature_names": self.feature_names,
            "ridge": self.ridge,
            "metadata": self.metadata,
            "seed": self.seed,
            "mean": self.mean,
            "covariance": self.covariance,
            "precision": self.precision,
            "fit_result": asdict(self.fit_result) if self.fit_result else None,
        }
        torch.save(payload, Path(path))

    @classmethod
    def load(cls, path: str | Path, *, map_location: str = "cpu") -> "ContinuousEnergyModel":
        payload = torch.load(Path(path), map_location=map_location, weights_only=False)
        model = cls(
            tuple(payload["feature_names"]),
            ridge=float(payload["ridge"]),
            metadata=dict(payload.get("metadata", {})),
            seed=int(payload.get("seed", 0)),
        )
        model.artifact_metadata = payload.get("artifact", model.artifact_metadata)
        model.mean = np.asarray(payload["mean"], dtype=float)
        model.covariance = np.asarray(payload["covariance"], dtype=float)
        model.precision = np.asarray(payload["precision"], dtype=float)
        if payload.get("fit_result") is not None:
            model.fit_result = ContinuousFitResult(**payload["fit_result"])
        model._fitted = True
        return model


__all__ = ["ContinuousAnalysisResult", "ContinuousEnergyModel", "ContinuousFitResult"]
