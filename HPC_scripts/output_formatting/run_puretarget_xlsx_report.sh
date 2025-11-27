#!/bin/bash

# Define variables
my_env=pacvar_output_format
script_dir="/kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/output_formatting"
output_dir="/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/analysis_SVS/pacvar/RUN_010_r84299_20250604_141714"
samplesheet="/kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/run_nf_pacvar/samplesheet_RUN_010.csv"

# Run the script inside the conda environment
conda run -n "$my_env" python3 "$script_dir/generate_puretarget_xlsx_report.py" "$output_dir" "$samplesheet"