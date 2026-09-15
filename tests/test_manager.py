import numpy as np
import pytest

from learning_energy_model import DataConfig, MultiDomainManager


def _training_data():
    X = np.array([[0.0], [1.0], [0.0], [1.0]])
    return X, np.array([0.0, 1.0, 0.0, 1.0])


def test_multi_domain_manager_fits_predicts_and_round_trips(tmp_path):
    X, y = _training_data()
    manager = MultiDomainManager(
        {"math": DataConfig(feature_names=("practice",), target_name="score")},
        model_kwargs={"max_epochs": 30, "min_epochs": 5, "tolerance": 0.1},
    )
    manager.fit("math", X, y)
    manager.fit("reading", X, 1.0 - y)
    assert manager.domains == ("math", "reading")
    np.testing.assert_allclose(manager.predict("math", X).probabilities, manager.get_model("math").predict(X).probabilities)
    assert manager.analyze("reading").assumptions

    path = tmp_path / "manager"
    manager.save(path)
    loaded = MultiDomainManager.load(path)
    assert loaded.domains == manager.domains
    np.testing.assert_allclose(
        loaded.predict("math", X).probabilities, manager.predict("math", X).probabilities
    )


def test_multi_domain_manager_rejects_unknown_or_duplicate_domains():
    manager = MultiDomainManager()
    with pytest.raises(ValueError, match="non-empty"):
        manager.add_domain("")
    manager.add_domain("math")
    with pytest.raises(ValueError, match="already"):
        manager.add_domain("math")
    with pytest.raises(KeyError, match="unknown domain"):
        manager.get_model("science")
