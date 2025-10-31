# puretarget
Scripts for analysis of PacBio PureTarget data
## analysis flow set-up on HPC
```bash
# analysis dir
mkdir /kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget
chgrp -R gict Revio_PureTarget
chmod -R g+w Revio_PureTarget

# conda environment
conda create -p /kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/conda/ bioconda::pbtk #3.5.0
conda install bioconda::pbmm2 #1.17.0
conda install bioconda::samtools #v1.22.1
conda install bioconda::trgt #v4.0.0
conda install bioconda::bcftools #1.22
conda install bioconda::mosdepth #0.3.11
conda install anaconda::tabulate #0.9.0
```
## analysis flow
Login to HPC + copy raw data
```bash
ml load awscli/2.17.54-GCCcore-13.2.

raw_data=/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/raw_data
run_name=r84299_20250623_141348

aws --endpoint-url https://s3.ugent.be s3 ls cmgg-upload/revio/
aws --endpoint-url https://s3.ugent.be s3 cp --recursive s3://cmgg-upload/revio/$run_name/ $raw_data/$run_name
```
Open new terminal + start analysis (+-5 minutes per sample)
```bash
#activate environment
conda activate /kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/conda

#define runname
raw_data=/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/raw_data
run_name=r84299_20250623_141348
raw_dir=$raw_data/$run_name/1_{A,B}01/

# make analysis dir
mkdir /kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/analysis_SVS
output_dir=/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/analysis_SVS
mkdir $output_dir/$run_name

# create an samplesheet "sample,barcode,karyotype"
touch $output_dir/$run_name/samplesheet.csv 

# perform puretarget analysis
cd /kyukon/home/gent/422/vsc42287/BIT11/puretarget/bin
python generate_puretarget_analysis_jobs.py \
    $raw_dir \
    $output_dir/$run_name \
    $output_dir/$run_name/samplesheet.csv
```
Post-analysis scripts
```bash
# after successful run, check output directory for results + run QC script
python generate_puretarget_qc_job.py \
    $output_dir/$run_name \
    $output_dir/$run_name/samplesheet.csv

# after successful puretarget_qc + run reformatting scripts
bash generate_puretarget_coverage_summary.sh $output_dir/$run_name
python generate_puretarget_qc_report.py $output_dir/$run_name
python generate_puretarget_qc_stats.py $output_dir/$run_name $output_dir/$run_name/samplesheet.csv
```
Remove raw_data
```bash
raw_dir=$raw_data/$run_name/
rm -Rv $raw_dir
```
Archive results
```bash
# to be discussed
# for now: copy QC files + sample dirs (without *mapped.bam, *svg, *merged.bam) to UZ share S:\MEDGENSeq\Revio\PureTarget
```