#!/bin/bash

#PBS -l walltime=12:00:00
#PBS -l nodes=1:ppn=32
#PBS -l mem=128gb
#PBS -m abe
#PBS -N pacvar_wgs

module load Nextflow/26.04.3 awscli

nextflow run stvdsomp/pacvar \
   -r v1.1.0_nextflow-26 \
   -latest \
   -resume \
   -profile vsc_ugent \
   -c "/kyukon/home/gent/422/vsc42287/BIT11/sync/HPC_scripts/run_nf_pacvar/my_config_wgs.config"


# Specs for one sample (Giab)

# -[nf-core/pacvar] Pipeline completed successfully-
# Completed at: 08-Aug-2026 07:48:49
# Duration    : 7h 51m 16s
# CPU hours   : 86.2
# Succeeded   : 17

# Used walltime       :   07:51:39.0
# Used CPU time       : 3-21:16:59.0
# % User (Computation): 98.63
# % System (I/O)      :  1.37
# Mem reserved        : 64G
# Max Mem used        : 63.96G (,node3615.doduo.os)
# Max Disk Write      : 433.60G (,node3615.doduo.os)
# Max Disk Read       : 2.60T (,node3615.doduo.os)