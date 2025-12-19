# Bio-informatics internship 2025-2026
## Overview
This repository contains scripts, workflows, and resources developed during my bioinformatics internship. It is organized into separate directories for HPC-based and WSL2-based environments, with subfolders for specific analyses, pipeline runs, and output formatting.
## Repository structure
The HPC_scripts directory contains scripts and workflows optimized for UGent HPC environment, the WSL2_scripts contains scripts compatible with the 'local' WSL2 environment.

```bash
bit_internship/
├── HPC_scripts/
│   ├── lima_demultiplex/    # Demultiplexing PacBio sequencing reads using lima (isolated)
│   ├── output_formatting/   # Formatting nf-core/pacvar outputs, generating Excel reports with motif visualization
│   ├── pbmerge_bam/         # Merging HiFi and fail BAM files using pbtk/pbmerge (isolated)
│   ├── puretarget_analysis/ # PureTarget analysis scripts, QC, coverage summaries, and job generation
│   └── run_nf_pacvar/       # Scripts and configs to run nf-core/pacvar using PBS job scheduling
│
└── WSL2_scripts/
    ├── output_formatting/   # Initial, local versions of output formatting scripts
    └── run_nf_pacvar/       # Scripts and configs to run nf-core/pavar locally
```
