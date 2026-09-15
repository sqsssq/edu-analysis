import json

from learning_energy_model.cli import main


def test_cli_fit_and_predict_round_trip(tmp_path, capsys):
    source = tmp_path / "data.csv"
    source.write_text("feature,outcome\n0,0\n1,1\n0,0\n1,1\n", encoding="utf-8")
    artifact = tmp_path / "model.pt"
    assert main(
        [
            "fit",
            "--input",
            str(source),
            "--features",
            "feature",
            "--target",
            "outcome",
            "--output",
            str(artifact),
            "--max-epochs",
            "30",
            "--min-epochs",
            "5",
        ]
    ) == 0
    fit_output = json.loads(capsys.readouterr().out)
    assert artifact.exists()
    assert fit_output["quality"]["passed"]

    assert main(
        ["predict", "--model", str(artifact), "--input", str(source)]
    ) == 0
    prediction_output = capsys.readouterr().out
    assert prediction_output.splitlines()[0] == "probability_0,probability_1,prediction"
    assert len(prediction_output.splitlines()) == 5

    assert main(["analyze", "--model", str(artifact)]) == 0
    analysis_output = json.loads(capsys.readouterr().out)
    assert len(analysis_output["h"]) == 2
    assert "higher_order_moments" in analysis_output
