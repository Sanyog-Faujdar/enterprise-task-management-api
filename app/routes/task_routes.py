from flask import Blueprint,request
from flask_jwt_extended import get_jwt_identity,jwt_required
from app.extensions import db
from app.models.task_models import Task
from app.models.task_assignment_model import TaskAssignment
from datetime import datetime
task_bp = Blueprint('task',__name__)

@task_bp.route('/tasks',methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())
    
    task = db.session.query(Task).join(TaskAssignment,Task.task_id == TaskAssignment.task_id).filter(TaskAssignment.user_id == user_id).all()
    
    return [{"task_id":task.task_id,
             "title":task.tiltle,
             "status":task.status,
             "deadline":task.deadline.isoformat()}],200

# @task_bp.route('/tasks/<int:task_id>',methods=["GET"])
# @jwt_required()
# def get_task(task_id):
#     user_id = int(get_jwt_identity())
#     task = db.session.get(Task,task_id)
#     if not task:
#         return {"message": "task not found"}, 404
#     for u_id in user_ids:
#         if u_id == user_id:
            

@task_bp.route('/tasks',methods = ["POST"])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    
    data = request.get_json()
    
    if not data:
        return {"message":"invalid input"},400
    
    print(data)
    title = data.get('title')
    description = data.get('description')
    deadline = datetime.strptime(data.get("deadline"),"%Y-%m-%d").date()
    status = data.get('status') 
    created_by = user_id
    
    if not title or not deadline or not status:
        return {"message":"invalid input"},400
    
    task = Task(title = title,
                description = description,
                deadline = deadline,
                status = status,
                created_by = created_by)
    db.session.add(task)
    
    db.session.flush()
    
    task_id = task.task_id 
    task_assign = TaskAssignment(task_id = task_id,
                    user_id = user_id)
    db.session.add(task_assign)
   
    db.session.commit()
    
    return{
        "message":"task added successfully",
        "task_id":task.task_id,
        "title": task.title,
        "description":task.description,
        "created_at":task.created_at.isoformat(),
        "deadline":task.deadline.isoformat()
    },201
