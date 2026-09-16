"""Export paper-style figures from a JSON report produced by the runner."""

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


def export_figures(report: dict[str, Any], output_dir: str | Path) -> list[Path]:
    """Write aggregate PNG figures without reading or retaining raw PISA rows."""
    import matplotlib.pyplot as plt

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    results = report.get("results", [])
    first_by_group: dict[str, dict[str, Any]] = {}
    for row in results:
        key = f"{row['economy']}_{row['outcome']}"
        first_by_group.setdefault(key, row)

    for key, row in first_by_group.items():
        effective = row["effective_interactions"]
        names = list(effective["values"])
        values = np.asarray(list(effective["values"].values()), dtype=float)
        fig, ax = plt.subplots(figsize=(max(7, len(names) * 0.45), 4))
        ax.bar(np.arange(len(names)), values, color="#176b87")
        ax.axhline(effective["mean"], color="#102b3a", label="mean")
        ax.axhline(effective["lower_benchmark"], color="#e47945", linestyle="--")
        ax.axhline(effective["upper_benchmark"], color="#e47945", linestyle="--", label="mean ± SD")
        ax.set_xticks(np.arange(len(names)), names, rotation=90)
        ax.set_ylabel("epsilon")
        ax.set_title(f"Effective interactions: {key}")
        ax.legend()
        path = destination / f"effective-interactions-{key}.png"
        fig.tight_layout()
        fig.savefig(path, dpi=180)
        plt.close(fig)
        outputs.append(path)

        response = row["temperature_response"]
        temperatures = np.asarray(response["temperature"], dtype=float)
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(temperatures, response["d_mean_energy_d_temperature"], label="d<E>/dT")
        ax.plot(temperatures, response["d_mean_magnetization_d_temperature"], label="dm/dT")
        ax.axvline(1.0, color="#62717e", linestyle=":", label="T=1")
        ax.set_xlabel("temperature")
        ax.set_ylabel("response")
        ax.set_title(f"Critical-state response: {key}")
        ax.legend()
        path = destination / f"temperature-response-{key}.png"
        fig.tight_layout()
        fig.savefig(path, dpi=180)
        plt.close(fig)
        outputs.append(path)

    for outcome in sorted({row["outcome"] for row in results}):
        values = []
        for row in results:
            if row["outcome"] == outcome:
                matrix = np.asarray(row["J"], dtype=float)
                values.extend(matrix[np.triu_indices_from(matrix, k=1)])
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(values, bins=40, color="#176b87", alpha=0.85)
        ax.set_xlabel("Jij")
        ax.set_ylabel("count")
        ax.set_title(f"Jij distribution: {outcome}")
        path = destination / f"J-distribution-{outcome}.png"
        fig.tight_layout()
        fig.savefig(path, dpi=180)
        plt.close(fig)
        outputs.append(path)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Export figures from a paper reproduction JSON report.")
    parser.add_argument("--report", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    export_figures(report, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
