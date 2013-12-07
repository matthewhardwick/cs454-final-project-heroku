import os
from flask import Flask,jsonify,render_template

app = Flask(__name__)
file = None

@app.route('/')
def index():
    file = open('inputfile1.txt').readlines()
    return render_template('index.html', input_file=file)

@app.route('/json')
def hello():
    someDict = { 'thisKey': 'value' }
    if file is None:
        file = []
    return jsonify(results = file)
