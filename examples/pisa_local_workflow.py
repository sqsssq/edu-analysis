"""Run the local, codebook-backed PISA preparation and fitting workflow."""

import argparse
import json
from pathlib import Path

from learning_energy_model import (
    DataConfig,
    LearningModel,
    PISAMapping,
    prepare_pisa_file,
    validate_tabular_data,
)


def _parse_names(value: str) -> tuple[str, ...]:
    names = tuple(item.strip() for item in value.split(",") if item.strip())
    if not names:
        raise ValueError("--features must contain at least one column")
    return names


def _parse_missing_values(value: str) -> tuple[float, ...]:
    if not value:
        return ()
    return tuple(float(item.strip()) for item in value.split(",") if item.strip())


def run(args: argparse.Namespace) -> None:
    features = _parse_names(args.features)
    mapping = PISAMapping(
        feature_names=features,
        target_name=args.target,
        weight_name=args.weight,
        missing_values=_parse_missing_values(args.missing_values),
    )
    prepared = prepare_pisa_file(args.input, mapping)
    mapped_table = {name: prepared.X[:, index] for index, name in enumerate(features)}
    mapped_table[args.target] = prepared.y
    if prepared.sample_weight is not None and args.weight is not None:
        mapped_table[args.weight] = prepared.sample_weight
    quality = validate_tabular_data(
        mapped_table,
        feature_names=features,
        target_name=args.target,
        weight_name=args.weight,
    )
    if not quality.passed:
        raise ValueError("mapped input quality checks failed: " + "; ".join(quality.issues))
    model = LearningModel(
        DataConfig(
            feature_names=prepared.feature_names,
            target_name=prepared.target_name,
            missing_strategy=args.missing_strategy,
            metadata={"interface": "pisa-local-workflow", "input": str(args.input)},
        ),
        max_epochs=args.max_epochs,
        min_epochs=args.min_epochs,
        max_exact_nodes=args.max_exact_nodes,
        seed=args.seed,
    )
    fit = model.fit(prepared.X, prepared.y, sample_weight=prepared.sample_weight)
    analysis = model.analyze()
    model.save(args.output_model)
    report = {
        "quality": quality.to_dict(),
        "fit": fit.to_dict(),
        "analysis": analysis.to_dict(),
    }
    Path(args.output_report).write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fit the model on a local mapped PISA file.")
    parser.add_argument("--input", required=True, help="local CSV/SAS/SPSS file or single-data-file ZIP")
    parser.add_argument("--features", required=True, help="comma-separated codebook variable names")
    parser.add_argument("--target", required=True, help="codebook target variable name")
    parser.add_argument("--weight", help="ordinary row-weight variable name")
    parser.add_argument("--missing-values", default="", help="comma-separated codebook missing codes")
    parser.add_argument("--output-model", required=True, help="local model artifact path")
    parser.add_argument("--output-report", required=True, help="aggregate JSON report path")
    parser.add_argument("--missing-strategy", choices=("error", "median"), default="median")
    parser.add_argument("--max-epochs", type=int, default=2_000)
    parser.add_argument("--min-epochs", type=int, default=25)
    parser.add_argument("--max-exact-nodes", type=int, default=20)
    parser.add_argument("--seed", type=int, default=0)
    return parser


def main() -> int:
    run(build_parser().parse_args())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
