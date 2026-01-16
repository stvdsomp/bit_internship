## Target coverage plotting

This folder contains three scripts that generate a multi-boxplot graph illustrating coverage distributions within one run.

### Files
- `bedcov_boxplot_prep.sh` - Bash script that generates per-sample TSV files containing the number of reads mapped to each repeat of interest defined in the BED file
- `generate_plot_per_region.R` - R script that generates the multi-boxplot graph from the TSV files, read coverage per repeat of interest
- `generate_plot_per_sample.R` - R script that generates the multi-boxplot graph from the TSV files, showing on-target read coverage per sample
