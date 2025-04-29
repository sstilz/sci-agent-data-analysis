import csv

# Step 1: Build image_idx -> modality map
modality_map = {}
with open('unpacked_filenames.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) == 3:
                try:
                    image_idx = int(parts[0])
                    modality = parts[2]
                    modality_map[image_idx] = modality
                except ValueError:
                    continue  # skip header or malformed lines

# Step 2: Read existing combined_metrics.csv and append modality
rows = []
with open('combined_metrics.csv', 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        image_idx = int(row['image_idx'])
        row['modality'] = modality_map.get(image_idx, 'Unknown')
        rows.append(row)

# Step 3: Write new CSV with added modality column
with open('combined_metrics_with_modality.csv', 'w', newline='') as outfile:
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Added modality info to {len(rows)} rows in 'combined_metrics_with_modality.csv'")
