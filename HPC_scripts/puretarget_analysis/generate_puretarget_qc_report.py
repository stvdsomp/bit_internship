import json
import sys

if len(sys.argv) != 2:
    print("Usage: python generate_puretarget_qc_report.py <output_dir>")
    sys.exit(1)

ouput_dir = sys.argv[1]
report=ouput_dir + "/puretarget-qc.report.json"
ouput_report=ouput_dir + "/puretarget-qc.report.txt"

with open(report) as f:
    data = json.load(f)

# print(data)

# Find the 'Sample summary' table
sample_table = None
for table in data.get("tables", []):
    if table.get("title") == "Sample summary":
        sample_table = table
        break

if not sample_table:
    print("Sample summary table not found.")
    exit(1)

# Extract headers and rows
headers = [col["header"] for col in sample_table["columns"]]
rows = list(zip(*(col["values"] for col in sample_table["columns"])))

with open(ouput_report, "w") as out:
    out.write("\t".join(headers) + "\n")
    for row in rows:
        out.write("\t".join(row) + "\n")

print(f"Sample summary table written to {ouput_report}")