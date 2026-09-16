"""Reproduce the paper's PISA protocol on a caller-supplied local data file.

This example intentionally keeps the raw PISA file local. It samples 1,200
complete rows 16 times per economy and outcome, uses the paper's standard-
deviation binarization, and fits with the exact KL/autodiff path.
"""

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from learning_energy_model import DataConfig, LearningModel, PISAMapping, read_pisa_file
from learning_energy_model.evaluation import compare_moment_orders

PAPER_FEATURES = (
    "HOMEPOS", "CULTPOSS", "HEDRES", "WEALTH", "ICTRES", "DISCLIMA",
    "TEACHSUP", "DIRINS", "PERFEED", "STIMREAD", "COMPETE", "WORKMAST",
    "EUDMO", "BEINGBULLIED", "ENTUSE", "SOIAICT", "ICTCLASS", "ICTOUTSIDE",
)
PAPER_OUTCOMES = ("PV1MATH", "PV1SCIE", "PV1READ")
PAPER_ECONOMIES = ("TAP", "HKG", "DEU", "USA", "GBR")


def _moments(fit: Any) -> tuple[dict[int, Any], dict[int, Any]]:
    observed = {
        1: fit.observed_means,
        2: fit.observed_pairwise_moments,
        3: {key: value for key, value in fit.observed_higher_order_moments.items()
            if key.count("×") == 2},
        4: {key: value for key, value in fit.observed_higher_order_moments.items()
            if key.count("×") == 3},
    }
    modeled = {
        1: fit.model_means,
        2: fit.model_pairwise_moments,
        3: {key: value for key, value in fit.model_higher_order_moments.items()
            if key.count("×") == 2},
        4: {key: value for key, value in fit.model_higher_order_moments.items()
            if key.count("×") == 3},
    }
    return observed, modeled


def _pearson(observed: Any, modeled: Any) -> float | None:
    x = np.asarray(list(observed.values()) if isinstance(observed, dict) else observed, dtype=float).reshape(-1)
    y = np.asarray(list(modeled.values()) if isinstance(modeled, dict) else modeled, dtype=float).reshape(-1)
    if x.size < 2 or np.std(x) == 0 or np.std(y) == 0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def _j_statistics(J: np.ndarray) -> dict[str, float]:
    values = J[np.triu_indices_from(J, k=1)]
    mean = float(values.mean())
    std = float(values.std())
    if std == 0:
        skewness = 0.0
        kurtosis = 0.0
    else:
        centered = values - mean
        skewness = float(np.mean(centered**3) / std**3)
        kurtosis = float(np.mean(centered**4) / std**4 - 3.0)
    return {"mean": mean, "std": std, "skewness": skewness, "kurtosis": kurtosis}


