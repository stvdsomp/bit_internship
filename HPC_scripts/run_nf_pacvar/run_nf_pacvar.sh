#!/bin/bash

#module swap cluster/donphan
#qsub -I -l nodes=1:ppn=8,mem=24gb,walltime=03:00:00

nextflow run stvdsomp/pacvar \
   -r dev_repeat_id \
   -latest \
   -resume \
   -profile vsc_ugent \
   -c my_config.config
