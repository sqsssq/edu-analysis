"""Optional local readers and explicit mappings for PISA-style files.

This module never downloads or packages PISA data. File readers are optional so
the core package remains usable without pandas/pyreadstat.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from .data import PreparedData, prepare_tabular_data


@dataclass(frozen=True)
class PISAMapping:
    """Explicit column contract for one local PISA analysis.

    ``missing_values`` lists source-specific numeric codes that should become
    ``NaN`` before the normal package missing-value strategy is applied. The
    caller is responsible for confirming these codes against the matching
    OECD codebook.
    """

    feature_names: tuple[str, ...]
    target_name: str
    weight_name: str | None = None
    missing_values: tuple[float, ...] = ()

    def prepare(self, table: Any) -> PreparedData:
        if self.missing_values:
            table = _replace_missing_codes(table, self.missing_values)
        return prepare_tabular_data(
            table,
            feature_names=self.feature_names,
            target_name=self.target_name,
            weight_name=self.weight_name,
        )


def _replace_missing_codes(table: Any, missing_values: tuple[float, ...]) -> Any:
    """Return a copy with configured numeric response codes converted to NaN."""
    codes = np.asarray(missing_values, dtype=float)
    if hasattr(table, "copy") and hasattr(table, "columns"):
        result = table.copy()
        for column in result.columns:
            values = np.asarray(result[column], dtype=float)
            result[column] = np.where(np.isin(values, codes), np.nan, values)
        return result
    if isinstance(table, dict):
        return {
            name: np.where(np.isin(np.asarray(values, dtype=float), codes), np.nan, values)
            for name, values in table.items()
        }
    raise TypeError("PISAMapping requires a mapping or a pandas-like table")


def read_pisa_file(path: str | Path) -> Any:
    """Read a local PISA CSV, SAS, or SPSS file using optional dependencies.

    The returned table stays in memory only. No source file is copied or
    included in model serialization.
    """
    try:
        import pandas as pd  # type: ignore[import-untyped]
    except ImportError as exc:
        raise ImportError(
            "read_pisa_file requires the optional 'pisa' dependencies; "
            "install with `pip install interpretable-learning-energy-model[pisa]`"
        ) from exc
    source = Path(path)
    suffix = source.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(source)
    if suffix in {".tsv", ".txt"}:
        return pd.read_csv(source, sep="\t")
    if suffix in {".sav", ".zsav"}:
        return pd.read_spss(source)
    if suffix in {".sas7bdat", ".xpt", ".xpt7"}:
        return pd.read_sas(source)
    raise ValueError("unsupported file type; use CSV, TSV, SAS, or SPSS")


def prepare_pisa_file(path: str | Path, mapping: PISAMapping) -> PreparedData:
    """Read and map one local PISA file without retaining the source table."""
    return mapping.prepare(read_pisa_file(path))
