from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import models

import routes

@app.before_first_request
def initialize_database():
    from db import db
    #db.drop_all()
    db.create_all()