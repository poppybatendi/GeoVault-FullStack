# utils/activity_logger.py

from extensions import db
from models.activity_log import ActivityLog

def log_activity(
    user_id,
    action,
    details=None
):

    activity = ActivityLog(
        user_id=user_id,
        action=action,
        details=details
    )

    db.session.add(activity)