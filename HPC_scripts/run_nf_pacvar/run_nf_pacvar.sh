#!/bin/bash

#module swap cluster/donphan
#sinfo
#qsub -I -l nodes=1:ppn=8,mem=24gb,walltime=03:00:00

nextflow run stvdsomp/pacvar \
   -r dev_personal \
   -latest \
   -profile vsc_ugent \
   -process.executor local \
   --input samplesheet_single.csv \
   --outdir ~/BIT11/local_output/pacvar_personal_C9ORF72 \
   --fasta /kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/hg38-noalt.fa \
   --fasta_fai /kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/hg38-noalt.fa.fai \
   --skip_demultiplexing true \
   --intervals /kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/bin/roi/PureTarget_repeat_expansion_panel_1.0.repeat_definition.GRCh38.bed \
   --workflow repeat \
   --repeat_id C9ORF72
