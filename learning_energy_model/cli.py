"""Command-line entry points for local CSV workflows."""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import TextIO

import numpy as np

from .config import DataConfig
from .data import prepare_tabular_data, validate_tabular_data
from .model import LearningModel


def _read_csv(path: str) -> dict[str, list[float]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV must contain a header row")
        columns: dict[str, list[float]] = {name: [] for name in reader.fieldnames}
        for row_number, row in enumerate(reader, start=2):
            for name, values in columns.items():
                value = row.get(name, "")
                try:
                    values.append(float(value) if value not in {None, ""} else np.nan)
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"CSV value in column {name!r}, row {row_number} is not numeric") from exc
    return columns


def _parse_features(value: str) -> tuple[str, ...]:
    names = tuple(name.strip() for name in value.split(",") if name.strip())
    if not names:
        raise ValueError("--features must contain at least one comma-separated column")
    return names


def _fit(args: argparse.Namespace) -> int:
    table = _read_csv(args.input)
    feature_names = _parse_features(args.features)
    quality = validate_tabular_data(
        table,
        feature_names=feature_names,
        target_name=args.target,
        weight_name=args.weight,
    )
    if not quality.passed:
        raise ValueError("input quality checks failed: " + "; ".join(quality.issues))
    prepared = prepare_tabular_data(
        table,
        feature_names=feature_names,
        target_name=args.target,
        weight_name=args.weight,
    )
    config = DataConfig(
        feature_names=prepared.feature_names,
        target_name=prepared.target_name,
        missing_strategy=args.missing_strategy,
        metadata={"input": str(args.input), "interface": "cli"},
    )
    model = LearningModel(
        config,
        learning_rate=args.learning_rate,
        max_epochs=args.max_epochs,
        min_epochs=args.min_epochs,
        max_exact_nodes=args.max_exact_nodes,
        seed=args.seed,
    )
    result = model.fit(
        prepared.X,
        prepared.y,
        sample_weight=prepared.sample_weight,
        method=args.method,
    )
    model.save(args.output)
    print(
        json.dumps(
            {"model_path": str(args.output), "quality": quality.to_dict(), "fit": result.to_dict()},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _write_predictions(predictions: np.ndarray, output: str, stream: TextIO) -> None:
    rows: list[list[str]] = [["probability_0", "probability_1", "prediction"]]
    rows.extend(
        [[f"{1.0 - p:.12g}", f"{p:.12g}", str(int(p >= 0.5))] for p in predictions]
    )
    if output == "-":
        writer = csv.writer(stream)
        writer.writerows(rows)
    else:
        with Path(output).open("w", newline="", encoding="utf-8") as handle:
            csv.writer(handle).writerows(rows)


def _predict(args: argparse.Namespace) -> int:
    model = LearningModel.load(args.model)
    table = _read_csv(args.input)
    features = np.column_stack([table[name] for name in model.preprocessor.feature_names])
    predictions = model.predict(features).probabilities
    _write_predictions(predictions, args.output, sys.stdout)
    return 0


def _analyze(args: argparse.Namespace) -> int:
    model = LearningModel.load(args.model)
    print(json.dumps(model.analyze().to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train and call an interpretable learning energy model.")
    commands = parser.add_subparsers(dest="command", required=True)
    fit = commands.add_parser("fit", help="fit a model from a numeric CSV")
    fit.add_argument("--input", required=True, help="input CSV path")
    fit.add_argument("--features", required=True, help="comma-separated feature columns")
    fit.add_argument("--target", required=True, help="target column")
    fit.add_argument("--weight", help="optional ordinary row-weight column")
    fit.add_argument("--output", required=True, help="model artifact path")
    fit.add_argument("--method", choices=("moment_matching", "kl"), default="moment_matching")
    fit.add_argument("--missing-strategy", choices=("error", "median"), default="error")
    fit.add_argument("--learning-rate", type=float, default=0.05)
    fit.add_argument("--max-epochs", type=int, default=2_000)
    fit.add_argument("--min-epochs", type=int, default=25)
    fit.add_argument("--max-exact-nodes", type=int, default=20)
    fit.add_argument("--seed", type=int, default=0)
    fit.set_defaults(handler=_fit)
    predict = commands.add_parser("predict", help="predict from a saved model and numeric CSV")
    predict.add_argument("--model", required=True, help="saved model artifact path")
    predict.add_argument("--input", required=True, help="input CSV with fitted feature columns")
    predict.add_argument("--output", default="-", help="prediction CSV path, or - for stdout")
    predict.set_defaults(handler=_predict)
    analyze = commands.add_parser("analyze", help="export an aggregate interpretability report")
    analyze.add_argument("--model", required=True, help="saved model artifact path")
    analyze.set_defaults(handler=_analyze)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.handler(args))
