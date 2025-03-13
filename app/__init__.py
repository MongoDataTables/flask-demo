# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app(config_object=None):
    app = Flask(__name__)

    # Configure the app
    if config_object:
        app.config.from_object(config_object)
    else:
        from app.config import Config
        app.config.from_object(Config)

    # Initialize extensions
    mongo.init_app(app)

    # IMPORTANT: Add this line to attach mongo to app
    app.mongo = mongo

    # Verify MongoDB connection
    with app.app_context():
        try:
            mongo.db.command('ping')
            print("MongoDB connected successfully!")

            # Initialize database (create indexes, etc.)
            from app.db_init import create_indexes
            create_indexes()
        except Exception as e:
            print(f"MongoDB connection error: {e}")

    # Register blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
