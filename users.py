from app import app
from db import db
from automap import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'login'
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