from sqlalchemy.sql.sqltypes import Integer
from werkzeug.exceptions import default_exceptions
from app import app
from users import user_exists
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from os import getenv

app.config['RECAPTCHA_PUBLIC_KEY'] = getenv("RECAPTCHA_PUBLIC_KEY")
app.config['RECAPTCHA_PRIVATE_KEY'] = getenv("RECAPTCHA_PRIVATE_KEY")

class RegisterForm(FlaskForm):
    realname = StringField("realname", validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    password1 = StringField("password1", validators=[DataRequired()])
    password2 = StringField("password2", validators=[DataRequired(), EqualTo("password1", "Passwords mismatch")])
    recaptcha = RecaptchaField()
    
    def validate_username(form, field):
        if user_exists(form.username.data):
            raise ValidationError("Username exists")

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
    recaptcha = RecaptchaField()

class CreateCalendar(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(5, 30, message="minimun length for name is 5 and maximum is 30")])
    description = StringField("description", default="")

class CreateCategory(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description", default="")  
      
class CreateJob(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description", default="")    
class CreateTask(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description", default="")
    planned_time = IntegerField("planned_time", default=0)

class CreateEvent(FlaskForm):
    start_time = DateTimeField("start_time", validators=[DataRequired()])
    end_time = DateTimeField("end_time", validators=[DataRequired()])
    planned_time = IntegerField("planned_time", default=0)
    actual_time = IntegerField("planned_time", default=0)