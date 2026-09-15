import numpy as np
import pytest

pytest.importorskip("matplotlib")

from learning_energy_model import DataConfig, LearningModel
from learning_energy_model.visualization import (
    plot_correlations,
    plot_interactions,
    plot_training_history,
)


def test_visualization_helpers_return_figures_and_axes():
    X = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]] * 4)
    y = np.array([0.0, 1.0, 1.0, 1.0] * 4)
    model = LearningModel(
        DataConfig(feature_names=("home", "support"), target_name="outcome"),
        max_epochs=5,
        min_epochs=1,
    )
    fit = model.fit(X, y)
    analysis = model.analyze()

    fig1, ax1 = plot_interactions(analysis)
    fig2, ax2 = plot_correlations(analysis, labels=("H", "S", "Y"))
    fig3, ax3 = plot_training_history(fit)
    assert ax1.get_title() == "Pairwise interactions (J)"
    assert ax2.get_title() == "Model correlations"
    assert ax3.get_xlabel() == "epoch"
    for fig in (fig1, fig2, fig3):
        fig.clf()
