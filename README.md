# Computational Exploration of siRNA Therapeutics: From Sequence Features to Experimental Context

An educational, reproducible workflow for structuring and descriptively exploring public small interfering RNA (siRNA) data. The project focuses on transparent data preparation for nucleic-acid therapeutics: sequence features are considered alongside target, chemistry, and experimental context.

> **Scope:** This repository contains no trained prediction model, no prediction-performance claim, and no causal biological conclusion. Its analyses are exploratory descriptions of the included source data.

## Project overview

Public siRNA datasets are heterogeneous. Measurements can differ by target gene, strand representation, chemical modification, cell system, assay, concentration, treatment duration, and activity endpoint. This project provides a source-aware framework that preserves this context rather than treating every reported activity value as directly comparable.

The current implementation includes a documented ingestion pathway for siRNAEfficacyDB, quality-control reporting, RNA sequence-feature extraction, and a reproducible exploratory notebook. A small explicitly labelled toy dataset remains for learning the basic workflow.

## Biological background

siRNAs are short double-stranded RNAs that can reduce complementary messenger RNA abundance through RNA interference (RNAi). Following cellular delivery, a guide (antisense) strand can be retained in the RNA-induced silencing complex (RISC). Argonaute-2 (AGO2) uses this guide to recognise complementary target transcripts and support gene silencing.

This mechanism makes siRNA an important modality in nucleic-acid therapeutics. Its experimental activity, however, cannot be understood from sequence alone: delivery, chemical design, target biology, cellular context, and assay design also matter.

## Computational workflow

```text
Public siRNA database
        ↓
Source-aware data harmonization
        ↓
Quality control and provenance audit
        ↓
Sequence feature extraction
        ↓
Experimental-context exploration
        ↓
Foundation for future modeling
```

The harmonised schema is defined in [`data_dictionary.csv`](data_dictionary.csv). It retains source identity and raw-record provenance while keeping source-specific endpoint definitions and missing fields explicit. Missing information is represented as `not_reported`; it is never inferred.

## Data sources

| Source | Current use | Provenance and access |
| --- | --- | --- |
| siRNAEfficacyDB / *Experimentally Supported siRNA Efficacy Dataset* | First real-data integration; 3,544 source records are represented in the processed local dataset. | [Figshare dataset page](https://figshare.com/articles/dataset/_b_Experimentally_Supported_siRNA_Efficacy_Dataset_b_/25908841); accessed 2026-09-27; source metadata records CC BY 4.0. |
| CMsiRNAdb | Schema-design candidate only; not downloaded or integrated. | Kept source-separated for any future work. |
| Example siRNA dataset | Small toy input used to demonstrate the initial pipeline. | [`data/raw/example_sirna_dataset.csv`](data/raw/example_sirna_dataset.csv); not experimental evidence. |

The raw siRNAEfficacyDB workbook and FASTA file are intentionally retained locally but ignored by Git. Their retrieval URLs, access date, license, and checksums are preserved in [`data/raw/siRNAEfficacyDB/source_metadata.json`](data/raw/siRNAEfficacyDB/source_metadata.json). The processed CSV is also ignored because it is a generated derivative. This keeps the repository lightweight and directs users to the original public source.

siRNAEfficacyDB and CMsiRNAdb must remain source-separated rather than being pooled into one activity benchmark: their reported chemistry, curation origins, endpoint definitions, and experimental contexts can be non-comparable.

## Current progress

- Defined a 23-field source-aware unified schema and a siRNAEfficacyDB field-mapping table.
- Integrated 3,544 siRNAEfficacyDB source records locally, retaining raw-record provenance and source-specific fields.
- Performed documented data-quality checks for missingness, duplicate records, nucleotide validity, and source activity-type distribution.
- Built reusable RNA sequence-feature utilities for length, GC content, nucleotide fractions, 5′ base, and seed region.
- Created a reproducible exploratory notebook and descriptive figures for sequence length, GC content, target frequency, and the source-reported activity value distribution.
- Added a public-information case-study summary of selected approved siRNA therapeutics for clinical-translational context.

See [`reports/sirnaefficacydb_exploration_summary.md`](reports/sirnaefficacydb_exploration_summary.md) for the descriptive analysis and [`reports/approved_sirna_therapeutics_case_study.md`](reports/approved_sirna_therapeutics_case_study.md) for the clinical context. These materials do not assert sequence rules or causal effects.

## Repository structure

```text
siRNA-Therapeutics-Analysis/
├── data/
│   ├── raw/                         # Toy input and source metadata; large raw files stay local
│   └── processed/                   # Locally generated harmonised datasets (Git-ignored)
├── figures/                         # Exported descriptive figures
├── notebooks/                       # Reproducible exploratory notebooks
├── reports/                         # Audits, summaries, and case-study notes
├── src/                             # Data ingestion, QC, and sequence-feature modules
├── data_dictionary.csv              # Source-aware unified-schema definition
├── data_dictionary_mapping_siRNAEfficacyDB.csv
├── PROJECT_OVERVIEW.md              # Interview-oriented project summary
├── GITHUB_UPLOAD_GUIDE.md           # Suggested publication workflow
├── requirements.txt
└── README.md
```

## Getting started

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter notebook notebooks/01_dataset_exploration.ipynb
```

For the real-data workflow, first retrieve the public siRNAEfficacyDB source files documented in `source_metadata.json` into `data/raw/siRNAEfficacyDB/`. Then run:

```powershell
python -m src.ingest_sirna_efficacydb
jupyter notebook notebooks/02_sirnaefficacydb_exploration.ipynb
```

The second command regenerates derived outputs locally. It is not required to browse the repository's source code, reports, or exported figures.

## Future directions

Once additional sources are carefully harmonised and held out by study/source where appropriate, this foundation could support:

- activity-prediction research with leakage-aware validation;
- off-target and transcript-context modelling;
- structured assessment of reported chemical modifications; and
- context-aware candidate prioritisation.

These are future directions, not completed capabilities.

## Responsible reuse

The repository is a computational learning and data-engineering project, not therapeutic or clinical guidance. Before publication, choose a license for this repository's original code and documentation, and review the terms of every external data source before redistributing source material.
