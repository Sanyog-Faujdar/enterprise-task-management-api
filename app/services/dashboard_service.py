from app.extensions import db 
from app.models.task_models import Task
from app.models.user_models import User
from app.models.task_assignment_model import TaskAssignment
from app.models.activity_log_model import ActivityLog
from datetime import datetime , date


def get_admin_dashboard():
    #  user data 
    total_user = User.query.count()
    admins = User.query.filter_by(role = User.ROLE_ADMIN).count()
    project_head = User.query.filter_by(role = User.ROLE_PROJECT_HEAD).count()
    member = User.query.filter_by(role = User.ROLE_MEMBER).count()
    # task data 
    active_tasks= Task.query.filter_by(is_deleted = False).count()
    total_tasks = Task.query.count() 
    task_deleted = Task.query.filter_by(is_deleted = True).count()
    task_completed = Task.query.filter_by(is_deleted = False,status = Task.STATUS_COMPLETED).count()
    task_closed = Task.query.filter_by(is_deleted = False,status = Task.STATUS_CLOSED).count()
    task_under_review = Task.query.filter_by(is_deleted = False,status = Task.STATUS_UNDER_REVIEW).count()
    task_in_progress = Task.query.filter_by(is_deleted = False,status = Task.STATUS_IN_PROGRESS).count()
    task_assigned = Task.query.filter_by(is_deleted = False,status = Task.STATUS_ASSIGNED).count()
    task_created = Task.query.filter_by(is_deleted = False,status = Task.STATUS_CREATED).count()
    task_overdue = Task.query.filter(Task.is_deleted == False,Task.deadline < date.today(),Task.status.notin_([Task.STATUS_COMPLETED,Task.STATUS_CLOSED])).count()
    #activity log 
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    logs_today = ActivityLog.query.filter(ActivityLog.created_at >= today_start,ActivityLog.created_at <= today_end).count()
    
    return {"users":
    {
    "total": total_user,
    "admins": admins,
    "project_heads": project_head,
    "members": member
    },
    "tasks":
    {
    "total": total_tasks,
    "active": active_tasks,
    "deleted": task_deleted,
    "created": task_created,
    "assigned": task_assigned,
    "in_progress": task_in_progress,
    "under_review": task_under_review,
    "completed": task_completed,
    "closed": task_closed,
    "overdue": task_overdue
    },
    "activity": {
    "logs_today": logs_today
    } }, 200



def get_head_dashboard(current_user):
    #users 
    members = db.session.query(TaskAssignment.member_id).join(Task).filter(Task.project_head_id == current_user.user_id).distinct().count() 
    #tasks 
    tasks = Task.query.filter_by(is_deleted = False , project_head_id = current_user.user_id)
    total_tasks = tasks.count()
    task_completed = tasks.filter(Task.status == Task.STATUS_COMPLETED).count()
    task_in_progress = tasks.filter(Task.status == Task.STATUS_IN_PROGRESS).count()
    task_under_review = tasks.filter(Task.status == Task.STATUS_UNDER_REVIEW).count()
    task_overdue = tasks.filter(Task.deadline < date.today(),Task.status.notin_([Task.STATUS_COMPLETED,Task.STATUS_CLOSED])).count()
    task_assigned = tasks.filter(Task.status == Task.STATUS_ASSIGNED).count()
    #activity log 
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    logs_today = ActivityLog.query.join(Task).filter(Task.project_head_id == current_user.user_id , ActivityLog.created_at >= today_start,ActivityLog.created_at <= today_end).count()
    
    return {
        "users":{
            "members":members
            },
        "tasks":{
            "total_tasks":total_tasks,
            "completed": task_completed,
            "in_progress":task_in_progress,
            "under_review":task_under_review,
            "overdue":task_overdue,
            "assigned":task_assigned},
        "activity":{
            "logs_today":logs_today
        }},200



def get_member_dashboard(current_user):
    tasks = Task.query.join(TaskAssignment).filter(TaskAssignment.member_id == current_user.user_id,Task.is_deleted == False)
    total = tasks.count()
    completed = tasks.filter(Task.status == Task.STATUS_COMPLETED).count()
    in_progress = tasks.filter(Task.status == Task.STATUS_IN_PROGRESS).count()
    overdue = tasks.filter(Task.deadline < date.today() , Task.status.notin_([ Task.STATUS_COMPLETED,Task.STATUS_CLOSED])).count()
    #activity log 
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    logs_today = ActivityLog.query.join(TaskAssignment).filter(TaskAssignment.member_id == current_user.user_id,ActivityLog.created_at >= today_start,ActivityLog.created_at <= today_end).count()
    return {
        "tasks":{
            "total":total,
            "completed":completed,
            "in_progress":in_progress,
            "overdue":overdue
        },
        "activity":{
            "logs_today":logs_today
        }
    },200