from app.extensions import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = "tasks"
    
    task_id = db.Column(db.Integer,primary_key = True)
    created_by = db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable=False)
    title = db.Column(db.String(100),nullable = False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20),nullable = False,default = "created")
    project_head_id = db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable=True)
    created_at = db.Column(db.DateTime,default = datetime.utcnow)
    deadline = db.Column(db.Date,nullable = False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime)
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    
    STATUS_CREATED = "created"
    STATUS_ASSIGNED = "assigned"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_UNDER_REVIEW = "under_review"
    STATUS_COMPLETED = "completed"
    STATUS_CLOSED = "closed"