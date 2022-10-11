from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from api.utils.logger import create_logger

# Load necessary objects for the app
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "info"
logger = create_logger()
marshmallow = Marshmallow()
