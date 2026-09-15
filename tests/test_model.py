import json

import numpy as np
import pytest

from learning_energy_model import DataConfig, LearningEnergyClassifier, LearningModel, __version__
from learning_energy_model.sampler import GibbsSampler


def test_fit_predict_and_analyze_on_binary_data():
    rng = np.random.default_rng(7)
    X = rng.normal(size=(400, 2))
    y = (0.8 * X[:, 0] - 0.4 * X[:, 1] + rng.normal(size=400) > 0).astype(float)
    model = LearningModel(
        DataConfig(feature_names=("home", "support"), target_name="outcome"),
        learning_rate=0.08,
        max_epochs=400,
        tolerance=0.03,
        min_epochs=10,
    )
    result = model.fit(X, y)
    assert result.epochs <= 400
    assert result.observed_means is not None
    assert result.model_pairwise_moments is not None
    assert result.observed_means.shape == (3,)
    prediction = model.predict(X[:8])
    assert prediction.probabilities.shape == (8,)
    assert np.all((prediction.probabilities >= 0) & (prediction.probabilities <= 1))
    analysis = model.analyze()
    assert analysis.h.shape == (3,)
    assert analysis.J.shape == (3, 3)
    assert analysis.correlations.shape == (3, 3)
    np.testing.assert_allclose(np.diag(analysis.correlations), 1.0)
    assert set(analysis.interventions) == {"home", "support"}
    assert "0×1×2" in analysis.higher_order_moments
    samples = model.sample(25)
    assert samples.shape == (25, 3)
    exported = json.loads(analysis.to_json())
    assert len(exported["h"]) == 3
    assert exported["assumptions"]
    assert "higher_order_moments" in exported


def test_predict_matches_the_model_conditional_energy():
    X = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]] * 20)
    y = np.array([0.0, 1.0, 1.0, 1.0] * 20)
    model = LearningModel(
        DataConfig(feature_names=("a", "b"), target_name="outcome"),
        max_epochs=80,
        tolerance=0.05,
        min_epochs=10,
        seed=4,
    )
    model.fit(X, y)

    result = model.predict(X[:4])
    expected_field = float(model.h[-1]) + X[:4] @ model.J[:2, 2].detach().cpu().numpy()
    expected = 1.0 / (1.0 + np.exp(expected_field))
    np.testing.assert_allclose(result.probabilities, expected)
    assert result.diagnostics["target_name"] == "outcome"
    assert result.diagnostics["conditional_on"] == ["a", "b"]


def test_predict_selects_named_columns_from_reordered_mapping():
    X = np.array([[0.0, 1.0], [1.0, 0.0], [1.0, 1.0], [0.0, 0.0]])
    y = np.array([1.0, 1.0, 1.0, 0.0])
    model = LearningModel(
        DataConfig(feature_names=("first", "second")),
        max_epochs=30,
        min_epochs=5,
        tolerance=0.1,
        seed=8,
    )
    model.fit(X, y)
    named = {"extra": [99.0] * 4, "second": X[:, 1], "first": X[:, 0]}
    np.testing.assert_allclose(
        model.predict(named).probabilities, model.predict(X).probabilities
    )
    with pytest.raises(ValueError, match="missing fitted feature"):
        model.predict({"first": X[:, 0]})


def test_sklearn_style_classifier_exposes_binary_probabilities_and_params():
    X = np.array([[0.0], [1.0], [0.0], [1.0]])
    y = np.array([0.0, 1.0, 0.0, 1.0])
    estimator = LearningEnergyClassifier(
        config=DataConfig(feature_names=("feature",)),
        model_kwargs={"max_epochs": 30, "min_epochs": 5, "tolerance": 0.1},
    )
    assert estimator.set_params(model_kwargs={"max_epochs": 30}) is estimator
    assert estimator.get_params()["model_kwargs"] == {"max_epochs": 30}
    estimator.fit(X, y)
    probabilities = estimator.predict_proba(X)
    assert probabilities.shape == (4, 2)
    np.testing.assert_allclose(probabilities.sum(axis=1), 1.0)
    np.testing.assert_array_equal(estimator.predict(X), (probabilities[:, 1] >= 0.5).astype(float))
    assert estimator.classes_.tolist() == [0.0, 1.0]
    assert estimator.analyze().assumptions


def test_analysis_can_export_one_row_dataframe_when_pandas_is_available():
    pytest.importorskip("pandas")
    X = np.array([[0.0], [1.0], [0.0], [1.0]])
    y = np.array([0.0, 1.0, 1.0, 0.0])
    model = LearningModel(DataConfig(feature_names=("feature",)), max_epochs=2)
    model.fit(X, y)
    frame = model.analyze().to_dataframe()
    assert frame.shape[0] == 1
    assert "assumptions" in frame.columns


