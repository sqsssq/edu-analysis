import numpy as np
import pytest

from learning_energy_model import (
    DataConfig,
    LearningModel,
    classify_effective_interactions,
    compare_moment_orders,
    threshold_sensitivity,
)


def test_compare_moment_orders_reports_errors_for_all_orders():
    report = compare_moment_orders(
        {
            1: np.array([0.2, 0.4]),
            2: np.array([[0.2, 0.1], [0.1, 0.4]]),
            3: {"0×1×2": 0.05},
        },
        {
            1: np.array([0.21, 0.39]),
            2: np.array([[0.2, 0.11], [0.11, 0.4]]),
            3: {"0×1×2": 0.06},
        },
        tolerances={1: 0.02, 2: 0.02, 3: 0.02},
    )
    assert report.passed
    assert report.max_absolute_error[1] == pytest.approx(0.01)
    assert report.to_dict()["passed"] is True


def test_compare_moment_orders_rejects_incomplete_orders():
    with pytest.raises(ValueError, match="orders must match"):
        compare_moment_orders({1: [0.2]}, {2: [0.2]})


def test_effective_interaction_and_temperature_response_are_exact():
    X = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    y = np.array([0.0, 1.0, 1.0, 1.0])
    model = LearningModel(
        DataConfig(feature_names=("a", "b"), target_name="outcome"),
        calculation="exact",
        max_epochs=10,
    )
    model.fit(X, y)
    values = model.effective_interactions()
    assert set(values) == {"a", "b"}
    classified = classify_effective_interactions(values)
    assert set(classified["classification"]) == {"a", "b"}
    response = model.temperature_response([0.5, 1.0, 1.5])
    assert len(response["mean_energy"]) == 3
    assert response["energies_finite"] is True
    assert response["response_derivative_method"] == "exact_covariance"


def test_threshold_sensitivity_returns_appendix_style_summary():
    data = np.array([[0.0, 0.1], [0.2, 0.3], [0.8, 0.7], [1.0, 0.9]])
    report = threshold_sensitivity(data, [-0.5, 0.0, 0.5])
    assert report["thresholds"] == [-0.5, 0.0, 0.5]
    assert len(report["correlations"]) == 3
