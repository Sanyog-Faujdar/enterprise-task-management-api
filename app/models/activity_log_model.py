from app.extensions import db
from datetime import datetime

class ActivityLog(db.Model):
    __tablename__ = "activity_logs"
    
    log_id = db.Column(db.Integer,primary_key = True)
    task_id = db.Column(db.Integer,db.ForeignKey("tasks.task_id"),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable = False)
    action = db.Column(db.String(100),nullable = False)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    
    task = db.relationship("Task")
    user = db.relationship("User")
    
    ACTION_CREATED = "TASK_CREATED"
    ACTION_HEAD_ASSIGN = "HEAD_ASSIGNED"
    ACTION_MEMBER_ASSIGN = "MEMBER_ASSIGNED"
    ACTION_STATUS = "STATUS_UPDATED"
    ACTION_DELET = "TASK_DELETED"
    ACTION_TASK_RESTORED = "TASK_RESTORED" 