"""Transparent data-quality checks for structured siRNA datasets."""

from typing import Dict, List

import pandas as pd

from .sequence_features import VALID_RNA_BASES


def _invalid_sequence_rows(dataframe: pd.DataFrame, column: str) -> List[int]:
    """Return dataframe index labels with missing, empty, or non-RNA sequences."""
    invalid_rows = []
    for index, value in dataframe[column].items():
        if not isinstance(value, str):
            invalid_rows.append(index)
            continue
        sequence = "".join(value.upper().split())
        if not sequence or set(sequence) - VALID_RNA_BASES:
            invalid_rows.append(index)
    return invalid_rows


def run_quality_checks(dataframe: pd.DataFrame) -> Dict[str, object]:
    """Summarise common quality issues without modifying the source dataframe.

    Returns a dictionary with per-column missing counts, duplicate paired
    sequences, invalid nucleotide rows for both strands, and activity-type
    frequencies. Index labels are retained so callers can trace records back to
    the original source data.
    """
    required_sequence_columns = {"sense_sequence", "antisense_sequence"}
    missing_sequence_columns = required_sequence_columns - set(dataframe.columns)
    if missing_sequence_columns:
        raise KeyError(
            "Missing sequence columns: " + ", ".join(sorted(missing_sequence_columns))
        )
    if "activity_type" not in dataframe.columns:
        raise KeyError("Missing required column: activity_type")

    # The guide/antisense strand is commonly the most useful identity for a
    # first-pass comparison. Report it separately from exact duplex duplicates.
    duplicate_sequence_mask = dataframe.duplicated(
        subset=["antisense_sequence"], keep=False
    )
    paired_sequence_columns = ["sense_sequence", "antisense_sequence"]
    duplicate_duplex_mask = dataframe.duplicated(subset=paired_sequence_columns, keep=False)

    return {
        "n_rows": len(dataframe),
        "missing_values_by_column": dataframe.isna().sum().to_dict(),
        "duplicate_sequence_rows": dataframe.index[duplicate_sequence_mask].tolist(),
        "n_duplicate_sequence_rows": int(duplicate_sequence_mask.sum()),
        "duplicate_duplex_rows": dataframe.index[duplicate_duplex_mask].tolist(),
        "invalid_sense_sequence_rows": _invalid_sequence_rows(
            dataframe, "sense_sequence"
        ),
        "invalid_antisense_sequence_rows": _invalid_sequence_rows(
            dataframe, "antisense_sequence"
        ),
        "activity_type_distribution": dataframe["activity_type"]
        .fillna("<missing>")
        .value_counts(dropna=False)
        .to_dict(),
    }