def run(
    table: Any,
    *,
    economy_column: str,
    economies: tuple[str, ...] = PAPER_ECONOMIES,
    features: tuple[str, ...] = PAPER_FEATURES,
    outcomes: tuple[str, ...] = PAPER_OUTCOMES,
    sample_size: int = 1200,
    repeats: int = 16,
    seed: int = 0,
    learning_rate: float = 0.05,
    max_epochs: int = 10_000,
    tolerance: float = 1e-3,
) -> dict[str, Any]:
    if sample_size <= 0 or repeats <= 0:
        raise ValueError("sample_size and repeats must be positive")
    results: list[dict[str, Any]] = []
    parameter_vectors: dict[str, list[np.ndarray]] = {}
    for economy_index, economy in enumerate(economies):
        subset = table[table[economy_column] == economy]
        for outcome_index, outcome in enumerate(outcomes):
            mapping = PISAMapping(
                feature_names=features,
                target_name=outcome,
                metadata={"protocol": "paper", "economy": economy},
            )
            prepared = mapping.prepare(subset)
            if len(prepared.X) < sample_size:
                raise ValueError(f"{economy}/{outcome} has fewer than {sample_size} complete rows")
            for repeat in range(1, repeats + 1):
                repeat_seed = seed + economy_index * 10_000 + outcome_index * 100 + repeat
                indices = np.random.default_rng(repeat_seed).choice(
                    len(prepared.X), size=sample_size, replace=False
                )
                model = LearningModel(
                    DataConfig(
                        feature_names=features,
                        target_name=outcome,
                        threshold_method="paper_std",
                        missing_strategy="error",
                        metadata={
                            "assessment_cycle": "PISA 2018",
                            "protocol": "A Neural Network Model for Learning - Application to PISA 2018 Data",
                            "economy": economy,
                            "sample_size": sample_size,
                            "repeat": repeat,
                        },
                    ),
                    calculation="exact",
                    max_exact_nodes=len(features) + 1,
                    learning_rate=learning_rate,
                    max_epochs=max_epochs,
                    tolerance=tolerance,
                    seed=repeat_seed,
                )
                fit = model.fit(prepared.X[indices], prepared.y[indices], method="kl")
                assert model.h is not None and model.J is not None
                observed, modeled = _moments(fit)
                comparison = compare_moment_orders(
                    observed,
                    modeled,
                    tolerances={order: tolerance for order in range(1, 5)},
                )
                results.append({
                    "economy": economy,
                    "outcome": outcome,
                    "repeat": repeat,
                    "seed": repeat_seed,
                    "sample_size": sample_size,
                    "threshold_method": "paper_std",
                    "training_method": "kl",
                    "calculation": fit.diagnostics.get("calculation"),
                    "converged": fit.converged,
                    "epochs": fit.epochs,
                    "mean_error": fit.mean_error,
                    "pairwise_error": fit.correlation_error,
                    "moment_pearson_r": {
                        str(order): _pearson(observed[order], modeled[order])
                        for order in range(1, 5)
                    },
                    "observed_moments": {str(order): observed[order] for order in range(1, 5)},
                    "modeled_moments": {str(order): modeled[order] for order in range(1, 5)},
                    "moment_comparison": comparison.to_dict(),
                    "h": model.h.detach().cpu().numpy().tolist(),
                    "J": model.J.detach().cpu().numpy().tolist(),
                    "J_statistics": _j_statistics(model.J.detach().cpu().numpy()),
                    "warnings": fit.warnings,
                })
                parameter_vectors.setdefault(f"{economy}/{outcome}", []).append(
                    np.concatenate([
                        model.h.detach().cpu().numpy(),
                        model.J.detach().cpu().numpy()[np.triu_indices(len(features) + 1, k=1)],
                    ])
                )

    repeat_correlations: dict[str, float | None] = {}
    for economy in economies:
        for outcome in outcomes:
            vectors = parameter_vectors.get(f"{economy}/{outcome}", [])
            correlations = []
            for left in range(len(vectors)):
                for right in range(left + 1, len(vectors)):
                    if np.std(vectors[left]) and np.std(vectors[right]):
                        correlations.append(float(np.corrcoef(vectors[left], vectors[right])[0, 1]))
            repeat_correlations[f"{economy}/{outcome}"] = (
                float(np.mean(correlations)) if correlations else None
            )
    return {
        "provenance": {
            "assessment_cycle": "PISA 2018",
            "economies": list(economies),
            "outcomes": list(outcomes),
            "feature_names": list(features),
            "respondent_level": "student",
            "source_rows_are_local_only": True,
        },
        "protocol": {
            "sample_size": sample_size,
            "repeats": repeats,
            "threshold_method": "paper_std",
            "strict_threshold": "f > population standard deviation",
            "training_method": "kl",
            "calculation": "exact",
            "learning_rate": learning_rate,
            "max_epochs": max_epochs,
            "tolerance": tolerance,
        },
        "results": results,
        "repeat_parameter_correlations": repeat_correlations,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the paper-aligned PISA 2018 reproduction protocol.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--economy-column", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--sample-size", type=int, default=1200)
    parser.add_argument("--repeats", type=int, default=16)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--learning-rate", type=float, default=0.05)
    parser.add_argument("--max-epochs", type=int, default=10_000)
    parser.add_argument("--tolerance", type=float, default=1e-3)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = run(
        read_pisa_file(args.input),
        economy_column=args.economy_column,
        sample_size=args.sample_size,
        repeats=args.repeats,
        seed=args.seed,
        learning_rate=args.learning_rate,
        max_epochs=args.max_epochs,
        tolerance=args.tolerance,
    )
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
