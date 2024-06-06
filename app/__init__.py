from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c4e53ee2876e8fed39373a33a80bd15a'

from app.models import home