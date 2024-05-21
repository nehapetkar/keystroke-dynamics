from app import app
from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import random
import uuid

random_paragraphs = [
    "c write know however late each that with because that place nation only for each change form consider we would interest with world so order or run more open that large write turn never over open each over change still old take hold need give by consider line only leave while what set up",
    "herat rea smar ttoetg in eth pranid thwi a fsit haert omtseu he gihtsno enw veirnep otoht sgni foor etah puoer fo a tnats fo ynam a dda dnif a morf gnitsetnu era gnihty sdog mrof yler dna sgnillof raey era spu yppah uoy evol ti evah dluoc uoy rof htiw eht tuoba hguorht sdow yenom eht ni dengocer ot tseug lla fo evig rof ynam ot nettogrof",
    "nac taht a si siht dna siht htiw sdrawot ni eb dluow siht erehw ,efil rof skrow eht hguorht hguorht ni krow a si siht nehw ,pu ti evah dluoc uoy sa tahw erusserp dluow uoy naht erusserp dluow uoy ,elbuod tnediug eht sa denwo siht etirw ot evig ot evah dluoc uoy",
    "eht no ylbaborp lla gniht hguorht dluow uoy saht raey tneserp a rof ,erutcurtsid a fo sdoog hguorht detnatsnoc a ni sdoog fo sraey eht ,erutcurtsid a ni sdoog hguorht eht raey tneserp a rof ,erutcurtsid a fo sdoog hguorht detnatsnoc a ni sdoog fo sraey eht",
    "teiravonni uoy evah dluoc uoy saht skool sgniht rof tnediug eb dluow uoy ,ti sretne eht fo sdoog a ni skool sgniht os siht raey ,sdoog fo sraey eht evah dluoc uoy saht skool sgniht rof tnediug eb dluow uoy ,ti sretne eht fo sdoog a ni skool sgniht os siht raey",
    "gniyd eht morf sdoog a ni smees t'nod I ,tnuoc sdoog a ni smees t'nod I ,tpecca eb dluow I tub sraey eht ni sraey eht fo skool sgniht dlot I ,skool sgniht rof tnediug eb dluow I tub sraey eht ni sraey eht fo skool sgniht dlot I have this to",
    "The sun rose over the tranquil ocean, casting golden reflections on the waves. Seagulls swooped and called in the early morning light. A lone fisherman cast his line from the pier, hoping for a big catch. The salty air was invigorating as joggers passed by, nodding in greeting. Dogs barked happily in the distance, chasing each other in play",
    "In the heart of the bustling city, neon lights illuminated the streets. People hurried past, their footsteps echoing on the pavement. A street performer played a lively tune on his saxophone, drawing a small crowd. Nearby, a food vendor sizzled up delicious-smelling kebabs. The scent mingled with the aroma of freshly brewed coffee from a nearby café",
    "The forest was alive with the sounds of chirping birds and rustling leaves. Sunlight filtered through the canopy, dappling the forest floor with patches of light. A deer cautiously stepped out from behind a tree, its ears flicking at every sound. Nearby, a squirrel scampered up a tree trunk, clutching an acorn in its mouth",
    "The city skyline glittered in the evening light, reflecting off the calm river. Cars hummed along the streets below, their headlights cutting through the dusk. A couple strolled hand in hand along the waterfront, pausing to watch a musician strumming a guitar. Laughter drifted from a nearby café, mingling with the aroma of freshly baked bread"]

# Generate a unique user ID for each user
def generate_unique_id():
    return str(uuid.uuid4())

# Store user IDs and usernames in a dictionary
user_info = {}

# Load existing user IDs and usernames from the CSV file
def load_user_info():
    with open('data.csv', 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            user_info[row[0]] = row[1]

load_user_info()

@app.route('/')
def home():
    paragraph = random.choice(random_paragraphs)
    return render_template('index.html', paragraph=paragraph)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username']
        paragraph = request.form['paragraph']

        if username in user_info.values():
            user_id = next(key for key, value in user_info.items() if value == username)
        else:
            user_id = generate_unique_id()
            user_info[user_id] = username

        with open('data.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([user_id, username, paragraph])

        return 'Data submitted successfully!'

@app.route('/random_paragraph', methods=['GET'])
def random_paragraph():
    paragraph = random.choice(random_paragraphs)
    return jsonify({'paragraph': paragraph})

