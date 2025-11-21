#!/bin/bash

nextflow run ~/BIT11/pacvar \
   -profile test,vsc_ugent \
   -c my_config_test.config \
   -stub-run \
   -resume
