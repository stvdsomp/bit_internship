#!/bin/bash

#module swap cluster/donphan
#qsub -I -l nodes=1:ppn=8,mem=24gb,walltime=03:00:00

nextflow run /kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/pbmerge_bam/main.nf \
   -c /kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/pbmerge_bam/my_config.config