#!/usr/bin/env bash

# Usage: bedcov_boxplot_prep.sh <RUN_NAME>

set -euo pipefail

# Setup environment and variables 
module load SAMtools/1.21-GCC-13.3.0

RUN_NAME=$1
BAM_DIR="/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/analysis_SVS/pacvar/$RUN_NAME/pbmm2"
BED_FILE="/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/bin/roi/PureTarget_repeat_expansion_panel_2.0.repeat_definition.GRCh38.bed"
OUT_DIR="/user/gent/422/vsc42287/BIT11/sync/HPC_scripts/target_coverage"
THREADS=4

mkdir -p "$OUT_DIR/${RUN_NAME}_cov"

OUT_TSV="$OUT_DIR/${RUN_NAME}_cov_summary.tsv"
echo -e "region\tsample\tcoverage" > "$OUT_TSV"

# Process HiFi BAM files
shopt -s nullglob

for BAM in "$BAM_DIR"/*hifi.aligned.bam; do
    SAMPLE=$(basename "$BAM" .hifi.aligned.bam)
    echo "Processing $SAMPLE"
    BEDCOV_TMP="$OUT_DIR/${RUN_NAME}_cov/${SAMPLE}.bedcov"

    # Calculate coverage sum per region
    samtools index -@ "$THREADS" "$BAM"
    samtools bedcov "$BED_FILE" "$BAM" > "$BEDCOV_TMP"
    rm -f "${BAM}.bai"

    # Normalize by region length and append to final table
    awk -v S="$SAMPLE" 'BEGIN{OFS="\t"}
        {
            len = $3 - $2
            cov = (len > 0) ? $NF / len : 0
            print $4, S, cov
        }' "$BEDCOV_TMP" >> "$OUT_TSV"
done

echo "Output file: $OUT_TSV"