from flask.globals import request
from app import app
from flask.helpers import flash
from forms import FlaskForm, DeleteCalendar, ModifyCalendar, DeleteCalendar, RegisterForm, LoginForm, LogoutForm
from forms import CreateCalendar, CreateCategory, ModifyCategory, DeleteCategory, JobForm, TaskForm
import datetime
from flask import render_template, redirect
import users
import calendars
from flask_login import current_user, login_required

@app.route("/", methods=["GET"])
def index():
    if not current_user.is_authenticated:
        return redirect("/login")
    return redirect("/calendars")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/calendars")
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if users.register_new_user(register_form.realname.data, register_form.username.data, register_form.password1.data):
            users.login(register_form.username.data, register_form.password1.data)
            return redirect("/calendars")
    return render_template("register.html", register_form=register_form)

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


@app.route("/calendars", methods=["GET", "POST"])
@login_required
def calendars_view():
    logout_form = LogoutForm()
    create_calendar_form = CreateCalendar()
    if create_calendar_form.validate_on_submit():
        new_calendar_id = calendars.create_new_calendar(create_calendar_form.name.data, create_calendar_form.description.data)
        return redirect("/calendar/"+str(new_calendar_id)+"/settings?tab=categories_and_jobs")
    return render_template("crud_calendars.html", users_calendars = calendars.get_users_calendars(current_user),
        create_calendar_form=create_calendar_form, current_user=current_user, logout_form=logout_form)

@app.route("/calendar/<int:id>/settings", methods=["GET", "POST"])
@login_required
def calendar_settings(id: int):
    calendar = calendars.get_calendar_by_id(id)
    if not calendars.current_user_has_modify_rights(calendar):
        return "forbidden", 403
    if not request.args.get("tab"):
        return redirect("/calendar/"+str(calendar.id)+"/settings?tab=basics")
    
    users_calendars=calendars.get_users_calendars(current_user)
    logout_form = LogoutForm()
    delete_calendar_form = DeleteCalendar()
    delete_calendar_form.expected.data = calendar.name
    modify_calendar_form = ModifyCalendar()
    create_category_form = CreateCategory()
    delete_category_form = DeleteCategory()
    modify_category_form = ModifyCategory()
    job_form =JobForm()

    categories = calendars.get_categories(calendar)

    #form actions
    tab = request.args.get("tab", "", str)
    action = request.args.get("action", "", str)
    category_id = request.args.get("category_id", None, int)
    category = None
    if category_id:
        category = next(c for c in categories if c.id == category_id)
    jobs = None
    job_id = request.args.get("job_id", None, int)
    if action == "view_jobs" or job_id:
        jobs = calendars.get_jobs(category)
    job = None
    if job_id:
        job = next(j for j in jobs if j.id == job_id)

    if tab == "basics":
        if action == "modify":
            if modify_calendar_form.validate_on_submit():
                calendar.name = modify_calendar_form.name.data
                calendar.description = modify_calendar_form.description.data
                calendar.private = modify_calendar_form.private.data
                calendars.modify_calendar(calendar)
                return redirect("/calendar/"+str(calendar.id)+"/settings?tab=basics&action=modify&success=true")
        elif action == "delete":
            if not calendars.current_user_has_owner_rights(calendar):
                return "forbidden", 403
            if delete_calendar_form.validate_on_submit():
                calendars.delete_calendar(calendar)
                return redirect("/calendars")
    elif tab == "categories_and_jobs":
        if action == "new_category":
            if create_category_form.validate_on_submit():
                calendars.create_new_category(calendar, create_category_form.name.data, create_category_form.description.data)
            else:
                flash_errors_in_form(create_category_form)
            return redirect("/calendar/"+str(calendar.id)+"/settings?tab=categories_and_jobs")
        elif action == "modify_category" and category_id:
            if modify_category_form.validate_on_submit():
                category.name = modify_category_form.name.data
                category.description = modify_category_form.description.data
                calendars.modify_category(calendar, category)
            else:
                flash_errors_in_form(modify_category_form)
            return redirect("/calendar/"+str(calendar.id)+"/settings?tab=categories_and_jobs")
        elif action == "delete_category" and category_id:
                if delete_category_form.validate_on_submit():
                    calendars.delete_category(calendar, category_id)
                    return redirect("/calendar/"+str(calendar.id)+"/settings?tab=categories_and_jobs")
        elif action == "new_job":
            if job_form.validate_on_submit():
                calendars.create_new_job(category, job_form.name.data, job_form.description.data)
            else:
                flash_errors_in_form(job_form)
            return redirect("/calendar/"+str(calendar.id) + 
                "/settings?tab=categories_and_jobs&action=view_jobs&category_id="+str(category_id))
        elif action == "modify_job":
            if job_form.validate_on_submit():
                job.name = job_form.name.data
                job.description = job_form.description.data
                calendars.modify_job(job)
            else:
                flash_errors_in_form(job_form)
            return redirect("/calendar/"+str(calendar.id) + 
                "/settings?tab=categories_and_jobs&action=view_jobs&category_id="+str(category_id))
        elif action == "delete_job":
            if job_form.validate_on_submit():
                calendars.delete_job(job)
            else:
                flash_errors_in_form(job_form)
            return redirect("/calendar/"+str(calendar.id) +
                "/settings?tab=categories_and_jobs&action=view_jobs&category_id="+str(category_id))

    return render_template("calendar_settings.html", logout_form=logout_form, modify_calendar_form=modify_calendar_form, 
        delete_calendar_form=delete_calendar_form, create_category_form=create_category_form, modify_category_form=modify_category_form,
        delete_category_form=delete_category_form, job_form=job_form,
        calendar=calendar, users_calendars=users_calendars, categories=categories, jobs=jobs, category=category, current_user=current_user)


