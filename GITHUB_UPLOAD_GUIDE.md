# GitHub Upload Guide

This repository is prepared for a lightweight public release. The `.gitignore` keeps local raw siRNAEfficacyDB files and generated processed CSVs on the workstation while retaining source metadata, code, notebooks, reports, figures, and the small labelled toy dataset.

## Before the first commit

1. Review the staged file list and confirm that no credentials, local environments, checkpoints, or raw data files are included.
2. Confirm that the files intended to remain local are still present locally; Git ignore rules do not delete them.
3. Choose a license for the repository's original code and documentation. Review source-data terms separately before redistributing any external data.

## Suggested commands

Run these commands from the repository root after creating an empty GitHub repository. Replace the placeholder URL with your repository URL.

```powershell
git init
git add .
git status
git commit -m "Initial public release"
git branch -M main
git remote add origin https://github.com/<your-account>/siRNA-Therapeutics-Analysis.git
git push -u origin main
```

`git status` is intentionally included before the commit as a final safeguard. The commands above are documentation only; no remote or push operation has been performed for this project.

## Recommended GitHub repository contents

- Documentation: `README.md`, `PROJECT_OVERVIEW.md`, data dictionaries, and reports.
- Code: the `src/` modules and notebook sources.
- Demonstration assets: the explicit toy CSV and descriptive figures.
- Source traceability: `data/raw/siRNAEfficacyDB/source_metadata.json`.

## Keep local or retrieve from the original source

- `data/raw/siRNAEfficacyDB/siRNA_data.xlsx`
- `data/raw/siRNAEfficacyDB/target gene sequence.fasta`
- `data/processed/siRNAEfficacyDB_processed.csv`
- Python environments, cache folders, notebook checkpoints, and local editor configuration

The original public source and retrieval information are documented in `data/raw/siRNAEfficacyDB/source_metadata.json` and linked in the README.
