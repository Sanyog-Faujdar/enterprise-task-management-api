from app.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique = True)
    password = db.Column(db.String(500),nullable = False) 
    created_at = db.Column(db.DateTime,default = datetime.utcnow)
    role = db.Column(db.String(50),nullable=False,default="member")
    
    ROLE_OWNER = "owner"
    ROLE_PROJECT_HEAD = "project_head"
    ROLE_MEMBER = "member"