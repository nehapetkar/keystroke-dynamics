# home.py

from app import app
from flask import render_template, request, jsonify
import csv
import random
import uuid
import json
import pandas as pd

random_paragraphs = [
    "As we navigate through the vast expanse of the digital age, it's crucial to maintain a balance between technological advancements and ethical considerations. This ensures a sustainable and inclusive future for all.",
    "The rapid evolution of artificial intelligence and machine learning is transforming industries at an unprecedented pace. Embracing these technologies responsibly will require robust frameworks and regulatory oversight.",
    "Climate change remains one of the most pressing challenges of our time. It demands coordinated global efforts to reduce carbon emissions and promote sustainable development practices.",
    "In the realm of quantum computing, researchers are breaking new ground with each passing day. The potential applications of quantum algorithms could revolutionize fields such as cryptography and material science.",
    "As urbanization continues to accelerate, smart cities are emerging as a solution to enhance the quality of life. Integrating technology with urban planning can lead to more efficient and sustainable living environments.",
    "In an ever-changing world where innovation drives progress, it's imperative to remember the importance of human connection and empathy. Balancing technological growth with social responsibility will lead to a more harmonious society.",
    "Environmental sustainability and economic growth are not mutually exclusive. By investing in green technologies and renewable energy, we can create jobs and protect our planet for future generations.",
    "As artificial intelligence becomes increasingly sophisticated, the challenge lies in guiding its development toward enhancing human capabilities rather than replacing them. Ethical AI can revolutionize industries while safeguarding individual autonomy.",
    "Globalization has interconnected economies and cultures, fostering unprecedented collaboration and innovation. However, it also demands a renewed focus on cultural sensitivity and equitable resource distribution.",
    "Renewable energy sources, such as solar and wind power, present viable alternatives to fossil fuels. Investing in these technologies can mitigate climate change and drive sustainable economic growth.",
]

user_info = {}  # Dictionary to store user IDs and usernames

def generate_unique_id():
    return str(uuid.uuid4())

def load_user_info():
    # Load existing user IDs and usernames from the CSV file
    try:
        with open('data/raw/data.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                user_info[row[0]] = row[1].lower()
    except FileNotFoundError:
        # If file does not exist, create it
        with open('data/raw/data.csv', 'w', newline='') as csvfile:
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

        with open('data/raw/data.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([user_id, username, json.dumps(keystrokes)])  # Store keystrokes as JSON string

        # Return success message
        return jsonify({
            'message': 'Data submitted successfully!',
        })
