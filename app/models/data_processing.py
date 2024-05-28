import pandas as pd
import json

def load_data(filepath):
    def parse_json(column):
        try:
            return json.loads(column)
        except:
            return column

    df = pd.read_csv(filepath, converters={'keystroke_data': parse_json})
    return df

def extract_features(keystrokes):
    dwell_time = keystrokes[-1]['time'] - keystrokes[0]['time']
    flight_time = 0
    press_press_time = 0
    release_release_time = 0
    
    for i in range(len(keystrokes) - 1):
        flight_time += keystrokes[i+1]['time'] - keystrokes[i]['time']
        if keystrokes[i]['event'] == 'p' and keystrokes[i+1]['event'] == 'p':
            press_press_time += keystrokes[i+1]['time'] - keystrokes[i]['time']
        elif keystrokes[i]['event'] == 'r' and keystrokes[i+1]['event'] == 'r':
            release_release_time += keystrokes[i+1]['time'] - keystrokes[i]['time']
    
    return {
        'dwell_time': dwell_time,
        'flight_time': flight_time,
        'press_press_time': press_press_time,
        'release_release_time': release_release_time
    }

def process_keystrokes(filepath):
    # Load the CSV data
    data = load_data(filepath)

    # Strip leading and trailing spaces from column names
    data.columns = data.columns.str.strip()
    
    # Check if 'keystroke_data' column exists
    if 'keystroke_data' in data.columns:
        # Parse the keystroke_data column
        data['keystroke_data'] = data['keystroke_data'].apply(json.loads)

    # List to hold the feature data
    features_data = []

    # Iterate through each row in the DataFrame
    for index, row in data.iterrows():
        user_id = row['user_id']
        user_name = row['user_name']
        keystrokes = row['keystroke_data']

        # Extract features from keystrokes
        features = extract_features(keystrokes)
        
        # Create a new row with the feature data
        feature_row = {
            'user_id': user_id,
            'user_name': user_name,
            **features
        }
        
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
