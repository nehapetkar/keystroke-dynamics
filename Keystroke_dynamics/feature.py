import pandas as pd
import json

# Load the CSV data
data = pd.read_csv('data.csv')

# Strip leading and trailing spaces from column names
data.columns = data.columns.str.strip()

# Check if 'keystroke_data' column exists
if 'keystroke_data' in data.columns:
    # Parse the keystroke_data column
    data['keystroke_data'] = data['keystroke_data'].apply(json.loads)
    
    # # Display the first few rows of the dataframe after parsing
    # print(data.head())
else:
    print("Column 'keystroke_data' not found in the DataFrame.")

# List to hold the expanded data
expanded_data = []

# Iterate through each row in the DataFrame
for index, row in data.iterrows():
    user_id = row['user_id']
    user_name = row['user_name']
    keystrokes = row['keystroke_data']
    
    # Iterate through each keystroke event
    for event in keystrokes:
        # Create a new row with the expanded data
        expanded_row = {
            'user_id': user_id,
            'user_name': user_name,
            'time': event['time'],
            'key': event['key'],
            'event': event['event']
        }
        # Append the new row to the list
        expanded_data.append(expanded_row)

# Create a new DataFrame from the expanded data
expanded_df = pd.DataFrame(expanded_data)

# Display the first few rows of the expanded DataFrame
print(expanded_df.head(20))

# Optionally, save the expanded DataFrame to a new CSV file
expanded_df.to_csv('expanded_data.csv', index=False)
