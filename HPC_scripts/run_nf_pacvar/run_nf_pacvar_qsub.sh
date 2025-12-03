#!/bin/bash

#PBS -l walltime=6:00:00
#PBS -l nodes=1:ppn=32
#PBS -l mem=32gb
#PBS -m abe
#PBS -N pacvar.r84299_20251021_160234

nextflow run stvdsomp/pacvar \
   -r dev_personal \
   -latest \
   -resume \
   -profile vsc_ugent \
   -c my_config_qsub.config
