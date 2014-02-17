from flask import Flask
from flask import render_template


@app.route('/')
@app.route('/index')

def index():
    return "Hello ConceptNet5!"
    