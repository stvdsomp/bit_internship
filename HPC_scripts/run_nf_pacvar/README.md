## nf-core/pacvar pipeline runner (HPC version)

This folder contains scripts and configuration files to run the nf-core/pacvar Nextflow pipeline using PBS job scheduling.

It includes multiple config templates, samplesheets, and wrapper scripts for different experimental setups, enabling batch processing and automated submission of jobs on HPC.

### Files
- `run_nf_pacvar*.sh` – shell wrappers to run the pipeline on the HPC
- `my_config*.config` – various config templates for different pipeline scenarios
- `samplesheet*.csv` – samplesheets corresponding to different runs and experiments
