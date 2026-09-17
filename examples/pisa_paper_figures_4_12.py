"""Recreate the paper-style Figures 3--11 from a local reproduction report.

The script consumes only the aggregate JSON report. It does not read raw PISA
rows and writes figures to a caller-selected local directory.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, cast

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


def _selected_row(
    groups: dict[tuple[str, str], list[dict[str, Any]]],
    model_dir: Path,
    economy: str,
    outcome: str,
) -> dict[str, Any]:
    model = LearningModel.load(model_dir / f"{economy}-{outcome}.pt")
    selection = cast(dict[str, Any], model.artifact_metadata["reproduction_selection"])
    repeat = int(selection["repeat"])
    return next(row for row in groups[(economy, outcome)] if row["repeat"] == repeat)


def _save(fig: Any, output_dir: Path, number: int, title: str) -> Path:
    import matplotlib.pyplot as plt

    path = output_dir / f"figure-{number:02d}-{title}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def export_paper_figures(report: dict[str, Any], output_dir: str | Path) -> list[Path]:
    """Export Figures 3--11 from a completed reproduction report."""
    import matplotlib.pyplot as plt

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    groups = _group_rows(report)
    outputs: list[Path] = []

    # Figures 3 and 4 use the paper's selected fit per economy/outcome and
    # display a separate correlation coefficient for each economy.
    model_dir = Path(report.get("model_artifact_directory", destination.parent / "pisa2018-paper-reproduction-models"))

    # Figure 3: magnetization and pairwise products.
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    for axis, order, title in zip(axes, ("1", "2"), ("A  magnetization", "B  pair product")):
        all_values: list[float] = []
        economy_correlations: list[float] = []
        for economy in ECONOMIES:
            observed: list[float] = []
            modeled: list[float] = []
            for outcome in OUTCOMES:
                row = _selected_row(groups, model_dir, economy, outcome)
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
            economy_correlations.append(_pearson(observed, modeled))
        limits = [0.0, max(all_values) * 1.02]
        axis.plot(limits, limits, color="#394b59", linewidth=1.2)
        axis.set(xlabel="data", ylabel="model", title=title)
        axis.set_xlim(limits)
        axis.set_ylim(limits)
        handles, labels = axis.get_legend_handles_labels()
        axis.legend(
            handles,
            [f"{label}   r={correlation:.4f}" for label, correlation in zip(labels, economy_correlations)],
            frameon=False,
            fontsize=8,
        )
    fig.suptitle("Figure 3: Comparison of observed and model-predicted moments")
    outputs.append(_save(fig, destination, 3, "lower-order-correlations"))

    # Figure 4: triple and quadruplet products, colored by economy.
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    for axis, order, label in zip(axes, ("3", "4"), ("Triple", "Quadruplet")):
        for economy in ECONOMIES:
            observed_higher: list[float] = []
            modeled_higher: list[float] = []
            for outcome in OUTCOMES:
                row = _selected_row(groups, model_dir, economy, outcome)
                observed_higher.extend(row["observed_moments"][order].values())
                modeled_higher.extend(row["modeled_moments"][order].values())
            axis.scatter(
                observed_higher,
                modeled_higher,
                s=5,
                alpha=0.28,
                color=ECONOMY_COLORS[economy],
                edgecolors="none",
                label=ECONOMY_LABELS[economy],
            )
        all_observed = [point.get_offsets().data[:, 0] for point in axis.collections]
        all_modeled = [point.get_offsets().data[:, 1] for point in axis.collections]
        observed_flat = np.concatenate(all_observed).tolist()
        modeled_flat = np.concatenate(all_modeled).tolist()
        limits = [0.0, max(observed_flat + modeled_flat) * 1.02]
        axis.plot(limits, limits, color="#394b59", linewidth=1.2)
        axis.set(xlabel="data", ylabel="model", title=f"{label} product")
        axis.set_xlim(limits)
        axis.set_ylim(limits)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Figure 4: Comparison of triple and quadruplet correlations")
    outputs.append(_save(fig, destination, 4, "higher-order-correlations"))

    # Figure 5: the paper's order is Math, Reading, Science, with distribution
    # statistics included in each economy legend entry.
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
    for axis, outcome in zip(axes, ("PV1MATH", "PV1READ", "PV1SCIE")):
        for economy in ECONOMIES:
            values: list[float] = []
            row = _selected_row(groups, model_dir, economy, outcome)
            matrix = np.asarray(row["J"], dtype=float)
            values.extend(matrix[np.triu_indices_from(matrix, k=1)].tolist())
            values_array = np.asarray(values, dtype=float)
            centered = values_array - values_array.mean()
            scale = float(values_array.std())
            skew = float((centered**3).mean() / scale**3) if scale else 0.0
            kurtosis = float((centered**4).mean() / scale**4 - 3.0) if scale else 0.0
            legend_label = (
                f"{ECONOMY_LABELS[economy]} "
                f"μ={values_array.mean():.3f} ({scale:.2f})\n"
                f"skw={skew:.2f}, kur={kurtosis:.2f}"
            )
            axis.hist(values, bins=35, density=True, histtype="step", linewidth=1.4,
                      color=ECONOMY_COLORS[economy], label=legend_label)
        axis.set_title(OUTCOME_LABELS[outcome])
        axis.set_xlabel("Jij")
        axis.legend(frameon=False, fontsize=8)
    axes[0].set_ylabel("Density")
    fig.suptitle("Figure 5: Jij distributions across five economies")
    outputs.append(_save(fig, destination, 5, "Jij-distributions"))

    # Figures 6--10: one economy per figure, one paper-style panel per outcome.
    # The paper uses one selected fitted model per economy/outcome and computes
    # the mean +/- SD benchmark separately within each outcome.
    model_dir = Path(report.get("model_artifact_directory", destination.parent / "pisa2018-paper-reproduction-models"))
    for number, economy in zip(range(6, 11), ECONOMIES):
        fig, axes = plt.subplots(1, 3, figsize=(12, 4.2), sharey=False)
        for axis, outcome in zip(axes, OUTCOMES):
            model_path = model_dir / f"{economy}-{outcome}.pt"
            model = LearningModel.load(model_path)
            selection = cast(dict[str, Any], model.artifact_metadata["reproduction_selection"])
            selected_repeat = int(selection["repeat"])
            row = next(
                item for item in groups[(economy, outcome)] if item["repeat"] == selected_repeat
            )
            interaction_report = cast(dict[str, Any], row["effective_interactions"])
            effective_values_array = np.asarray(
                list(cast(dict[str, float], interaction_report["values"]).values()), dtype=float
            )
            effective_mean = float(effective_values_array.mean())
            effective_std = float(effective_values_array.std(ddof=0))
            node_indices = np.arange(effective_values_array.size)
            axis.plot(node_indices, effective_values_array, color="#3d8dcc", linewidth=1.2)
            axis.axhline(effective_mean + effective_std, color="#ff7f0e", linewidth=1.0, label="mean+std of ε")
            axis.axhline(effective_mean - effective_std, color="#2ca02c", linewidth=1.0, label="mean-std of ε")
            axis.set_xticks(node_indices, [str(i) for i in node_indices])
            axis.set(xlabel="Frozen node i", ylabel="ε", title=f"{ECONOMY_LABELS[economy]} {OUTCOME_LABELS[outcome]}")
            axis.legend(frameon=False, fontsize=7, loc="best")
        fig.suptitle(f"Figure {number}: ε̄_outcome versus frozen node i in {economy}")
        outputs.append(_save(fig, destination, number, f"effective-interactions-{economy}"))

    # Figure 11: response from the selected model artifact for each group.
    # Recompute over the full temperature range; the aggregate report only
    # stores the original narrow scan used by the first reproduction run.
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharex=True)
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

    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Export paper-style Figures 3--11.")
    parser.add_argument("--report", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    paths = export_paper_figures(report, args.output_dir)
    print(f"exported {len(paths)} figures to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
