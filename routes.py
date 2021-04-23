from app import app
from flask.helpers import flash
from forms import RegisterForm, LoginForm, LogoutForm, CreateCalendar, CreateCategory, CreateJob, CreateTask, CreateEvent
from flask import render_template, redirect
import users
import calendars
from flask_login import current_user, login_required

@app.route("/", methods=["GET"])
def index():
    #print(current_user.realname)
    if not current_user.is_authenticated:
        #return render_template("index.html")
        return redirect("/login")
    return redirect("/calendars")

#login

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/calendars")
    #logout_form = LogoutForm()
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if users.register_new_user(register_form.realname.data, register_form.username.data, register_form.password1.data):
            users.login(register_form.username.data, register_form.password1.data)
            return redirect("/calendars")
    return render_template("register.html", register_form=register_form)#, logout_form=logout_form)

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if users.login(login_form.username.data, login_form.password.data):
            return redirect("/calendars")
        else:
            flash("Wrong username or password")
    return render_template("login.html", login_form=login_form, current_user=current_user)

@app.route("/logout", methods=["POST"])
def logout_post_reg():
    users.logout()
    return redirect("/logout")

@app.route("/logout", methods=["GET"])
def logout_get_reg():
    if current_user.is_authenticated:
        return "error logging out"
    return "<p>logout successfull</p> <a href=\"/\">Frontpage</a>"


#calendars

@login_required
@app.route("/calendars", methods=["GET", "POST"])
def calendars_view():
    logout_form = LogoutForm()
    create_calendar_form = CreateCalendar()
    if create_calendar_form.validate_on_submit():
        new_calendar_id = calendars.create_new_calendar(create_calendar_form.name.data, create_calendar_form.description.data)
        return redirect("/calendar/"+str(new_calendar_id)+"/settings")
    return render_template("crud_calendars.html",
    users_calendars = calendars.get_users_calendars(current_user), create_calendar_form=create_calendar_form, logout_form=logout_form)

@login_required
@app.route("/calendar/<int:id>/settings", methods=["GET", "POST"])
def calendar_settings(id: int):
    calendar = calendars.get_calendar_by_id(id)
    if not calendars.current_user_has_modify_rights(calendar):
        return "forbidden", 403

    logout_form = LogoutForm()
    create_category_form = CreateCategory()
    create_job_form = CreateJob()
    create_task_form = CreateTask()
    create_event_form = CreateEvent()

    if create_category_form.validate_on_submit():
        calendars.create_new_category(calendar, create_category_form.name.data, create_category_form.description.data)

    return render_template("calendar_settings.html",
    logout_form=logout_form, category_form=create_category_form, job_form=create_job_form, task_form=create_task_form, event_form=create_event_form,
    calendar=calendar, users_calendars=calendars.get_users_calendars(current_user), get_categories=calendars.get_categories, get_jobs=calendars.get_jobs, current_user=current_user)


#@app.route("/calendar/<int:id>/full", methods=["GET", "POST"])
#def calendar_testi(id):
#    calendar = calendars.get_calendar_by_id(id)
#    if not calendars.current_user_is_calendar_owner(calendar):
#        return "forbidden", 403
#    
#    create_category_form = CreateCategory()
#    create_job_form = CreateJob()
#    create_task_form = CreateTask()
#    create_event_form = CreateEvent()
#
#    if create_category_form.validate_on_submit():
#        calendars.create_new_category(calendar, create_category_form.name.data, create_category_form.description.data)
#
#    return render_template("full.html",
#    category_form=create_category_form, job_form=create_job_form, task_form=create_task_form, event_form=create_event_form,
#    calendar=calendar, users_calendars=calendars.get_users_calendars(current_user), get_categories=calendars.get_categories, get_jobs=calendars.get_jobs, current_user=current_user)

@app.route("/calendar/<int:id>", methods=["GET", "POST"])
@login_required
def calendar(id):
    calendar = calendars.get_calendar_by_id(id)
    if not calendars.current_user_is_calendar_owner(calendar):
        return "forbidden", 403
    
    logout_form = LogoutForm()
    create_category_form = CreateCategory()
    create_job_form = CreateJob()
    create_task_form = CreateTask()
    create_event_form = CreateEvent()

    if create_category_form.validate_on_submit():
        calendars.create_new_category(calendar, create_category_form.name.data, create_category_form.description.data)

    return render_template("calendar.html",
    logout_form=logout_form, category_form=create_category_form, job_form=create_job_form, task_form=create_task_form, event_form=create_event_form,
    calendar=calendar, users_calendars=calendars.get_users_calendars(current_user), get_categories=calendars.get_categories, get_jobs=calendars.get_jobs, current_user=current_user)

    