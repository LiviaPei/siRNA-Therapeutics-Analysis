"""Source-preserving ingestion for the public siRNAEfficacyDB release.

This module creates a source-separated processed table, a field-mapping ledger,
and mechanical audit reports. It does not modify the raw download, merge sources,
train a model, or make biological inferences.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from src.data_quality import run_quality_checks


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIRECTORY = PROJECT_ROOT / "data" / "raw" / "siRNAEfficacyDB"
RAW_WORKBOOK = RAW_DIRECTORY / "siRNA_data.xlsx"
RAW_FASTA = RAW_DIRECTORY / "target gene sequence.fasta"
DATA_DICTIONARY = PROJECT_ROOT / "data_dictionary.csv"
PROCESSED_OUTPUT = PROJECT_ROOT / "data" / "processed" / "siRNAEfficacyDB_processed.csv"
MAPPING_OUTPUT = PROJECT_ROOT / "data_dictionary_mapping_siRNAEfficacyDB.csv"
RAW_AUDIT_OUTPUT = PROJECT_ROOT / "reports" / "siRNAEfficacyDB_raw_audit.md"
QUALITY_OUTPUT = PROJECT_ROOT / "reports" / "siRNAEfficacyDB_quality_report.md"
METADATA_OUTPUT = RAW_DIRECTORY / "source_metadata.json"

SOURCE_DATASET = "siRNAEfficacyDB"
SOURCE_URL = "https://figshare.com/articles/dataset/_b_Experimentally_Supported_siRNA_Efficacy_Dataset_b_/25908841"
SOURCE_DOWNLOAD_URL = "https://ndownloader.figshare.com/files/46578250"
SOURCE_FASTA_DOWNLOAD_URL = "https://ndownloader.figshare.com/files/46578241"
SOURCE_DATASET_NAME = "Experimentally Supported siRNA Efficacy Dataset"
SOURCE_LICENSE = "CC BY 4.0"
ACCESS_DATE = "2026-09-27"
NOT_REPORTED = "not_reported"
VALID_RNA_BASES = frozenset("AUGC")


def _sha256(path: Path) -> str:
    """Return a SHA-256 digest for one downloaded file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_value(value: Any) -> Any:
    """Convert pandas values to JSON-safe source-preserving values."""
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        return value.item()
    return value


def _text_or_not_reported(value: Any) -> str:
    """Return source text or the project's explicit missing-data sentinel."""
    if pd.isna(value) or str(value).strip() == "":
        return NOT_REPORTED
    return str(value)


def _parse_number_and_unit(value: Any) -> tuple[Any, str]:
    """Split an explicitly formatted source value into number and unit.

    Values are split only when the entire source value follows ``number + unit``.
    No unit conversion or unit inference is performed.
    """
    source_text = _text_or_not_reported(value)
    if source_text == NOT_REPORTED:
        return NOT_REPORTED, NOT_REPORTED

    match = re.fullmatch(
        r"\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*([^\d\s].*?)\s*",
        source_text,
    )
    if not match:
        return NOT_REPORTED, NOT_REPORTED

    number_text, unit = match.groups()
    return float(number_text), unit


def _load_unified_fields() -> list[str]:
    """Read unified field order from the frozen project data dictionary."""
    dictionary = pd.read_csv(DATA_DICTIONARY)
    return dictionary["field_name"].tolist()


def _raw_record_json(row: pd.Series) -> str:
    """Serialize every original spreadsheet field without dropping columns."""
    source_record = {column: _source_value(value) for column, value in row.items()}
    return json.dumps(source_record, ensure_ascii=False, separators=(",", ":"))


