#!/bin/bash

#PBS -l walltime=00:30:00
#PBS -l nodes=1:ppn=2
#PBS -l mem=4gb
#PBS -N pacvar_repeat_report

export NXF_SINGULARITY_CACHEDIR=/kyukon/scratch/gent/vo/000/gvo00082/vsc42287/singularity

module load Nextflow/26.04.3 awscli

nextflow run stvdsomp/report \
   -r pacvar_repeat_nextflow-26 \
   -latest \
   -profile s3_ugent,singularity \
   --pacvar_repeat.input /user/gent/422/vsc42287/BIT11/sync/HPC_scripts/output_formatting/samplesheet_RUN_011.csv \
   --outdir /user/gent/422/vsc42287/BIT11/sync/HPC_scripts/output_formatting/results