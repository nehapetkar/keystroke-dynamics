# home.py

from app import app
from flask import render_template, request, jsonify, redirect, url_for
import csv
import random
import json
import pandas as pd

# Initialize a counter to generate unique integer IDs starting from 110
current_id = 110

# random paragraphs 
random_paragraphs = [
   "united states"
]

user_info = {}  # Dictionary to store user IDs mapped to usernames

def load_user_info():
    global current_id
    # Load existing user IDs and usernames from the CSV file
    try:
        with open('data/data1.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                user_id = int(row[0])
                username = row[1]
                user_info[username] = user_id
                current_id = max(current_id, user_id)
    except FileNotFoundError:
        pass

load_user_info()

def generate_unique_id():
    global current_id
    current_id += 1
    return current_id

# index.html
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('train_page'))
    else:
        paragraph = random.choice(random_paragraphs)
        return render_template('index.html', paragraph=paragraph)
    
# test_page.html
@app.route('/test_page.html')
def test_page():
    paragraph = random.choice(random_paragraphs)
    return render_template('test_page.html', paragraph=paragraph)

@app.route('/submit', methods=['POST'])
def submit():
    global current_id
    if request.method == 'POST':
        username = request.form['username'].lower()
        keystrokes = json.loads(request.form['keystrokes'])  # Parse JSON data

        # Check if the username already exists
        if username in user_info:
            user_id = user_info[username]
        else:
            user_id = generate_unique_id()
            user_info[username] = user_id

        # store the json data
        with open('data/data1.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([user_id, username, json.dumps(keystrokes)])  

        # Return success message
        return jsonify({
            'message': 'Data submitted successfully!',
        })


@app.route('/submit_test', methods=['POST'])
def submit_test():
    # Your submission handling code here
    global current_id
    if request.method == 'POST':
        username = request.form['username'].lower()
        keystrokes = json.loads(request.form['keystrokes'])  # Parse JSON data

        # Check if the username already exists
        if username in user_info:
            user_id = user_info[username]
        else:
            user_id = generate_unique_id()
            user_info[username] = user_id

        # store the json data
        with open('data/test_data.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([user_id, username, json.dumps(keystrokes)])  

        # Return success message
        return jsonify({
            'message': 'Data submitted successfully!',
        })