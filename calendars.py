from db import db
from models import User, Calendar, Category, Job, Task, Event
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

def current_user_has_owner_rights(calendar: Calendar):
    return current_user_is_calendar_owner(calendar)

def get_categories(calendar: Calendar):
    categories = db.session.query(Category).filter(Category.calendar==calendar).all()
    return categories

def create_new_category(calendar: Calendar, name: str, description: str):
    category = Category(calendar_id=calendar.id, name=name, description=description)
    db.session.add(category)
    db.session.commit()

def get_jobs(category: Category):
    jobs = db.session.query(Job).filter(Job.category==category).all()
    return jobs