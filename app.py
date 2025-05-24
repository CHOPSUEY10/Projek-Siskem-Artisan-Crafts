import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

def create_app():
    # create the app
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # configure logging
    logging.basicConfig(level=logging.DEBUG)
    
    # configure the database
    database_url = os.environ.get("DATABASE_URL", "sqlite:///artisan_crafts.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # initialize the app with the extension
    db.init_app(app)
    
    with app.app_context():
        # Import models here so they're registered with SQLAlchemy
        import models  # noqa: F401
        
        # Create all tables
        db.create_all()
        
        # Initialize sample data if database is empty
        from utils import init_sample_data
        init_sample_data()
    
    # Register blueprints
    from core import bp as core_bp
    app.register_blueprint(core_bp)
    
    from auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app

# Create the app instance
app = create_app()
