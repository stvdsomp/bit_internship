#!/usr/bin/env python3

import gzip
import os
import sys
from collections import defaultdict

METRICS = ["GT", "AL", "ALLR", "SD", "MC", "MS", "AP", "AM"]


def discover_samples(run_dir):
    """
    Returns a set of sample names from <sample>.sorted.vcf.gz files
    """
    samples = set()
    for fn in os.listdir(run_dir):
        if fn.endswith(".sorted.vcf.gz"):
            samples.add(fn.replace(".sorted.vcf.gz", ""))
    return samples


def parse_vcf(vcf_path):
    """
    Returns:
      data[TRID][METRIC] = value
    """
    data = {}

    with gzip.open(vcf_path, "rt") as f:
        for line in f:
            if line.startswith("##") or line.startswith("#CHROM"):
                continue

            fields = line.rstrip().split("\t")
            sample_field = fields[9]

            # Ignore fully missing calls
            if sample_field == ".:.:.:.:.:.:.:.":
                continue

            format_vals = sample_field.split(":")
            fmt = dict(zip(METRICS, format_vals))

            # Extract TRID
            info = fields[7]
            trid = None
            for entry in info.split(";"):
                if entry.startswith("TRID="):
                    trid = entry.split("=", 1)[1]
                    break

            if trid is None:
                continue

            data[trid] = {m: fmt.get(m, ".") for m in METRICS}

    return data


def write_sample_comparison(sample, out, RUN1, RUN2, RUN_NR):
    vcf1 = os.path.join(RUN1, f"{sample}.sorted.vcf.gz")
    vcf2 = os.path.join(RUN2, f"{sample}.sorted.vcf.gz")

    print(f"Processing sample: {sample}")

    d1 = parse_vcf(vcf1)
    d2 = parse_vcf(vcf2)

    all_trids = sorted(set(d1) | set(d2))

    out.write(f"\nSAMPLE={sample}\n")

    for trid in all_trids:
        out.write(f"TRID={trid}\n")
        out.write(f"METRIC\tRUN_{RUN_NR}\tRUN_{RUN_NR}_noFail\n")

        for m in METRICS:
            v1 = d1.get(trid, {}).get(m, ".")
            v2 = d2.get(trid, {}).get(m, ".")
            out.write(f"{m}\t{v1}\t{v2}\n")

        out.write("\n")


def main():

    RUN_NR = sys.argv[1]
    RUN1 = f"/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/analysis_SVS/pacvar/RUN_{RUN_NR}/bcftools"
    RUN2 = f"/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/analysis_SVS/pacvar/RUN_{RUN_NR}_noFail/bcftools"

    samples_run = discover_samples(RUN1)

    out_file = f"RUN_{RUN_NR}_comparison.tsv"

    with open(out_file, "w") as out:
        out.write(f"TR comparison RUN_{RUN_NR} vs RUN_{RUN_NR}_noFail\n")

        for sample in samples_run:
            write_sample_comparison(sample, out, RUN1, RUN2, RUN_NR)


if __name__ == "__main__":
    main()
