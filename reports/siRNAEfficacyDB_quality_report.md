# siRNAEfficacyDB processed-data quality report

## Dataset and grain

- Source-separated dataset: `siRNAEfficacyDB` only.
- Processed rows: 3544.
- Intended grain: one processed record per `source_dataset` + `source_record_id`.
- This report is mechanical data validation. It does not evaluate efficacy, compare experimental systems, or draw biological conclusions.

## Missing rate by unified field

`not_reported` is counted as missing because it denotes information not supplied by this source. It is an expected provenance-preserving value, not an inferred value.

| field | missing_count | missing_rate |
| --- | --- | --- |
| source_dataset | 0 | 0.00% |
| source_record_id | 0 | 0.00% |
| provenance_url | 0 | 0.00% |
| source_raw_record | 0 | 0.00% |
| source_raw_file | 0 | 0.00% |
| target_gene | 0 | 0.00% |
| sense_sequence | 0 | 0.00% |
| antisense_sequence | 0 | 0.00% |
| chemical_modification | 3544 | 100.00% |
| chemical_modification_reported | 3544 | 100.00% |
| modification_position | 3544 | 100.00% |
| activity_value | 0 | 0.00% |
| activity_unit | 0 | 0.00% |
| activity_type | 0 | 0.00% |
| assay_method | 0 | 0.00% |
| assay_method_reported | 0 | 0.00% |
| cell_line | 0 | 0.00% |
| cell_type | 3544 | 100.00% |
| concentration | 0 | 0.00% |
| concentration_unit | 0 | 0.00% |
| treatment_time | 0 | 0.00% |
| treatment_unit | 0 | 0.00% |
| reference | 0 | 0.00% |

## Duplicate checks

| Check | Affected rows | Affected-row rate |
| --- | ---: | ---: |
| Duplicate source_dataset + source_record_id | 0 | 0.00% |
| Exact duplicate processed records | 0 | 0.00% |
| Repeated sense + antisense sequence pairs | 44 | 1.24% |
| Repeated antisense sequences (`run_quality_checks`) | 44 | 1.24% |

Repeated sequence pairs are reported for review and are not removed or interpreted as an error.

## Sequence validity

Validity rule: a non-missing sequence must contain only A, U, G, and C after uppercasing and whitespace removal. The source sequence text is not altered by this check.

| Strand | Invalid or missing rows | Rate |
| --- | ---: | ---: |
| Sense | 0 | 0.00% |
| Antisense | 0 | 0.00% |

The reusable `src.data_quality.run_quality_checks` module was also run. It reported 0 invalid sense rows and 0 invalid antisense rows.

## Activity-type distribution

| activity_type | record_count |
| --- | --- |
| %Inhibition | 3544 |

## Interpretation boundary

No records were excluded, deduplicated, normalized across assays, or used for activity prediction. The dataset remains source-separated from CMsiRNAdb and all other sources.
