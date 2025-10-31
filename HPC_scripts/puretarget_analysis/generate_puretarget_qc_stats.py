import csv
import sys
import re
from collections import defaultdict, OrderedDict

### extract "@HD" info of the sample specific output files of puretarget-qc tool

def read_samplesheet(samplesheet_path):
    with open(samplesheet_path, newline='') as csvfile:
        return list(csv.DictReader(csvfile))


def extract_coverage_info(samples,input_dir):
    
    # Store all info keys and sample values
    all_keys = set()
    sample_data = {}
    for sample in samples:
        samplename = sample['sample']
        filepath = input_dir + '/puretarget-qc.' + samplename + '.txt'
        info_dict = OrderedDict()
        
        with open(filepath) as f:
            for line in f:
                if line.startswith("@HD") and not line.startswith("@HD NUM"):
                    # Remove '@HD ' and split at first space to get the info type
                    parts = line[4:].strip().split(None, 1)
                    if len(parts) == 2:
                        main_info, rest = parts
                        main_info = main_info.replace(":", "")  # Remove any colon from info
                        # Split on tab or multiple spaces
                        fields = re.split(r'\t+|\s{2,}', rest)
                        for field in fields:
                            if ':' in field:
                                subkey, value = field.split(':', 1)
                                subkey = subkey.replace(":", "").strip()
                                value = value.strip()
                                fullkey = f"{main_info} {subkey}" if subkey else main_info
                                info_dict[fullkey] = value
                                all_keys.add(fullkey)
                            else:
                                if field:
                                    # Attach to previous info if possible
                                    if info_dict and list(info_dict.values())[-1] == "":
                                        last_key = list(info_dict.keys())[-1]
                                        info_dict[last_key] = field.strip()
                                    else:
                                        info_dict[field.strip()] = ""
                                        all_keys.add(field.strip())
            sample_data[samplename] = info_dict

    # Sort all keys for consistent order
    all_keys = sorted(all_keys)

    # Write the big table
    output_file = input_dir + "/puretarget_qc.coverage.all_samples.tsv"
    with open(output_file, "w") as out:
        out.write("Info\t" + "\t".join(sample_data.keys()) + "\n")
        for key in all_keys:
            row = [key]
            for sample in sample_data:
                row.append(sample_data[sample].get(key, ""))
            out.write("\t".join(row) + "\n")
    print(f"write out {output_file}")

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python generate_puretarget_qc_stats.py <output_dir> <samplesheet>")
        sys.exit(1)

    output_dir = sys.argv[1]
    samplesheet = sys.argv[2]

    samples = read_samplesheet(samplesheet)
    extract_coverage_info(samples,output_dir)

if __name__ == "__main__":
    main()
