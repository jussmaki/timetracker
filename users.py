from flask_login.utils import logout_user
from wtforms.validators import ValidationError
from app import app
from db import db
from models import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, current_user, login_user

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    #return db.session.query(User).filter_by(id=1).first()
    return db.session.query(User).get(user_id)

def user_exists(username: str):
    #print(username)
    print(db.session.query(User).filter_by(username=username).count())
    if db.session.query(User).filter_by(username=username).count() > 0:
        return True
    return False

def register_new_user(realname: str, username: str, password: str):
    user = User(realname=realname, username=username, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return True

def login(username: str, password: str):
    user = db.session.query(User).filter_by(username=username).first()
    #print(user.id)
    #print(check_password_hash(user.password_hash, password))
    if user is not None and check_password_hash(user.password_hash, password):
        #print("logged in")
        return login_user(user)
    return False
def logout():
    return logout_user()

def get_user_by_id(id: int):
    return db.session.query(User).filter_by(id=id).first()