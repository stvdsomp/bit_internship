## lima demultiplexing (isolated)
This folder contains scripts and reference files for demultiplexing PacBio sequencing reads using `lima`.
The workflow separates reads based on barcodes defined in the sample sheet and prepares them for downstream analysis.
These scripts were used to test the functionality of `lima` outside of the nf-core/pacvar pipeline.

### Files
- `Ampli-Fi_Barcoded_Sample_Name_File.csv` - samplesheet with barcode information (not used by `lima` command-line tool)
- `Amplifi_TwistUDIadapters_noP7P5.fasta` - adapter sequences for demultiplexing
- `Amplifi_TwistUDIadapters_noP7P5_subset.fasta` - subset of relevant adapters
- `demultiplex*.sh` - shell script to run demultiplexing 
- `lima.man` - manual for `lima` command usage
- `conda` - Conda environment setup for running the scripts
