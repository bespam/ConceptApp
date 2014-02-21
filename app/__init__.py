from flask import Flask
import os

app = Flask(__name__)
#load secret keys locally from config.py file or from heroku config
try:
    app.config.from_object('config')
except:
    app.config['CONCEPTAPP_API_KEY'] = os.environ['CONCEPTAPP_API_KEY']
    app.config['CONCEPTAPP_CSE_ID'] = os.environ['CONCEPTAPP_CSE_ID']
    
from app import views