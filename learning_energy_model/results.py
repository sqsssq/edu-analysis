"""Structured results returned by the public API."""

import json
from dataclasses import asdict, dataclass, field
from typing import Any, cast

import numpy as np


def _json_safe(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


class ResultExportMixin:
    """Provide stable JSON-compatible export without requiring pandas."""

    def to_dict(self) -> dict[str, Any]:
        return _json_safe(asdict(cast(Any, self)))

    def to_json(self, *, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent, sort_keys=True)


@dataclass
class FitResult(ResultExportMixin):
    converged: bool
    epochs: int
    objective_history: list[float]
    mean_error: float
    correlation_error: float
    warnings: list[str] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass
class PredictionResult(ResultExportMixin):
    probabilities: np.ndarray
    uncertainty: np.ndarray
    labels: np.ndarray | None = None
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisResult(ResultExportMixin):
    h: np.ndarray
    J: np.ndarray
    means: np.ndarray
    pairwise_moments: np.ndarray
    energy_statistics: dict[str, float]
    interventions: dict[str, dict[str, float]]
    assumptions: list[str]
    limitations: list[str]
    diagnostics: dict[str, Any] = field(default_factory=dict)
