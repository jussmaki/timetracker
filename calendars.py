from db import db
from models import User, Calendar, Category, Job, Task
from flask_login import current_user

def create_new_calendar(name: str, description: str):
    calendar = Calendar(owner_id=current_user.id, name=name, description=description)
    db.session.add(calendar)
    db.session.commit()
    return calendar.id
def modify_calendar(calendar: Calendar, name: str, description: str, private: bool):
    db.session.query(Calendar).filter(Calendar.id == calendar.id).update(
        {Calendar.name: name, Calendar.description: description, Calendar.private: private})
    db.session.commit()

def modify_calendar(calendar: Calendar):
    db.session.query(Calendar).filter(Calendar.id == calendar.id).update(
        {Calendar.name: calendar.name, Calendar.description: calendar.description, Calendar.private: calendar.private})
    db.session.commit()

def delete_calendar(calendar: Calendar):
    db.session.query(Calendar).filter(Calendar.id == calendar.id).delete()
    db.session.commit()

def get_users_calendars(user: User):
    calendars = db.session.query(Calendar).filter_by(owner_id=user.id).all()
    return calendars

def get_calendar_by_id(id: int):
    return db.session.query(Calendar).filter_by(id=id).first()


def current_user_is_calendar_owner(calendar: Calendar):
    if calendar is None:
        return False
    if (db.session.query(Calendar).filter_by(id=calendar.id, owner_id=current_user.id).first()):
        return True
    return False

def current_user_has_modify_rights(calendar: Calendar):
    return current_user_is_calendar_owner(calendar)
    #if calendar is None:
    #    return False
    #if (db.session.query(Calendar).
    #if (db.session.query(Calendar).filter_by(id=calendar.id, owner_id=current_user.id).first()):
    #    return True
    #return False

def calendar_is_public_or_current_user_has_view_rights(calendar: Calendar):
    #to be done
    return current_user_is_calendar_owner(calendar)

def current_user_has_owner_rights(calendar: Calendar):
    return current_user_is_calendar_owner(calendar)

def get_categories(calendar: Calendar):
    categories = db.session.query(Category).filter(Category.calendar==calendar).all()
    return categories

def create_new_category(calendar: Calendar, name: str, description: str):
    category = Category(calendar_id=calendar.id, name=name, description=description)
    db.session.add(category)
    db.session.commit()

def delete_category(calendar: Calendar, category_id: int):
    db.session.query(Category).filter(Category.id == category_id, Category.calendar_id == calendar.id).delete()
    db.session.commit()

def modify_category(calendar: Calendar, category: Category):
    #db.session.query(Category).filter(Category.id == category.id, Category.calendar_id.id == calendar.id).update(
    #    {Category.name: category.name, Category.description: calendar.description})
    #db.session.commit()    
    db.session.query(Category).filter(Category.id == category.id).update(
        {Category.name: category.name, Category.description: category.description})
    db.session.commit()    

def get_jobs(category: Category):
    jobs = db.session.query(Job).filter(Job.category==category).all()
    return jobs

def get_jobs_by_calendar(calendar: Calendar):
    jobs = db.session.query(Job).select_from(Calendar).join(Category, Category.calendar_id == Calendar.id).join(Job, Job.category_id == Category.id).filter(Calendar.id == calendar.id).all()
    return jobs

def create_new_job(category: Category, name: str, description:str):
    job = Job(category_id = category.id, name = name, description = description)
    db.session.add(job)
    db.session.commit()

def modify_job(job: Job):
    #db.session.query(Category).filter(Category.id == category.id, Category.calendar_id.id == calendar.id).update(
    #    {Category.name: category.name, Category.description: calendar.description})
    #db.session.commit()    
    db.session.query(Job).filter(Job.id == job.id).update(
        {Job.name: job.name, Job.description: job.description})
    db.session.commit()    

def delete_job(job: Job):
    db.session.query(Job).filter(Job.id == job.id).delete()
    db.session.commit()

def create_new_task(job: Job, name: str, description: str, planned_time: int):
    task = Task(job_id=job.id, name=name, description=description, planned_time=planned_time)
    db.session.add(task)
    db.session.commit()

def get_tasks(calendar: Calendar):
    
    tasks = db.session.query(Task).select_from(Calendar).join(Category, Category.calendar_id == Calendar.id).join(Job, Job.category_id == Category.id).join(Task, Task.job_id == Job.id).filter(Calendar.id == calendar.id).all()
    

    #tasks = db.session.query(Calendar, Category, Job, Task).join(Category, Category.calendar_id == Calendar.id).join(Job, Job.category_id == Category.id).join(Task, Task.job_id == Job.id).filter(Calendar.id == calendar.id).all()
    
    #tasks = db.session.query(Calendar, Category, Job, Task).select_from(Task).join(Category).join(Job).join(Task).filter(Calendar.id == calendar.id).all()
    
    #.filter(Calendar.id == calendar.id).all()
    
    #).filter(Job.category==category).all()
    return tasks