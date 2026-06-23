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
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    if current_user.role == User.ROLE_ADMIN:
        tasks = Task.query.all()
    elif current_user.role == User.ROLE_PROJECT_HEAD:
        tasks = Task.query.filter_by(project_head_id = current_user_id).all()
    else:
        tasks = db.session.query(Task).join(TaskAssignment,Task.task_id == TaskAssignment.task_id).filter(TaskAssignment.member_id == current_user_id).all()
    
    return [{"task_id":task.task_id,
             "created_by":task.created_by,
             "title":task.title,
             "status":task.status,
             "deadline":task.deadline.isoformat(),
             "project_head_id":task.project_head_id} for task in tasks ],200

@task_bp.route('/tasks/<int:task_id>',methods=["GET"])
@jwt_required()
def get_task(task_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    task = db.session.get(Task,task_id) 
    if not task:
        return {"message":"task not found"}, 404
    
    if (current_user.role == User.ROLE_ADMIN ):
        pass
    elif (current_user.role == User.ROLE_PROJECT_HEAD):
        if task.project_head_id != current_user_id:
            return {"message":"forbidden"},403
    else:
        assignment = TaskAssignment.query.filter_by(task_id = task_id,member_id = current_user_id).first()
        if not assignment:
            return {"message": "forbidden"}, 403
    
    return {"task_id": task.task_id,
    "title": task.title,
    "description": task.description,
    "status": task.status,
    "created_by": task.created_by,
    "project_head_id": task.project_head_id,
    "created_at": task.created_at.isoformat(),
    "deadline": task.deadline.isoformat()},200
            

@task_bp.route('/tasks',methods = ["POST"])
@jwt_required()
def create_task():
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    if current_user.role != User.ROLE_ADMIN:
        return {"message":"forbidden"},403
    
    data = request.get_json()
    if not data:
        return {"message":"invalid input"},400
    
    title = data.get('title')
    description = data.get('description')
    deadline = data.get("deadline")
    status = Task.STATUS_CREATED
    created_by = current_user.user_id
    if not title or not deadline :
        return {"message":"invalid input"},400
    
    deadline = datetime.strptime(deadline,"%Y-%m-%d").date()
    
    task = Task(title = title,
                description = description,
                deadline = deadline,
                status = status,
                created_by = created_by)
    db.session.add(task)
    db.session.commit()
    
    return{
        "message":"task added successfully",
        "task_id":task.task_id,
        "title": task.title,
        "description":task.description,
        "created_at":task.created_at.isoformat(),
        "deadline":task.deadline.isoformat(),
        "status":task.status,
        "project_head_id": task.project_head_id},201

@task_bp.route("/tasks/<int:task_id>",methods=["PUT"])
@jwt_required()
def put_tasks(task_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    VALID_STATUSES = {Task.STATUS_CREATED,Task.STATUS_ASSIGNED,Task.STATUS_IN_PROGRESS,Task.STATUS_UNDER_REVIEW,Task.STATUS_COMPLETED,Task.STATUS_CLOSED}
    task = db.session.get(Task,task_id)
    if not task:
        return {"message":"task not found"}, 404
    data = request.get_json()
    if not data :
        return {"message":"invalid input"},400
    
    if current_user.role == User.ROLE_ADMIN:
        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "deadline" in data:
            task.deadline = datetime.strptime(data["deadline"],"%Y-%m-%d").date()
    elif current_user.role == User.ROLE_PROJECT_HEAD:
        is_head = task.project_head_id ==current_user_id
        if not is_head:
            return {"message":"forbidden"},403
        if "status" in data:
            if data["status"] not in VALID_STATUSES:
                return{"message":"not valid status"},400
            task.status = data["status"]
        if "description" in data:
            task.description = data["description"]
        if "deadline" in data:
            task.deadline = datetime.strptime(data["deadline"],"%Y-%m-%d").date()
    else:
        is_assigned = TaskAssignment.query.filter_by(member_id = current_user_id,task_id=task_id).first()
        if not is_assigned:
            return {"message":"forbidden"},403
        if "status" in data:
            if data["status"] not in VALID_STATUSES:
                return{"message":"not valid status"},400
            task.status = data["status"]
    db.session.commit()
    return {"task_id":task.task_id,
        "title": task.title,
        "description":task.description,
        "status":task.status,
        "deadline":task.deadline.isoformat(),
        "updated_by":current_user.user_id,
        "created_by":task.created_by},200

@task_bp.route("/tasks/<int:task_id>",methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    task = db.session.get(Task,task_id)
    if not task:
        return {"message":"task not found"},404
    current_user = db.session.get(User,user_id)
    if current_user.role != User.ROLE_ADMIN:
        return {"message":"forbidden"},403
    
    assignments = TaskAssignment.query.filter_by(task_id = task_id).all()
    for assignment in assignments:
        db.session.delete(assignment)
    
    db.session.delete(task)
    db.session.commit()
    return {"message":"task deleted successfully",
            "task_id": task_id},200

@task_bp.route("/tasks/<int:task_id>/assign-member",methods = ["POST"])
@jwt_required()
def assign_task_to_member(task_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    task = db.session.get(Task,task_id)
    if not task:
        return {"message":"task not found"},404
    
    if task.project_head_id is None:
        return {"message":"assign project head first"},400
    
    data = request.get_json()
    if not data :
        return {"message":"invalid input"},400 
    
    to_assign = data.get("user_id")
    target_user = db.session.get(User, to_assign)
    if not target_user:
        return {"message":"user does not exist"},404
    
    if target_user.role != User.ROLE_MEMBER:
        return {"message":"only members can be assigned"},400
    
    
    if  current_user.role == User.ROLE_ADMIN :
        pass
    elif current_user.role == User.ROLE_PROJECT_HEAD:
        allowed = current_user_id == task.project_head_id
        if not allowed:
            return{"message":"forbidden"},403
    else:
        return {"message":"forbidden"},403
    if  (TaskAssignment.query.filter_by(member_id = to_assign,task_id = task_id).first()):
        return {"message":"user already assigned"},409
    task_assigned = TaskAssignment(member_id = to_assign,task_id = task_id)
    db.session.add(task_assigned)
    db.session.commit() 
    
    return {"message":"task assigned successful",
            "assigned_by":current_user_id,
            "assigned_to":task_assigned.member_id,
            "task":task_assigned.task_id},201

@task_bp.route("/tasks/<int:task_id>/assign-head",methods = ["POST"])
@jwt_required()
def assign_project_head(task_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    if current_user.role != User.ROLE_ADMIN :
        return {"message":"forbidden"},403
    
    task = db.session.get(Task,task_id)
    if not task:
        return{"message":"task not found"},404
    
    data = request.get_json()
    if not data:
        return {"message":"inavlid inpiut"},400
    
    head_id = data.get("project_head_id")
    head = db.session.get(User,head_id)
    if not head:
        return {"message":"user not found"},404
    
    if head.role != User.ROLE_PROJECT_HEAD:
        return {"message":"user is not a project head"},400
    
    if task.project_head_id == head_id:
        return {"message":"already assigned as project head"},409
    
    task.project_head_id = head_id
    
    task.status = Task.STATUS_ASSIGNED
    db.session.commit() 
    return {"message":"project head assigned successfully",
            "assigned_by":current_user_id,
            "assigned_to":task.project_head_id,
            "task":task_id},201 