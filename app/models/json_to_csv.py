# json_to_csv.py
# extract the json to columns

import pandas as pd
import json
from datetime import datetime

def load_data(filepath):
    def parse_json(column):
        try:
            return json.loads(column)
        except:
            return column

    df = pd.read_csv(filepath, converters={'keystroke_data': parse_json})
    return df

def extract_keystroke_events(keystrokes):
    events = {'time': [], 'key': [], 'event': []}
    for event in keystrokes:
        time = datetime.fromtimestamp(event['time'] / 1000)  # Convert milliseconds to datetime
        events['time'].append(time)
        events['key'].append(event['key'])
        events['event'].append(event['event'])

    return events

def process_keystrokes(filepath):
    # Load the CSV data
    data = load_data(filepath)

    # Strip leading and trailing spaces from column names
    data.columns = data.columns.str.strip()

    # Check if 'keystroke_data' column exists and parse it
    if 'keystroke_data' in data.columns:
        data['keystroke_data'] = data['keystroke_data'].apply(json.loads)

    # List to hold the structured feature data
    structured_data = []

    # Iterate through each row in the DataFrame
    for index, row in data.iterrows():
        user_data = row.to_dict()
        keystrokes = user_data.pop('keystroke_data')
        user_id = user_data['user_id']
        user_name = user_data['user_name']

        # Extract keystroke events
        keystroke_events = extract_keystroke_events(keystrokes)

        # Prepare rows for the structured data
        for i in range(len(keystroke_events['time'])):
            event_row = {'user_id': user_id, 'user_name': user_name}
            event_row['event_time'] = keystroke_events['time'][i]
            event_row['key'] = keystroke_events['key'][i]
            event_row['event'] = keystroke_events['event'][i]
            structured_data.append(event_row)

    # Create a new DataFrame from the structured data
    structured_df = pd.DataFrame(structured_data)

    return structured_df

def save_data(df, filepath):
    df.to_csv(filepath, index=False)

def main():
    raw_data_path = 'data/raw/data.csv'
    processed_data_path = 'data/processed/final_data.csv'
    
    structured_df = process_keystrokes(raw_data_path)
    save_data(structured_df, processed_data_path)

if __name__ == "__main__":
    main()
