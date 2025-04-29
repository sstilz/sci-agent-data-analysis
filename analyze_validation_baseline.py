import csv
from collections import defaultdict

# Initialize accumulators
total_dsc = 0.0
total_nsd = 0.0
total_count = 0

modality_stats = defaultdict(lambda: {'count': 0, 'dsc_sum': 0.0, 'nsd_sum': 0.0})

# Read the CSV and populate the stats
with open('combined_metrics_with_modality.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        dsc = float(row['DSC_metric'])
        nsd = float(row['NSD_metric'])
        modality = row['modality']

        total_dsc += dsc
        total_nsd += nsd
        total_count += 1

        modality_stats[modality]['count'] += 1
        modality_stats[modality]['dsc_sum'] += dsc
        modality_stats[modality]['nsd_sum'] += nsd

# Write results to file
with open('validation_baseline_analytics.txt', 'w') as out:
    out.write("=== Overall Metrics ===\n")
    out.write(f"Average DSC: {total_dsc / total_count:.6f}\n")
    out.write(f"Average NSD: {total_nsd / total_count:.6f}\n\n")

    out.write("=== Per-Modality Metrics ===\n")
    for modality, stats in modality_stats.items():
        count = stats['count']
        avg_dsc = stats['dsc_sum'] / count
        avg_nsd = stats['nsd_sum'] / count
        percent = (count / total_count) * 100

        out.write(f"Modality: {modality}\n")
        out.write(f"  Count: {count} ({percent:.2f}%)\n")
        out.write(f"  Average DSC: {avg_dsc:.6f}\n")
        out.write(f"  Average NSD: {avg_nsd:.6f}\n\n")

print("Analytics written to 'validation_baseline_analytics.txt'")
