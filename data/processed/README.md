# Generated processed data

Processed datasets are generated locally from public source files and are intentionally excluded from version control. This avoids redistributing derived records while keeping the repository lightweight.

To recreate the current siRNAEfficacyDB processed dataset, retrieve the public raw files described in `data/raw/siRNAEfficacyDB/source_metadata.json` and run:

```powershell
python -m src.ingest_sirna_efficacydb
```

The command writes `siRNAEfficacyDB_processed.csv` to this directory together with the related audits and mapping ledger in their documented locations.
