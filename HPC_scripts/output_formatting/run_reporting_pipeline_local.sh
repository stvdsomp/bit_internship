#!/bin/bash

# conda activate nextflow 

nextflow run stvdsomp/report \
   -r pacvar_repeat_nextflow-25 \
   -latest \
   -profile vsc_ugent \
   --pacvar_repeat.input samplesheet_RUN_025.csv \
   --outdir results \
   --igenomes_base ./ \
   --igenomes_ignore
