"""Management of independent target models for multiple domains."""

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .config import DataConfig
from .model import LearningModel
from .results import AnalysisResult, FitResult, PredictionResult


class MultiDomainManager:
    """Fit and serve independent :class:`LearningModel` instances by domain."""

    def __init__(
        self,
        configs: Mapping[str, DataConfig] | None = None,
        *,
        model_kwargs: Mapping[str, Any] | None = None,
    ) -> None:
        self.model_kwargs = dict(model_kwargs or {})
        self._models: dict[str, LearningModel] = {}
        for domain, config in (configs or {}).items():
            self.add_domain(domain, config)

    @property
    def domains(self) -> tuple[str, ...]:
        """Return registered domain names in insertion order."""
        return tuple(self._models)

    def add_domain(self, domain: str, config: DataConfig | None = None) -> None:
        """Register an unfitted independent model for ``domain``."""
        self._validate_domain(domain)
        if domain in self._models:
            raise ValueError(f"domain {domain!r} is already registered")
        self._models[domain] = LearningModel(config, **self.model_kwargs)

    def get_model(self, domain: str) -> LearningModel:
        """Return the model for a registered domain."""
        self._validate_domain(domain)
        try:
            return self._models[domain]
        except KeyError as exc:
            raise KeyError(f"unknown domain {domain!r}; available: {list(self.domains)}") from exc

    def fit(
        self,
        domain: str,
        X: Any,
        y: Any,
        sample_weight: Any | None = None,
    ) -> FitResult:
        """Fit one domain and return its structured fit result."""
        if domain not in self._models:
            self.add_domain(domain)
        return self._models[domain].fit(X, y, sample_weight=sample_weight)

    def predict(self, domain: str, X: Any) -> PredictionResult:
        """Return predictions from one fitted domain."""
        return self.get_model(domain).predict(X)

    def analyze(self, domain: str) -> AnalysisResult:
        """Return the structured interpretability report for one domain."""
        return self.get_model(domain).analyze()

    def save(self, path: str | Path) -> None:
        """Save each domain artifact and a JSON manifest in a directory."""
        root = Path(path)
        root.mkdir(parents=True, exist_ok=True)
        manifest: dict[str, Any] = {"format_version": 1, "domains": {}}
        for index, (domain, model) in enumerate(self._models.items()):
            filename = f"model-{index:03d}.pt"
            model.save(root / filename)
            manifest["domains"][domain] = filename
        (root / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
        )

    @classmethod
    def load(cls, path: str | Path) -> "MultiDomainManager":
        """Load a manager directory written by :meth:`save`."""
        root = Path(path)
        try:
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"manager manifest not found in {root}") from exc
        if manifest.get("format_version") != 1 or not isinstance(manifest.get("domains"), dict):
            raise ValueError("unsupported or invalid manager manifest")
        manager = cls()
        for domain, filename in manifest["domains"].items():
            if not isinstance(domain, str) or not isinstance(filename, str):
                raise TypeError("manager manifest domain entries must be strings")
            manager._models[domain] = LearningModel.load(root / filename)
        return manager

    @staticmethod
    def _validate_domain(domain: str) -> None:
        if not isinstance(domain, str) or not domain:
            raise ValueError("domain must be a non-empty string")
