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
    if args.mapping:
        mapping = PISAMapping.load(args.mapping)
    else:
        if not args.features or not args.target:
            raise ValueError("--features and --target are required when --mapping is not used")
        mapping = PISAMapping(
            feature_names=_parse_names(args.features),
            target_name=args.target,
            weight_name=args.weight,
            missing_values=_parse_missing_values(args.missing_values),
            metadata={
                "cycle": args.cycle or "",
                "scope": args.scope or "",
                "codebook": args.codebook or "",
            },
        )
    features = mapping.feature_names
    target = mapping.target_name
    weight = mapping.weight_name
    cycle = args.cycle or str(mapping.metadata.get("cycle", ""))
    scope = args.scope or str(mapping.metadata.get("scope", ""))
    codebook = args.codebook or str(mapping.metadata.get("codebook", ""))
    if not cycle or not scope or not codebook:
        raise ValueError("cycle, scope, and codebook must be supplied or present in the mapping metadata")
    prepared = prepare_pisa_file(args.input, mapping)
    mapped_table = {name: prepared.X[:, index] for index, name in enumerate(features)}
    mapped_table[target] = prepared.y
    if prepared.sample_weight is not None and weight is not None:
        mapped_table[weight] = prepared.sample_weight
    quality = validate_tabular_data(
        mapped_table,
        feature_names=features,
        target_name=target,
        weight_name=weight,
    )
    if not quality.passed:
        raise ValueError("mapped input quality checks failed: " + "; ".join(quality.issues))
    model = LearningModel(
        DataConfig(
            feature_names=prepared.feature_names,
            target_name=prepared.target_name,
            sample_weight_name=weight,
            threshold_method=args.threshold_method,
            missing_strategy=args.missing_strategy,
            metadata={
                "interface": "pisa-local-workflow",
                "input": str(args.input),
                "mapping": str(args.mapping) if args.mapping else None,
                "assessment_cycle": cycle,
                "scope": scope,
                "codebook_reference": codebook,
            },
        ),
        max_epochs=args.max_epochs,
        min_epochs=args.min_epochs,
        max_exact_nodes=args.max_exact_nodes,
        calculation=args.calculation,
        mc_max_rhat=args.mc_max_rhat,
        mc_min_effective_sample_size=args.mc_min_effective_sample_size,
        mc_max_mcse=args.mc_max_mcse,
        seed=args.seed,
    )
    fit = model.fit(
        prepared.X,
        prepared.y,
        sample_weight=prepared.sample_weight,
        method=args.training_method,
    )
    analysis = model.analyze()
    model.save(args.output_model)
    report = {
        "quality": quality.to_dict(),
        "provenance": {
            "assessment_cycle": cycle,
            "scope": scope,
            "codebook_reference": codebook,
            "mapping": mapping.to_dict(),
        },
        "reproduction_protocol": {
            "threshold_method": args.threshold_method,
            "training_method": args.training_method,
            "calculation": args.calculation,
            "sample_size": prepared.X.shape[0],
            "seed": args.seed,
        },
        "fit": fit.to_dict(),
        "analysis": analysis.to_dict(),
    }
    Path(args.output_report).write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fit the model on a local mapped PISA file.")
    parser.add_argument("--input", required=True, help="local CSV/SAS/SPSS file or single-data-file ZIP")
    parser.add_argument("--mapping", help="reviewed PISAMapping JSON contract")
    parser.add_argument("--features", help="comma-separated codebook variable names")
    parser.add_argument("--target", help="codebook target variable name")
    parser.add_argument("--weight", help="ordinary row-weight variable name")
    parser.add_argument("--missing-values", default="", help="comma-separated codebook missing codes")
    parser.add_argument("--cycle", help="assessment cycle, e.g. PISA 2018 or PISA 2022")
    parser.add_argument("--scope", help="country/economy or multi-country scope")
    parser.add_argument("--codebook", help="local codebook reference or version")
    parser.add_argument("--output-model", required=True, help="local model artifact path")
    parser.add_argument("--output-report", required=True, help="aggregate JSON report path")
    parser.add_argument("--missing-strategy", choices=("error", "median", "mean", "zero"), default="median")
    parser.add_argument(
        "--threshold-method",
        choices=("median", "quantile", "paper_std"),
        default="median",
        help="binary threshold rule; paper_std reproduces the paper's f > std rule",
    )
    parser.add_argument(
        "--training-method",
        choices=("moment_matching", "kl"),
        default="moment_matching",
        help="training objective; kl reproduces the paper's explicit KL-gradient path",
    )
    parser.add_argument("--max-epochs", type=int, default=2_000)
    parser.add_argument("--min-epochs", type=int, default=25)
    parser.add_argument("--max-exact-nodes", type=int, default=20)
    parser.add_argument("--calculation", choices=("auto", "exact", "monte_carlo"), default="auto")
    parser.add_argument("--mc-max-rhat", type=float, default=1.1)
    parser.add_argument("--mc-min-effective-sample-size", type=float, default=100.0)
    parser.add_argument("--mc-max-mcse", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=0)
    return parser


def main() -> int:
    run(build_parser().parse_args())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
