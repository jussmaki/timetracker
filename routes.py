from logging import log
from operator import methodcaller
from flask.helpers import flash
from flask_wtf import form
from app import app
from forms import RegisterForm, LoginForm, CreateCalendar
#from flask import session
from flask import render_template, redirect
import users
import calendars
from flask_login import current_user

@app.route("/", methods=["GET", "POST"])
def index():
    #print(current_user.realname)
    if not current_user.is_authenticated:
        return render_template("index.html")
    create_calendar_form = CreateCalendar()
    if create_calendar_form.validate_on_submit():
        new_calendar_id = calendars.create_new_calendar(create_calendar_form.name.data, create_calendar_form.description.data)
        redirect("/calendar/"+str(new_calendar_id))
    return render_template("crud_calendars.html",
    users_calendars = calendars.get_users_calendars(current_user), create_calendar_form=create_calendar_form)
    

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