import numpy as np
import pytest

from learning_energy_model import compare_moment_orders


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
