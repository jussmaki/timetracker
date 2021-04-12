#from flask.app import Flask
#from models import Calendar
from operator import methodcaller
from flask.helpers import flash
from flask_wtf import form
from app import app
from forms import RegisterForm, LoginForm, CreateCalendar, CreateCategory, CreateJob, CreateTask, CreateEvent
#from flask import session
from flask import render_template, redirect
import users
import calendars
from flask_login import current_user, login_required

@app.route("/", methods=["GET", "POST"])
def index():
    #print(current_user.realname)
    if not current_user.is_authenticated:
        return render_template("index.html")
    return calendars_view()

#login

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
        return "<p>logout successfull</p> <a href=\"/\">Frontpage</a>"
    return "error logging out"

#calendars

def calendars_view():
    create_calendar_form = CreateCalendar()
    if create_calendar_form.validate_on_submit():
        new_calendar_id = calendars.create_new_calendar(create_calendar_form.name.data, create_calendar_form.description.data)
        redirect("/calendar/"+str(new_calendar_id))
    return render_template("crud_calendars.html",
    users_calendars = calendars.get_users_calendars(current_user), create_calendar_form=create_calendar_form)

@app.route("/calendar/<int:id>", methods=["GET", "POST"])
@login_required
def calendar(id):
    calendar = calendars.get_calendar_by_id(id)
    if not calendars.current_user_is_calendar_owner(calendar):
        return "forbidden", 403
    #calendar.ca
    #testi = calendars.get_all_calendar_objects(calendar)
    #print(testi)
    #return("toimii")
    
    create_category_form = CreateCategory()
    create_job_form = CreateJob()
    create_task_form = CreateTask()
    create_event_form = CreateEvent()

    if create_category_form.validate_on_submit():
        calendars.create_new_category(calendar, create_category_form.name.data, create_category_form.description.data)

    return render_template("calendar.html",
    category_form=create_category_form, job_form=create_job_form, task_form=create_task_form, event_form=create_event_form,
    calendar=calendar, users_calendars=calendars.get_users_calendars(current_user), get_categories=calendars.get_categories, get_jobs=calendars.get_jobs, current_user=current_user)

    