from flask import Blueprint,request
from flask_jwt_extended import get_jwt_identity,jwt_required
from app.extensions import db
from app.models.task_models import Task
from app.models.user_models import User
from app.models.task_assignment_model import TaskAssignment
from app.models.activity_log_model import ActivityLog
from datetime import datetime , date
from app.utils.activity_logger import create_log
from app.services.dashboard_service import get_head_dashboard , get_member_dashboard , get_admin_dashboard
from app.docs.task_docs import create_task_docs,assign_head_docs,assign_member_docs,get_tasks_docs,get_task_docs,task_modification_docs,delete_task_docs,restore_task_docs
from app.docs.logs_docs import get_logs_docs
from app.docs.dashboard_docs import get_dashboard_docs
from flasgger import swag_from

task_bp = Blueprint('task',__name__)
VALID_STATUSES = {Task.STATUS_CREATED,Task.STATUS_ASSIGNED,Task.STATUS_IN_PROGRESS,Task.STATUS_UNDER_REVIEW,Task.STATUS_COMPLETED,Task.STATUS_CLOSED}

@task_bp.route('/tasks',methods=["GET"])
@jwt_required()
@swag_from(get_tasks_docs)
def get_tasks():
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    if current_user.role == User.ROLE_ADMIN:
        tasks = Task.query.filter_by(is_deleted=False).all()
    elif current_user.role == User.ROLE_PROJECT_HEAD:
        tasks = Task.query.filter_by(project_head_id = current_user_id,is_deleted=False).all()
    else:
        tasks = db.session.query(Task).join(TaskAssignment,Task.task_id == TaskAssignment.task_id).filter(TaskAssignment.member_id == current_user_id,Task.is_deleted==False).all()
    
    return [{"task_id":task.task_id,
             "created_by":task.created_by,
             "title":task.title,
             "status":task.status,
             "deadline":task.deadline.isoformat(),
             "project_head_id":task.project_head_id} for task in tasks ],200

