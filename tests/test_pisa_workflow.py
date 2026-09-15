import json

import pytest

from examples.pisa_local_workflow import build_parser, run
from learning_energy_model import PISAMapping


def test_pisa_workflow_accepts_mapping_contract(tmp_path):
    pytest.importorskip("pandas")
    input_path = tmp_path / "student.csv"
    input_path.write_text(
        "feature_a,feature_b,target,weight\n"
        "0,0,0,1\n"
        "0,1,1,1\n"
        "1,0,1,2\n"
        "1,1,1,2\n",
        encoding="utf-8",
    )
    mapping_path = tmp_path / "mapping.json"
    PISAMapping(
        feature_names=("feature_a", "feature_b"),
        target_name="target",
        weight_name="weight",
        metadata={"cycle": "PISA 2022", "scope": "SYN", "codebook": "fixture"},
    ).save(mapping_path)
    model_path = tmp_path / "model.pt"
    report_path = tmp_path / "report.json"
    args = build_parser().parse_args(
        [
            "--input",
            str(input_path),
            "--mapping",
            str(mapping_path),
            "--output-model",
            str(model_path),
            "--output-report",
            str(report_path),
            "--calculation",
            "exact",
            "--max-epochs",
            "2",
        ]
    )
    run(args)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert model_path.exists()
    assert report["quality"]["passed"] is True
    assert report["fit"]["diagnostics"]["calculation"] == "exact"
