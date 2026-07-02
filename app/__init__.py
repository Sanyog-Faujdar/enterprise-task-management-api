from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.task_routes import task_bp
from app.config import Config
from app.extensions import db,migrate,jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    from app.models.user_models import User
    from app.models.task_models import Task
    from app.models.task_assignment_model import TaskAssignment
    from app.models.activity_log_model import ActivityLog
    migrate.init_app(app,db)
    
    jwt.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    return app
