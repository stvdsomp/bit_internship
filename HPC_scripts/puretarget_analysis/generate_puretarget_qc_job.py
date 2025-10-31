import configparser
import csv
import os
import sys
import subprocess
import glob

def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['DEFAULT']

def read_samplesheet(samplesheet_path):
    with open(samplesheet_path, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def generate_job_script(samples, constants, output_dir):
    def find_unique(pattern, sample, label):
        matches = glob.glob(pattern)
        if len(matches) == 1:
            return matches[0]
        elif len(matches) == 0:
            print(f"{sample}: no {label} file found")
        else:
            print(f"{sample}: multiple {label} files found: {matches}")
        return None

    bams_mapping = [
        find_unique(os.path.join(output_dir, sample, "*mapped.bam"), sample, "mapped.bam")
        for sample in samples
    ]
    bams_spanning = [
        find_unique(os.path.join(output_dir, sample, "*spanning.sorted.bam"), sample, "spanning.sorted.bam")
        for sample in samples
    ]
    trgt_vcf = [
        find_unique(os.path.join(output_dir, sample, "*.sorted.vcf.gz"), sample, "sorted.vcf.gz")
        for sample in samples
    ]
    # Remove None values
    bams_mapping = [b for b in bams_mapping if b]
    bams_spanning = [b for b in bams_spanning if b]
    trgt_vcf = [v for v in trgt_vcf if v]

    bams_mapping_list = ",".join(bams_mapping)
    bams_spanning_list = ",".join(bams_spanning)
    trgt_vcf_list = ",".join(trgt_vcf)
    samples_list = ",".join(samples)
    output_script = os.path.join(output_dir, "puretarget_qc.sh")
    print(f"writing {output_script}")
    with open(output_script, 'w') as f:
        f.write(f"""#!/bin/bash
#PBS -l walltime=1:00:00
#PBS -l nodes=1:ppn=1
#PBS -m abe
#PBS -N puretarget_qc
#PBS -o {output_dir}/
#PBS -e {output_dir}/

# Constants
conda_env={constants['conda_env']}
repeats={constants['repeats']}
output_prefix={output_dir}/puretarget-qc

# Parameters
output_dir={output_dir}

export PATH=$conda_env:$PATH

echo "Generation puretarget-qc"
puretarget-qc \\
    --catalog "$repeats" \\
    --bams {bams_mapping_list} \\
    --spanning {bams_spanning_list} \\
    --vcf {trgt_vcf_list} \\
    --sample-names {samples_list} \\
    --output-prefix "$output_prefix"

if [ $? -ne 0 ]; then
    printf "  Error: puretarget-qc failed.\\n" >&2
    exit 1
else
    printf "  puretarget-qc successful.\\n"
fi

""")
    try:
        result = subprocess.run(["qsub", output_script], check=True, capture_output=True, text=True)
        print("Job submitted successfully.")
        print("Job ID:", result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("Error submitting job:")
        print(e.stderr.strip())

def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_puretarget_qc_job.py <output_dir> <samplesheet>")
        sys.exit(1)

    output_dir = sys.argv[1]
    samplesheet = sys.argv[2]

    constants = read_config("/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/bin/cmgg_puretarget.ini")
    samples = read_samplesheet(samplesheet)
    samples_list = [item["sample"] for item in samples]
    # print(samples_list)
    generate_job_script(samples_list, constants, output_dir)

if __name__ == "__main__":
    main()
