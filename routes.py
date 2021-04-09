from wtforms.validators import ValidationError
from forms import RegisterForm
from app import app
from flask import session
from flask import render_template, redirect
import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
            if users.register_new_user(form.realname.data, form.username.data, form.password1.data):
                return render_template("create_user_success.html")
    return render_template('register.html', form=form)

@app.route("/login")
def login():
    return ""