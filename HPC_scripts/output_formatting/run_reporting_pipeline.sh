#!/bin/bash

# conda activate nextflow 

nextflow run stvdsomp/report \
   -r dev_pacvar_repeat \
   -latest \
   -profile vsc_ugent \
   --pacvar_repeat.input samplesheet_RUN_025.csv \
   --outdir results \
   --igenomes_base ./ \
   --igenomes_ignore
