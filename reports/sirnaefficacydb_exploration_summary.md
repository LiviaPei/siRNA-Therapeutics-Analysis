# siRNAEfficacyDB exploratory analysis summary

## Scope

This is a source-separated descriptive analysis of `siRNAEfficacyDB_processed.csv`. It contains no predictive model, causal inference, cross-source pooling, or biological efficacy claim.

## Dataset overview

|    | metric                        |   value |
|---:|:------------------------------|--------:|
|  0 | number of records             |    3544 |
|  1 | number of target genes        |      42 |
|  2 | sense sequences available     |    3544 |
|  3 | antisense sequences available |    3544 |
|  4 | activity values available     |    3544 |

### Activity type distribution

|             |   record_count |
|:------------|---------------:|
| %Inhibition |           3544 |

## Observed sequence distributions

Features were calculated descriptively from the antisense strand.

### Sequence length and GC content

|                 |    count |   mean |   std |    min |    25% |    50% |    75% |    max |
|:----------------|---------:|-------:|------:|-------:|-------:|-------:|-------:|-------:|
| sequence_length | 3544.000 | 20.604 | 0.797 | 19.000 | 21.000 | 21.000 | 21.000 | 21.000 |
| GC_content      | 3544.000 |  0.525 | 0.129 |  0.143 |  0.429 |  0.524 |  0.619 |  0.952 |

### Mean nucleotide composition

|    |   mean_fraction |
|:---|----------------:|
| A  |           0.208 |
| U  |           0.267 |
| G  |           0.267 |
| C  |           0.257 |

## Observed target distribution

Top source-reported target labels are shown without gene-name normalization.

| target_gene        |   record_count |   record_share |
|:-------------------|---------------:|---------------:|
| EGFP               |        702.000 |          0.198 |
| Mmp7               |        150.000 |          0.042 |
| C6orf110           |        145.000 |          0.041 |
| TCAP               |        144.000 |          0.041 |
| RAB6IP1            |        126.000 |          0.036 |
| Cyclophilin B      |         90.000 |          0.025 |
| P2RX3              |         90.000 |          0.025 |
| Firefly luciferase |         87.000 |          0.025 |
| UBE2G1             |         79.000 |          0.022 |
| UBE2N              |         79.000 |          0.022 |

## Observed activity distribution

|       |   activity_value |
|:------|-----------------:|
| count |         3544.000 |
| mean  |           65.100 |
| std   |           22.802 |
| min   |          -27.800 |
| 25%   |           50.152 |
| 50%   |           67.000 |
| 75%   |           82.525 |
| max   |          134.100 |

|                             |   minimum |   maximum |   range_width |
|:----------------------------|----------:|----------:|--------------:|
| source-reported %Inhibition |   -27.800 |   134.100 |       161.900 |

## Interpretation boundary

All values and figures are observed distributions in this source. They do not show that a sequence feature causes activity, do not establish a biological mechanism, and do not constitute an activity benchmark across databases.
