#!/bin/bash

#PBS -l walltime=12:00:00
#PBS -l nodes=1:ppn=32
#PBS -l mem=32gb
#PBS -m abe
#PBS -N pacvar_repeat_PureTarget

module load Nextflow/26.04.3 awscli

nextflow run stvdsomp/pacvar \
   -r v1.1.0_nextflow-26 \
   -latest \
   -resume \
   -profile vsc_ugent \
   -c "/kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/run_nf_pacvar/my_config_PureTarget_v1.1.0.config"
