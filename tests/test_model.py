import numpy as np

from learning_energy_model import DataConfig, LearningModel


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
    prediction = model.predict(X[:8])
    assert prediction.probabilities.shape == (8,)
    assert np.all((prediction.probabilities >= 0) & (prediction.probabilities <= 1))
    analysis = model.analyze()
    assert analysis.h.shape == (3,)
    assert analysis.J.shape == (3, 3)
    assert set(analysis.interventions) == {"home", "support"}


def test_save_and_load_preserves_predictions(tmp_path):
    X = np.array([[0.0], [1.0], [0.2], [0.8], [0.9], [0.1]])
    y = np.array([0.0, 1.0, 0.0, 1.0, 1.0, 0.0])
    config = DataConfig(feature_names=("feature",), target_name="target")
    model = LearningModel(config, max_epochs=100, tolerance=0.1, min_epochs=5)
    model.fit(X, y)
    path = tmp_path / "model.pt"
    model.save(path)
    loaded = LearningModel.load(path)
    np.testing.assert_allclose(model.predict(X).probabilities, loaded.predict(X).probabilities)

