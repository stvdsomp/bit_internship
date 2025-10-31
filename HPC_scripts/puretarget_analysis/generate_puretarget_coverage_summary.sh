#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: $0 <input_dir>"
    exit 1
fi

input_dir="$1"
outfile="$input_dir/summary_mean_coverage_per_target.tsv"

cd $input_dir
# get all files
files=(./*/*.coverage.regions.bed.gz)

# extract sample names from filenames
samples=()
for f in "${files[@]}"; do
    sample=$(basename "$f" .coverage.regions.bed.gz)
    samples+=("$sample")
done

# create header
header="Chr\tStart\tStop\tInfo"
for s in "${samples[@]}"; do
    header="$header\t$s"
done
echo -e "$header" > "$outfile"

# create array of column 5 for each file
tmpfiles=()
for f in "${files[@]}"; do
    tmp=$(mktemp)
    # use zcat to read gzipped file
    zcat "$f" | awk '{print $5}' > "$tmp"
    tmpfiles+=("$tmp")
done

# create region identifier from first file
regions=$(mktemp)
zcat "${files[0]}" | awk '{print $1"\t"$2"\t"$3"\t"$4}' > "$regions"

# combine regions + coverage columns
paste "$regions" "${tmpfiles[@]}" >> "$outfile"

# clean up
rm "$regions" "${tmpfiles[@]}"
