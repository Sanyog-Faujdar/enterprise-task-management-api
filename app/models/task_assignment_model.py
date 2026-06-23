from app.extensions import db
from datetime import datetime

class TaskAssignment(db.Model):
    __tablename__ = "task_assignments"
    
    assign_id = db.Column(db.Integer,nullable = False,primary_key = True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'),nullable = False)
    member_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable = False)
    assigned_at = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    db.UniqueConstraint('task_id','user_id',name='unique_task_user')