@app.route("/calendar/<int:id>", methods=["GET", "POST"])
@login_required
def calendar(id):
    calendar = calendars.get_calendar_by_id(id)
    if not calendars.calendar_is_public_or_current_user_has_view_rights(calendar):
        return "forbidden", 403

    logout_form = LogoutForm()
    task_form = TaskForm()
    jobs = calendars.get_jobs_by_calendar(calendar)
    tasks = calendars.get_tasks(calendar)

    #form actions
    action = request.args.get("action", "", str)
    job_id = request.args.get("job_id", None, int)
    task_id = request.args.get("task_id", None, int)
    if job_id:
        job = next(j for j in jobs if j.id == job_id)
    task = None
    if task_id:
        task = next(t for t in tasks if t.id == task_id)
    if action == "new_task":
        if task_form.validate_on_submit():
            calendars.create_new_task(job, task_form.name.data, task_form.description.data, task_form.planned_time.data)
        else:
            flash_errors_in_form(task_form)
        return redirect("/calendar/"+str(calendar.id)+"?view=tasks")
    elif action == "delete_task":
        if task_form.validate_on_submit():
            calendars.delete_task(task)
        else:
            flash_errors_in_form(task_form)
        return redirect("/calendar/"+str(calendar.id)+"?view=tasks")
    elif action == "modify_task":
        if task_form.validate_on_submit():
            task.name = task_form.name.data
            task.description = task_form.description.data
            task.done = task_form.done.data
            task.planned_time = task_form.actual_time.data
            task.actual_time = task_form.actual_time.data
            calendars.modify_task(task)
        else:
            flash_errors_in_form(task_form)
        return redirect("/calendar/"+str(calendar.id)+"?view=tasks&task_id="+str(task_id))

    if not request.args.get("view"):
        return redirect("/calendar/"+str(calendar.id)+"?view=tasks")

    return render_template("calendar.html", logout_form=logout_form, task_form=task_form,
        calendar=calendar, users_calendars=calendars.get_users_calendars(current_user),
        jobs=jobs, tasks=tasks, selected_task=task, current_user=current_user)

def flash_errors_in_form(form: FlaskForm):
    for field, errors in form.errors.items():
        for error in errors:
            flash(error)

