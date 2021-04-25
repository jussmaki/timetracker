from flask.globals import request
from app import app
from flask.helpers import flash
from forms import DeleteCalendar, ModifyCalendar, DeleteCalendar, RegisterForm, LoginForm, LogoutForm, CreateCalendar, CreateCategory, CreateJob, CreateTask, CreateEvent
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
        return "error logging out", 500
    return redirect("/")


#calendars

@app.route("/calendars", methods=["GET", "POST"])
@login_required
def calendars_view():
    logout_form = LogoutForm()
    create_calendar_form = CreateCalendar()
    if create_calendar_form.validate_on_submit():
        new_calendar_id = calendars.create_new_calendar(create_calendar_form.name.data, create_calendar_form.description.data)
        return redirect("/calendar/"+str(new_calendar_id)+"/settings?tab=categories_and_jobs")
    return render_template("crud_calendars.html",
    users_calendars = calendars.get_users_calendars(current_user), create_calendar_form=create_calendar_form, current_user=current_user, logout_form=logout_form)

@app.route("/calendar/<int:id>/settings", methods=["GET", "POST"])
@login_required
def calendar_settings(id: int):
    calendar = calendars.get_calendar_by_id(id)
    if not calendars.current_user_has_modify_rights(calendar):
        return "forbidden", 403
    if not request.args.get("tab"):
        return redirect("/calendar/"+str(calendar.id)+"/settings?tab=basics")
    logout_form = LogoutForm()
    delete_calendar_form = DeleteCalendar()
    delete_calendar_form.expected.data = calendar.name
    modify_calendar_form = ModifyCalendar()
    create_category_form = CreateCategory()
    create_job_form = CreateJob()
    create_task_form = CreateTask()
    create_event_form = CreateEvent()

    #form actions
    action = request.args.get("action", "none", str)
    if action == "modify":
        if not calendars.current_user_has_modify_rights(calendar):
            return "forbidden", 403
        if modify_calendar_form.validate_on_submit():
            calendar.name = modify_calendar_form.name.data
            calendar.description = modify_calendar_form.description.data
            calendar.private = modify_calendar_form.private.data
            calendars.modify_calendar(calendar)
            return redirect("/calendar/"+str(calendar.id)+"/settings?tab=basics&action=modify&success=true")
        else:
            #return render_template?
            pass
    elif action == "delete":
        if not calendars.current_user_has_owner_rights(calendar):
            return "forbidden", 403
        if delete_calendar_form.validate_on_submit():
            calendars.delete_calendar(calendar)
            return redirect("/calendars")

    #after form handling, so does not overwrite data received

    modify_calendar_form.name.data = calendar.name
    modify_calendar_form.description.data = calendar.description
    modify_calendar_form.private.data = calendar.private

    #print(modify_calendar_form.is_submitted(), create_category_form.is_submitted())

    #if create_category_form.validate_on_submit():
    #    calendars.create_new_category(calendar, create_category_form.name.data, create_category_form.description.data)

    return render_template("calendar_settings.html",
    logout_form=logout_form, modify_calendar_form=modify_calendar_form, delete_calendar_form=delete_calendar_form, category_form=create_category_form, job_form=create_job_form, task_form=create_task_form, event_form=create_event_form,
    calendar=calendar, users_calendars=calendars.get_users_calendars(current_user), get_categories=calendars.get_categories, get_jobs=calendars.get_jobs, current_user=current_user)

@app.route("/calendar/<int:id>/settings/modify", methods=["POST"])
@login_required
def modify_calendar(id: int):
    calendar = calendars.get_calendar_by_id(id)
    if not calendars.current_user_has_modify_rights(calendar):
        return "forbidden", 403
    modify_calendar_form = ModifyCalendar()
    if modify_calendar_form.validate_on_submit():
        calendar.name = modify_calendar_form.name.data
        calendar.description = modify_calendar_form.description.data
        calendar.private = modify_calendar_form.private.data
        calendars.modify_calendar(calendar)
        #calendars.modify_calendar(calendar, modify_calendar_form.name.data, modify_calendar_form.description.data, modify_calendar_form.private.data)
    #error_str = ""
    #for errors in modify_calendar_form.errors.items():
    #    error_str.join(errors)
    #if error_str != "": flash(error_str)
    return redirect("/calendar/"+str(calendar.id)+"/settings?tab=basics")


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
    if not request.args.get("view"):
        return redirect("/calendar/"+str(calendar.id)+"?view=week")   
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

    