# home.py

from app import app
from flask import render_template, request, jsonify
import csv
import random
import uuid
import json
import pandas as pd

# random paragraphs 
random_paragraphs = [
   "A good way to increase your typing speed is to type easy sentences over and over. That will help you to type smoothly without pausing. Try taking a typing speed test before and after to see for yourself. You can even work through this section multiple times and then track your progress.",
   "Keystroke dynamics analyzes typing rhythm to identify users based on unique typing patterns. It offers continuous authentication using timing and pressure of keystrokes."
]


user_info = {}  # Dictionary to store user IDs and usernames

def generate_unique_id():
    return str(uuid.uuid4())

def load_user_info():
    # Load existing user IDs and usernames from the CSV file
    try:
        with open('data/raw/data1.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                user_info[row[0]] = row[1].lower()
    except FileNotFoundError:
        # If file does not exist, create it
        with open('data/raw/data1.csv', 'w', newline='') as csvfile:
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

        # check for existing user
        if username in user_info.values():
            user_id = next(key for key, value in user_info.items() if value == username)
        else:
            user_id = generate_unique_id()
            user_info[user_id] = username

        # store the json data
        with open('data/raw/data1.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([user_id, username, json.dumps(keystrokes)])  

        # Return success message
        return jsonify({
            'message': 'Data submitted successfully!',
        })
