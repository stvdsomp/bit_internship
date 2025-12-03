#!/usr/bin/env nextflow

process MERGE_BAM {
    tag "$sample"
    container "https://depot.galaxyproject.org/singularity/pbtk:3.5.0--h9ee0642_0"

    publishDir "/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/raw_data/r84299_20251021_160234/1_A01/merged_reads", mode: "copy"

    input:
    tuple val(sample), path(hifi), path(fail)

    output:
    path "${sample}.merged.bam"

    script:
    """
    pbmerge -o ${sample}.merged.bam ${hifi} ${fail}
    """
}

workflow {
    samplesheet_ch = Channel.fromPath(params.samplesheet)
                        .splitCsv(header:true)
                        .map { row -> tuple(row.sample, file(row.hifi_bam), file(row.fail_bam))}

    MERGE_BAM(samplesheet_ch)
}