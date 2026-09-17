"""Recreate the paper-style Figures 3--12 from a local reproduction report.

The script consumes only the aggregate JSON report. It does not read raw PISA
rows and writes figures to a caller-selected local directory.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

from learning_energy_model import LearningModel

ECONOMIES = ("TAP", "HKG", "DEU", "USA", "GBR")
OUTCOMES = ("PV1MATH", "PV1SCIE", "PV1READ")
ECONOMY_LABELS = {"TAP": "tw", "HKG": "hk", "DEU": "gm", "USA": "usa", "GBR": "uk"}
OUTCOME_LABELS = {"PV1MATH": "Math", "PV1SCIE": "Science", "PV1READ": "Reading"}
ECONOMY_COLORS = {
    "TAP": "#2f80c0",
    "HKG": "#f2994a",
    "DEU": "#43a047",
    "USA": "#e53935",
    "GBR": "#8e6bbf",
}


def _pearson(x: list[float], y: list[float]) -> float:
    left = np.asarray(x, dtype=float)
    right = np.asarray(y, dtype=float)
    if left.size < 2 or np.std(left) == 0 or np.std(right) == 0:
        return float("nan")
    return float(np.corrcoef(left, right)[0, 1])


def _group_rows(report: dict[str, Any]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in report["results"]:
        groups[(row["economy"], row["outcome"])].append(row)
    return groups


def _save(fig: Any, output_dir: Path, number: int, title: str) -> Path:
    import matplotlib.pyplot as plt

    path = output_dir / f"figure-{number:02d}-{title}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def export_paper_figures(report: dict[str, Any], output_dir: str | Path) -> list[Path]:
    """Export Figures 3--12 from a completed reproduction report."""
    import matplotlib.pyplot as plt

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    groups = _group_rows(report)
    outputs: list[Path] = []

    # Figure 3: first- and second-order observed-versus-model moments.
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    for axis, order, label in zip(axes, ("1", "2"), ("Single node", "Pairwise")):
        all_values: list[float] = []
        for economy in ECONOMIES:
            observed: list[float] = []
            modeled: list[float] = []
            for outcome in OUTCOMES:
                for row in groups[(economy, outcome)]:
                    observed_moments = np.asarray(row["observed_moments"][order], dtype=float)
                    modeled_moments = np.asarray(row["modeled_moments"][order], dtype=float)
                    if order == "2":
                        indices = np.triu_indices_from(observed_moments, k=1)
                        observed.extend(observed_moments[indices].tolist())
                        modeled.extend(modeled_moments[indices].tolist())
                    else:
                        observed.extend(observed_moments.tolist())
                        modeled.extend(modeled_moments.tolist())
            all_values.extend(observed)
            all_values.extend(modeled)
            axis.scatter(
                observed,
                modeled,
                s=5,
                alpha=0.28,
                color=ECONOMY_COLORS[economy],
                edgecolors="none",
                label=ECONOMY_LABELS[economy],
            )
            axis.text(
                0.04,
                0.92 - 0.06 * ECONOMIES.index(economy),
                f"{ECONOMY_LABELS[economy]} r={_pearson(observed, modeled):.3f}",
                color=ECONOMY_COLORS[economy],
                transform=axis.transAxes,
                fontsize=8,
            )
        limits = [0.0, max(all_values) * 1.02]
        axis.plot(limits, limits, color="#394b59", linewidth=1.2)
        axis.set(xlabel="Observed moment", ylabel="Model moment", title=label)
        axis.set_xlim(limits)
        axis.set_ylim(limits)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Figure 3: Observed versus model first- and second-order moments")
    outputs.append(_save(fig, destination, 3, "lower-order-correlations"))

    # Figure 4: pooled triple and quadruplet correlations, colored by economy.
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    for axis, order, label in zip(axes, ("3", "4"), ("Triple", "Quadruplet")):
        all_observed: list[float] = []
        all_modeled: list[float] = []
        for economy in ECONOMIES:
            observed_higher: list[float] = []
            modeled_higher: list[float] = []
            for outcome in OUTCOMES:
                for row in groups[(economy, outcome)]:
                    observed_higher.extend(row["observed_moments"][order].values())
                    modeled_higher.extend(row["modeled_moments"][order].values())
            all_observed.extend(observed_higher)
            all_modeled.extend(modeled_higher)
            axis.scatter(
                observed_higher,
                modeled_higher,
                s=5,
                alpha=0.28,
                color=ECONOMY_COLORS[economy],
                edgecolors="none",
                label=ECONOMY_LABELS[economy],
            )
        limits = [0.0, max(all_observed + all_modeled) * 1.02]
        axis.plot(limits, limits, color="#394b59", linewidth=1.2)
        axis.set(xlabel="Observed correlation", ylabel="Model correlation", title=label)
        axis.text(0.04, 0.92, f"r = {_pearson(all_observed, all_modeled):.3f}", transform=axis.transAxes)
        axis.set_xlim(limits)
        axis.set_ylim(limits)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Figure 4: Observed versus model triple and quadruplet correlations")
    outputs.append(_save(fig, destination, 4, "higher-order-correlations"))

    # Figure 5: one panel per outcome, overlaying the five economies.
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
    for axis, outcome in zip(axes, OUTCOMES):
        for economy in ECONOMIES:
            values: list[float] = []
            for row in groups[(economy, outcome)]:
                matrix = np.asarray(row["J"], dtype=float)
                values.extend(matrix[np.triu_indices_from(matrix, k=1)].tolist())
            axis.hist(values, bins=35, density=True, histtype="step", linewidth=1.4,
                      color=ECONOMY_COLORS[economy], label=ECONOMY_LABELS[economy])
        axis.set_xlim(-0.4, 1.0)
        axis.set_title(OUTCOME_LABELS[outcome])
        axis.set_xlabel("Jij")
        axis.legend(frameon=False, fontsize=8)
    axes[0].set_ylabel("Density")
    fig.suptitle("Figure 5: Jij distributions across five economies")
    outputs.append(_save(fig, destination, 5, "Jij-distributions"))

    # Figures 6--10: one economy per figure, three outcome curves.
    for number, economy in zip(range(6, 11), ECONOMIES):
        fig, axis = plt.subplots(figsize=(9, 4.8))
        for outcome in OUTCOMES:
            rows = groups[(economy, outcome)]
            names = list(rows[0]["effective_interactions"]["values"])
            effective_matrix = np.asarray(
                [[r["effective_interactions"]["values"][name] for name in names] for r in rows]
            )
            axis.plot(np.arange(len(names)), effective_matrix.mean(axis=0), marker="o", markersize=2.5,
                      linewidth=1.3, label=OUTCOME_LABELS[outcome])
        all_effective_values = np.asarray([
            value
            for outcome in OUTCOMES
            for row in groups[(economy, outcome)]
            for value in row["effective_interactions"]["values"].values()
        ])
        mean = float(all_effective_values.mean())
        std = float(all_effective_values.std(ddof=0))
        axis.axhline(mean, color="#394b59", linewidth=1.0)
        axis.axhline(mean - std, color="#e47945", linestyle="--", linewidth=1.0)
        axis.axhline(mean + std, color="#e47945", linestyle="--", linewidth=1.0)
        axis.set_xticks(np.arange(len(names)), [str(i) for i in range(len(names))])
        axis.set(xlabel="Frozen node i", ylabel="epsilon_outcome", title=f"Figure {number}: {economy}")
        axis.legend(frameon=False)
        outputs.append(_save(fig, destination, number, f"effective-interactions-{economy}"))

    # Figure 11: response from the selected model artifact for each group.
    # Recompute over the full temperature range; the aggregate report only
    # stores the original narrow scan used by the first reproduction run.
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharex=True)
    model_dir = Path(report.get("model_artifact_directory", destination.parent / "pisa2018-paper-reproduction-models"))
    temperatures = np.linspace(0.05, 4.0, 161)
    for economy in ECONOMIES:
        label = ECONOMY_LABELS[economy]
        responses = []
        for outcome in OUTCOMES:
            model_path = model_dir / f"{economy}-{outcome}.pt"
            model = LearningModel.load(model_path)
            responses.append(model.temperature_response(temperatures))
        energy = np.asarray([response["d_mean_energy_d_temperature"] for response in responses]).mean(axis=0)
        magnetization = np.asarray(
            [response["d_mean_magnetization_d_temperature"] for response in responses]
        ).mean(axis=0)
        axes[0].plot(temperatures, energy, linewidth=1.4, label=label)
        axes[1].plot(temperatures, magnetization, linewidth=1.4, label=label)
    for axis, title, ylabel in zip(axes, ("Specific heat", "Magnetization response"), ("d<E>/dT", "dm/dT")):
        axis.axvline(1.0, color="#394b59", linestyle=":", linewidth=1.0)
        axis.set_xlim(0.0, 4.0)
        axis.set(xlabel="Temperature T", ylabel=ylabel, title=title)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Figure 11: Critical-state responses across five economies")
    outputs.append(_save(fig, destination, 11, "critical-state-responses"))

    # Figure 12: threshold sensitivity, averaged over the three outcomes.
    fig, axis = plt.subplots(figsize=(7.5, 5))
    for economy in ECONOMIES:
        curves = [report["protocol_diagnostics"][f"{economy}/{outcome}"]["threshold_sensitivity"] for outcome in OUTCOMES]
        thresholds = np.asarray(curves[0]["thresholds"], dtype=float)
        correlations = np.asarray([c["correlations"] for c in curves]).mean(axis=0)
        axis.plot(thresholds, correlations, linewidth=1.4, label=ECONOMY_LABELS[economy])
    axis.set(xlabel="Threshold theta", ylabel="Pearson correlation rho", title="Figure A.12: Threshold sensitivity")
    axis.legend(frameon=False)
    axis.set_ylim(0.15, 1.03)
    outputs.append(_save(fig, destination, 12, "threshold-sensitivity"))
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Export paper-style Figures 3--12.")
    parser.add_argument("--report", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    paths = export_paper_figures(report, args.output_dir)
    print(f"exported {len(paths)} figures to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
