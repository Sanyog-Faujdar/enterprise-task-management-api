from app.extensions import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = "tasks"
    
    created_by = db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable=False)
    task_id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20),nullable = False)
    created_at = db.Column(db.DateTime,default = datetime.utcnow)
    deadline = db.Column(db.Date,nullable = False)