def test_save_and_load_preserves_predictions(tmp_path):
    X = np.array([[0.0], [1.0], [0.2], [0.8], [0.9], [0.1]])
    y = np.array([0.0, 1.0, 0.0, 1.0, 1.0, 0.0])
    config = DataConfig(
        feature_names=("feature",), target_name="target", metadata={"source": "synthetic"}
    )
    model = LearningModel(config, max_epochs=100, tolerance=0.1, min_epochs=5)
    model.fit(X, y)
    path = tmp_path / "model.pt"
    model.save(path)
    loaded = LearningModel.load(path)
    np.testing.assert_allclose(model.predict(X).probabilities, loaded.predict(X).probabilities)
    assert loaded.fit_result is not None
    np.testing.assert_allclose(loaded.fit_result.observed_means, model.fit_result.observed_means)
    assert loaded.config.metadata == {"source": "synthetic"}
    assert loaded.config.sample_weight_name is None
    assert loaded.artifact_metadata["package_version"] == __version__


def test_gibbs_sampler_matches_uniform_exact_moments():
    import torch

    h = torch.zeros(3, dtype=torch.float64)
    J = torch.zeros((3, 3), dtype=torch.float64)
    result = GibbsSampler(samples=300, burn_in=200, chains=4, seed=11).moments(h, J)
    means, pairwise, _, diagnostics = result
    np.testing.assert_allclose(means.numpy(), 0.5, atol=0.08)
    np.testing.assert_allclose(pairwise.numpy()[np.triu_indices(3, 1)], 0.25, atol=0.1)
    assert diagnostics["draws"] == 1_200
    assert diagnostics["max_rhat"] < 1.2
    assert 1.0 <= diagnostics["min_effective_sample_size"] <= diagnostics["draws"]
    assert len(diagnostics["rhat_by_node"]) == 3


def test_gibbs_sampler_rejects_invalid_configuration_and_parameters():
    import torch

    with pytest.raises(ValueError, match="positive"):
        GibbsSampler(samples=0)
    with pytest.raises(ValueError, match="positive"):
        GibbsSampler(samples=10, chains=1.5)
    with pytest.raises(ValueError, match="matching square"):
        GibbsSampler(samples=10).sample(torch.zeros(2), torch.zeros((2, 3)))
    with pytest.raises(ValueError, match="symmetric"):
        GibbsSampler(samples=10).sample(torch.zeros(2), torch.tensor([[0.0, 1.0], [0.0, 0.0]]))


def test_gibbs_sampler_agrees_with_exact_moments_on_known_model():
    import torch

    h = torch.tensor([-0.35, 0.2, 0.45], dtype=torch.float64)
    J = torch.tensor(
        [[0.0, -0.3, 0.15], [-0.3, 0.0, 0.25], [0.15, 0.25, 0.0]],
        dtype=torch.float64,
    )
    states = torch.tensor(
        [[(value >> shift) & 1 for shift in (2, 1, 0)] for value in range(8)],
        dtype=torch.float64,
    )
    energies = states @ h + 0.5 * ((states @ J) * states).sum(dim=1)
    probabilities = torch.softmax(-energies, dim=0)
    exact_means = probabilities @ states
    exact_pairs = torch.einsum("n,ni,nj->ij", probabilities, states, states)

    sampled_means, sampled_pairs, _, _ = GibbsSampler(
        samples=1_000, burn_in=500, chains=4, seed=23
    ).moments(h, J)
    np.testing.assert_allclose(sampled_means.numpy(), exact_means.numpy(), atol=0.045)
    np.testing.assert_allclose(
        sampled_pairs.numpy()[np.triu_indices(3, 1)],
        exact_pairs.numpy()[np.triu_indices(3, 1)],
        atol=0.06,
    )


def test_model_switches_to_monte_carlo_above_exact_threshold():
    rng = np.random.default_rng(13)
    X = rng.integers(0, 2, size=(30, 3)).astype(float)
    y = (X[:, 0].astype(int) ^ X[:, 1].astype(int)).astype(float)
    model = LearningModel(
        DataConfig(feature_names=("a", "b", "c")),
        max_exact_nodes=2,
        mc_samples=40,
        mc_burn_in=30,
        mc_chains=2,
        max_epochs=3,
    )
    result = model.fit(X, y)
    assert result.diagnostics["calculation"] == "monte_carlo"
    analysis = model.analyze()
    assert analysis.diagnostics["chains"] == 2
    assert model.sample(10).shape == (10, 4)


