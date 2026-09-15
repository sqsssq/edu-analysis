"""Run a deterministic synthetic parameter-recovery benchmark."""

import argparse
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np

from learning_energy_model import DataConfig, LearningModel, compare_moment_orders


def run(output: str | Path | None = None) -> dict[str, Any]:
    """Fit a known three-node distribution and return an aggregate report."""
    true_h = np.array([-0.35, 0.2, 0.45])
    true_J = np.array(
        [[0.0, -0.3, 0.15], [-0.3, 0.0, 0.25], [0.15, 0.25, 0.0]]
    )
    states = np.asarray(list(itertools.product((0.0, 1.0), repeat=3)))
    energies = states @ true_h + 0.5 * ((states @ true_J) * states).sum(axis=1)
    probabilities = np.exp(-energies - np.max(-energies))
    probabilities /= probabilities.sum()
    counts = np.maximum(np.rint(probabilities * 2_000_000).astype(int), 1)
    observations = np.repeat(states, counts, axis=0)

    model = LearningModel(
        DataConfig(feature_names=("x0", "x1"), target_name="target"),
        calculation="exact",
        learning_rate=0.08,
        max_epochs=1_500,
        min_epochs=25,
        tolerance=0.0005,
        seed=2,
    )
    fit = model.fit(observations[:, :2], observations[:, 2])
    analysis = model.analyze()
    comparison = compare_moment_orders(
        {1: fit.observed_means, 2: fit.observed_pairwise_moments, 3: fit.observed_higher_order_moments},
        {1: fit.model_means, 2: fit.model_pairwise_moments, 3: fit.model_higher_order_moments},
        tolerances={1: 0.01, 2: 0.01, 3: 0.01},
    )
    report = {
        "benchmark": "synthetic_exact_parameter_recovery",
        "n_samples": int(observations.shape[0]),
        "nodes": ["x0", "x1", "target"],
        "calculation": fit.diagnostics,
        "fit": fit.to_dict(),
        "moment_comparison": comparison.to_dict(),
        "parameter_error": {
            "max_abs_h": float(np.max(np.abs(analysis.h - true_h))),
            "max_abs_J": float(np.max(np.abs(analysis.J - true_J))),
        },
    }
    if output is None:
        return report
    Path(output).write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="aggregate JSON output path; stdout when omitted")
    args = parser.parse_args()
    report = run(args.output)
    if args.output is None:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
