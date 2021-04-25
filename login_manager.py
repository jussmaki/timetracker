from app import app
from flask_login import LoginManager
from users import load_user

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "/login"
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return load_user(user_id)