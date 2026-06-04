from extensions import db

class GeologicalSample(db.Model):

    __tablename__ = "geological_samples"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    mineral = db.Column(
        db.String(100),
        nullable=False
    )

    location = db.Column(
        db.String(100),
        nullable=False
    )

    depth_meters = db.Column(
        db.Float,
        nullable=False
    )

    latitude = db.Column(
        db.Float,
        nullable=True
    )

    longitude = db.Column(
        db.Float,
        nullable=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    reports = db.relationship(
    "ExplorationReport",
    backref="sample",
    lazy=True,
    cascade="all, delete, delete-orphan"
    )

    def to_dict(self):

        return {
            "id": self.id,
            "mineral": self.mineral,
            "location": self.location,
            "depth_meters": self.depth_meters,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "user_id": self.user_id
        }