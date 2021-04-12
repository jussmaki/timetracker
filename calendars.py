from app import app
#from wtforms.validators import ValidationError
from db import db
from models import User, Calendar, Category, Job, Task, Event
from users import current_user
from sqlalchemy import literal

def create_new_calendar(name: str, description: str):
    calendar = Calendar(owner_id=current_user.id, name=name, description=description)
    db.session.add(calendar)
    db.session.commit()
    #calendar_id = calendar.id
    print("id:", calendar.id)
    return calendar.id

def get_users_calendars(user: User):
    #calendars = db.session.query(Calendar).filter_by(id=user.id)
    calendars = db.session.query(Calendar).filter_by(owner_id=user.id).all()
    #calendars = db.session.query(User).join(Calendar.owner_id)
    print(calendars)
    return calendars

def get_calendar_by_id(id: int):
    return db.session.query(Calendar).filter_by(id=id).first()


def current_user_is_calendar_owner(calendar: Calendar):
    if calendar is None:
        return False
    if (db.session.query(Calendar).filter_by(id=calendar.id, owner_id=current_user.id).first()):
        return True
    return False

#def get_all_calendar_objects(calendar: Calendar):
    #calendar = db.session.query(Calendar).filter_by(id=id).first()
    #categories = db.session.query(Category).filter_by(calendar_id=calendar.id).all()
    #jobs = db.session.query(Job).join(Category.id).join
#    objects = db.session.query(Calendar, Category, Job, Task, Event).select_from(Calendar).join(Category, isouter=True).join(Job, isouter=True).join(Task).join(Event, isouter=True).filter(Calendar.id == calendar.id).all()
#    print(objects)
#    return objects

#def get_calendars_categories(calendar: Calendar):
#    categories = db.session.query(Category).filter_by(calendar_id=calendar.id)
#    return categories

def get_categories(calendar: Calendar):
    categories = db.session.query(Category).filter(Category.calendar==calendar).all()
    #print(categories)
    return categories

def create_new_category(calendar: Calendar, name: str, description: str):
    category = Category(calendar_id=calendar.id, name=name, description=description)
    db.session.add(category)
    db.session.commit()    

def get_jobs(category: Category):
    jobs = db.session.query(Job).filter(Job.category==category).all()
    return jobs