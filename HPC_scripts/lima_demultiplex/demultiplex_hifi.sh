#!/bin/bash

#PBS -l walltime=4:00:00
#PBS -l nodes=1:ppn=32
#PBS -l mem=24gb
#PBS -m abe
#PBS -N m84299_251021_160938_s1.hifi_reads.demux

# Create conda env with lima
# conda create -p /kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/lima_demultiplex/conda bioconda::lima #2.13.0

# Constants
conda_env='/kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/lima_demultiplex/conda/bin'
input_bam='/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/raw_data/r84299_20251021_160234/1_A01/hifi_reads/m84299_251021_160938_s1.hifi_reads.bam'
barcodes='/kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/lima_demultiplex/Amplifi_TwistUDIadapters_noP7P5_subset.fasta'
output_prefix='/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/raw_data/r84299_20251021_160234/1_A01/hifi_reads/m84299_251021_160938_s1.hifi_reads.bam'
samplesheet='/kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/lima_demultiplex/Ampli-Fi_Barcoded_Sample_Name_File.csv'

# Make conda environment visible
export PATH=$conda_env:$PATH

# Run demultiplexing using lima
echo "Demultiplexing using lima..."

lima \
    $input_bam \
    $barcodes \
    $output_prefix \
    --split-named \
    --neighbors \
    --num-threads 32

echo "Lima demultiplexing completed"

# The --biosample-csv option only exists in SMRT Link GUI, not in the CLI lima
# lima "$input_dir/$input_sample" $barcodes --biosample-csv $samplesheet --split-named --neighbors
