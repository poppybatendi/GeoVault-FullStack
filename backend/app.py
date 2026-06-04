from flask import Flask
from config import Config
from extensions import db

from models.sample import GeologicalSample
from models.user import User
from models.activity_log import ActivityLog
from models.exploration_report import ExplorationReport

from routes.samples import samples_bp
from routes.auth import auth_bp

from flask_jwt_extended import JWTManager

import os

from flask_cors import CORS

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173"
            ]
        }
    }
)
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config.from_object(Config)

db.init_app(app)

jwt = JWTManager(app)

app.register_blueprint(samples_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return {
        "message": "GeoVault API Running"
    }

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)