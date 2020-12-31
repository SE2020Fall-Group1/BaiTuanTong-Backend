from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_mail import Mail
from flask_login import LoginManager
db = SQLAlchemy()
cache = Cache()
mail = Mail()
login_manager = LoginManager()
