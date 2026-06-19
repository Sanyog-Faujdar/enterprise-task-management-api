from flask import Blueprint,request
from flask_jwt_extended import get_jwt_identity,jwt_required
from app.extensions import db
from app.models.task_models import Task
from app.models.user_models import User
from app.models.task_assignment_model import TaskAssignment
from datetime import datetime

task_bp = Blueprint('task',__name__)

@task_bp.route('/tasks',methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())
    
    tasks = db.session.query(Task).join(TaskAssignment,Task.task_id == TaskAssignment.task_id).filter(TaskAssignment.user_id == user_id).all()
    
    return [{"task_id":task.task_id,
             "title":task.title,
             "status":task.status,
             "deadline":task.deadline.isoformat()} for task in tasks ],200

@task_bp.route('/tasks/<int:task_id>',methods=["GET"])
@jwt_required()
def get_task(task_id):
    user_id = int(get_jwt_identity())
    task = db.session.get(Task,task_id)

    if not task:
        return {"message":"task not found"}, 404
    
    assignment = TaskAssignment.query.filter_by(task_id = task_id,user_id = user_id).first()
    if not assignment:
        return {"message": "forbidden"}, 403
    
    return{"title":task.title,
           "description":task.description,
           "status":task.status,
           "created_at":task.created_at.isoformat(),
           "deadline":task.deadline.isoformat()},200
            

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

@task_bp.route("/tasks/<int:task_id>",methods=["PUT"])
@jwt_required()
def put_tasks(task_id):
    user_id = int(get_jwt_identity())
    task = db.session.get(Task,task_id)
    if not task:
        return {"message":"task not found"}, 404
    
    is_creator = (task.created_by == user_id)
    assign_user = TaskAssignment.query.filter_by(task_id = task_id,user_id = user_id).first()
    is_assigned = assign_user is not None
    if not (is_assigned or is_creator):
        return {"message": "forbidden"}, 403
    
    data = request.get_json()
    if not data :
        return {"message":"invalid input"},400
    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "status" in data:
        task.status = data["status"]
    if "deadline" in data:
        task.deadline = datetime.strptime(data["deadline"],"%Y-%m-%d").date()
    db.session.commit()
    return {"task_id":task.task_id,
        "title": task.title,
        "description":task.description,
        "status":task.status,
        "deadline":task.deadline.isoformat(),
        "updated_by":user_id,
        "created_by":task.created_by},200

@task_bp.route("/tasks/<int:task_id>",methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    task = db.session.get(Task,task_id)
    if not task:
        return {"message":"task not found"},404
    
    if task.created_by != user_id:
        return {"message":"forbidden"},403
    
    assignments = TaskAssignment.query.filter_by(task_id = task_id).all()
    for assignment in assignments:
        db.session.delete(assignment)
    
    db.session.delete(task)
    db.session.commit()
    return {"message":"task deleted successfully",
            "task_id": task_id},200

@task_bp.route("/tasks/<int:task_id>/assign",methods = ["POST"])
@jwt_required()
def assign_task(task_id):
    user_id = int(get_jwt_identity())
    task = db.session.get(Task,task_id)
    if not task:
        return {"message":"task not found"},404
    
    if task.created_by != user_id:
        return {"message":"forbidden"},403
    
    data = request.get_json()
    if not data :
        return {"message":"invalid input"},400
    
    to_assign = data.get("user_id")
    if not (User.query.filter_by(user_id = to_assign).first()):
        return {"message":"user does not exist"},404
    if  (TaskAssignment.query.filter_by(user_id = to_assign,task_id = task_id).first()):
        return {"message":"user already assigned"},409
    
    task_assigned = TaskAssignment(user_id = to_assign,task_id = task_id)
    db.session.add(task_assigned)
    db.session.commit()
    
    return {"message":"task assigned successful",
            "assigned_by":user_id,
            "assigned_to":task_assigned.user_id,
            "task":task_assigned.task_id},201
