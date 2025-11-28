#!/bin/bash

# Define variables
my_env=pacvar_output_format

# Run the script inside the conda environment
conda run -n "$my_env" python3 "./color_motifs_test.py"