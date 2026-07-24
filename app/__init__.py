from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.task_routes import task_bp
from app.config import Config
from app.extensions import db,migrate,jwt
from flasgger import Swagger

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
    swagger_template = {
        "swagger":"2.0",
        "info":{
            "title":"Enterprise Task Manangement API",
            "description":"REST API built with flask , PostgreSQL and JWT Authentication featuring RBAC , Activity Logs , Dashboard analytics and Task Workflow.",
            "version":"1.0.0",
            "contact":{
                "name":"Sanyog Faujdar"
            }
        }, 
        "securityDefinitions":{
            "Bearer":{
                "type":"apiKey",
                "name":"Authorization",
                "in":"header",
                "description":(
                    "Enter JWT token in this format:\n\n"
                    "Bearer <your_access_token>"
                )
            }
        }
    }
    Swagger(app,template = swagger_template)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    return app

@app.route("/")
def home():
    return {
        "status": "running",
        "project": "Enterprise Task Management API",
        "docs": "/apidocs/"
    }, 200