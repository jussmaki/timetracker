from wtforms.fields.core import BooleanField
from app import app
from users import user_exists
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from os import getenv

app.config['RECAPTCHA_PUBLIC_KEY'] = getenv("RECAPTCHA_PUBLIC_KEY")
app.config['RECAPTCHA_PRIVATE_KEY'] = getenv("RECAPTCHA_PRIVATE_KEY")

class RegisterForm(FlaskForm):
    realname = StringField("realname", validators=[DataRequired(), Length(5, 30, message="minimun length for name is 5 and maximum is 30")])
    username = StringField("username", validators=[DataRequired(), Length(5, 30, message="minimun length for name is 5 and maximum is 30")])
    password1 = PasswordField("password1", validators=[DataRequired(), Length(5, 30, message="minimun length for password is 8 and maximum is 100")])
    password2 = PasswordField("password2", validators=[DataRequired(), EqualTo("password1", "Passwords mismatch")])
    recaptcha = RecaptchaField()
    
    def validate_username(form, field):
        if user_exists(form.username.data):
            raise ValidationError("Username exists")

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

class LogoutForm(FlaskForm):
    pass

class CreateCalendar(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(3, 30, message="minimun length for name is 3 and maximum is 30")])
    description = StringField("description", default="", validators=[Length(0, 30, message="maximum lenght for description is 30")])

class ModifyCalendar(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(3, 30, message="minimun length for name is 3 and maximum is 30")])
    description = StringField("description", validators=[Length(0, 30, message="maximum length for description is 30")])
    private = BooleanField("private")

class DeleteCalendar(FlaskForm):
    expected = StringField("expected", default="")
    name = StringField("name", validators=[DataRequired(), EqualTo("expected", "Calendar name does not match")])
    delete = BooleanField("delete", validators=[DataRequired()])

class CreateCategory(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(3, 30, message="minimun length for name is 3 and maximum is 30")])
    description = StringField("description", default="", validators=[Length(0, 30, message="maximum length for description is 30")])  

class ModifyCategory(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(3, 30, message="minimun length for name is 3 and maximum is 30")])
    description = StringField("description", validators=[Length(0, 30, message="maximum length for description is 30")])

class DeleteCategory(FlaskForm):
    delete = BooleanField("delete", validators=[DataRequired()])
      
class JobForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description", default="", validators=[Length(0, 30, message="maximum length for description is 30")])
    delete = BooleanField("delete", default=False)

class TaskForm(FlaskForm):
    job_id = IntegerField("id", default=0)
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description", default="", validators=[Length(0, 30, message="maximum length for description is 30")])
    done = BooleanField("done", default=False)
    planned_time = IntegerField("planned_time", default=0)
    actual_time = IntegerField("actual_time", default=0)
    delete = BooleanField("delete", default=False)