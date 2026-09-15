import numpy as np
import pytest

from learning_energy_model import (
    DataConfig,
    LearningModel,
    prepare_tabular_data,
    validate_tabular_data,
)


def test_prepare_tabular_data_extracts_named_columns_and_weights():
    prepared = prepare_tabular_data(
        {
            "support": [1.0, 2.0, np.nan],
            "resources": [3.0, 4.0, 5.0],
            "outcome": [0.0, 1.0, 1.0],
            "weight": [1.0, 2.0, 1.0],
        },
        feature_names=("support", "resources"),
        target_name="outcome",
        weight_name="weight",
    )
    assert prepared.X.shape == (3, 2)
    np.testing.assert_array_equal(prepared.y, [0.0, 1.0, 1.0])
    np.testing.assert_array_equal(prepared.sample_weight, [1.0, 2.0, 1.0])


def test_prepare_tabular_data_rejects_bad_weights():
    with pytest.raises(ValueError, match="sample weights"):
        prepare_tabular_data(
            {"x": [1, 2], "y": [0, 1], "weight": [0, 0]},
            feature_names=("x",),
            target_name="y",
            weight_name="weight",
        )


def test_prepare_tabular_data_rejects_nonfinite_weights():
    with pytest.raises(ValueError, match="finite"):
        prepare_tabular_data(
            {"x": [1, 2], "y": [0, 1], "weight": [1, np.inf]},
            feature_names=("x",),
            target_name="y",
            weight_name="weight",
        )


def test_validate_tabular_data_reports_missingness_and_weight_issues():
    report = validate_tabular_data(
        {
            "x": [1.0, np.nan, 3.0],
            "y": [0.0, 1.0, 1.0],
            "weight": [1.0, -1.0, 0.0],
        },
        feature_names=("x",),
        target_name="y",
        weight_name="weight",
    )
    assert not report.passed
    assert report.row_count == 3
    assert report.missing_fraction["x"] == 1 / 3
    assert any("weights" in issue for issue in report.issues)
    assert report.to_dict()["passed"] is False


def test_validate_tabular_data_accepts_missing_values_when_otherwise_valid():
    report = validate_tabular_data(
        {"x": [1.0, np.nan], "y": [0.0, 1.0], "weight": [1.0, 2.0]},
        feature_names=("x",),
        target_name="y",
        weight_name="weight",
    )
    assert report.passed
    assert report.infinite_count == {"x": 0, "y": 0, "weight": 0}


def test_core_preprocessor_rejects_infinite_values():
    model = LearningModel(DataConfig(feature_names=("x",)))
    with pytest.raises(ValueError, match="infinity"):
        model.preprocessor.fit(np.array([[1.0], [np.inf]]), np.array([0.0, 1.0]))


@pytest.mark.parametrize(
    ("strategy", "expected"),
    [("median", 2.0), ("mean", 2.0), ("zero", 0.0)],
)
def test_missing_strategies_impute_before_binarization(strategy, expected):
    model = LearningModel(DataConfig(feature_names=("x",), missing_strategy=strategy))
    binary_X, _ = model.preprocessor.fit(
        np.array([[1.0], [np.nan], [3.0]]), np.array([0.0, 1.0, 1.0])
    ).transform(np.array([[1.0], [np.nan], [3.0]]), np.array([0.0, 1.0, 1.0]))
    assert model.preprocessor.feature_medians is not None
    assert model.preprocessor.feature_medians[0] == expected
    assert binary_X[1, 0] == float(expected >= 2.0)


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"feature_names": ("",)}, "non-empty"),
        ({"feature_names": ("x",), "target_name": "x"}, "target_name"),
        ({"feature_names": ("x",), "thresholds": {"x": np.inf}}, "thresholds"),
        ({"feature_names": ("x",), "target_threshold": np.nan}, "target_threshold"),
        ({"feature_names": ("x",), "sample_weight_name": "x"}, "sample_weight_name"),
        ({"feature_names": ("x",), "sample_weight_name": ""}, "sample_weight_name"),
    ],
)
def test_data_config_rejects_invalid_names_and_thresholds(kwargs, message):
    with pytest.raises(ValueError, match=message):
        DataConfig(**kwargs)