def build_processed_dataframe(raw_dataframe: pd.DataFrame) -> pd.DataFrame:
    """Map siRNAEfficacyDB rows into the existing unified source-aware schema."""
    concentration = raw_dataframe["Concentration"].map(_parse_number_and_unit)
    treatment_time = raw_dataframe["Hours"].map(_parse_number_and_unit)

    processed = pd.DataFrame(
        {
            "source_dataset": SOURCE_DATASET,
            "source_record_id": raw_dataframe["ID"].map(_text_or_not_reported),
            "provenance_url": SOURCE_URL,
            "source_raw_record": raw_dataframe.apply(_raw_record_json, axis=1),
            "source_raw_file": RAW_WORKBOOK.name,
            "target_gene": raw_dataframe["Gene"].map(_text_or_not_reported),
            "sense_sequence": raw_dataframe["Sense_19mer"].map(_text_or_not_reported),
            "antisense_sequence": raw_dataframe["Antisense_21mer"].map(_text_or_not_reported),
            "chemical_modification": NOT_REPORTED,
            "chemical_modification_reported": NOT_REPORTED,
            "modification_position": NOT_REPORTED,
            "activity_value": raw_dataframe["%Inhibition"],
            "activity_unit": "%",
            "activity_type": "%Inhibition",
            "assay_method": raw_dataframe["Technology"].map(_text_or_not_reported),
            "assay_method_reported": raw_dataframe["Technology"].map(_text_or_not_reported),
            "cell_line": raw_dataframe["Cell"].map(_text_or_not_reported),
            "cell_type": NOT_REPORTED,
            "concentration": [value for value, _ in concentration],
            "concentration_unit": [unit for _, unit in concentration],
            "treatment_time": [value for value, _ in treatment_time],
            "treatment_unit": [unit for _, unit in treatment_time],
            "reference": raw_dataframe["PMID"].map(_text_or_not_reported),
        }
    )

    unified_fields = _load_unified_fields()
    if list(processed.columns) != unified_fields:
        raise ValueError("Processed columns do not match the existing data dictionary.")
    return processed


def _mapping_rows() -> list[dict[str, str]]:
    """Return an explicit mapping ledger for every source column and gap."""
    rows = [
        {"original_field": "__dataset_metadata__", "mapped_field": "source_dataset", "notes": "Constant: siRNAEfficacyDB."},
        {"original_field": "ID", "mapped_field": "source_record_id", "notes": "Copied exactly; no local ID is generated."},
        {"original_field": "__dataset_metadata__", "mapped_field": "provenance_url", "notes": "Constant official Figshare dataset URL."},
        {"original_field": "__entire_source_row__", "mapped_field": "source_raw_record", "notes": "Every original field is serialized without dropping columns."},
        {"original_field": "__source_file__", "mapped_field": "source_raw_file", "notes": "Constant: siRNA_data.xlsx."},
        {"original_field": "Gene", "mapped_field": "target_gene", "notes": "Copied exactly as reported; no alias resolution."},
        {"original_field": "Sense_19mer", "mapped_field": "sense_sequence", "notes": "Copied exactly; no complementary strand is derived."},
        {"original_field": "Antisense_21mer", "mapped_field": "antisense_sequence", "notes": "Copied exactly; no complementary strand is derived."},
        {"original_field": "not_in_siRNAEfficacyDB", "mapped_field": "chemical_modification", "notes": "Set to literal not_reported; no chemistry is inferred."},
        {"original_field": "not_in_siRNAEfficacyDB", "mapped_field": "chemical_modification_reported", "notes": "Set to literal not_reported."},
        {"original_field": "not_in_siRNAEfficacyDB", "mapped_field": "modification_position", "notes": "Set to literal not_reported."},
        {"original_field": "%Inhibition", "mapped_field": "activity_value", "notes": "Copied without rescaling."},
        {"original_field": "%Inhibition", "mapped_field": "activity_unit", "notes": "Set to % because the source field name explicitly includes the percent symbol."},
        {"original_field": "%Inhibition", "mapped_field": "activity_type", "notes": "Set to exact source field label %Inhibition."},
        {"original_field": "Technology", "mapped_field": "assay_method", "notes": "Copied as explicit source-reported assay text."},
        {"original_field": "Technology", "mapped_field": "assay_method_reported", "notes": "Copied verbatim as source-reported assay text."},
        {"original_field": "Cell", "mapped_field": "cell_line", "notes": "Copied as reported; values are not split or reclassified."},
        {"original_field": "not_in_siRNAEfficacyDB", "mapped_field": "cell_type", "notes": "Set to literal not_reported."},
        {"original_field": "Concentration", "mapped_field": "concentration", "notes": "Extract only exact number-plus-unit source values; otherwise not_reported."},
        {"original_field": "Concentration", "mapped_field": "concentration_unit", "notes": "Extract only exact number-plus-unit source values; otherwise not_reported."},
        {"original_field": "Hours", "mapped_field": "treatment_time", "notes": "Extract only exact number-plus-unit source values; otherwise not_reported."},
        {"original_field": "Hours", "mapped_field": "treatment_unit", "notes": "Extract only exact number-plus-unit source values; otherwise not_reported."},
        {"original_field": "PMID", "mapped_field": "reference", "notes": "Copied exactly as a source reference identifier."},
    ]
    retained_only_fields = [
        "Accession_number", "Authors", "Gene_ID", "5.end dG", "3' end dG",
        "Sec.dG", "Hsieh", "Amarzguioui", "GC stretch", "Whole dG", "Katoh",
        "Takasaki", "Reynolds", "Ui-Tei", "%GC", "i-score", "Title", "Year",
        "Abstract", "Journal", "Pubdate",
    ]
    rows.extend(
        {
            "original_field": source_field,
            "mapped_field": NOT_REPORTED,
            "notes": "No direct unified field; retained losslessly in source_raw_record and the immutable raw workbook.",
        }
        for source_field in retained_only_fields
    )
    return rows


