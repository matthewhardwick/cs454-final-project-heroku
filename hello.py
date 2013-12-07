import os
from flask import Flask
#import flask

app = Flask(__name__)

@app.route('/')
def hello():
    someDict = { thisKey: value }
    #return flask.jsonify(someDict)
    return "hello"
