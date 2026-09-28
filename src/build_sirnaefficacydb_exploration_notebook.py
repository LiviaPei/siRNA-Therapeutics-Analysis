"""Build the reproducible descriptive siRNAEfficacyDB exploration notebook."""

from pathlib import Path

import nbformat as nbf


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_NOTEBOOK = PROJECT_ROOT / "notebooks" / "02_sirnaefficacydb_exploration.ipynb"


def markdown(text: str):
    """Create a Markdown notebook cell."""
    return nbf.v4.new_markdown_cell(text)


def code(text: str):
    """Create a Python notebook cell."""
    return nbf.v4.new_code_cell(text)


def build_notebook() -> nbf.NotebookNode:
    """Create a source-separated, descriptive analysis notebook."""
    notebook = nbf.v4.new_notebook()
    notebook["cells"] = [
        markdown(
            "# siRNAEfficacyDB exploratory analysis\n\n"
            "This notebook describes the observed structure of the processed "
            "siRNAEfficacyDB records. It does not train a model, evaluate "
            "causality, or establish sequence-design rules."
        ),
        markdown(
            "## tl;dr\n\n"
            "- This source-separated descriptive analysis contains **3,544** "
            "processed siRNAEfficacyDB records across **42** source-reported "
            "target genes.\n"
            "- Both strand fields are available for all records. The observed "
            "source-reported activity values span **-27.8 to 134.1** on the "
            "source `%Inhibition` scale.\n"
            "- Sequence length, GC content, nucleotide composition, target "
            "frequency, and activity values are shown as observed distributions only. "
            "They do not support causal claims or activity prediction."
        ),
        markdown(
            "## Context & Methods\n\n"
            "### Source and scope\n\n"
            "Input: `data/processed/siRNAEfficacyDB_processed.csv`, generated "
            "from the source-preserved siRNAEfficacyDB download. This notebook "
            "uses this source alone and does not merge CMsiRNAdb or any other dataset.\n\n"
            "### Key assumptions\n\n"
            "- `activity_value`, `activity_unit`, and `activity_type` retain the "
            "source-reported endpoint and scale; no cross-assay normalization is performed.\n"
            "- Basic sequence features are calculated from `antisense_sequence`. "
            "The feature utility uppercases sequence text for calculation only; source "
            "sequence strings remain unchanged in the processed dataset.\n"
            "- Target names, assay text, and cell-line text are source-reported labels. "
            "No identifier resolution, ontology mapping, or biological interpretation is attempted."
        ),
        code(
            "from pathlib import Path\n"
            "import sys\n\n"
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n"
            "import seaborn as sns\n\n"
            "PROJECT_ROOT = Path.cwd().resolve()\n"
            "if PROJECT_ROOT.name == 'notebooks':\n"
            "    PROJECT_ROOT = PROJECT_ROOT.parent\n"
            "if str(PROJECT_ROOT) not in sys.path:\n"
            "    sys.path.insert(0, str(PROJECT_ROOT))\n\n"
            "from src.sequence_features import add_sequence_features\n\n"
            "DATA_PATH = PROJECT_ROOT / 'data' / 'processed' / 'siRNAEfficacyDB_processed.csv'\n"
            "FIGURE_DIRECTORY = PROJECT_ROOT / 'figures'\n"
            "REPORT_PATH = PROJECT_ROOT / 'reports' / 'sirnaefficacydb_exploration_summary.md'\n"
            "FIGURE_DIRECTORY.mkdir(exist_ok=True)\n"
            "REPORT_PATH.parent.mkdir(exist_ok=True)\n\n"
            "sns.set_theme(style='whitegrid', context='notebook')\n"
            "PLOT_COLOR = '#386FA4'\n"
            "ACCENT_COLOR = '#C57B57'"
        ),
        markdown("## Data\n\n### 1. Load the source-separated processed dataset"),
        code(
            "sirna_df = pd.read_csv(DATA_PATH, keep_default_na=False)\n"
            "expected_source = {'siRNAEfficacyDB'}\n"
            "assert set(sirna_df['source_dataset']) == expected_source, 'Unexpected source mixing detected.'\n"
            "assert len(sirna_df.columns) == 23, 'Unexpected unified schema width.'\n"
            "sirna_df.head(3)"
        ),
        markdown("## Results\n\n### 2. Dataset overview"),
        code(
            "activity_values = pd.to_numeric(sirna_df['activity_value'], errors='coerce')\n"
            "sequence_available = {\n"
            "    'sense_sequence': int(sirna_df['sense_sequence'].ne('not_reported').sum()),\n"
            "    'antisense_sequence': int(sirna_df['antisense_sequence'].ne('not_reported').sum()),\n"
            "}\n"
            "overview = pd.DataFrame({\n"
            "    'metric': ['number of records', 'number of target genes', 'sense sequences available', 'antisense sequences available', 'activity values available'],\n"
            "    'value': [\n"
            "        len(sirna_df),\n"
            "        sirna_df['target_gene'].nunique(),\n"
            "        sequence_available['sense_sequence'],\n"
            "        sequence_available['antisense_sequence'],\n"
            "        int(activity_values.notna().sum()),\n"
            "    ],\n"
            "})\n"
            "display(overview)\n"
            "display(sirna_df['activity_type'].value_counts(dropna=False).rename('record_count').to_frame())"
        ),
        markdown("### 3. Sequence analysis\n\nFeatures below are descriptive calculations on the antisense strand."),
        code(
            "feature_df = add_sequence_features(sirna_df, sequence_column='antisense_sequence')\n"
            "sequence_summary = feature_df[[\n"
            "    'sequence_length', 'GC_content', 'A_fraction', 'U_fraction', 'G_fraction', 'C_fraction'\n"
            "]].describe().T\n"
            "display(sequence_summary)\n\n"
            "mean_composition = (\n"
            "    feature_df[['A_fraction', 'U_fraction', 'G_fraction', 'C_fraction']]\n"
            "    .mean()\n"
            "    .rename(lambda label: label[0])\n"
            "    .rename('mean_fraction')\n"
            "    .to_frame()\n"
            ")\n"
            "display(mean_composition)"
        ),
        code(
            "fig, ax = plt.subplots(figsize=(7, 4.5))\n\n"
            "sns.histplot(\n"
            "    data=feature_df, x='sequence_length', discrete=True, color=PLOT_COLOR, ax=ax\n"
            ")\n"
            "ax.set(\n"
            "    title='Observed antisense sequence-length distribution\\nsiRNAEfficacyDB (descriptive)',\n"
            "    xlabel='Sequence length (nt)', ylabel='Record count'\n"
            ")\n\n"
            "fig.tight_layout()\n"
            "fig.savefig(FIGURE_DIRECTORY / 'siRNAEfficacyDB_sequence_length_distribution.png', dpi=250, bbox_inches='tight')\n"
            "plt.show()\n\n"
            "fig, ax = plt.subplots(figsize=(7, 4.5))\n\n"
            "sns.histplot(data=feature_df, x='GC_content', bins=20, color=ACCENT_COLOR, ax=ax)\n"
            "ax.set(\n"
            "    title='Observed antisense GC-content distribution\\nsiRNAEfficacyDB (descriptive)',\n"
            "    xlabel='GC content', ylabel='Record count'\n"
            ")\n\n"
            "fig.tight_layout()\n"
            "fig.savefig(FIGURE_DIRECTORY / 'siRNAEfficacyDB_gc_content_distribution.png', dpi=250, bbox_inches='tight')\n"
            "plt.show()"
        ),
        markdown("### 4. Target analysis\n\nTarget labels are retained exactly as reported by the source."),
        code(
            "top_targets = sirna_df['target_gene'].value_counts().head(15)\n"
            "top_target_table = top_targets.rename_axis('target_gene').rename('record_count').to_frame()\n"
            "top_target_table['record_share'] = top_target_table['record_count'] / len(sirna_df)\n"
            "display(top_target_table.style.format({'record_share': '{:.1%}'}))"
        ),
        code(
            "plot_targets = top_targets.sort_values()\n"
            "fig, ax = plt.subplots(figsize=(9, 6))\n"
            "ax.barh(plot_targets.index, plot_targets.values, color=PLOT_COLOR)\n"
            "ax.set(\n"
            "    title='Most frequent source-reported target genes\\nsiRNAEfficacyDB (top 15, descriptive)',\n"
            "    xlabel='Record count', ylabel='Target gene'\n"
            ")\n"
            "fig.tight_layout()\n"
            "fig.savefig(FIGURE_DIRECTORY / 'siRNAEfficacyDB_top_target_genes.png', dpi=250, bbox_inches='tight')\n"
            "plt.show()"
        ),
        markdown("### 5. Activity analysis\n\nThe histogram displays the source-reported `%Inhibition` values without rescaling."),
        code(
            "activity_summary = activity_values.describe().to_frame(name='activity_value')\n"
            "activity_range = pd.DataFrame({\n"
            "    'minimum': [activity_values.min()],\n"
            "    'maximum': [activity_values.max()],\n"
            "    'range_width': [activity_values.max() - activity_values.min()],\n"
            "}, index=['source-reported %Inhibition'])\n"
            "display(activity_summary)\n"
            "display(activity_range)"
        ),
        code(
            "fig, ax = plt.subplots(figsize=(8, 4.5))\n"
            "sns.histplot(activity_values.dropna(), bins=30, color=ACCENT_COLOR, ax=ax)\n"
            "ax.set(\n"
            "    title='Observed source-reported activity-value distribution\\nsiRNAEfficacyDB (descriptive)',\n"
            "    xlabel='Activity value (%Inhibition)', ylabel='Record count'\n"
            ")\n"
            "fig.tight_layout()\n"
            "fig.savefig(FIGURE_DIRECTORY / 'siRNAEfficacyDB_activity_value_distribution.png', dpi=250, bbox_inches='tight')\n"
            "plt.show()"
        ),
        markdown(
            "## Takeaways\n\n"
            "- The notebook presents observed distributions for records from one public source.\n"
            "- It does not claim that any sequence feature causes a particular activity value.\n"
            "- Reported target frequencies reflect this source dataset and should not be interpreted as therapeutic prevalence or target importance.\n"
            "- Activity values retain the source endpoint and should not be treated as a cross-dataset benchmark without a separate comparability review."
        ),
        markdown("### 6. Write the descriptive summary report"),
        code(
            "def markdown_table(frame, float_format=None):\n"
            "    if float_format is None:\n"
            "        return frame.to_markdown()\n"
            "    return frame.to_markdown(floatfmt=float_format)\n\n"
            "report_lines = [\n"
            "    '# siRNAEfficacyDB exploratory analysis summary',\n"
            "    '',\n"
            "    '## Scope',\n"
            "    '',\n"
            "    'This is a source-separated descriptive analysis of `siRNAEfficacyDB_processed.csv`. It contains no predictive model, causal inference, cross-source pooling, or biological efficacy claim.',\n"
            "    '',\n"
            "    '## Dataset overview',\n"
            "    '',\n"
            "    markdown_table(overview, float_format='.3f'),\n"
            "    '',\n"
            "    '### Activity type distribution',\n"
            "    '',\n"
            "    markdown_table(sirna_df['activity_type'].value_counts(dropna=False).rename('record_count').to_frame()),\n"
            "    '',\n"
            "    '## Observed sequence distributions',\n"
            "    '',\n"
            "    'Features were calculated descriptively from the antisense strand.',\n"
            "    '',\n"
            "    '### Sequence length and GC content',\n"
            "    '',\n"
            "    markdown_table(sequence_summary.loc[['sequence_length', 'GC_content']].round(3), float_format='.3f'),\n"
            "    '',\n"
            "    '### Mean nucleotide composition',\n"
            "    '',\n"
            "    markdown_table(mean_composition.round(3), float_format='.3f'),\n"
            "    '',\n"
            "    '## Observed target distribution',\n"
            "    '',\n"
            "    'Top source-reported target labels are shown without gene-name normalization.',\n"
            "    '',\n"
            "    markdown_table(top_target_table.head(10).round({'record_share': 3}), float_format='.3f'),\n"
            "    '',\n"
            "    '## Observed activity distribution',\n"
            "    '',\n"
            "    markdown_table(activity_summary.round(3), float_format='.3f'),\n"
            "    '',\n"
            "    markdown_table(activity_range.round(3), float_format='.3f'),\n"
            "    '',\n"
            "    '## Interpretation boundary',\n"
            "    '',\n"
            "    'All values and figures are observed distributions in this source. They do not show that a sequence feature causes activity, do not establish a biological mechanism, and do not constitute an activity benchmark across databases.',\n"
            "]\n"
            "REPORT_PATH.write_text('\\n'.join(report_lines) + '\\n', encoding='utf-8')\n"
            "print(f'Wrote descriptive summary: {REPORT_PATH}')"
        ),
    ]
    notebook["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.x"},
    }
    return notebook


def main() -> None:
    """Write the notebook in nbformat rather than hand-editing JSON."""
    OUTPUT_NOTEBOOK.parent.mkdir(exist_ok=True)
    nbf.write(build_notebook(), OUTPUT_NOTEBOOK)


if __name__ == "__main__":
    main()
