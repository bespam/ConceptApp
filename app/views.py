from flask import render_template
from app import app


@app.route('/')
def index():
    posts = [
    { 
        'author': { 'nickname': 'John' }, 
        'body': 'Beautiful day in Portland!' 
    },
    { 
        'author': { 'nickname': 'Susan' }, 
        'body': 'The Avengers movie was so cool!' 
    }
    return render_template('index.html',
        title = 'Home',
        user = "Igor",
        posts = posts)
    