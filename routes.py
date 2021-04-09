from logging import log
from flask.helpers import flash
from app import app
from forms import RegisterForm, LoginForm
from flask import session
from flask import render_template, redirect
import users
from flask_login import current_user

@app.route("/")
def index():
    #print(current_user)
    if current_user.is_authenticated: #and current_user.get_id() != None:
        print("logged in")
        return "<a href=\"/logout\">log out</a>"
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
            if users.register_new_user(form.realname.data, form.username.data, form.password1.data):
                return render_template("create_user_success.html")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if users.login(form.username.data, form.password.data) == True:
            return redirect("/")
        else:
            flash("Wrong username or password")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    if users.logout():
        #return redirect("/")
        return "logout successfull"
    return "error logging out"