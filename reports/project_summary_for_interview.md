# Project Overview

**Computational Exploration of siRNA Therapeutics: From Sequence Features to Experimental Context** is a reproducible data workflow for learning how public siRNA evidence can be made usable for computational analysis. The project was selected because siRNA therapeutics sit at a productive intersection of target biology, sequence design, experimental perturbation, and delivery/chemistry constraints.

For an interview narrative, this work can be connected to prior AIDD experience, transcriptomics, and perturbation biology **only where that accurately reflects the candidate’s own background**. The shared theme is the need to move from biological measurements and perturbations to structured, traceable computational evidence. In this project, nucleic-acid therapeutics add a further layer: siRNA activity depends on both sequence and experimental context.

# Biological Background

siRNA is a short double-stranded RNA modality used to reduce expression of a complementary messenger RNA (mRNA). Through RNA interference (RNAi), a guide strand is loaded into the RNA-induced silencing complex (RISC). Argonaute 2 (AGO2) within this machinery uses guide-target complementarity to promote target-mRNA silencing. Reduced target mRNA can reduce production of the encoded protein.

This mechanism makes siRNA therapeutics conceptually relevant to perturbation biology: an explicit molecular intervention is connected to a defined transcript and downstream biological readout. Translation to medicines also requires attention to delivery, chemical modification, tissue/cell context, and the endpoint used to measure activity.

# Computational Workflow

```text
Public siRNA database
        ↓
Source-aware data harmonization
        ↓
Quality control
        ↓
Sequence feature extraction
        ↓
Experimental context exploration
        ↓
Future modeling foundation
```

The workflow preserves source identifiers, raw source rows, original activity labels/units, and unreported fields. This prevents incompatible experimental records from being silently treated as one uniform activity benchmark.

# Current Results

The project currently includes one real, source-separated public dataset: **siRNAEfficacyDB**.

- Integrated **3,544** records from the source-preserved public release.
- Retained **42** source-reported target-gene labels without identifier normalization.
- Performed sequence quality checks; the processed dataset has sequence fields for all records and no sequences failing the project’s A/U/G/C validity rule after uppercase/whitespace normalization for validation.
- Implemented source-aware schema fields, raw-file metadata, a raw audit, an explicit mapping ledger, and a processed-data quality report.
- Generated descriptive exploratory analyses for sequence length, GC content, nucleotide composition, target-frequency distribution, and the source-reported activity-value distribution.

These are workflow outputs and observed distributions. They do **not** establish biological rules, causal effects of sequence features, therapeutic efficacy, or cross-dataset comparability.

# Future Directions

Once additional data have been curated and comparability assumptions have been documented, the framework could support carefully scoped extensions:

- Activity prediction with source-aware splits and independent validation.
- Off-target modeling using guide/seed and transcriptome context.
- Chemical-modification representation and optimization, using datasets with explicit modification annotations.
- Candidate prioritization that integrates target biology, delivery constraints, experimental context, and uncertainty rather than sequence alone.

These directions are intentionally future work. They are not implemented in the current project.
