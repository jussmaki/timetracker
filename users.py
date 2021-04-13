from db import db
from models import User
from flask_login.utils import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

def load_user(user_id):
    return db.session.query(User).get(user_id)

def user_exists(username: str):
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
    if user is not None and check_password_hash(user.password_hash, password):
        return login_user(user)
    return False
def logout():
    return logout_user()

def get_user_by_id(id: int):
    return db.session.query(User).filter_by(id=id).first()