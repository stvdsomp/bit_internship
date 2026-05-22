#!/bin/bash

FOLDER="/user/gent/422/vsc42287/BIT11/sync/HPC_scripts/output_formatting/results/pacvar_repeat/reports"

for file in "$FOLDER"/*.xlsx; do
    filename=$(basename "$file")

    # Replace ".pacvar_repeat_report.xlsx" with "_noFail.pacvar_repeat_report.xlsx"
    newname="${filename/.pacvar_repeat_report.xlsx/_noFail.pacvar_repeat_report.xlsx}"

    mv "$file" "$FOLDER/$newname"
done