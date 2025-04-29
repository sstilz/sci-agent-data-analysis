import csv
import random
from collections import defaultdict
from argparse import ArgumentParser
import os
import pandas as pd
from sklearn.model_selection import train_test_split

# path/to/analyze_validation_baselines> python get_validation_subset.py --num_files 10 --seed 41

def get_idx_list(seed, num_files):
    input_filepath = os.path.join(os.getcwd(), 'entire_dataset_summaries/csv_data/combined_metrics_with_modality.csv')

    output_index_filepath = os.path.join(os.getcwd(), f'subset_analytics/idx_lists/selected_{num_files}_indexes_seed_{seed}.txt')

    # Load full dataset
    data = []
    modality_buckets = defaultdict(list)

    with open(input_filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            image_idx = int(row['image_idx'])
            dsc = float(row['DSC_metric'])
            nsd = float(row['NSD_metric'])
            modality = row['modality']
            data.append({
                'image_idx': image_idx,
                'DSC_metric': dsc,
                'NSD_metric': nsd,
                'modality': modality
            })
            modality_buckets[modality].append(image_idx)

    # Select 1 sample per modality (minimum guarantee)
    random.seed(seed)
    selected_idxs = []
    for modality, idxs in modality_buckets.items():
        selected_idxs.append(random.choice(idxs))

    remaining = num_files - len(selected_idxs)
    if remaining < 0:
        raise ValueError(f"num_files={num_files} is less than the number of unique modalities!")

    # Get remaining samples randomly (but reproducibly)
    remaining_pool = [item['image_idx'] for item in data if item['image_idx'] not in selected_idxs]
    random.shuffle(remaining_pool)
    selected_idxs += remaining_pool[:remaining]
    selected_idxs = sorted(selected_idxs)

    # Save selected indexes to file
    idx_list = []
    with open(output_index_filepath, 'w') as f:
        for idx in selected_idxs:
            f.write(f"{idx}\n")
            idx_list.append(idx)

    print(f"Saved selected indexes to: {output_index_filepath}")
    return data, idx_list

def get_data():
    input_filepath = os.path.join(os.getcwd(), 'entire_dataset_summaries/csv_data/combined_metrics_with_modality.csv')

    # Load full dataset
    data = []

    with open(input_filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            image_idx = int(row['image_idx'])
            dsc = float(row['DSC_metric'])
            nsd = float(row['NSD_metric'])
            modality = row['modality']
            data.append({
                'image_idx': image_idx,
                'DSC_metric': dsc,
                'NSD_metric': nsd,
                'modality': modality
            })
    return data

def summarize_idx_list(data, output_analytics_file, idx_list):
    # Analytics for selected data
    selected_data = [item for item in data if item['image_idx'] in idx_list]
    total_dsc = sum(item['DSC_metric'] for item in selected_data)
    total_nsd = sum(item['NSD_metric'] for item in selected_data)
    overall_avg_dsc = total_dsc / len(selected_data)
    overall_avg_nsd = total_nsd / len(selected_data)

    subset_stats = defaultdict(list)
    for item in selected_data:
        subset_stats[item['modality']].append(item)

    # Write summary to file
    # Write summary to file
    with open(output_analytics_file, 'w') as out:
        out.write("=== Subset Summary ===\n")
        out.write(f"Total samples: {len(selected_data)}\n")
        out.write(f"Overall Avg DSC: {overall_avg_dsc:.6f}\n")
        out.write(f"Overall Avg NSD: {overall_avg_nsd:.6f}\n\n")

        out.write("=== Per-Modality Breakdown ===\n")
        for modality, entries in subset_stats.items():
            count = len(entries)
            percent = (count / len(selected_data)) * 100
            avg_dsc = sum(e['DSC_metric'] for e in entries) / count
            avg_nsd = sum(e['NSD_metric'] for e in entries) / count

            out.write(f"Modality: {modality}\n")
            out.write(f"  Count: {count} ({percent:.2f}%)\n")
            out.write(f"  Avg DSC: {avg_dsc:.6f}\n")
            out.write(f"  Avg NSD: {avg_nsd:.6f}\n\n")

        out.write("=== Selected Image Indexes ===\n")
        out.write(f"{idx_list}\n")  # <--- This line prints the list-style format

    print(f"Analytics written to: {output_analytics_file}")

def split_data():
    df = pd.read_csv(os.path.join(os.getcwd(), 'entire_dataset_summaries/csv_data/combined_metrics_with_modality.csv'))

    assert 'image_idx' in df.columns and 'modality' in df.columns, "CSV must contain 'image_idx' and 'modality' columns"

    # Initialize lists for train and test indices
    val_indices = []
    test_indices = []

    # Group by modality and split
    for modality, group in df.groupby('modality'):
        train, test = train_test_split(group['image_idx'].tolist(), test_size=0.5, random_state=42, shuffle=True)
        val_indices.extend(train)
        test_indices.extend(test)

    # Sort indices if desired
    val_indices.sort()
    test_indices.sort()

    # Now val_indices and test_indices contain the split
    print("Train indices:", val_indices[:10])  # Just showing first 10 for brevity
    print("Test indices:", test_indices[:10])
    print("Lengths", len(val_indices), len(test_indices))

    return val_indices, test_indices

if __name__ == "__main__":
    parser = ArgumentParser(description="Select a validation subset from the dataset.")
    parser.add_argument("--num_files", type=int, default=10, help="Number of files to select for validation.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    args = parser.parse_args()

    num_files = args.num_files
    seed = args.seed

    # To get a validation subset
    # data, idx_list = get_idx_list(seed, num_files)
    # output_analytics_file = f'subset_analytics/summaries/subset_{args.num_files}_analytics_seed_{seed}.txt'
    # summarize_idx_list(data, output_analytics_file, idx_list)

    # To split validation set into 50-50 validation and test
    val_indices, test_indices = split_data()
    data = get_data()
    summarize_idx_list(data,  f'subset_analytics/summaries/SPLIT_VALIDATION_SET_analytics_seed_{seed}.txt', val_indices)
    summarize_idx_list(data, f'subset_analytics/summaries/SPLIT_TEST_SET_analytics_seed_{seed}.txt', test_indices)

    print("Done!")