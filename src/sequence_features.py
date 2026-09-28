"""RNA sequence feature extraction for descriptive siRNA analysis."""

from typing import Iterable, Union

import numpy as np
import pandas as pd


VALID_RNA_BASES = frozenset("AUGC")


def _normalise_sequence(sequence: str) -> str:
    """Return an uppercase, whitespace-free RNA sequence.

    Raises a ``ValueError`` when the input is missing, empty, or contains bases
    other than A, U, G, or C. Modified bases should be represented in a separate
    metadata field until a project-specific encoding policy is defined.
    """
    if not isinstance(sequence, str):
        raise ValueError("RNA sequence must be a string.")

    cleaned = "".join(sequence.upper().split())
    if not cleaned:
        raise ValueError("RNA sequence cannot be empty.")

    invalid_bases = sorted(set(cleaned) - VALID_RNA_BASES)
    if invalid_bases:
        raise ValueError(
            "RNA sequence contains invalid nucleotide(s): "
            + ", ".join(invalid_bases)
        )
    return cleaned


def calculate_sequence_features(sequence: str, seed_length: int = 7) -> dict:
    """Calculate basic, interpretable features for one RNA sequence.

    Parameters
    ----------
    sequence:
        RNA sequence written 5′→3′ with A/U/G/C bases.
    seed_length:
        Number of 5′ bases to report as the seed region. The default is 7 for
        descriptive use only; biological conventions should be documented for a
        specific downstream analysis.

    Returns
    -------
    dict
        Sequence length, base fractions, GC content, 5′ base, and seed region.
    """
    if seed_length < 1:
        raise ValueError("seed_length must be at least 1.")

    rna = _normalise_sequence(sequence)
    length = len(rna)
    fractions = {base: rna.count(base) / length for base in "AUGC"}

    return {
        "sequence_length": length,
        "GC_content": fractions["G"] + fractions["C"],
        "A_fraction": fractions["A"],
        "U_fraction": fractions["U"],
        "G_fraction": fractions["G"],
        "C_fraction": fractions["C"],
        "5_prime_base": rna[0],
        "seed_region": rna[:seed_length],
    }


def add_sequence_features(
    dataframe: pd.DataFrame,
    sequence_column: str = "antisense_sequence",
    seed_length: int = 7,
) -> pd.DataFrame:
    """Append RNA features to a dataframe without changing its input columns.

    Rows with missing or invalid sequences receive ``NaN`` feature values. Use
    ``data_quality.run_quality_checks`` to identify and resolve them before any
    downstream comparison.
    """
    if sequence_column not in dataframe.columns:
        raise KeyError(f"Sequence column not found: {sequence_column}")

    feature_rows = []
    for sequence in dataframe[sequence_column]:
        try:
            feature_rows.append(calculate_sequence_features(sequence, seed_length))
        except ValueError:
            feature_rows.append(
                {
                    "sequence_length": np.nan,
                    "GC_content": np.nan,
                    "A_fraction": np.nan,
                    "U_fraction": np.nan,
                    "G_fraction": np.nan,
                    "C_fraction": np.nan,
                    "5_prime_base": np.nan,
                    "seed_region": np.nan,
                }
            )

    features = pd.DataFrame(feature_rows, index=dataframe.index)
    return pd.concat([dataframe.copy(), features], axis=1)
