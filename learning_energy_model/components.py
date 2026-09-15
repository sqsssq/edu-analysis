"""Protocols for replacing package components without changing the model API."""

from typing import Any, Protocol

import torch


class PreprocessorProtocol(Protocol):
    """Minimum interface required by :class:`LearningModel`."""

    feature_names: tuple[str, ...]

    def fit(self, X: Any, y: Any) -> "PreprocessorProtocol": ...

    def transform(self, X: Any, y: Any) -> tuple[Any, Any]: ...

    def transform_features(self, X: Any) -> Any: ...


class SamplerProtocol(Protocol):
    """Minimum interface for a non-exact binary-state sampler."""

    def sample(self, h: torch.Tensor, J: torch.Tensor, **kwargs: Any) -> Any: ...

    def moments(
        self, h: torch.Tensor, J: torch.Tensor, **kwargs: Any
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, dict[str, Any]]: ...


class TrainerProtocol(Protocol):
    """Minimum interface for a caller-provided training lifecycle."""

    def fit(
        self,
        model: Any,
        X: Any,
        y: Any,
        *,
        sample_weight: Any | None = None,
        method: str = "moment_matching",
    ) -> Any: ...


class AnalyzerProtocol(Protocol):
    """Minimum interface for a caller-provided aggregate analysis lifecycle."""

    def analyze(self, model: Any) -> Any: ...
