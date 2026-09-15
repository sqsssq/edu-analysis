"""Exact pairwise binary maximum-entropy energy model."""

from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np
import torch

from .config import DataConfig
from .preprocessing import BinaryPreprocessor
from .results import AnalysisResult, FitResult, PredictionResult


class LearningModel:
    """Fit an interpretable binary pairwise energy model.

    The energy convention is ``E(s) = h·s + sum(i<j) J[i,j] s[i]s[j]`` and
    the model distribution is ``p(s) ∝ exp(-E(s))`` at temperature one.
    ``J`` is stored symmetrically with a zero diagonal.
    """

    def __init__(
        self,
        config: DataConfig | None = None,
        *,
        learning_rate: float = 0.05,
        max_epochs: int = 2_000,
        tolerance: float = 1e-3,
        min_epochs: int = 25,
        max_exact_nodes: int = 20,
        device: str | None = None,
        seed: int = 0,
    ) -> None:
        self.config = config or DataConfig()
        self.learning_rate = learning_rate
        self.max_epochs = max_epochs
        self.tolerance = tolerance
        self.min_epochs = min_epochs
        self.max_exact_nodes = max_exact_nodes
        self.device = torch.device(device or "cpu")
        self.seed = seed
        self.preprocessor = BinaryPreprocessor(self.config)
        self.h: torch.Tensor | None = None
        self.J: torch.Tensor | None = None
        self._states: torch.Tensor | None = None
        self._fitted = False
        self.fit_result: FitResult | None = None

    @property
    def n_nodes(self) -> int:
        if self.h is None:
            raise RuntimeError("model has not been fitted")
        return int(self.h.numel())

    @property
    def target_index(self) -> int:
        return self.n_nodes - 1

    def _enumerate_states(self, n_nodes: int) -> torch.Tensor:
        if n_nodes > self.max_exact_nodes:
            raise NotImplementedError(
                "Monte Carlo sampling is planned for v0.2; exact enumeration "
                f"supports at most {self.max_exact_nodes} nodes"
            )
        values = torch.arange(2**n_nodes, device=self.device, dtype=torch.long)
        shifts = torch.arange(n_nodes - 1, -1, -1, device=self.device, dtype=torch.long)
        return ((values[:, None] >> shifts) & 1).to(torch.float64)

    @staticmethod
    def _weighted_mean(data: torch.Tensor, weights: torch.Tensor) -> torch.Tensor:
        return (data * weights[:, None]).sum(dim=0) / weights.sum()

    @staticmethod
    def _weighted_pairwise(data: torch.Tensor, weights: torch.Tensor) -> torch.Tensor:
        return torch.einsum("n,ni,nj->ij", weights, data, data) / weights.sum()

    def _energies(self, states: torch.Tensor) -> torch.Tensor:
        if self.h is None or self.J is None:
            raise RuntimeError("model parameters are not initialized")
        return states @ self.h + 0.5 * ((states @ self.J) * states).sum(dim=1)

    def _model_moments(self) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        if self._states is None:
            raise RuntimeError("exact states are not initialized")
        energies = self._energies(self._states)
        log_probs = torch.log_softmax(-energies, dim=0)
        probs = torch.exp(log_probs)
        means = probs @ self._states
        pairwise = torch.einsum("n,ni,nj->ij", probs, self._states, self._states)
        return means, pairwise, energies

    def fit(self, X: Any, y: Any, sample_weight: Any | None = None) -> FitResult:
        """Fit parameters by matching empirical first- and second-order moments."""
        torch.manual_seed(self.seed)
        binary_X, binary_y = self.preprocessor.fit(X, y).transform(X, y)
        data_np = np.column_stack([binary_X, binary_y])
        n_samples, n_features = data_np.shape
        if n_features > self.max_exact_nodes:
            raise NotImplementedError(
                "Monte Carlo sampling is planned for v0.2; exact training supports "
                f"at most {self.max_exact_nodes} nodes"
            )
        data = torch.as_tensor(data_np, dtype=torch.float64, device=self.device)
        if sample_weight is None:
            weights = torch.ones(n_samples, dtype=torch.float64, device=self.device)
        else:
            weights = torch.as_tensor(np.asarray(sample_weight, dtype=float).reshape(-1), dtype=torch.float64, device=self.device)
            if len(weights) != n_samples or torch.any(weights < 0) or float(weights.sum()) <= 0:
                raise ValueError("sample_weight must be non-negative and match the number of rows")

        self.h = torch.zeros(n_features, dtype=torch.float64, device=self.device)
        self.J = torch.zeros((n_features, n_features), dtype=torch.float64, device=self.device)
        self._states = self._enumerate_states(n_features)
        data_means = self._weighted_mean(data, weights)
        data_pairs = self._weighted_pairwise(data, weights)
        history = []
        converged = False
        mean_error = float("inf")
        correlation_error = float("inf")

        for epoch in range(1, self.max_epochs + 1):
            model_means, model_pairs, energies = self._model_moments()
            mean_delta = data_means - model_means
            pair_delta = data_pairs - model_pairs
            pair_delta.fill_diagonal_(0.0)
            mean_error = float(torch.max(torch.abs(mean_delta)))
            correlation_error = float(torch.max(torch.abs(pair_delta)))
            objective = float((-torch.log_softmax(-energies, dim=0) * torch.ones_like(energies)).mean())
            history.append(objective)
            self.h += self.learning_rate * mean_delta
            self.J += self.learning_rate * pair_delta
            self.J.fill_diagonal_(0.0)
            self.J.copy_((self.J + self.J.T) / 2)
            if epoch >= self.min_epochs and max(mean_error, correlation_error) <= self.tolerance:
                converged = True
                break

        warnings = []
        if not converged:
            warnings.append("moment matching did not reach the requested tolerance")
        self._fitted = True
        self.fit_result = FitResult(
            converged=converged,
            epochs=epoch,
            objective_history=history,
            mean_error=mean_error,
            correlation_error=correlation_error,
            warnings=warnings,
            diagnostics={"n_samples": n_samples, "n_nodes": n_features, "calculation": "exact"},
        )
        return self.fit_result

    def _require_fitted(self) -> None:
        if not self._fitted or self.h is None or self.J is None:
            raise RuntimeError("fit the model before calling this method")

    def predict(self, X: Any) -> PredictionResult:
        """Return the conditional probability that the target node equals one."""
        self._require_fitted()
        assert self.h is not None and self.J is not None
        binary_X = self.preprocessor.transform_features(X)
        target_field = float(self.h[self.target_index]) + binary_X @ self.J[: self.target_index, self.target_index].detach().cpu().numpy()
        probabilities = 1.0 / (1.0 + np.exp(target_field))
        uncertainty = np.sqrt(probabilities * (1.0 - probabilities))
        return PredictionResult(
            probabilities=probabilities,
            uncertainty=uncertainty,
            diagnostics={"target_name": self.config.target_name, "conditional_on": list(self.preprocessor.feature_names)},
        )

    def analyze(self) -> AnalysisResult:
        """Return parameters, exact moments, energy statistics, and node freezing results."""
        self._require_fitted()
        assert self.h is not None and self.J is not None
        means, pairs, energies = self._model_moments()
        baseline_target = float(means[self.target_index])
        interventions: dict[str, dict[str, float]] = {}
        assert self._states is not None
        for index, name in enumerate(self.preprocessor.feature_names):
            mask = self._states[:, index] == 0
            frozen_states = self._states[mask]
            frozen_energies = self._energies(frozen_states)
            frozen_probs = torch.softmax(-frozen_energies, dim=0)
            frozen_mean = float((frozen_probs * frozen_states[:, self.target_index]).sum())
            interventions[name] = {
                "baseline_target_probability": baseline_target,
                "frozen_target_probability": frozen_mean,
                "model_internal_difference": frozen_mean - baseline_target,
            }
        h = self.h.detach().cpu().numpy().copy()
        J = self.J.detach().cpu().numpy().copy()
        return AnalysisResult(
            h=h,
            J=J,
            means=means.detach().cpu().numpy(),
            pairwise_moments=pairs.detach().cpu().numpy(),
            energy_statistics={
                "mean": float(energies.mean()),
                "std": float(energies.std()),
                "min": float(energies.min()),
                "max": float(energies.max()),
            },
            interventions=interventions,
            assumptions=[
                "Variables are represented as binary nodes.",
                "The energy convention is E=h·s+sum(i<j)J[i,j]s[i]s[j].",
                "Node freezing is a model-internal intervention, not a causal effect.",
            ],
            limitations=[
                "Exact enumeration is limited by the configured node threshold.",
                "No individual educational recommendation is produced.",
                "PISA complex-survey inference is not implemented in v0.1.",
            ],
        )

    def save(self, path: Any) -> None:
        self._require_fitted()
        assert self.h is not None and self.J is not None
        payload = {
            "config": asdict(self.config),
            "preprocessor": {
                "feature_names": self.preprocessor.feature_names,
                "thresholds": self.preprocessor.thresholds,
                "target_threshold": self.preprocessor.target_threshold,
                "feature_medians": self.preprocessor.feature_medians,
                "target_median": self.preprocessor.target_median,
            },
            "h": self.h.detach().cpu(),
            "J": self.J.detach().cpu(),
            "fit_result": asdict(self.fit_result) if self.fit_result else None,
            "settings": {
                "learning_rate": self.learning_rate,
                "max_epochs": self.max_epochs,
                "tolerance": self.tolerance,
                "min_epochs": self.min_epochs,
                "max_exact_nodes": self.max_exact_nodes,
                "seed": self.seed,
            },
        }
        torch.save(payload, Path(path))

    @classmethod
    def load(cls, path: Any, *, map_location: str = "cpu") -> "LearningModel":
        payload = torch.load(Path(path), map_location=map_location, weights_only=False)
        config = DataConfig(**payload["config"])
        model = cls(config, **payload["settings"], device=map_location)
        model.preprocessor = BinaryPreprocessor(config)
        state = payload["preprocessor"]
        model.preprocessor.feature_names = tuple(state["feature_names"])
        model.preprocessor.thresholds = dict(state["thresholds"])
        model.preprocessor.target_threshold = state["target_threshold"]
        model.preprocessor.feature_medians = state["feature_medians"]
        model.preprocessor.target_median = state["target_median"]
        model.preprocessor._fitted = True
        model.h = payload["h"].to(model.device)
        model.J = payload["J"].to(model.device)
        model._states = model._enumerate_states(model.h.numel())
        model._fitted = True
        if payload["fit_result"] is not None:
            model.fit_result = FitResult(**payload["fit_result"])
        return model
