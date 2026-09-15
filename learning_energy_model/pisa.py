"""Optional local readers and explicit mappings for PISA-style files.

This module never downloads or packages PISA data. File readers are optional so
the core package remains usable without pandas/pyreadstat.
"""

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from zipfile import ZipFile

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

    def __post_init__(self) -> None:
        if not self.feature_names:
            raise ValueError("feature_names must contain at least one column")
        if len(set(self.feature_names)) != len(self.feature_names):
            raise ValueError("feature_names must be unique")
        if self.target_name in self.feature_names:
            raise ValueError("target_name must not also be a feature name")
        if self.weight_name is not None and self.weight_name in (*self.feature_names, self.target_name):
            raise ValueError("weight_name must identify a separate column")
        missing_values = np.asarray(self.missing_values, dtype=float)
        if not np.isfinite(missing_values).all():
            raise ValueError("missing_values must be finite numeric codes")

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
    """Read a local PISA CSV, SAS, SPSS, or single-data-file ZIP.

    The returned table stays in memory only. No source file is copied or
    included in model serialization. ZIP members are extracted to a temporary
    file and are never unpacked into the project directory.
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
    if suffix == ".zip":
        supported = {".csv", ".sav", ".zsav", ".sas7bdat", ".xpt", ".xpt7", ".tsv", ".txt"}
        with ZipFile(source) as archive:
            candidates = [
                name
                for name in archive.namelist()
                if not name.endswith("/") and Path(name).suffix.lower() in supported
            ]
            if len(candidates) != 1:
                raise ValueError(
                    "ZIP must contain exactly one supported data file; "
                    f"found {len(candidates)}"
                )
            member = candidates[0]
            with tempfile.NamedTemporaryFile(suffix=Path(member).suffix) as temporary:
                with archive.open(member) as source_file:
                    shutil.copyfileobj(source_file, temporary)
                temporary.flush()
                return read_pisa_file(temporary.name)
    if suffix == ".csv":
        return pd.read_csv(source)
    if suffix in {".tsv", ".txt"}:
        return pd.read_csv(source, sep="\t")
    if suffix in {".sav", ".zsav"}:
        return pd.read_spss(source)
    if suffix in {".sas7bdat", ".xpt", ".xpt7"}:
        return pd.read_sas(source)
    raise ValueError("unsupported file type; use CSV, TSV, SAS, SPSS, or ZIP")


def prepare_pisa_file(path: str | Path, mapping: PISAMapping) -> PreparedData:
    """Read and map one local PISA file without retaining the source table."""
    return mapping.prepare(read_pisa_file(path))
