"""Structured results returned by the public API."""

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class FitResult:
    converged: bool
    epochs: int
    objective_history: list[float]
    mean_error: float
    correlation_error: float
    warnings: list[str] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass
class PredictionResult:
    probabilities: np.ndarray
    uncertainty: np.ndarray
    labels: np.ndarray | None = None
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisResult:
    h: np.ndarray
    J: np.ndarray
    means: np.ndarray
    pairwise_moments: np.ndarray
    energy_statistics: dict[str, float]
    interventions: dict[str, dict[str, float]]
    assumptions: list[str]
    limitations: list[str]

