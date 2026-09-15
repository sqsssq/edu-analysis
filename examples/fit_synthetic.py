"""Run the complete package workflow without any external dataset.

Usage:
    python examples/fit_synthetic.py /tmp/learning-model.pt
"""

import sys
from pathlib import Path

import numpy as np

from learning_energy_model import DataConfig, LearningModel


def main(output_path: str = "learning-model.pt") -> None:
    rng = np.random.default_rng(2026)
    X = rng.normal(size=(500, 3))
    y = (0.9 * X[:, 0] - 0.5 * X[:, 1] + 0.25 * X[:, 2] + rng.normal(size=500) > 0).astype(float)
    config = DataConfig(
        feature_names=("resource", "support", "engagement"),
        target_name="outcome",
    )
    model = LearningModel(config, seed=2026, max_epochs=500, tolerance=0.03)
    fit_result = model.fit(X, y)
    analysis = model.analyze()
    model.save(output_path)
    print(f"converged={fit_result.converged}, epochs={fit_result.epochs}")
    print(f"calculation={fit_result.diagnostics['calculation']}")
    print(f"target_probability={analysis.means[-1]:.3f}")
    print(f"saved={Path(output_path).resolve()}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "learning-model.pt")