def _markdown_table(headers: Iterable[str], rows: Iterable[Iterable[Any]]) -> str:
    """Create a small Markdown table with safely escaped cell values."""
    header_list = list(headers)
    lines = [
        "| " + " | ".join(header_list) + " |",
        "| " + " | ".join("---" for _ in header_list) + " |",
    ]
    for row in rows:
        cells = [str(cell).replace("|", "\\|").replace("\n", " ") for cell in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_raw_audit(raw_dataframe: pd.DataFrame) -> None:
    """Write the requested source-file profile without changing raw values."""
    file_rows = []
    for path in (RAW_WORKBOOK, RAW_FASTA):
        file_rows.append((path.name, path.stat().st_size, _sha256(path)))
    column_rows = [
        (column, str(dtype), int(raw_dataframe[column].isna().sum()), f"{raw_dataframe[column].isna().mean():.2%}")
        for column, dtype in raw_dataframe.dtypes.items()
    ]
    text = f"""# siRNAEfficacyDB raw audit

## Source record

- Dataset name: {SOURCE_DATASET_NAME}
- Dataset URL: {SOURCE_URL}
- Direct data URL: {SOURCE_DOWNLOAD_URL}
- Access date: {ACCESS_DATE}
- License: {SOURCE_LICENSE}
- Workbook sheet: `all data`
- Raw table grain: one spreadsheet row per source `ID`; this has not been independently biologically validated.

## Downloaded files

{_markdown_table(["file", "size_bytes", "sha256"], file_rows)}

## Workbook structure

- Rows: {len(raw_dataframe)}
- Columns: {len(raw_dataframe.columns)}
- Column names: {", ".join(f'`{column}`' for column in raw_dataframe.columns)}

## Column types and missingness

{_markdown_table(["column", "pandas_dtype", "missing_count", "missing_rate"], column_rows)}

## Scope note

This is a structural audit of the unmodified downloaded workbook. It does not assess assay quality, biological activity, or therapeutic performance.
"""
    RAW_AUDIT_OUTPUT.write_text(text, encoding="utf-8")


def _sequence_invalid_mask(series: pd.Series) -> pd.Series:
    """Flag values that are missing or include bases outside uppercase A/U/G/C."""
    def is_invalid(value: Any) -> bool:
        if not isinstance(value, str) or value == NOT_REPORTED:
            return True
        normalized = "".join(value.upper().split())
        return not normalized or bool(set(normalized) - VALID_RNA_BASES)

    return series.map(is_invalid)


def write_quality_report(processed: pd.DataFrame) -> None:
    """Write mechanical completeness, duplication, sequence, and endpoint checks."""
    module_quality = run_quality_checks(processed)
    missing_rows = []
    for column in processed.columns:
        missing_mask = processed[column].isna() | processed[column].eq(NOT_REPORTED)
        missing_rows.append((column, int(missing_mask.sum()), f"{missing_mask.mean():.2%}"))

    duplicate_source_ids = processed.duplicated(
        subset=["source_dataset", "source_record_id"], keep=False
    )
    duplicate_exact_records = processed.duplicated(keep=False)
    duplicate_duplexes = processed.duplicated(
        subset=["sense_sequence", "antisense_sequence"], keep=False
    )
    invalid_sense = _sequence_invalid_mask(processed["sense_sequence"])
    invalid_antisense = _sequence_invalid_mask(processed["antisense_sequence"])
    activity_rows = processed["activity_type"].value_counts(dropna=False).items()

    text = f"""# siRNAEfficacyDB processed-data quality report

## Dataset and grain

- Source-separated dataset: `{SOURCE_DATASET}` only.
- Processed rows: {len(processed)}.
- Intended grain: one processed record per `source_dataset` + `source_record_id`.
- This report is mechanical data validation. It does not evaluate efficacy, compare experimental systems, or draw biological conclusions.

## Missing rate by unified field

`not_reported` is counted as missing because it denotes information not supplied by this source. It is an expected provenance-preserving value, not an inferred value.

{_markdown_table(["field", "missing_count", "missing_rate"], missing_rows)}

## Duplicate checks

| Check | Affected rows | Affected-row rate |
| --- | ---: | ---: |
| Duplicate source_dataset + source_record_id | {int(duplicate_source_ids.sum())} | {duplicate_source_ids.mean():.2%} |
| Exact duplicate processed records | {int(duplicate_exact_records.sum())} | {duplicate_exact_records.mean():.2%} |
| Repeated sense + antisense sequence pairs | {int(duplicate_duplexes.sum())} | {duplicate_duplexes.mean():.2%} |
| Repeated antisense sequences (`run_quality_checks`) | {module_quality['n_duplicate_sequence_rows']} | {module_quality['n_duplicate_sequence_rows'] / len(processed):.2%} |

Repeated sequence pairs are reported for review and are not removed or interpreted as an error.

## Sequence validity

Validity rule: a non-missing sequence must contain only A, U, G, and C after uppercasing and whitespace removal. The source sequence text is not altered by this check.

| Strand | Invalid or missing rows | Rate |
| --- | ---: | ---: |
| Sense | {int(invalid_sense.sum())} | {invalid_sense.mean():.2%} |
| Antisense | {int(invalid_antisense.sum())} | {invalid_antisense.mean():.2%} |

The reusable `src.data_quality.run_quality_checks` module was also run. It reported {len(module_quality['invalid_sense_sequence_rows'])} invalid sense rows and {len(module_quality['invalid_antisense_sequence_rows'])} invalid antisense rows.

## Activity-type distribution

{_markdown_table(["activity_type", "record_count"], activity_rows)}

## Interpretation boundary

No records were excluded, deduplicated, normalized across assays, or used for activity prediction. The dataset remains source-separated from CMsiRNAdb and all other sources.
"""
    QUALITY_OUTPUT.write_text(text, encoding="utf-8")


def write_mapping_ledger() -> None:
    """Write the requested original-field-to-unified-field mapping ledger."""
    with MAPPING_OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["original_field", "mapped_field", "notes"]
        )
        writer.writeheader()
        writer.writerows(_mapping_rows())


