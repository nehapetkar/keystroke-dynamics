import csv
import json
import os

def convert_to_desired_format(input_file, output_file):
    # Define column headers for the output CSV
    headers = ['user']
    for i in range(13):
        headers.extend([f'press-{i}', f'release-{i}'])

    # Check if the output file already exists to avoid rewriting the header
    file_exists = os.path.isfile(output_file)

    # Open input file and output file in append mode
    with open(input_file, 'r') as infile, open(output_file, 'a', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write header row if the file does not exist
        if not file_exists:
            writer.writerow(headers)

        # Process each row in the input CSV
        for row in reader:
            user_id = row[0]
            keystrokes = row[2]

            # Parse JSON data
            try:
                keystrokes = json.loads(keystrokes)
            except json.JSONDecodeError:
                print(f"Error decoding JSON for user {user_id}. Skipping this entry.")
                continue

            # Initialize list to store times
            times = [''] * 26

            # Populate press and release events
            index = 0
            for event in keystrokes:
                time = event['time']
                event_type = event['event']

                if event_type == 'p':
                    times[index] = time
                    index += 1
                elif event_type == 'r':
                    times[index] = time
                    index += 1

            # Append user ID and times to the output CSV
            output_row = [user_id] + times
            writer.writerow(output_row)

# Example usage:
convert_to_desired_format('data/data1.csv', 'data/train.csv')
