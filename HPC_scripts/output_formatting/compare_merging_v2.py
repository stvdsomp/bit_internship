#!/usr/bin/env python3

import gzip
import os
import sys
from collections import defaultdict

METRICS = ["GT", "AL", "ALLR", "SD", "MC", "MS", "AP", "AM"]

TRID_LIST = [
    "CANVAS_RFC1",
    "DM1_DMPK",
    "DM2_CNBP",
    "DRPLA_ATN1",
    "FECD3_TCF4",
    "FRDA_FXN",
    "FTDALS1_C9orf72",
    "FXS_FMR1",
    "HD_HTT",
    "OPMD_PABPN1",
    "SBMA_AR",
    "SCA10_ATXN10",
    "SCA12_PPP2R2B",
    "SCA17_TBP",
    "SCA1_ATXN1",
    "SCA2_ATXN2",
    "SCA3_ATXN3",
    "SCA6_CACNA1A",
    "SCA7_ATXN7",
    "SCA8_ATXN8OS",
]

def discover_samples(run_dir):
    """
    Returns a set of sample names from <sample>.sorted.vcf.gz files
    """
    samples = set()
    for fn in os.listdir(run_dir):
        if fn.endswith(".sorted.vcf.gz"):
            samples.add(fn.replace(".sorted.vcf.gz", ""))
    return samples


def split_value(val):
    """
    Returns (field1, field2)
    """
    if val in (".", "", None):
        return ".", "."
    if "," in val:
        a, b = val.split(",", 1)
        return a, b
    return val, "."


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


def collect_metric(samples, RUN1, RUN2, METRIC):
    """
    Returns:
      data[TRID][SAMPLE]["RUN"] = metrics
      data[TRID][SAMPLE]["NOFAIL"] = metrics
    """
    data = {trid: {} for trid in TRID_LIST}

    for sample in samples:
        print(f"Parsing {sample}")

        d_run1 = parse_vcf(os.path.join(RUN1, f"{sample}.sorted.vcf.gz"))
        d_run2  = parse_vcf(os.path.join(RUN2, f"{sample}.sorted.vcf.gz"))

        for trid in TRID_LIST:
            data[trid].setdefault(sample, {})
            data[trid][sample]["RUN"] = d_run1.get(trid, {}).get(METRIC, ".")
            data[trid][sample]["NOFAIL"] = d_run2.get(trid, {}).get(METRIC, ".")

    return data


def write_metric_table(data, samples, RUN_NR, METRIC, out_file):

    with open(out_file, "w") as out:

        # Header
        out.write("\t")
        for s in samples:
            out.write(
                f"{s}\t{s}\t{s}_noFail\t{s}_noFail\t"
            )
        out.write("\n")

        out.write("TRID")
        for _ in samples:
            out.write(
                f"\tRUN_{RUN_NR}\tRUN_{RUN_NR}\t"
                f"RUN_{RUN_NR}_noFail\tRUN_{RUN_NR}_noFail"
            )
        out.write("\n")

        # Rows
        for trid in TRID_LIST:
            out.write(f"{METRIC}_{trid}")

            for s in samples:
                v_run = data[trid].get(s, {}).get("RUN", ".")
                v_nf  = data[trid].get(s, {}).get("NOFAIL", ".")

                r1, r2 = split_value(v_run)
                n1, n2 = split_value(v_nf)

                out.write(f"\t{r1}\t{r2}\t{n1}\t{n2}")

            out.write("\n")


def main():

    if len(sys.argv) != 3:
        print(f"\nUsage: python compare_merging_v2.py <009|010|011|...> <GT|AL|ALLR|SD|MC|MS|AP|AM>\n")
        sys.exit(1)

    RUN_NR = sys.argv[1]
    METRIC = sys.argv[2]

    RUN1 = f"/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/analysis_SVS/pacvar/RUN_{RUN_NR}/bcftools"
    RUN2 = f"/kyukon/data/gent/vo/000/gvo00082/research/ICT/VAL/Revio_PureTarget/analysis_SVS/pacvar/RUN_{RUN_NR}_noFail/bcftools"

    samples_run = discover_samples(RUN1)

    data = collect_metric(samples_run, RUN1, RUN2, METRIC)

    out_file = f"RUN_{RUN_NR}_{METRIC}_summary.tsv"
    write_metric_table(data, samples_run, RUN_NR, METRIC, out_file)

    print(f"\nWritten: {out_file}")


if __name__ == "__main__":
    main()
