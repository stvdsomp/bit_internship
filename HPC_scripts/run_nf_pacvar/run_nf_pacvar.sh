#!/bin/bash

nextflow run stvdsomp/pacvar \
   -r dev_personal \
   -latest \
   -profile vsc_ugent \
   -process.executor local \
   --input samplesheet_single.csv \
   --outdir ~/BIT11/local_output/pacvar_personal \
   --fasta /kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/hg38-noalt.fa \
   --fasta_fai /kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/hg38-noalt.fa.fai \
   --skip_demultiplexing true \
   --intervals /kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/bin/roi/PureTarget_repeat_expansion_panel_1.0.repeat_definition.GRCh38.bed \
   --workflow repeat \
   --repeat_id C9ORF72
  #--repeat_id "AR,ATN1,ATXN1,ATXN10,ATXN2,ATXN3,ATXN7,ATXN8,C9ORF72,CACNA1A,CNBP,DMPK,FMR1,FXN,HTT,PABPN1,PPP2R2B,RFC1,TBP,TCF4"
  #--cleanup False 
