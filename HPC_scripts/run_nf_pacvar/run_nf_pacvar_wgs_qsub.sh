#!/bin/bash

#PBS -l walltime=6:00:00
#PBS -l nodes=1:ppn=96
#PBS -l mem=64gb
#PBS -m abe
#PBS -N pacvar_wgs_Twist

export NXF_HOME=/data/gent/422/vsc42287/.nextflow
export NXF_WORK=/data/gent/422/vsc42287/work
export APPTAINER_CACHEDIR=/data/gent/422/vsc42287/.apptainer
export APPTAINER_TMPDIR=/data/gent/422/vsc42287/.apptainer/tmp

module load Nextflow/25.04.8

nextflow run nf-core/pacvar \
   -r master \
   -resume \
   -latest \
   -profile vsc_ugent \
   -c "/kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/run_nf_pacvar/my_config_wgs_qsub.config"
