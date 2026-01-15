## Target coverage plotting

This folder contains two scripts that generate a multi-boxplot graph illustrating coverage distributions. Each boxplot represents the coverage for a specific target repeat of interest, using data combined from all samples in the run.

### Files
- `bedcov_boxplot_prep.sh` - Bash script that generates per-sample TSV files containing the number of reads mapped to each repeat of interest defined in the BED file
- `generate_plot.R` - R script that generates the multi-boxplot graph from the TSV files
