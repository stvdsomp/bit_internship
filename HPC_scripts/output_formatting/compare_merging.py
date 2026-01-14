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


def collect_all_data(samples, RUN1, RUN2):
    """
    Returns:
      data[TRID][SAMPLE]["RUN"] = metrics
      data[TRID][SAMPLE]["NOFAIL"] = metrics
    """
    data = {}

    for sample in samples:
        print(f"Parsing sample: {sample}")

        d_run1 = parse_vcf(os.path.join(RUN1, f"{sample}.sorted.vcf.gz"))
        d_run2  = parse_vcf(os.path.join(RUN2, f"{sample}.sorted.vcf.gz"))

        for trid in set(d_run1) | set(d_run2):
            data.setdefault(trid, {})
            data[trid].setdefault(sample, {})
            data[trid][sample]["RUN"] = d_run1.get(trid, {})
            data[trid][sample]["NOFAIL"] = d_run2.get(trid, {})

    return data


def write_trid_blocks(data, samples, RUN_NR, out_file):
    with open(out_file, "w") as out:

        for trid in sorted(data):
            # Header line with samples
            out.write(f"TRID={trid}")
            for s in samples:
                out.write(f"\tSAMPLE={s}\t")
            out.write("\n")

            # Second header line
            out.write("METRIC")
            for _ in samples:
                out.write(f"\tRUN_{RUN_NR}\tRUN_{RUN_NR}_noFail")
            out.write("\n")

            # Metrics
            for m in METRICS:
                out.write(m)
                for s in samples:
                    run_val = data[trid].get(s, {}).get("RUN", {}).get(m, ".")
                    nf_val  = data[trid].get(s, {}).get("NOFAIL", {}).get(m, ".")
                    out.write(f"\t{run_val}\t{nf_val}")
                out.write("\n")

            out.write("\n")


def main():

    if len(sys.argv) != 2:
        print(f"\nUsage: python compare_merging_v1.py <009|010|011|...>\n")
        sys.exit(1)

    RUN_NR = sys.argv[1]

    RUN1 = f"/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/analysis_SVS/pacvar/RUN_{RUN_NR}/bcftools"
    RUN2 = f"/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/analysis_SVS/pacvar/RUN_{RUN_NR}_noFail/bcftools"

    samples_run = discover_samples(RUN1)

    data = collect_all_data(samples_run, RUN1, RUN2)

    out_file = f"RUN_{RUN_NR}_comparison.tsv"
    write_trid_blocks(data, samples_run, RUN_NR, out_file)

    print(f"\nWritten: {out_file}")


if __name__ == "__main__":
    main()
