from zipfile import ZipFile

import numpy as np
import pytest

from learning_energy_model import PISAMapping, prepare_pisa_file


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


def test_mapping_contract_round_trips_without_rows(tmp_path):
    mapping = PISAMapping(
        feature_names=("ST123", "ST456"),
        target_name="PV1MATH",
        weight_name="W_FSTUWT",
        missing_values=(-9999.0,),
        metadata={"cycle": "PISA 2022", "scope": "JPN", "codebook": "reviewed.pdf"},
    )
    path = tmp_path / "mapping.json"
    mapping.save(path)
    loaded = PISAMapping.load(path)
    assert loaded == mapping
    assert "rows" not in loaded.to_dict()


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"feature_names": (), "target_name": "y"}, "at least one"),
        ({"feature_names": ("x", "x"), "target_name": "y"}, "unique"),
        ({"feature_names": ("y",), "target_name": "y"}, "target_name"),
        ({"feature_names": ("x",), "target_name": "y", "weight_name": "x"}, "weight_name"),
        ({"feature_names": ("x",), "target_name": "y", "missing_values": (np.inf,)}, "finite"),
    ],
)
def test_pisa_mapping_rejects_invalid_contracts(kwargs, message):
    with pytest.raises(ValueError, match=message):
        PISAMapping(**kwargs)


def test_prepare_pisa_file_reads_a_single_data_file_zip(tmp_path):
    pytest.importorskip("pandas")
    csv_path = tmp_path / "student.csv"
    csv_path.write_text("feature,outcome,weight\n1,0,1\n2,1,2\n", encoding="utf-8")
    archive_path = tmp_path / "student.zip"
    with ZipFile(archive_path, "w") as archive:
        archive.write(csv_path, arcname="student.csv")

    prepared = prepare_pisa_file(
        archive_path,
        PISAMapping(
            feature_names=("feature",), target_name="outcome", weight_name="weight"
        ),
    )
    assert prepared.X.shape == (2, 1)
    np.testing.assert_array_equal(prepared.sample_weight, [1.0, 2.0])


def test_pisa_zip_reader_rejects_multiple_data_files(tmp_path):
    pytest.importorskip("pandas")
    archive_path = tmp_path / "multiple.zip"
    with ZipFile(archive_path, "w") as archive:
        archive.writestr("a.csv", "x\n1\n")
        archive.writestr("b.csv", "x\n2\n")
    with pytest.raises(ValueError, match="exactly one"):
        from learning_energy_model.pisa import read_pisa_file

        read_pisa_file(archive_path)
