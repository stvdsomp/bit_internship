#!/bin/bash

# Define variables
my_env=bit11
script_dir="/home/svdsompe/BIT11/sync/WSL2_scripts/output_formatting"
output_dir="/home/svdsompe/BIT11/local_data/r84299_20250623_141348"
samplesheet="$output_dir/samplesheet.csv"

# Run the script inside the conda environment
conda run -n "$my_env" python3 "$script_dir/generate_puretarget_xlsx_report.py" "$output_dir" "$samplesheet"