@task_bp.route('/tasks/<int:task_id>',methods=["GET"])
@jwt_required()
@swag_from(get_task_docs)
def get_task(task_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    task = db.session.get(Task,task_id) 
    if not task or task.is_deleted:
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
@swag_from(create_task_docs)
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
    db.session.flush()
    create_log(task.task_id,current_user_id,ActivityLog.ACTION_CREATED,f"task '{task.title}' created successfully")
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
@swag_from(task_modification_docs)
def put_tasks(task_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    task = db.session.get(Task,task_id)
    if not task or task.is_deleted :
        return {"message":"task not found"}, 404
    data = request.get_json()
    if not data :
        return {"message":"invalid input"},400
    
    if current_user.role == User.ROLE_ADMIN :
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
            if data["status"] not in Task.VALID_STATUSES:
                return{"message":"not valid status"},400
            if task.status != data["status"]:
                old_status = task.status
                task.status = data["status"]
                create_log(task.task_id,current_user_id,ActivityLog.ACTION_STATUS_UPDATED,f"Status changed from {old_status} to {task.status}")
        if "description" in data:
            task.description = data["description"]
        if "deadline" in data:
            task.deadline = datetime.strptime(data["deadline"],"%Y-%m-%d").date()
    else:
        is_assigned = TaskAssignment.query.filter_by(member_id = current_user_id,task_id=task_id).first()
        if not is_assigned:
            return {"message":"forbidden"},403
        if "status" in data:
            if data["status"] not in Task.VALID_STATUSES:
                return{"message":"not valid status"},400
            if task.status != data["status"]:
                old_status = task.status
                task.status = data["status"]
                create_log(task.task_id,current_user_id,ActivityLog.ACTION_STATUS_UPDATED,f"Status changed from {old_status} to {task.status}")
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
@swag_from(delete_task_docs)
def delete_task(task_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    if current_user.role != User.ROLE_ADMIN:
        return {"message":"forbidden"},403
    
    task = db.session.get(Task,task_id)
    if not task:
        return {"message":"task not found"},404
    
    #already deleted 
    if task.is_deleted:
        return{"message":"task alreday deleted"},409
    
    #soft delete
    task.is_deleted = True
    task.deleted_by = current_user_id
    task.deleted_at = datetime.utcnow()
    create_log(task.task_id,current_user_id,ActivityLog.ACTION_DELET,f"task move to recycle bin")
    db.session.commit()
    return {"message":"task moved to recycle bin",
            "task_id": task_id},200

@task_bp.route("/tasks/<int:task_id>/assign-member",methods = ["POST"])
@jwt_required()
@swag_from(assign_member_docs)
def assign_task_to_member(task_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    task = db.session.get(Task,task_id)
    if not task or task.is_deleted:
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
    db.session.flush()
    create_log(task.task_id,current_user_id,ActivityLog.ACTION_MEMBER_ASSIGN,f"Assigned {target_user.name} as member")
    db.session.commit() 
    
    return {"message":"task assigned successful",
            "assigned_by":current_user_id,
            "assigned_to":task_assigned.member_id,
            "task":task_assigned.task_id},201

@task_bp.route("/tasks/<int:task_id>/assign-head",methods = ["POST"])
@jwt_required()
@swag_from(assign_head_docs)
def assign_project_head(task_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    if current_user.role != User.ROLE_ADMIN :
        return {"message":"forbidden"},403
    
    task = db.session.get(Task,task_id)
    if not task or task.is_deleted:
        return{"message":"task not found"},404
    
    data = request.get_json()
    if not data:
        return {"message":"inavlid inpiut"},400
    
    head_id = data.get("project_head_id")
    if not head_id:
        return {"message": "project_head_id is required"}, 400
    head = db.session.get(User,head_id)
    if not head:
        return {"message":"user not found"},404
    
    if head.role == User.ROLE_MEMBER:
        head.role = User.ROLE_PROJECT_HEAD
    
    if head.role != User.ROLE_PROJECT_HEAD:
        return {"message":"user is not a project head"},400
    
    if task.project_head_id == head_id:
        return {"message":"already assigned as project head"},409
    
    task.project_head_id = head_id
    task.status = Task.STATUS_ASSIGNED
    create_log(task.task_id,current_user_id,ActivityLog.ACTION_HEAD_ASSIGN,f"assigned {head.name} as project head")
    db.session.commit() 
    return {"message":"project head assigned successfully",
            "assigned_by":current_user_id,
            "assigned_to":task.project_head_id,
            "task":task_id},201 

@task_bp.route("/logs",methods = ["GET"])
@jwt_required()
@swag_from(get_logs_docs)
def get_logs():
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    if current_user.role == User.ROLE_ADMIN:
        logs = ActivityLog.query
    elif current_user.role == User.ROLE_PROJECT_HEAD:
        logs = ActivityLog.query.join(Task,ActivityLog.task_id == Task.task_id).filter(Task.project_head_id == current_user_id)
    else :
        logs = ActivityLog.query.join(TaskAssignment,ActivityLog.task_id == TaskAssignment.task_id).filter(TaskAssignment.member_id == current_user_id)
    
    # task based log
    task_id = request.args.get("task_id")
    if task_id :
        logs = logs.filter(ActivityLog.task_id == int(task_id))
    
    # action based log 
    action = request.args.get("action")
    if action:
        logs = logs.filter(ActivityLog.action == action)
    
    #user based log
    user_id = request.args.get("user_id")
    if user_id:
        logs = logs.filter(ActivityLog.user_id == int(user_id))
    
    # date based log 
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    if from_date and to_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        logs = logs.filter(ActivityLog.created_at >= from_date,ActivityLog.created_at <= to_date)
    elif from_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d") 
        logs = logs.filter(ActivityLog.created_at >= from_date)
    elif to_date:
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        logs = logs.filter(ActivityLog.created_at <= to_date)
    
    #pagination
    page = request.args.get("page",1,type=int)
    per_page = min(request.args.get("per_page",20,type=int),100)
    logs = logs.order_by(ActivityLog.created_at.desc()).paginate(page=page,per_page=per_page,error_out=False)
    
    return {"page":logs.page,
        "per_page":logs.per_page,
        "total":logs.total,
        "pages":logs.pages,
        "has_next":logs.has_next,
        "has_prev":logs.has_prev,
        "logs":[
            {"log_id":log.log_id,
            "task_id":log.task_id,
            "user_id": log.user_id,
            "action": log.action,
            "details": log.details,
            "created_at": log.created_at.isoformat()
            }for log in logs.items]
        },200

@task_bp.route("/tasks/<int:task_id>/restore",methods = ["PATCH"])
@jwt_required()
@swag_from(restore_task_docs)
def task_restore(task_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    if current_user.role != User.ROLE_ADMIN:
        return {"message":"forbidden"},403
    
    task = db.session.get(Task,task_id)
    if not task :
        return{"message":"task not found"},404
    
    if task.is_deleted == False:
        return {"message":"task is already active"},409
    
    task.is_deleted = False
    task.deleted_at = None
    task.deleted_by = None
    
    create_log(task.task_id,current_user_id,ActivityLog.ACTION_TASK_RESTORED,f"{task.title} restored from recycle bin")
    db.session.commit()
    
    return {"message":"task restored from recycle bin",
            "task_id":task.task_id},200

@task_bp.route("/dashboard",methods=["GET"])
@jwt_required()
@swag_from(get_dashboard_docs)
def see_dashborad():
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    if current_user.role == User.ROLE_ADMIN:
        return get_admin_dashboard()
    
    elif current_user.role == User.ROLE_PROJECT_HEAD:
        return get_head_dashboard(current_user)
    
    else :
        return get_member_dashboard(current_user)