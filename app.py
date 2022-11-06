from flask import Flask, jsonify, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.automap import automap_base
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy.orm import Session
import pandas as pd

# instantiate Flask object 
app = Flask(__name__)

@app.route('/')
def home():
    str = 'Hello World !'
    return str



if __name__ == '__main__':
    app.run(debug=True)

