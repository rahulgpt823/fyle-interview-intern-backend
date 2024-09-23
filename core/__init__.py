# core/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configure the SQLAlchemy part of the app instance
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Import and register blueprints
    from core.apis.assignments import student_assignments_resources, teacher_assignments_resources
    from core.apis.assignments.principal import principal_api
    app.register_blueprint(student_assignments_resources, url_prefix='/student')
    app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
    app.register_blueprint(principal_api, url_prefix='/principal')

    # Import and register error handlers
    from core.server import register_error_handlers
    register_error_handlers(app)

    return app