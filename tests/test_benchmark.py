from examples.parameter_recovery_benchmark import run


def test_parameter_recovery_benchmark_returns_aggregate_evidence(tmp_path):
    output = tmp_path / "benchmark.json"
    report = run(output)
    assert report["calculation"]["calculation"] == "exact"
    assert report["moment_comparison"]["passed"] is True
    assert report["parameter_error"]["max_abs_h"] < 0.03
    assert report["parameter_error"]["max_abs_J"] < 0.03
    assert output.exists()
