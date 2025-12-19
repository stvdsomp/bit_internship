# PureTarget Excel Report Generator
## Overview
This script generates an Excel (XLSX) report summarizing tandem repeat genotypes from a VCF file produced by the nf-core/pacvar pipeline.
For each sample in the samplesheet, the script parses the TRGT VCF output and creates a structured, user-friendly Excel report with:
-	A menu sheet for easy navigation between repeats
-	One worksheet per tandem repeat (TRID)
-	Allele-specific information including:
o	Repeat length and length range
o	Read support
o	Motif counts and motif spans
o	Purity and methylation
o	Color-highlighted repeat motifs within sequences
The resulting report is intended for downstream interpretation and clinical review.
Note: This script does not include figures (e.g. motif or methylation plots).
________________________________________
## Input
Required inputs
1.	Samplesheet (CSV)
o	Contains at least a sample column with sample names matching the VCF filenames
o	Example:
o	sample
o	SAMPLE_001
o	SAMPLE_002
2.	Output directory
o	The main output directory produced by the nf-core/pacvar pipeline
o	The script assumes the presence of a trgt/ subdirectory containing VCF files: <output_dir>/trgt/<sample_name>.vcf.gz
o	
o	
________________________________________
## Output
For each sample, the script creates:
<output_dir>/output_report/
└── <sample_name>_PureTarget_report.xlsx
Excel report structure
•	Menu sheet
o	Sample name
o	TRGT version
o	Dropdown list to select a repeat
o	Clickable hyperlink to jump to the selected repeat sheet
•	One sheet per TRID
o	Repeat metadata (ID, genomic position, expected motifs)
o	Allele-specific table:
	Allele label
	Length
	Length range
	Reads spanning allele
	Motif count
	Motif span
	Purity
	Mean methylation
	Sequence with colored motifs
Motifs are color-coded consistently across alleles, and non-motif bases are visually highlighted to aid interpretation.
