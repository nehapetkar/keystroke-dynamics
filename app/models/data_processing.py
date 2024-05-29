# data_processing.py
# convert json to dataframes and extracted features

import pandas as pd
import json
import numpy as np

def load_data(filepath):
    def parse_json(column):
        try:
            return json.loads(column)
        except:
            return column

    df = pd.read_csv(filepath, converters={'keystroke_data': parse_json})
    return df

def extract_dwell_times(keystrokes):
    dwell_times = []
    key_press_times = {}

    for event in keystrokes:
        key = event['key']
        time = event['time']
        if event['event'] == 'p':  # key press
            key_press_times[key] = time
        elif event['event'] == 'r':  # key release
            if key in key_press_times:
                dwell_time = time - key_press_times[key]
                dwell_times.append(dwell_time)
                del key_press_times[key]
    
    return dwell_times

def aggregate_features(dwell_times):
    if len(dwell_times) == 0:
        return {
            'mean_dwell_time': np.nan,
            'std_dwell_time': np.nan,
            'min_dwell_time': np.nan,
            'max_dwell_time': np.nan,
        }
    
    return {
        'mean_dwell_time': np.mean(dwell_times),
        'std_dwell_time': np.std(dwell_times),
        'min_dwell_time': np.min(dwell_times),
        'max_dwell_time': np.max(dwell_times),
    }

def process_keystrokes(filepath):
    # Load the CSV data
    data = load_data(filepath)

    # Strip leading and trailing spaces from column names
    data.columns = data.columns.str.strip()

    # Check if 'keystroke_data' column exists and parse it
    if 'keystroke_data' in data.columns:
        data['keystroke_data'] = data['keystroke_data'].apply(json.loads)

    # List to hold the feature data
    features_data = []

    # Iterate through each row in the DataFrame
    for index, row in data.iterrows():
        user_data = row.to_dict()
        keystrokes = user_data.pop('keystroke_data')

        # Extract dwell times
        dwell_times = extract_dwell_times(keystrokes)

        # Aggregate dwell time features
        dwell_features = aggregate_features(dwell_times)

        # Create a new row with original data and dwell time features
        feature_row = {**user_data, **dwell_features}
        
        # Append the new row to the list
        features_data.append(feature_row)

    # Create a new DataFrame from the feature data
    features_df = pd.DataFrame(features_data)
    return features_df

def save_data(df, filepath):
    df.to_csv(filepath, index=False)

def main():
    raw_data_path = 'data/raw/data.csv'
    processed_data_path = 'data/processed/final_data.csv'
    
    features_df = process_keystrokes(raw_data_path)
    save_data(features_df, processed_data_path)

if __name__ == "__main__":
    main()
