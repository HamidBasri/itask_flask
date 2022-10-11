import imp
from flask import Flask

from api.utils import logger
from api.config.config import Config, Permissions
from api.config.migrate import initialize_database
from api.config.routes import generate_routes
from api.config.loader import db, bcrypt, login_manager, marshmallow
import os



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize database
    db.init_app(app)

    # Check if there is no database.
    if not os.path.exists(Config.DATABASE_PATH):
        with app.app_context():
            # New db app if no database.
            db.app = app

           
            try:
                # Create all database tables.
                db.create_all()
                
                initialize_database(db)
        
            except Exception as e:
                logger.error(e)
                os.remove(Config.DATABASE_PATH)
                raise Exception("Failed initialize database")

    bcrypt.init_app(app)
    login_manager.init_app(app)
    marshmallow.init_app(app)

    # Generate routes.
    generate_routes(app)

    return app
