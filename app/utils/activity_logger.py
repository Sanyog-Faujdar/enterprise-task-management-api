from app.extensions import db
from app.models.activity_log_model import ActivityLog

def create_log(task_id,user_id,action,details=None):
    log = ActivityLog(task_id = task_id,user_id = user_id,
                      action = action,details=details)
    db.session.add(log)