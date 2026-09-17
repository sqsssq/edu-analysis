"""Validate a completed local PISA paper-reproduction report and artifacts."""

import argparse
import json
from pathlib import Path
from typing import Any, cast

from learning_energy_model import LearningModel

ECONOMIES = ("TAP", "HKG", "DEU", "USA", "GBR")
OUTCOMES = ("PV1MATH", "PV1SCIE", "PV1READ")


def _check_diagnostic(diagnostic: dict[str, Any]) -> bool:
    return (
        float(diagnostic["max_rhat"]) <= 1.1
        and float(diagnostic["min_effective_sample_size"]) >= 100.0
        and float(diagnostic["max_mcse"]) <= 0.05
    )


def validate(report_path: str | Path, model_dir: str | Path, figure_dir: str | Path) -> dict[str, Any]:
    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    results = report["results"]
    rows_by_group: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in results:
        rows_by_group.setdefault((row["economy"], row["outcome"]), []).append(row)

    moment_checks: dict[str, dict[str, int]] = {}
    for order in ("1", "2", "3", "4"):
        order_passes = [
            float(row["moment_comparison"]["max_absolute_error"][order])
            <= float(row["moment_comparison"]["tolerances"][order])
            for row in results
            if order in row["moment_comparison"]["max_absolute_error"]
        ]
        moment_checks[order] = {
            "passed": sum(bool(value) for value in order_passes),
            "total": len(order_passes),
        }

    model_path = Path(model_dir)
    model_files = sorted(model_path.glob("*.pt"))
    figure_files = sorted(Path(figure_dir).glob("figure-*.png"))
    selection_checks = []
    normalization_checks = []
    mc_checks = []
    effective_lengths = []
    target_prevalences = []
    for economy in ECONOMIES:
        for outcome in OUTCOMES:
            rows = rows_by_group[(economy, outcome)]
            path = model_path / f"{economy}-{outcome}.pt"
            model = LearningModel.load(path)
            selection = cast(dict[str, Any], model.artifact_metadata["reproduction_selection"])
            selected_row = next(row for row in rows if row["repeat"] == selection["repeat"])
            selection_checks.append(selected_row["repeat"] == selection["repeat"])
            normalization_checks.append(model.config.normalization == "zscore")
            fit_result = model.fit_result
            assert fit_result is not None and fit_result.observed_means is not None
            target_prevalences.append(float(fit_result.observed_means[-1]))
            interaction = cast(dict[str, Any], selected_row["effective_interaction_diagnostics"])
            effective_lengths.append(len(interaction["values"]))
            mc_checks.append(_check_diagnostic(interaction["baseline_diagnostics"]))
            mc_checks.extend(_check_diagnostic(item) for item in interaction["clamp_diagnostics"].values())

    convergence = sum(bool(row["converged"]) for row in results)
    checks = {
        "report_rows": len(results) == 240,
        "groups": len(rows_by_group) == 15 and all(len(rows) == 16 for rows in rows_by_group.values()),
        "model_files": len(model_files) == 15,
        "figure_files": len(figure_files) == 9,
        "selection_metadata": all(selection_checks),
        "zscore_normalization": all(normalization_checks),
        "non_degenerate_targets": all(0.0 < value < 1.0 for value in target_prevalences),
        "converged_runs": convergence == 240,
        "effective_interaction_lengths": all(value == 18 for value in effective_lengths),
        "monte_carlo_diagnostics": all(mc_checks),
    }
    result = {
        "report": str(report_path),
        "models": str(model_dir),
        "figures": str(figure_dir),
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "converged_runs": {"passed": convergence, "total": len(results)},
        "moment_checks": moment_checks,
        "target_prevalence_range": [min(target_prevalences), max(target_prevalences)],
        "monte_carlo_diagnostic_checks": {"passed": sum(mc_checks), "total": len(mc_checks)},
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--figure-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = validate(args.report, args.model_dir, args.figure_dir)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