def test_binary_inputs_are_not_collapsed_by_median_threshold():
    X = np.array([[0.0], [1.0], [0.0], [1.0]])
    y = np.array([0.0, 1.0, 1.0, 0.0])
    model = LearningModel(DataConfig(feature_names=("binary",), target_name="target"), max_epochs=1)
    binary_X, binary_y = model.preprocessor.fit(X, y).transform(X, y)
    np.testing.assert_array_equal(binary_X[:, 0], X[:, 0])
    np.testing.assert_array_equal(binary_y, y)


def test_moment_matching_recovers_a_small_known_model():
    import torch

    true_h = torch.tensor([-0.35, 0.2, 0.45], dtype=torch.float64)
    true_J = torch.tensor(
        [[0.0, -0.3, 0.15], [-0.3, 0.0, 0.25], [0.15, 0.25, 0.0]],
        dtype=torch.float64,
    )
    states = torch.tensor(
        [[(value >> shift) & 1 for shift in (2, 1, 0)] for value in range(8)],
        dtype=torch.float64,
    )
    energies = states @ true_h + 0.5 * ((states @ true_J) * states).sum(dim=1)
    probabilities = torch.softmax(-energies, dim=0)
    indices = torch.multinomial(
        probabilities,
        12_000,
        replacement=True,
        generator=torch.Generator().manual_seed(31),
    )
    observations = states[indices].numpy()
    model = LearningModel(
        DataConfig(feature_names=("a", "b"), target_name="outcome"),
        learning_rate=0.08,
        max_epochs=500,
        tolerance=0.025,
        min_epochs=25,
        seed=5,
    )
    result = model.fit(observations[:, :2], observations[:, 2])
    assert result.converged
    np.testing.assert_allclose(model.h.numpy(), true_h.numpy(), atol=0.4)
    np.testing.assert_allclose(
        model.J.numpy()[np.triu_indices(3, 1)],
        true_J.numpy()[np.triu_indices(3, 1)],
        atol=0.4,
    )


def test_exact_moment_matching_recovers_a_known_distribution():
    """Use deterministic state counts to separate optimizer error from MC error."""
    true_h = np.array([-0.35, 0.2, 0.45])
    true_J = np.array(
        [[0.0, -0.3, 0.15], [-0.3, 0.0, 0.25], [0.15, 0.25, 0.0]]
    )
    states = np.array([[(value >> shift) & 1 for shift in (2, 1, 0)] for value in range(8)])
    energies = states @ true_h + 0.5 * ((states @ true_J) * states).sum(axis=1)
    probabilities = np.exp(-energies)
    probabilities /= probabilities.sum()
    counts = np.floor(100_000 * probabilities).astype(int)
    counts[0] += 100_000 - counts.sum()
    observations = np.repeat(states, counts, axis=0)

    model = LearningModel(
        DataConfig(feature_names=("a", "b"), target_name="outcome"),
        learning_rate=0.08,
        max_epochs=1_000,
        tolerance=0.001,
        min_epochs=25,
        seed=2,
    )
    result = model.fit(observations[:, :2], observations[:, 2])

    assert result.converged
    np.testing.assert_allclose(model.h.numpy(), true_h, atol=0.08)
    np.testing.assert_allclose(
        model.J.numpy()[np.triu_indices(3, 1)], true_J[np.triu_indices(3, 1)], atol=0.08
    )


def test_kl_autodiff_path_is_available_for_exact_models():
    X = np.array([[0.0], [1.0], [0.0], [1.0], [1.0], [0.0]])
    y = np.array([0.0, 1.0, 0.0, 1.0, 1.0, 0.0])
    model = LearningModel(
        DataConfig(feature_names=("feature",), target_name="target"),
        learning_rate=0.05,
        max_epochs=120,
        tolerance=0.08,
        min_epochs=10,
    )
    result = model.fit(X, y, method="kl")
    assert result.diagnostics["training_method"] == "kl"
    assert model.predict(X).probabilities.shape == (6,)


def test_kl_autodiff_path_rejects_large_models():
    X = np.zeros((4, 3))
    y = np.zeros(4)
    model = LearningModel(DataConfig(feature_names=("a", "b", "c")), max_exact_nodes=2)
    with pytest.raises(ValueError, match="requires exact enumeration"):
        model.fit(X, y, method="kl")


def test_weighted_training_rejects_nonfinite_weights():
    X = np.array([[0.0], [1.0], [0.0], [1.0]])
    y = np.array([0.0, 1.0, 1.0, 0.0])
    model = LearningModel(DataConfig(feature_names=("feature",)), max_epochs=1)
    with pytest.raises(ValueError, match="finite"):
        model.fit(X, y, sample_weight=np.array([1.0, np.inf, 1.0, 1.0]))
