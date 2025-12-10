#!/bin/bash

# Define variables
my_env=pacvar_output_format
script_dir="/kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/output_formatting"
output_dir="/kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/output_formatting"
samplesheet="/kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/output_formatting/samplesheet_TEST.csv"

# Run the script inside the conda environment
conda run -n "$my_env" python3 "$script_dir/generate_puretarget_xlsx_report_TEST.py" "$output_dir" "$samplesheet"