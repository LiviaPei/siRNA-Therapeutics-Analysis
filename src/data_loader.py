"""Data loading and schema validation helpers for siRNA datasets."""

from pathlib import Path
from typing import Union

import pandas as pd


REQUIRED_COLUMNS = [
    "sirna_id",
    "target_gene",
    "sense_sequence",
    "antisense_sequence",
    "chemical_modification",
    "activity_value",
    "activity_type",
    "cell_line",
    "assay_method",
    "concentration",
    "treatment_time",
    "reference",
]


def load_sirna_data(filepath: Union[str, Path]) -> pd.DataFrame:
    """Load a siRNA CSV file and apply basic dataframe validation.

    Parameters
    ----------
    filepath:
        Path to a CSV using the project input schema.

    Returns
    -------
    pandas.DataFrame
        The loaded data. `activity_value` is coerced to numeric where possible.

    Raises
    ------
    FileNotFoundError
        If the supplied path does not exist.
    ValueError
        If required schema columns are missing.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    dataframe = pd.read_csv(path)
    validate_dataframe(dataframe)
    dataframe["activity_value"] = pd.to_numeric(
        dataframe["activity_value"], errors="coerce"
    )
    return dataframe


def validate_dataframe(dataframe: pd.DataFrame) -> None:
    """Validate that a dataframe includes the minimum project schema.

    This is a schema check rather than a data-cleaning step: missing values and
    invalid sequences are intentionally handled by ``data_quality`` so they can
    be reported transparently.
    """
    if dataframe.empty:
        raise ValueError("Dataset is empty; provide at least one siRNA record.")

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in dataframe.columns
    ]
    if missing_columns:
        raise ValueError(
            "Dataset is missing required columns: " + ", ".join(missing_columns)
        )
