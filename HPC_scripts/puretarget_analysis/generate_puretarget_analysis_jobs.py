import configparser
import csv
import os
import sys
import subprocess

def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['DEFAULT']

def read_samplesheet(samplesheet_path):
    with open(samplesheet_path, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def generate_job_script(sample, constants, raw_data_dir, output_dir):
    sample_name = sample['sample']
    barcode = sample['barcode']
    karyotype = sample['karyotype']

    output_script = f"{output_dir}/puretarget_{sample_name}.sh"
    print(f"writing {output_script}")
    with open(output_script, 'w') as f:
        f.write(f"""#!/bin/bash
#PBS -l walltime=1:00:00
#PBS -l nodes=1:ppn={constants['threads']}
#PBS -l mem={constants['memory']}
#PBS -m abe
#PBS -N {sample_name}
#PBS -o {output_dir}/
#PBS -e {output_dir}/

# Constants
conda_env={constants['conda_env']}
fasta={constants['fasta']}
repeats={constants['repeats']}
pbmerge_version={constants['pbmerge_version']}
pbmm2_version={constants['pbmm2_version']}
pbmm2_parameters=({constants['pbmm2_parameters']})
samtools_version={constants['samtools_version']}
trgt_version={constants['trgt_version']}
trgt_parameters=({constants['trgt_parameters']})
bcftools_version={constants['bcftools_version']}
mosdepth_version={constants['mosdepth_version']}
threads={constants['threads']}

# Parameters
raw_data_dir={raw_data_dir}
output_dir={output_dir}
sample={sample_name}
barcode={barcode}
karyotype={karyotype}

echo "Analysing sample $sample (barcode: $barcode, karyotype: $karyotype)"
output_dir="${{output_dir}}/${{sample}}"
mkdir -vp "$output_dir"
output_prefix="${{output_dir}}/${{sample}}"

export PATH=$conda_env:$PATH

fail_reads=($raw_data_dir/fail_reads/*.fail_reads.$barcode.bam)
hifi_reads=($raw_data_dir/hifi_reads/*.hifi_reads.$barcode.bam)

if [ ${{#fail_reads[@]}} -eq 0 ]; then
  echo "Error: No fail_reads files found for barcode '$barcode'" >&2
  exit 1
fi

if [ ${{#hifi_reads[@]}} -eq 0 ]; then
  echo "Error: No hifi_reads files found for barcode '$barcode'" >&2
  exit 1
fi

echo "Merging files with pbmerge v$pbmerge_version:"
printf "  - %s\\n" "${{hifi_reads[@]}}"
printf "  - %s\\n" "${{fail_reads[@]}}"
pbmerge -o $output_prefix.merged.bam ${{hifi_reads[@]}} ${{fail_reads[@]}}

if [ $? -ne 0 ]; then
    printf "  Error: Merging failed.\\n" >&2
    exit 1
else
    printf "  Merging successful.\\n"
fi
echo "Mapping reads with pbmm2 v$pbmm2_version"
pbmm2 align \\
    ${{pbmm2_parameters[@]}} \\
    "$fasta" \\
    "$output_prefix.merged.bam" \\
    "$output_prefix.mapped.bam" \\
    --num-threads "$threads"

if [ $? -ne 0 ]; then
    printf "  Error: Mapping failed.\\n" >&2
    exit 1
else
    printf "  Mapping successful.\\n"
fi

echo "Index mapped BAM with samtools v$samtools_version"
samtools index $output_prefix.mapped.bam

if [ $? -ne 0 ]; then
    printf "  Error: Indexing failed.\\n" >&2
    exit 1
else
    printf "  Indexing successful.\\n"
fi

echo "Genotype tandem repeats with trgt v$trgt_version"

trgt genotype \\
    "${{trgt_parameters[@]}}" \\
    --genome "$fasta" \\
    --repeats "$repeats" \\
    --reads "$output_prefix.mapped.bam" \\
    --karyotype "$karyotype" \\
    --output-prefix "$output_prefix"

if [ $? -ne 0 ]; then
    printf "  Error: Repeat genotyping failed.\\n" >&2
    exit 1
else
    printf "  Repeat genotyping successful.\\n"
fi

echo "Sort and index VCF with bcftools v$bcftools_version"

bcftools sort -Ob -o "$output_prefix.sorted.vcf.gz" "$output_prefix.vcf.gz"

if [ $? -ne 0 ]; then
    printf "  Error: VCF sorting failed.\\n" >&2
    exit 1
else
    printf "  VCF sorting successful.\\n"
fi

bcftools index $output_prefix.sorted.vcf.gz

if [ $? -ne 0 ]; then
    printf "  Error: VCF indexing failed.\\n" >&2
    exit 1
else
    printf "  VCF indexing successful.\\n"
    rm -v $output_prefix.vcf.gz
fi

echo "Sort and index spanning BAM with samtools v$samtools_version"

samtools sort "$output_prefix.spanning.bam" -o "$output_prefix.spanning.sorted.bam"

if [ $? -ne 0 ]; then
    printf "  Error: BAM sorting failed.\\n" >&2
    exit 1
else
    printf "  BAM sorting successful.\\n"
fi

samtools index "$output_prefix.spanning.sorted.bam"


if [ $? -ne 0 ]; then
    printf "  Error: BAM indexing failed.\\n" >&2
    exit 1
else
	printf "  BAM indexing successful.\\n"
	rm -v $output_prefix.spanning.bam
fi

echo "Plot tandem repeats with trgt v$trgt_version"

for repeat_id in $(grep -o "ID=[^;]*" "$repeats" | sed 's/ID=//' | paste -sd' '); do
    
    trgt plot --genome "$fasta" \\
		--repeats "$repeats" \\
		--vcf "$output_prefix.sorted.vcf.gz" \\
		--spanning-reads "$output_prefix.spanning.sorted.bam" \\
		--repeat-id "$repeat_id" \\
		--show motifs \\
		--image "$output_prefix.$repeat_id.motifs.svg"
    
    trgt plot --genome "$fasta" \\
		--repeats "$repeats" \\
		--vcf "$output_prefix.sorted.vcf.gz" \\
		--spanning-reads "$output_prefix.spanning.sorted.bam" \\
		--repeat-id "$repeat_id" \\
		--show meth \\
		--image "$output_prefix.$repeat_id.meth.svg"
done


echo "Calculate mean coverage with mosdepth v$mosdepth_version"
mosdepth -n -b "$repeats" "$output_prefix.coverage" "$output_prefix.spanning.sorted.bam"

if [ $? -ne 0 ]; then
    printf "  Error: Coverage calculation failed.\\n" >&2
    exit 1
else
	printf "  Coverage calculation successful.\\n"
fi

echo "Analysis finished"

""")
    try:
        result = subprocess.run(["qsub", output_script], check=True, capture_output=True, text=True)
        print("Job submitted successfully.")
        print("Job ID:", result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("Error submitting job:")
        print(e.stderr.strip())

def main():
    if len(sys.argv) != 4:
        print("Usage: python generate_puretarget_analysis_jobs.py <raw_data_dir> <output_dir> <samplesheet>")
        sys.exit(1)

    raw_data_dir = sys.argv[1]
    output_dir = sys.argv[2]
    samplesheet = sys.argv[3]

    constants = read_config("/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/bin/cmgg_puretarget.ini")
    samples = read_samplesheet(samplesheet)

    for sample in samples:
        generate_job_script(sample, constants, raw_data_dir, output_dir)

if __name__ == "__main__":
    main()
