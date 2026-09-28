# siRNAEfficacyDB raw audit

## Source record

- Dataset name: Experimentally Supported siRNA Efficacy Dataset
- Dataset URL: https://figshare.com/articles/dataset/_b_Experimentally_Supported_siRNA_Efficacy_Dataset_b_/25908841
- Direct data URL: https://ndownloader.figshare.com/files/46578250
- Access date: 2026-09-27
- License: CC BY 4.0
- Workbook sheet: `all data`
- Raw table grain: one spreadsheet row per source `ID`; this has not been independently biologically validated.

## Downloaded files

| file | size_bytes | sha256 |
| --- | --- | --- |
| siRNA_data.xlsx | 594693 | 6a2d01cdbc4d522ea783d164868266883f3cdb5ca1b267f4959ad224926bfd47 |
| target gene sequence.fasta | 196534 | 37238b168a26045eb5fa00402ee4cf0a41e82e054df8554e4f031a4a448c5c67 |

## Workbook structure

- Rows: 3544
- Columns: 31
- Column names: `ID`, `Accession_number`, `Authors`, `Gene`, `Gene_ID`, `Antisense_21mer`, `Sense_19mer`, `5.end dG`, `3' end dG`, `Sec.dG`, `Hsieh`, `Amarzguioui`, `GC stretch`, `Whole dG`, `Katoh`, `Takasaki`, `Reynolds`, `Ui-Tei`, `%GC`, `i-score`, `%Inhibition`, `Technology`, `Cell`, `Concentration`, `Hours`, `Title`, `PMID`, `Year`, `Abstract`, `Journal`, `Pubdate`

## Column types and missingness

| column | pandas_dtype | missing_count | missing_rate |
| --- | --- | --- | --- |
| ID | str | 0 | 0.00% |
| Accession_number | str | 0 | 0.00% |
| Authors | str | 0 | 0.00% |
| Gene | str | 0 | 0.00% |
| Gene_ID | object | 0 | 0.00% |
| Antisense_21mer | str | 0 | 0.00% |
| Sense_19mer | str | 0 | 0.00% |
| 5.end dG | float64 | 0 | 0.00% |
| 3' end dG | float64 | 0 | 0.00% |
| Sec.dG | float64 | 41 | 1.16% |
| Hsieh | int64 | 0 | 0.00% |
| Amarzguioui | int64 | 0 | 0.00% |
| GC stretch | int64 | 0 | 0.00% |
| Whole dG | float64 | 0 | 0.00% |
| Katoh | float64 | 0 | 0.00% |
| Takasaki | float64 | 0 | 0.00% |
| Reynolds | int64 | 0 | 0.00% |
| Ui-Tei | str | 0 | 0.00% |
| %GC | float64 | 0 | 0.00% |
| i-score | float64 | 0 | 0.00% |
| %Inhibition | float64 | 0 | 0.00% |
| Technology | str | 0 | 0.00% |
| Cell | str | 0 | 0.00% |
| Concentration | str | 0 | 0.00% |
| Hours | str | 0 | 0.00% |
| Title | str | 0 | 0.00% |
| PMID | int64 | 0 | 0.00% |
| Year | int64 | 0 | 0.00% |
| Abstract | str | 0 | 0.00% |
| Journal | str | 0 | 0.00% |
| Pubdate | datetime64[us] | 0 | 0.00% |

## Scope note

This is a structural audit of the unmodified downloaded workbook. It does not assess assay quality, biological activity, or therapeutic performance.
