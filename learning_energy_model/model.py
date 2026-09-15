"""Pairwise binary maximum-entropy energy model."""

from dataclasses import asdict
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np
import torch

from .components import AnalyzerProtocol, PreprocessorProtocol, SamplerProtocol, TrainerProtocol
from .config import DataConfig
from .data import TabularQualityReport, prepare_tabular_data, validate_tabular_data
from .preprocessing import BinaryPreprocessor
from .results import AnalysisResult, FitResult, PredictionResult
from .sampler import GibbsSampler
from .version import __version__


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
        mc_samples: int = 2_000,
        mc_burn_in: int = 500,
        mc_thinning: int = 1,
        mc_chains: int = 4,
        calculation: str = "auto",
        mc_max_rhat: float = 1.1,
        mc_min_effective_sample_size: float = 100.0,
        mc_max_mcse: float = 0.05,
        preprocessor: PreprocessorProtocol | None = None,
        sampler: SamplerProtocol | None = None,
        trainer: TrainerProtocol | None = None,
        analyzer: AnalyzerProtocol | None = None,
        device: str | None = None,
        seed: int = 0,
    ) -> None:
        if calculation not in {"auto", "exact", "monte_carlo"}:
            raise ValueError("calculation must be 'auto', 'exact', or 'monte_carlo'")
        if mc_max_rhat < 1.0 or not np.isfinite(mc_max_rhat):
            raise ValueError("mc_max_rhat must be finite and at least 1")
        if mc_min_effective_sample_size <= 0 or not np.isfinite(mc_min_effective_sample_size):
            raise ValueError("mc_min_effective_sample_size must be finite and positive")
        if mc_max_mcse <= 0 or not np.isfinite(mc_max_mcse):
            raise ValueError("mc_max_mcse must be finite and positive")
        self.config = config or DataConfig()
        self.learning_rate = learning_rate
        self.max_epochs = max_epochs
        self.tolerance = tolerance
        self.min_epochs = min_epochs
        self.max_exact_nodes = max_exact_nodes
        self.mc_samples = mc_samples
        self.mc_burn_in = mc_burn_in
        self.mc_thinning = mc_thinning
        self.mc_chains = mc_chains
        self.calculation = calculation
        self.mc_max_rhat = mc_max_rhat
        self.mc_min_effective_sample_size = mc_min_effective_sample_size
        self.mc_max_mcse = mc_max_mcse
        self.device = torch.device(device or "cpu")
        self.seed = seed
        self.preprocessor = preprocessor or BinaryPreprocessor(self.config)
        self.trainer = trainer
        self.analyzer = analyzer
        self.h: torch.Tensor | None = None
        self.J: torch.Tensor | None = None
        self._states: torch.Tensor | None = None
        self._fitted = False
        self.fit_result: FitResult | None = None
        self.last_quality_report: TabularQualityReport | None = None
        self.artifact_metadata = {
            "format_version": 1,
            "package": "interpretable-learning-energy-model",
            "package_version": __version__,
        }
        self.sampler = sampler or GibbsSampler(
                samples=mc_samples,
                burn_in=mc_burn_in,
                thinning=mc_thinning,
                chains=mc_chains,
                seed=seed,
            )

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
            raise ValueError("exact enumeration requested above max_exact_nodes")
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

    def _model_moments(
        self, *, seed_offset: int = 0
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, dict[str, Any]]:
        if self._states is not None:
            energies = self._energies(self._states)
            log_probs = torch.log_softmax(-energies, dim=0)
            probs = torch.exp(log_probs)
            means = probs @ self._states
            pairwise = torch.einsum("n,ni,nj->ij", probs, self._states, self._states)
            return means, pairwise, energies, {"calculation": "exact"}
        assert self.h is not None and self.J is not None
        means, pairwise, energies, diagnostics = self.sampler.moments(
            self.h, self.J, seed_offset=seed_offset
        )
        return means, pairwise, energies, diagnostics

    def _higher_order_moments(self, *, max_order: int = 4) -> dict[str, float]:
        """Return model joint moments for orders three through ``max_order``."""
        self._require_fitted()
        assert self.h is not None and self.J is not None
        if self._states is not None:
            states = self._states
            probabilities = torch.softmax(-self._energies(states), dim=0)
        else:
            states = self.sampler.sample(self.h, self.J, seed_offset=991).samples
            probabilities = torch.full(
                (states.shape[0],),
                1.0 / states.shape[0],
                dtype=torch.float64,
                device=states.device,
            )
        moments: dict[str, float] = {}
        for order in range(3, min(max_order, states.shape[1]) + 1):
            for indices in combinations(range(states.shape[1]), order):
                value = states[:, indices].prod(dim=1)
                moments["×".join(str(index) for index in indices)] = float(
                    (value * probabilities).sum()
                )
        return moments

    def _sampling_quality(self, diagnostics: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
        """Evaluate configured Monte Carlo calibration thresholds."""
        if diagnostics.get("calculation") == "exact":
            return True, {"quality_passed": True, "quality_checks": {}}
        checks = {
            "max_rhat": float(diagnostics.get("max_rhat", float("inf")))
            <= self.mc_max_rhat,
            "min_effective_sample_size": float(
                diagnostics.get("min_effective_sample_size", 0.0)
            )
            >= self.mc_min_effective_sample_size,
            "max_mcse": float(diagnostics.get("max_mcse", float("inf")))
            <= self.mc_max_mcse,
        }
        return all(checks.values()), {
            "quality_passed": all(checks.values()),
            "quality_checks": checks,
            "quality_thresholds": {
                "max_rhat": self.mc_max_rhat,
                "min_effective_sample_size": self.mc_min_effective_sample_size,
                "max_mcse": self.mc_max_mcse,
            },
        }

    @staticmethod
    def _empirical_higher_order_moments(
        data: torch.Tensor, weights: torch.Tensor, *, max_order: int = 4
    ) -> dict[str, float]:
        """Return weighted observed joint moments for orders three through four."""
        moments: dict[str, float] = {}
        normalised = weights / weights.sum()
        for order in range(3, min(max_order, data.shape[1]) + 1):
            for indices in combinations(range(data.shape[1]), order):
                value = data[:, indices].prod(dim=1)
                moments["×".join(str(index) for index in indices)] = float(
                    (value * normalised).sum()
                )
        return moments

    def _fit_kl(self, data: torch.Tensor, weights: torch.Tensor) -> FitResult:
        """Fit the exact negative log-likelihood with PyTorch autodiff."""
        if self._states is None:
            raise ValueError("method='kl' requires exact enumeration; use moment matching for larger models")
        assert self.h is not None and self.J is not None
        data_means = self._weighted_mean(data, weights)
        data_pairs = self._weighted_pairwise(data, weights)
        optimizer = torch.optim.Adam([self.h, self.J], lr=self.learning_rate)
        history: list[float] = []
        converged = False
        mean_error = float("inf")
        correlation_error = float("inf")
        for epoch in range(1, self.max_epochs + 1):
            optimizer.zero_grad()
            data_energy = self._energies(data)
            state_energy = self._energies(self._states)
            objective = (data_energy * weights).sum() / weights.sum() + torch.logsumexp(
                -state_energy, dim=0
            )
            objective.backward()
            optimizer.step()
            with torch.no_grad():
                self.J.fill_diagonal_(0.0)
                self.J.copy_((self.J + self.J.T) / 2)
                model_means, model_pairs, _, _ = self._model_moments()
                mean_delta = model_means - data_means
                pair_delta = model_pairs - data_pairs
                pair_delta.fill_diagonal_(0.0)
                mean_error = float(torch.max(torch.abs(mean_delta)))
                correlation_error = float(torch.max(torch.abs(pair_delta)))
            history.append(float(objective.detach()))
            if epoch >= self.min_epochs and max(mean_error, correlation_error) <= self.tolerance:
                converged = True
                break
        warnings = []
        if not converged:
            warnings.append("KL/autodiff training did not reach the requested tolerance")
        model_means, model_pairs, _, _ = self._model_moments()
        self.h = self.h.detach()
        self.J = self.J.detach()
        self._fitted = True
        observed_higher = self._empirical_higher_order_moments(data, weights)
        model_higher = self._higher_order_moments()
        self.fit_result = FitResult(
            converged=converged,
            epochs=epoch,
            objective_history=history,
            mean_error=mean_error,
            correlation_error=correlation_error,
            warnings=warnings,
            diagnostics={
                "n_samples": int(data.shape[0]),
                "n_nodes": int(data.shape[1]),
                "calculation": "exact",
                "training_method": "kl",
            },
            observed_means=data_means.detach().cpu().numpy(),
            model_means=model_means.detach().cpu().numpy(),
            observed_pairwise_moments=data_pairs.detach().cpu().numpy(),
            model_pairwise_moments=model_pairs.detach().cpu().numpy(),
            observed_higher_order_moments=observed_higher,
            model_higher_order_moments=model_higher,
        )
        return self.fit_result

    def fit(
        self,
        X: Any,
        y: Any,
        sample_weight: Any | None = None,
        *,
        method: str = "moment_matching",
    ) -> FitResult:
        """Fit parameters by moment matching or exact KL/autodiff training."""
        if self.trainer is not None:
            result = self.trainer.fit(self, X, y, sample_weight=sample_weight, method=method)
            if not isinstance(result, FitResult):
                raise TypeError("custom trainer must return a FitResult")
            return result
        if method not in {"moment_matching", "kl"}:
            raise ValueError("method must be 'moment_matching' or 'kl'")
        torch.manual_seed(self.seed)
        binary_X, binary_y = self.preprocessor.fit(X, y).transform(X, y)
        data_np = np.column_stack([binary_X, binary_y])
        n_samples, n_features = data_np.shape
        data = torch.as_tensor(data_np, dtype=torch.float64, device=self.device)
        if sample_weight is None:
            weights = torch.ones(n_samples, dtype=torch.float64, device=self.device)
        else:
            weights = torch.as_tensor(np.asarray(sample_weight, dtype=float).reshape(-1), dtype=torch.float64, device=self.device)
            if (
                len(weights) != n_samples
                or not torch.all(torch.isfinite(weights))
                or torch.any(weights < 0)
                or float(weights.sum()) <= 0
            ):
                raise ValueError(
                    "sample_weight must be finite, non-negative, and match the number of rows"
                )

        self.h = torch.zeros(
            n_features, dtype=torch.float64, device=self.device, requires_grad=method == "kl"
        )
        self.J = torch.zeros(
            (n_features, n_features),
            dtype=torch.float64,
            device=self.device,
            requires_grad=method == "kl",
        )
        if self.calculation == "exact":
            if n_features > self.max_exact_nodes:
                raise ValueError(
                    "calculation='exact' requires n_nodes <= max_exact_nodes; "
                    "use calculation='monte_carlo' or 'auto' for larger models"
                )
            self._states = self._enumerate_states(n_features)
        elif self.calculation == "monte_carlo":
            self._states = None
        else:
            self._states = (
                self._enumerate_states(n_features)
                if n_features <= self.max_exact_nodes
                else None
            )
        if method == "kl":
            return self._fit_kl(data, weights)
        data_means = self._weighted_mean(data, weights)
        data_pairs = self._weighted_pairwise(data, weights)
        history = []
        converged = False
        mean_error = float("inf")
        correlation_error = float("inf")

        for epoch in range(1, self.max_epochs + 1):
            model_means, model_pairs, energies, sampling_diagnostics = self._model_moments(
                seed_offset=epoch
            )
            # For p(s) ∝ exp(-E), the log-likelihood gradient is
            # model_moment - empirical_moment for both h and J.
            mean_delta = model_means - data_means
            pair_delta = model_pairs - data_pairs
            pair_delta.fill_diagonal_(0.0)
            mean_error = float(torch.max(torch.abs(mean_delta)))
            correlation_error = float(torch.max(torch.abs(pair_delta)))
            objective = float(energies.mean())
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
        sampling_quality_passed, sampling_quality = self._sampling_quality(sampling_diagnostics)
        if not sampling_quality_passed:
            warnings.append("Monte Carlo diagnostics did not meet configured quality thresholds")
        final_model_means, final_model_pairs, _, _ = self._model_moments(
            seed_offset=self.max_epochs + 1
        )
        self._fitted = True
        self.fit_result = FitResult(
            converged=converged,
            epochs=epoch,
            objective_history=history,
            mean_error=mean_error,
            correlation_error=correlation_error,
            warnings=warnings,
            diagnostics={
                "n_samples": n_samples,
                "n_nodes": n_features,
                "calculation": "exact" if self._states is not None else "monte_carlo",
                "training_method": "moment_matching",
                **sampling_diagnostics,
                **sampling_quality,
            },
            observed_means=data_means.detach().cpu().numpy(),
            model_means=final_model_means.detach().cpu().numpy(),
            observed_pairwise_moments=data_pairs.detach().cpu().numpy(),
            model_pairwise_moments=final_model_pairs.detach().cpu().numpy(),
            observed_higher_order_moments=self._empirical_higher_order_moments(data, weights),
            model_higher_order_moments=self._higher_order_moments(),
        )
        return self.fit_result

    def fit_table(
        self,
        table: Any,
        *,
        feature_names: tuple[str, ...] | None = None,
        target_name: str | None = None,
        weight_name: str | None = None,
        method: str = "moment_matching",
    ) -> FitResult:
        """Validate, prepare, and fit directly from a named table or mapping."""
        selected_features = feature_names or self.config.feature_names
        selected_target = target_name or self.config.target_name
        selected_weight = weight_name or self.config.sample_weight_name
        if not selected_features:
            raise ValueError("feature_names are required when fitting a named table")
        quality = validate_tabular_data(
            table,
            feature_names=selected_features,
            target_name=selected_target,
            weight_name=selected_weight,
        )
        if not quality.passed:
            raise ValueError("input quality checks failed: " + "; ".join(quality.issues))
        self.last_quality_report = quality
        prepared = prepare_tabular_data(
            table,
            feature_names=selected_features,
            target_name=selected_target,
            weight_name=selected_weight,
        )
        self.config = self.config.copy_with(
            feature_names=prepared.feature_names,
            target_name=prepared.target_name,
            sample_weight_name=selected_weight,
        )
        self.preprocessor = BinaryPreprocessor(self.config)
        return self.fit(
            prepared.X,
            prepared.y,
            sample_weight=prepared.sample_weight,
            method=method,
        )

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

    def sample(self, n_samples: int = 1_000) -> np.ndarray:
        """Draw binary states from the fitted joint model distribution."""
        self._require_fitted()
        if n_samples <= 0:
            raise ValueError("n_samples must be positive")
        assert self.h is not None and self.J is not None
        if self._states is not None:
            energies = self._energies(self._states)
            probabilities = torch.softmax(-energies, dim=0)
            generator = torch.Generator(device=self.device)
            generator.manual_seed(self.seed)
            indices = torch.multinomial(
                probabilities, n_samples, replacement=True, generator=generator
            )
            return self._states[indices].detach().cpu().numpy()
        sampler = GibbsSampler(
            samples=n_samples,
            burn_in=self.mc_burn_in,
            thinning=self.mc_thinning,
            chains=self.mc_chains,
            seed=self.seed,
        )
        return sampler.sample(self.h, self.J).samples[:n_samples].detach().cpu().numpy()

    def analyze(self) -> AnalysisResult:
        """Return parameters, exact moments, energy statistics, and node freezing results."""
        self._require_fitted()
        if self.analyzer is not None:
            result = self.analyzer.analyze(self)
            if not isinstance(result, AnalysisResult):
                raise TypeError("custom analyzer must return an AnalysisResult")
            return result
        return self._builtin_analyze()

    def _builtin_analyze(self) -> AnalysisResult:
        """Run the built-in aggregate analysis implementation."""
        self._require_fitted()
        assert self.h is not None and self.J is not None
        means, pairs, energies, sampling_diagnostics = self._model_moments()
        baseline_target = float(means[self.target_index])
        interventions: dict[str, dict[str, float]] = {}
        for index, name in enumerate(self.preprocessor.feature_names):
            if self._states is not None:
                mask = self._states[:, index] == 0
                frozen_states = self._states[mask]
                frozen_energies = self._energies(frozen_states)
                frozen_probs = torch.softmax(-frozen_energies, dim=0)
                frozen_mean = float((frozen_probs * frozen_states[:, self.target_index]).sum())
            else:
                assert self.h is not None and self.J is not None
                frozen_means, _, _, _ = self.sampler.moments(
                    self.h,
                    self.J,
                    clamp_index=index,
                    clamp_value=0.0,
                    seed_offset=index + 1,
                )
                frozen_mean = float(frozen_means[self.target_index])
            interventions[name] = {
                "baseline_target_probability": baseline_target,
                "frozen_target_probability": frozen_mean,
                "model_internal_difference": frozen_mean - baseline_target,
            }
        h = self.h.detach().cpu().numpy().copy()
        J = self.J.detach().cpu().numpy().copy()
        means_array = means.detach().cpu().numpy()
        pairs_array = pairs.detach().cpu().numpy()
        variances = means_array * (1.0 - means_array)
        denominator = np.sqrt(np.outer(variances, variances))
        correlations = np.divide(
            pairs_array - np.outer(means_array, means_array),
            denominator,
            out=np.zeros_like(pairs_array),
            where=denominator > 1e-12,
        )
        return AnalysisResult(
            h=h,
            J=J,
            means=means_array,
            pairwise_moments=pairs_array,
            correlations=correlations,
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
                "Monte Carlo results require convergence diagnostics to be reviewed.",
            ],
            diagnostics=sampling_diagnostics,
            higher_order_moments=self._higher_order_moments(),
        )

    def save(self, path: Any) -> None:
        self._require_fitted()
        assert self.h is not None and self.J is not None
        if not isinstance(self.preprocessor, BinaryPreprocessor):
            raise TypeError(
                "saving models with a custom preprocessor is unsupported; "
                "serialize its contract separately and use it at runtime"
            )
        if not isinstance(self.sampler, GibbsSampler):
            raise TypeError(
                "saving models with a custom sampler is unsupported; "
                "serialize its configuration separately and use it at runtime"
            )
        if self.trainer is not None or self.analyzer is not None:
            raise TypeError(
                "saving models with custom trainer or analyzer components is unsupported; "
                "serialize those components separately and use them at runtime"
            )
        payload = {
            "artifact": self.artifact_metadata,
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
            "quality_report": self.last_quality_report.to_dict() if self.last_quality_report else None,
            "random_state": {
                "torch": torch.get_rng_state(),
                "numpy": np.random.get_state(),
            },
            "settings": {
                "learning_rate": self.learning_rate,
                "max_epochs": self.max_epochs,
                "tolerance": self.tolerance,
                "min_epochs": self.min_epochs,
                "max_exact_nodes": self.max_exact_nodes,
                "mc_samples": self.mc_samples,
                "mc_burn_in": self.mc_burn_in,
                "mc_thinning": self.mc_thinning,
                "mc_chains": self.mc_chains,
                "calculation": self.calculation,
                "mc_max_rhat": self.mc_max_rhat,
                "mc_min_effective_sample_size": self.mc_min_effective_sample_size,
                "mc_max_mcse": self.mc_max_mcse,
                "seed": self.seed,
            },
        }
        torch.save(payload, Path(path))

    @classmethod
    def load(cls, path: Any, *, map_location: str = "cpu") -> "LearningModel":
        payload = torch.load(Path(path), map_location=map_location, weights_only=False)
        config = DataConfig(**payload["config"])
        settings = dict(payload["settings"])
        settings.setdefault("calculation", "auto")
        settings.setdefault("mc_max_rhat", 1.1)
        settings.setdefault("mc_min_effective_sample_size", 100.0)
        settings.setdefault("mc_max_mcse", 0.05)
        model = cls(config, **settings, device=map_location)
        model.artifact_metadata = payload.get(
            "artifact",
            {
                "format_version": 1,
                "package": "interpretable-learning-energy-model",
                "package_version": __version__,
            },
        )
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
        if model.calculation == "exact":
            model._states = model._enumerate_states(model.h.numel())
        elif model.calculation == "monte_carlo":
            model._states = None
        else:
            model._states = (
                model._enumerate_states(model.h.numel())
                if model.h.numel() <= model.max_exact_nodes
                else None
            )
        model._fitted = True
        if payload["fit_result"] is not None:
            model.fit_result = FitResult(**payload["fit_result"])
        quality_payload = payload.get("quality_report")
        if quality_payload is not None:
            model.last_quality_report = TabularQualityReport(
                row_count=quality_payload["row_count"],
                column_names=tuple(quality_payload["column_names"]),
                missing_fraction=dict(quality_payload["missing_fraction"]),
                infinite_count=dict(quality_payload["infinite_count"]),
                issues=tuple(quality_payload["issues"]),
                passed=quality_payload["passed"],
            )
        return model
