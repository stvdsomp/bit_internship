## nf-core/pacvar pipeline runner (locally)

This folder contains a local WSL2 setup to test and run the nf-core/pacvar Nextflow pipeline.

It was used to iteratively test pipeline execution, experiment with configuration options, and inspect outputs on a small scale before adapting workflows for HPC. This process helped develop a functional local testing version of the pipeline.

### Files
- `run_nf_pacvar_test_local.sh` - shell wrapper to run the pipeline locally
- `my_config_test.config` - dynamic config file for local test runs
- `samplesheet*.csv` - samplesheets for testing newly added features
