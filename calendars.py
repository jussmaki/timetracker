from app import app
#from wtforms.validators import ValidationError
from db import db
from models import User, Calendar
from users import current_user

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