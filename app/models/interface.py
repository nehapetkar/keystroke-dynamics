# interface.py

import json
import joblib
import pandas as pd
from pynput import keyboard
import time
from sklearn.metrics import accuracy_score

# Load the trained model
model_path = 'data/models/rf_classifier.pkl'
rf_classifier = joblib.load(model_path)

# Initialize data collection variables
keystroke_data = []
start_time = None

def on_press(key):
    global start_time
    try:
        if start_time is None:
            start_time = time.time()
        if hasattr(key, 'char'):
            keystroke_data.append({'key': key.char, 'time': time.time() - start_time, 'event': 'p'})
            print(key.char, end='', flush=True)
        elif key == keyboard.Key.space:
            keystroke_data.append({'key': 'space', 'time': time.time() - start_time, 'event': 'p'})
            print(' ', end='', flush=True)
        elif key == keyboard.Key.backspace:
            keystroke_data.append({'key': 'backspace', 'time': time.time() - start_time, 'event': 'p'})
            print('\b \b', end='', flush=True)  # Simulate backspace in terminal
    except AttributeError:
        pass

def on_release(key):
    global start_time
    try:
        if hasattr(key, 'char'):
            keystroke_data.append({'key': key.char, 'time': time.time() - start_time, 'event': 'r'})
        elif key == keyboard.Key.space:
            keystroke_data.append({'key': 'space', 'time': time.time() - start_time, 'event': 'r'})
        elif key == keyboard.Key.backspace:
            keystroke_data.append({'key': 'backspace', 'time': time.time() - start_time, 'event': 'r'})
    except AttributeError:
        pass
    if key == keyboard.Key.esc:
        return False

def capture_keystrokes():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def extract_dwell_times(keystrokes):
    dwell_times = []
    key_press_times = {}

    for event in keystrokes:
        key = event['key']
        time = event['time']
        if event['event'] == 'p':
            key_press_times[key] = time
        elif event['event'] == 'r':
            if key in key_press_times:
                dwell_time = time - key_press_times[key]
                dwell_times.append(dwell_time)
                del key_press_times[key]
    
    return dwell_times

def main():
    actual_users = []
    predicted_users = []
    
    while True:
        actual_user = input("Enter the actual user (or type 'exit' to quit): ")
        if actual_user.lower() == 'exit':
            break

        print("Please type the following paragraph and press ESC when done:")
        print("The quick brown fox jumps over the lazy dog.")

        # Reset keystroke data
        global keystroke_data
        keystroke_data = []

        # Capture keystrokes
        capture_keystrokes()

        # Extract dwell times
        dwell_times = extract_dwell_times(keystroke_data)

        # Aggregate features
        features = {
            'mean_dwell_time': [sum(dwell_times) / len(dwell_times)] if dwell_times else [0],
            'std_dwell_time': [pd.Series(dwell_times).std()] if dwell_times else [0],
            'min_dwell_time': [min(dwell_times)] if dwell_times else [0],
            'max_dwell_time': [max(dwell_times)] if dwell_times else [0],
        }

        # Create DataFrame
        df_features = pd.DataFrame(features)

        # Predict user
        user_prediction = rf_classifier.predict(df_features)
        predicted_user = user_prediction[0]
        print(f"\nAuthenticated user: {predicted_user}")

        # Append results for evaluation
        actual_users.append(actual_user)
        predicted_users.append(predicted_user)

    # Evaluate model performance
    if actual_users:
        accuracy = accuracy_score(actual_users, predicted_users)
        print(f"Model Accuracy: {accuracy}")

if __name__ == "__main__":
    main()
