from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Table, Text, text
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from db import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    realname = Column(Text, nullable=False)
    username = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)

class Calendar(db.Model):
    __tablename__ = 'calendars'

    id = Column(Integer, primary_key=True)
    owner_id = Column(ForeignKey('users.id'))
    name = Column(Text)
    description = Column(Text)
    private = Column(Boolean, nullable=False, server_default=text("true"))

    owner = relationship('User')

#t_access_rights = Table(
#    'access_rights', metadata,
#    Column('calendar_id', ForeignKey('calendars.id')),
#    Column('user_id', ForeignKey('users.id')),
#    Column('view_calendar', Boolean, nullable=False),
#    Column('modify_calendar', Boolean, nullable=False),
#    Column('change_rights', Boolean, nullable=False),
#    Column('delete_calendar', Boolean, nullable=False)
#)

class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    calendar_id = Column(ForeignKey('calendars.id'))
    name = Column(Text, nullable=False)
    description = Column(Text)

    calendar = relationship('Calendar')

class Job(db.Model):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    category_id = Column(ForeignKey('categories.id'))
    name = Column(Text, nullable=False)
    description = Column(Text)

    category = relationship('Category')

class Task(db.Model):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    job_id = Column(ForeignKey('jobs.id'))
    #calendar_id = Column(ForeignKey('calendars.id'))
    name = Column(Text, nullable=False)
    description = Column(Text)
    planned_time = Column(Integer, server_default=text("0"))

    #calendar = relationship('Calendar')
    job = relationship('Job')

class Event(db.Model):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    task_id = Column(ForeignKey('tasks.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    #planned_time = Column(Integer)
    actual_time = Column(Integer)

    task = relationship('Task')
