# home.py

from app import app, keystroke_analysis
from flask import render_template, request, jsonify
import csv
import random
import uuid
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import joblib

random_paragraphs = [
    "c write know however late each that with because that place nation only for each change form consider we would interest with world so order or run more open that large write turn never over open each over change still old take hold need give by consider line only leave while what set up",
]

user_info = {}  # Dictionary to store user IDs and usernames

def generate_unique_id():
    return str(uuid.uuid4())

def load_user_info():
    # Load existing user IDs and usernames from the CSV file
    try:
        with open('data.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                user_info[row[0]] = row[1].lower()
    except FileNotFoundError:
        # If file does not exist, create it
        with open('data.csv', 'w', newline='') as csvfile:
            pass

load_user_info()

@app.route('/')
def home():
    paragraph = random.choice(random_paragraphs)
    return render_template('index.html', paragraph=paragraph)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username'].lower()
        keystrokes = json.loads(request.form['keystrokes'])  # Parse JSON data

        if username in user_info.values():
            user_id = next(key for key, value in user_info.items() if value == username)
        else:
            user_id = generate_unique_id()
            user_info[user_id] = username

        with open('data.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([user_id, username, json.dumps(keystrokes)])  # Store keystrokes as JSON string

        # Return success message
        return jsonify({
            'message': 'Data submitted successfully!',
        })

@app.route('/train', methods=['GET'])
def train_model():
    # Load keystroke data from CSV file
    df = pd.read_csv('data.csv', names=['user_id', 'username', 'keystrokes'])
    
    # Preprocess data and extract features
    features = []
    for _, row in df.iterrows():
        try:
            keystrokes = json.loads(row['keystrokes'])
        except json.JSONDecodeError:
            # Skip rows with invalid JSON data
            continue
        
        dwell_times = keystroke_analysis.calculate_dwell_time(keystrokes)
        flight_times = keystroke_analysis.calculate_flight_time(keystrokes)
        digraph_latencies = keystroke_analysis.calculate_digraph_latency(keystrokes)
        typing_speed = keystroke_analysis.calculate_typing_speed(keystrokes, len(keystrokes))
        
        feature_vector = [len(dwell_times), len(flight_times), len(digraph_latencies), typing_speed]
        features.append(feature_vector)
    
    # Split data into features and target labels
    X = pd.DataFrame(features, columns=['dwell_times', 'flight_times', 'digraph_latencies', 'typing_speed'])
    y = df['user_id']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train SVM model
    svm_model = SVC(kernel='linear', C=1.0)
    svm_model.fit(X_train_scaled, y_train)
    
    # Evaluate model
    accuracy = svm_model.score(X_test_scaled, y_test)
    
    # Save trained model
    joblib.dump(svm_model, 'svm_model.pkl')
    
    return jsonify({'message': f'Model trained successfully! Accuracy: {accuracy}'})