def write_metadata() -> None:
    """Record download provenance alongside immutable raw files."""
    metadata = {
        "dataset_name": SOURCE_DATASET_NAME,
        "source_dataset": SOURCE_DATASET,
        "dataset_url": SOURCE_URL,
        "data_download_url": SOURCE_DOWNLOAD_URL,
        "fasta_download_url": SOURCE_FASTA_DOWNLOAD_URL,
        "access_date": ACCESS_DATE,
        "license": SOURCE_LICENSE,
        "files": {
            RAW_WORKBOOK.name: {"sha256": _sha256(RAW_WORKBOOK)},
            RAW_FASTA.name: {"sha256": _sha256(RAW_FASTA)},
        },
    }
    METADATA_OUTPUT.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def main() -> None:
    """Run the reproducible siRNAEfficacyDB ingestion and audit workflow."""
    if not RAW_WORKBOOK.exists() or not RAW_FASTA.exists():
        raise FileNotFoundError("Expected raw siRNAEfficacyDB files are missing.")

    PROCESSED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    RAW_AUDIT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    raw_dataframe = pd.read_excel(RAW_WORKBOOK, sheet_name="all data")
    processed = build_processed_dataframe(raw_dataframe)

    write_metadata()
    write_raw_audit(raw_dataframe)
    write_mapping_ledger()
    processed.to_csv(PROCESSED_OUTPUT, index=False)
    write_quality_report(processed)


if __name__ == "__main__":
    main()
