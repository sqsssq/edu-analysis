import numpy as np

from learning_energy_model import PISAMapping


def test_pisa_mapping_replaces_codebook_missing_values():
    mapping = PISAMapping(
        feature_names=("feature",),
        target_name="outcome",
        weight_name="w_fstuwt",
        missing_values=(-9999.0,),
    )
    prepared = mapping.prepare(
        {
            "feature": [1.0, -9999.0, 3.0],
            "outcome": [0.0, 1.0, -9999.0],
            "w_fstuwt": [1.0, 1.0, 2.0],
        }
    )
    assert np.isnan(prepared.X[1, 0])
    assert np.isnan(prepared.y[2])
    np.testing.assert_array_equal(prepared.sample_weight, [1.0, 1.0, 2.0])
