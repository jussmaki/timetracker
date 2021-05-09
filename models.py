from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text, text
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
    private = Column(Boolean, nullable=False, server_default=text('true'))

    owner = relationship('User', cascade='all, delete', passive_deletes=True)

class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    calendar_id = Column(ForeignKey('calendars.id'))
    name = Column(Text, nullable=False)
    description = Column(Text)

    calendar = relationship('Calendar', cascade='all, delete', passive_deletes=True)

class Job(db.Model):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    category_id = Column(ForeignKey('categories.id'))
    name = Column(Text, nullable=False)
    description = Column(Text)

    category = relationship('Category', cascade='all, delete', passive_deletes=True)

class Task(db.Model):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    job_id = Column(ForeignKey('jobs.id'))
    name = Column(Text, nullable=False)
    description = Column(Text)
    done = Column(Boolean, nullable=False, server_default=text('false'))
    planned_time = Column(Integer, server_default=text("0"))
    actual_time = Column(Integer, server_default=text('0'))

    job = relationship('Job', cascade='all, delete', passive_deletes=True)