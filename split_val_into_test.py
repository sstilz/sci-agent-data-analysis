import pandas as pd
from sklearn.model_selection import train_test_split
import os
 
# Load your CSV
def split_data():
    df = pd.read_csv(os.path.join(os.getcwd(), 'entire_dataset_summaries/csv_data/combined_metrics_with_modality.csv'))

    assert 'image_idx' in df.columns and 'modality' in df.columns, "CSV must contain 'image_idx' and 'modality' columns"

    # Initialize lists for train and test indices
    train_indices = []
    test_indices = []

    # Group by modality and split
    for modality, group in df.groupby('modality'):
        train, test = train_test_split(group['image_idx'].tolist(), test_size=0.5, random_state=42, shuffle=True)
        train_indices.extend(train)
        test_indices.extend(test)

    # Sort indices if desired
    train_indices.sort()
    test_indices.sort()

    # Now train_indices and test_indices contain the split
    print("Train indices:", train_indices[:10])  # Just showing first 10 for brevity
    print("Test indices:", test_indices[:10])
    print("Lengths", len(train_indices), len(test_indices))

    return train_indices, test_indices
s