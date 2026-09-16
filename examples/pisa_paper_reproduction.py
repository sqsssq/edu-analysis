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

from learning_energy_model import (
    DataConfig,
    LearningModel,
    PISAMapping,
    classify_effective_interactions,
    read_pisa_file,
    threshold_sensitivity,
)
from learning_energy_model.evaluation import compare_moment_orders

PAPER_FEATURES = (
    "HOMEPOS", "CULTPOSS", "HEDRES", "WEALTH", "ICTRES", "DISCLIMA",
    "TEACHSUP", "DIRINS", "PERFEED", "STIMREAD", "COMPETE", "WORKMAST",
    "EUDMO", "BEINGBULLIED", "ENTUSE", "SOIAICT", "ICTCLASS", "ICTOUTSIDE",
)
PAPER_OUTCOMES = ("PV1MATH", "PV1SCIE", "PV1READ")
PAPER_ECONOMIES = ("TAP", "HKG", "DEU", "USA", "GBR")


def _json_default(value: Any) -> Any:
    if hasattr(value, "tolist"):
        return value.tolist()
    raise TypeError(f"unsupported JSON value: {type(value).__name__}")


def _economy_subset(table: Any, economy_column: str, economy: str) -> Any:
    """Select an economy across SAS readers that return strings or bytes."""
    values = table[economy_column]
    normalized = values.map(
        lambda value: value.decode(errors="replace").strip()
        if isinstance(value, bytes)
        else str(value).strip()
    )
    return table[normalized == economy]


def _moments(fit: Any) -> tuple[dict[int, Any], dict[int, Any]]:
    observed: dict[int, Any] = {
        1: fit.observed_means,
        2: fit.observed_pairwise_moments,
    }
    modeled: dict[int, Any] = {
        1: fit.model_means,
        2: fit.model_pairwise_moments,
    }
    for order, separator_count in ((3, 2), (4, 3)):
        observed_values = {
            key: value
            for key, value in fit.observed_higher_order_moments.items()
            if key.count("×") == separator_count
        }
        modeled_values = {
            key: value
            for key, value in fit.model_higher_order_moments.items()
            if key.count("×") == separator_count
        }
        if observed_values or modeled_values:
            observed[order] = observed_values
            modeled[order] = modeled_values
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
    missing_values: tuple[float, ...] = (),
    seed: int = 0,
    learning_rate: float = 0.05,
    max_epochs: int = 10_000,
    tolerance: float = 1e-3,
    status_file: str | Path | None = None,
) -> dict[str, Any]:
    if sample_size <= 0 or repeats <= 0:
        raise ValueError("sample_size and repeats must be positive")
    results: list[dict[str, Any]] = []
    parameter_vectors: dict[str, list[np.ndarray]] = {}
    protocol_diagnostics: dict[str, Any] = {}
    total_runs = len(economies) * len(outcomes) * repeats
    status_path = Path(status_file) if status_file is not None else None
    if status_path is not None:
        status_path.parent.mkdir(parents=True, exist_ok=True)
        status_path.write_text(
            json.dumps(
                {"done": 0, "total": total_runs, "current": "starting", "status": "running"},
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    for economy_index, economy in enumerate(economies):
        subset = _economy_subset(table, economy_column, economy)
        if len(subset) == 0:
            raise ValueError(f"no rows found for economy {economy!r} in {economy_column!r}")
        for outcome_index, outcome in enumerate(outcomes):
            mapping = PISAMapping(
                feature_names=features,
                target_name=outcome,
                missing_values=missing_values,
                metadata={"protocol": "paper", "economy": economy},
            )
            prepared = mapping.prepare(subset)
            complete = np.isfinite(prepared.X).all(axis=1) & np.isfinite(prepared.y)
            X_complete, y_complete = prepared.X[complete], prepared.y[complete]
            if len(X_complete) < sample_size:
                raise ValueError(f"{economy}/{outcome} has fewer than {sample_size} complete rows")
            protocol_diagnostics[f"{economy}/{outcome}"] = {
                "complete_rows": len(X_complete),
                "threshold_sensitivity": threshold_sensitivity(
                    np.column_stack([X_complete, y_complete]),
                    np.linspace(-0.5, 0.5, 1_000).tolist(),
                ),
            }
            for repeat in range(1, repeats + 1):
                repeat_seed = seed + economy_index * 10_000 + outcome_index * 100 + repeat
                indices = np.random.default_rng(repeat_seed).choice(
                    len(X_complete), size=sample_size, replace=False
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
                fit = model.fit(X_complete[indices], y_complete[indices], method="kl")
                assert model.h is not None and model.J is not None
                observed, modeled = _moments(fit)
                moment_orders = sorted(observed)
                comparison = compare_moment_orders(
                    observed,
                    modeled,
                    tolerances={order: tolerance for order in moment_orders},
                )
                effective = model.effective_interactions()
                temperature_response = model.temperature_response(np.linspace(0.5, 1.5, 101))
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
                        for order in moment_orders
                    },
                    "observed_moments": {str(order): observed[order] for order in moment_orders},
                    "modeled_moments": {str(order): modeled[order] for order in moment_orders},
                    "moment_comparison": comparison.to_dict(),
                    "effective_interactions": classify_effective_interactions(effective),
                    "temperature_response": temperature_response,
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
                if status_path is not None:
                    status_path.write_text(
                        json.dumps(
                            {
                                "done": len(results),
                                "total": total_runs,
                                "current": f"{economy}/{outcome}/repeat-{repeat}",
                                "converged": fit.converged,
                                "status": "running",
                            },
                            indent=2,
                        )
                        + "\n",
                        encoding="utf-8",
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
    if status_path is not None:
        status_path.write_text(
            json.dumps(
                {"done": total_runs, "total": total_runs, "current": "finished", "status": "finished"},
                indent=2,
            )
            + "\n",
            encoding="utf-8",
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
        "protocol_diagnostics": protocol_diagnostics,
        "repeat_parameter_correlations": repeat_correlations,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the paper-aligned PISA 2018 reproduction protocol.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--economy-column", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--sample-size", type=int, default=1200)
    parser.add_argument("--repeats", type=int, default=16)
    parser.add_argument(
        "--missing-values",
        default="",
        help="comma-separated source missing codes reviewed against the OECD codebook",
    )
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--learning-rate", type=float, default=0.05)
    parser.add_argument("--max-epochs", type=int, default=10_000)
    parser.add_argument("--tolerance", type=float, default=1e-3)
    parser.add_argument("--status-file", help="write aggregate progress JSON while running")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = run(
            read_pisa_file(args.input),
            economy_column=args.economy_column,
            sample_size=args.sample_size,
            repeats=args.repeats,
            missing_values=tuple(
                float(item) for item in args.missing_values.split(",") if item.strip()
            ),
            seed=args.seed,
            learning_rate=args.learning_rate,
            max_epochs=args.max_epochs,
            tolerance=args.tolerance,
            status_file=args.status_file,
        )
    except Exception as exc:
        if args.status_file:
            Path(args.status_file).write_text(
                json.dumps(
                    {
                        "done": 0,
                        "total": 240,
                        "current": "failed",
                        "status": "failed",
                        "message": str(exc),
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        raise
    Path(args.output).write_text(
        json.dumps(report, ensure_ascii=False, indent=2, default=_json_default),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
