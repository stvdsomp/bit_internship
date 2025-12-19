# nf-core/pacvar Excel report generator (HPC version)
This folder contains Python scripts for formatting ``nf-core/pacvar`` outputs and generating Excel reports on HPC environments.

## Files
- `color_motifs_test.py` - Python script to test the visualization of motifs
- `generate_puretarget_xlsx_report_v*.py` - Python script for generating Excel reports
- `run_color_motifs_test.sh` - shell wrapper to run the motif visualization tests
- `run_puretarget_xlsx_report_v*.sh` - shell wrapper to run the report script

## Versions
- `v1` - Generates one Excel file for each repeat of interest defined in the samplesheet. This approach ensures that only the genotype of the targeted repeat is visible to lab technicians and supervisors, minimizing exposure to incidental findings.
- `v2` - Generates a single comprehensive Excel file containing genotypes for all repeats present in the VCF output of `nf-core/pacvar`. A menu sheet with dropdown menu and hyperlink will guide users to the repeat of interest, while still limiting the risk of incidental findings.

## Functionality (v2)
This script generates an Excel (XLSX) report summarizing tandem repeat genotypes from a VCF file produced by the `nf-core/pacvar` pipeline.

For each sample in the samplesheet, the script parses the TRGT VCF output and creates a structured, user-friendly Excel report with:
-	A menu sheet for easy navigation between repeats, containing:
    - A dropdown list to select a repeat
    - A clickable hyperlink to jump to the selected repeat sheet
-	One worksheet per tandem repeat, including allele-specific information:
    - Repeat length and length range
    - Read support
    - Motif counts and motif spans
    - Purity and methylation
    - Color-highlighted repeat motifs within sequences
The resulting report is intended for downstream interpretation and clinical review.
Note: This script does not include motif or methylation plots.

## Input
- Samplesheet (CSV)
    - Contains at least a sample column with sample names matching the VCF filenames

Example: 
```bash
sample
sample1
sample2
```
- Output directory
    - The main output directory produced by the `nf-core/pacvar` pipeline
    - The script assumes the presence of a trgt/ subdirectory containing VCF
```bash
<output_dir>/trgt/
└── <sample_name>.vcf.gz
```

## Output
For each sample, the script creates Excel (XLSX) report in a new subdirectory:
```bash
<output_dir>/output_report/
└── <sample_name>_PureTarget_report.xlsx
```
