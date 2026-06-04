from extensions import db
from datetime import datetime

class ExplorationReport(db.Model):

    __tablename__ = "exploration_reports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    sample_id = db.Column(
        db.Integer,
        db.ForeignKey("geological_samples.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "filename": self.filename,
            "sample_id": self.sample_id,
            "user_id": self.user_id,
            "uploaded_at": self.uploaded_at.isoformat()
        }