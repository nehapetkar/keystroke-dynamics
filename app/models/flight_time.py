import pandas as pd
import json

# Step 1: Read data from data1.csv
data = pd.read_csv('data/raw/data1.csv', names=['uuid', 'user_name', 'keystrokes'])

# Step 2: Parse JSON string to extract keystroke information
def extract_keystrokes(row):
    try:
        keystrokes = json.loads(row['keystrokes'])
        return keystrokes
    except Exception as e:
        return None

data['keystrokes'] = data.apply(extract_keystrokes, axis=1)

# Print out the rows with parsing errors
print("Rows with parsing errors:")
print(data[data['keystrokes'].isnull()])

# Step 3: Calculate flight time between consecutive keys
flight_times = []
for _, row in data.iterrows():
    keystrokes = row['keystrokes']
    if keystrokes is None:
        continue
    user_name = row['user_name']
    prev_release_key = None
    for key in keystrokes:
        if key['event'] == 'p':  # Key press event
            if prev_release_key is not None:
                flight_time = key['time'] - prev_release_key['time']
                flight_times.append({
                    'user_name': user_name,
                    'from_key': prev_release_key['key'],
                    'to_key': key['key'],
                    'flight_time': flight_time
                })
        elif key['event'] == 'r':  # Key release event
            prev_release_key = key

# Step 4: Write results to final_data1.csv
final_data = pd.DataFrame(flight_times)
final_data.to_csv('data/processed/final_data1.csv', index=False)
