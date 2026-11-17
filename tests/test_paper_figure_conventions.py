"""Checks for paper-specific figure parameter conventions."""

import importlib.util
from pathlib import Path

import numpy as np
import pytest

SCRIPT = Path(__file__).parents[1] / "examples" / "pisa_paper_figures_4_12.py"
SPEC = importlib.util.spec_from_file_location("pisa_paper_figures_4_12", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_paper_spin_couplings_convert_sign_and_scale() -> None:
    matrix = np.asarray(
        [
            [0.0, -0.8, 0.4],
            [-0.8, 0.0, -1.2],
            [0.4, -1.2, 0.0],
        ]
    )

    converted = MODULE._paper_spin_couplings(matrix)

    np.testing.assert_allclose(converted, [0.2, -0.1, 0.3])


def test_paper_spin_couplings_rejects_non_square_input() -> None:
    with pytest.raises(ValueError, match="square"):
        MODULE._paper_spin_couplings(np.zeros((2, 3)))
