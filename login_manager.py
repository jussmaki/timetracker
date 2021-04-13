from app import app
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from users import load_user
    return load_user(user_id)