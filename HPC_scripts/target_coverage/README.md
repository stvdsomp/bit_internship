## Target coverage plotting

This folder contains three scripts that generate a multi-boxplot graph illustrating coverage distributions within one run.

### Files
- `bedcov_boxplot_prep.sh` - Bash script to generate TSV file containing the number of reads mapped to each repeat of interest defined in the BED file, for all samples in a run
- `generate_plot_per_region.R` - R script to generate multi-boxplot graph from the TSV file, showing read coverage per repeat of interest
- `generate_plot_per_sample.R` - R script to generate multi-boxplot graph from the TSV file, showing on-target read coverage per sample
