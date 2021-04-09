from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

database_url = getenv("DATABASE_URL").replace("postgres://", "postgresql://") #to make heroku postgres database url compatible with SQLAlchemy 1.4.x :)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False

if getenv("FLASK_ENV") == "development":
    app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

import automap