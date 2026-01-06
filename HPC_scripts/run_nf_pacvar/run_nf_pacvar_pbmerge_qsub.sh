#!/bin/bash

#PBS -l walltime=12:00:00
#PBS -l nodes=1:ppn=32
#PBS -l mem=32gb
#PBS -m abe
#PBS -N pacvar_pbmerge_demux

module load Nextflow/25.04.8

nextflow run stvdsomp/pacvar \
   -r dev_pbmerge_post \
   -resume \
   -latest \
   -profile vsc_ugent \
   -c "/kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/run_nf_pacvar/my_config_pbmerge_qsub.config"
