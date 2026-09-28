# Project Overview: Computational Exploration of siRNA Therapeutics

## Motivation

siRNA therapeutics sit at the intersection of molecular biology, data engineering, and drug development. They are a useful computational-biology case because a reported activity measurement is shaped by more than a nucleotide sequence: target selection, chemistry, delivery-related design, cell context, assay choice, concentration, and treatment duration can all affect how a record should be interpreted.

This project was designed as an interview-ready example of how experience with AIDD-adjacent data work, transcriptomics, and perturbation biology can transfer to nucleic-acid therapeutics. The objective is not to claim a predictive model; it is to build a trustworthy foundation for future modelling.

## Methodology

1. **Preserve source provenance.** A source-aware unified schema records dataset identity, source-record IDs, URLs, raw-record content, and source-specific reported fields. Unavailable fields use `not_reported` rather than inferred values.
2. **Harmonise without over-normalising.** siRNAEfficacyDB is integrated through a documented field mapping. Sources with potentially non-comparable endpoints or chemistry are not pooled into a single activity benchmark.
3. **Audit data quality.** The pipeline reports missingness, duplicate records, RNA nucleotide validity, and source activity-type distributions before exploration.
4. **Extract interpretable sequence features.** Reusable utilities calculate length, GC content, nucleotide fractions, 5′ base, and seed region from RNA sequences.
5. **Use descriptive exploration.** The notebook presents observed distributions for sequence, target labels, and source-reported activity values, without causal or therapeutic claims.

## Key outcomes

- A 23-field source-aware data dictionary and a dataset-specific mapping table.
- Local integration of 3,544 siRNAEfficacyDB source records spanning 42 source target-gene labels.
- Reproducible quality-control reports and an exploratory notebook with exported figures.
- Separation of raw source data, generated processed data, and lightweight version-controlled documentation for reproducible public sharing.
- A concise case study of selected approved siRNA medicines to connect the computational workflow with clinical translation.

## What this demonstrates

The repository demonstrates practical computational-biology habits: careful provenance tracking, explicit missing-data handling, modular Python utilities, reproducible notebooks, and restrained interpretation of heterogeneous public data. It provides a defensible starting point for later work on activity prediction, off-target assessment, reported-modification analysis, or candidate prioritisation—only after additional curation and appropriate validation design.

## Project boundaries

No model has been trained. No prediction performance is reported. No sequence feature, target, or experimental attribute is presented as causing siRNA activity. All completed analyses are exploratory and source-specific.
