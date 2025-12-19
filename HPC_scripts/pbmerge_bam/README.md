## pbtk/pbmerge merging (isolated)

This folder contains Nextflow scripts and config files for merging BAM files.
The workflow combines HiFi and fail BAM data from the same samples into unified BAM files, which is necessary for the `nf-core/pacvar` repeat workflow.
These scripts were used to test the `pbtk/pbmerge` functionality, prior to integrating it into the `nf-core/pacvar` pipeline.

### Files
- `main.nf` - Nextflow workflow script for BAM merging
- `my_config.config` - main config file for the workflow
- `run_pbmerge.sh` - shell wrappers to run the workflow on the HPC
- `samplesheet.csv` - example samplesheet defining input HiFi and fail BAM files
