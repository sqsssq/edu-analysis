import numpy as np

from learnenergy import ContinuousEnergyModel


def test_continuous_model_recovers_mean_covariance_and_conditional_mean():
    rng = np.random.default_rng(31)
    mean = np.array([1.0, -0.5, 0.25])
    covariance = np.array(
        [[1.2, 0.3, -0.1], [0.3, 0.9, 0.2], [-0.1, 0.2, 0.7]],
        dtype=float,
    )
    data = rng.multivariate_normal(mean, covariance, size=2_000)
    model = ContinuousEnergyModel(("a", "b", "c"), ridge=0.0, seed=31)
    result = model.fit(data)

    assert result.converged
    np.testing.assert_allclose(result.model_mean, mean, atol=0.08)
    np.testing.assert_allclose(result.model_covariance, covariance, atol=0.1)
    analysis = model.analyze()
    assert analysis.precision.shape == (3, 3)
    assert analysis.interactions.shape == (3, 3)
    conditional = model.conditional_mean([np.nan, 0.2, -0.1], target_index=0)
    fitted = analysis.covariance
    expected = analysis.mean[0] + fitted[0, 1:] @ np.linalg.solve(
        fitted[1:, 1:], np.array([0.2, -0.1]) - analysis.mean[1:]
    )
    np.testing.assert_allclose(conditional, expected, atol=1e-10)


def test_continuous_model_supports_named_tables_sampling_and_reload(tmp_path):
    rng = np.random.default_rng(32)
    table = {"first": rng.normal(size=80), "second": rng.normal(size=80)}
    model = ContinuousEnergyModel(ridge=1e-5, seed=32)
    result = model.fit_table(table, feature_names=("first", "second"))
    assert result.diagnostics["model_family"] == "continuous_gaussian_quadratic"
    assert model.sample(12).shape == (12, 2)

    path = tmp_path / "continuous.pt"
    model.save(path)
    loaded = ContinuousEnergyModel.load(path)
    np.testing.assert_allclose(loaded.analyze().mean, model.analyze().mean)
    assert loaded.feature_names == ("first", "second")


def test_continuous_model_rejects_nonfinite_values_and_bad_weights():
    model = ContinuousEnergyModel(("x",))
    with np.testing.assert_raises(ValueError):
        model.fit([[np.nan], [1.0]])
    with np.testing.assert_raises(ValueError):
        model.fit([[0.0], [1.0]], sample_weight=[1.0, -1.0])
