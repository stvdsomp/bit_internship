#!/bin/bash

script_dir = "/home/svdsompe/BIT11/sync/WSL2_scripts/output_formatting"
output_dir = "/home/svdsompe/BIT11/local_data/r84299_20250623_141348"
samplesheet = "$OUTPUT_DIR/samplesheet.csv"

conda activate bit11
python3 script_dir/generate_puretarget_xlsx_report.py $output_dir $samplesheet