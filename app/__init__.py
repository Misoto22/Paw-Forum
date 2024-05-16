from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from .models import db
import os


# Create app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)

    # Ensure the database file path exists
    database_path = os.path.join(app.root_path, 'app.db')
    if not os.path.exists(database_path):
        open(database_path, 'w').close()

    # Create database tables
    with app.app_context():
        db.create_all()

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Load user from database
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User # Import here to avoid circular dependencies
        return User.query.get(int(user_id))
    
    from .routes import init_app_routes  # Import routes after db to avoid circular import
    init_app_routes(app) # Initialize routes

    return app
