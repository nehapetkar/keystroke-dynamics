import pandas as pd
import json
import numpy as np

# load data
def load_data(filepath):
    def parse_json(column):
        try:
            return json.loads(column)
        except:
            return column

    df = pd.read_csv(filepath, converters={'keystroke_data': parse_json})
    return df

# extract dwell time, flight time, press-press, release-release
def extract_keystroke_features(keystrokes):
    features = {}
    key_press_times = {}
    previous_release_time = None
    previous_key = None

    for event in keystrokes:
        key = event['key']
        time = event['time']
        event_type = event['event']

        if event_type == 'p':  # key press
            key_press_times[key] = time
            features[f'{key}_press_time'] = time

            if previous_release_time is not None:
                features[f'{previous_key}_to_{key}_flight_time'] = time - previous_release_time

        elif event_type == 'r':  # key release
            if key in key_press_times:
                press_time = key_press_times[key]
                duration = time - press_time
                features[f'{key}_release_time'] = time
                features[f'{key}_dwell_time'] = duration
                if previous_key is not None:
                    features[f'{previous_key}_to_{key}_press_press_time'] = press_time - key_press_times[previous_key]
                    features[f'{previous_key}_to_{key}_release_release_time'] = time - previous_release_time
                previous_release_time = time
                previous_key = key

    return features

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

        # Extract keystroke features
        keystroke_features = extract_keystroke_features(keystrokes)

        # Create a new row with original data and keystroke features
        feature_row = {**user_data, **keystroke_features}
        
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
