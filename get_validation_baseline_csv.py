import re
import csv
import os

# List of your text files in the correct order
filenames = [
    'all_baselines_0_1750.txt',
    'all_baselines_1750_3500.txt',
    'all_baselines_3500_5250.txt',
    'all_baselines_5250_7000.txt',
    'all_baselines_7000_8750.txt',
    'all_baselines_8750_10500.txt',
    'all_baselines_10500_12250.txt',
    'all_baselines_12250_13072.txt'
]

full_paths = [os.path.join(os.getcwd(), 'validation_baselines', f) for f in filenames]

# Regex to match lines with evaluation metrics
eval_line_regex = re.compile(r'^(\d+) \| DSC: ([0-9.]+) \| NSD: ([0-9.]+)')

output_rows = []
image_global_idx = 0

for filename in full_paths:
    with open(filename, 'r') as f:
        for line in f:
            match = eval_line_regex.match(line.strip())
            if match:
                dsc = float(match.group(2))
                nsd = float(match.group(3))
                output_rows.append([image_global_idx, dsc, nsd])
                image_global_idx += 1

# Write to CSV
with open('combined_metrics.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['image_idx', 'DSC_metric', 'NSD_metric'])
    writer.writerows(output_rows)

print(f"Successfully wrote {len(output_rows)} entries to combined_metrics.csv")
# 