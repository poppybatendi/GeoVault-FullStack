import csv
from io import TextIOWrapper
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

import os
from sqlalchemy import func
from utils.activity_logger import log_activity
from models.activity_log import ActivityLog
from werkzeug.utils import secure_filename
from flask import send_from_directory

from flask import (
    Blueprint,
    jsonify,
    request,
    current_app
)
from flask import send_from_directory

from extensions import db
from models.sample import GeologicalSample
from models.exploration_report import ExplorationReport

from math import radians
from math import sin
from math import cos
from math import sqrt
from math import atan2

def haversine(
    lat1,
    lon1,
    lat2,
    lon2
):

    R = 6371

    dlat = radians(
        lat2 - lat1
    )

    dlon = radians(
        lon2 - lon1
    )

    a = (
        sin(dlat / 2) ** 2
        +
        cos(radians(lat1))
        *
        cos(radians(lat2))
        *
        sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c

samples_bp = Blueprint("samples", __name__)


# ==================================
# UPLOAD GEOLOGICAL REPORT
# ==================================
@samples_bp.route("/samples/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({
            "error": "No file uploaded"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No selected file"
        }), 400

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    return jsonify({
        "message": "File uploaded successfully",
        "filename": filename
    })

# ==================================
# UPLOAD REPORT TO SAMPLE
# ==================================
@samples_bp.route("/reports/upload", methods=["POST"])
@jwt_required()
def upload_report():

    current_user_id = int(
        get_jwt_identity()
    )

    title = request.form.get("title")
    sample_id = request.form.get("sample_id")

    if not title:
        return jsonify({
            "error": "Title is required"
        }), 400

    if not sample_id:
        return jsonify({
            "error": "Sample ID is required"
        }), 400

    sample = GeologicalSample.query.get(
        sample_id
    )

    if not sample:
        return jsonify({
            "error": "Sample not found"
        }), 404

    if sample.user_id != current_user_id:
        return jsonify({
            "error": "Unauthorized"
        }), 403

    if "file" not in request.files:
        return jsonify({
            "error": "File is required"
        }), 400

    file = request.files["file"]

    filename = secure_filename(
        file.filename
    )

    filepath = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    print("UPLOAD REPORT ROUTE HIT")
    print("TITLE =", title)
    print("SAMPLE_ID =", sample_id)
    print("FILENAME =", filename)

    report = ExplorationReport(
        title=title,
        filename=filename,
        sample_id=sample.id,
        user_id=current_user_id
    )

    db.session.add(report)

    log_activity(
        user_id=current_user_id,    
        action="UPLOAD_REPORT",
        details=f"Uploaded report {filename}"
    )

    db.session.commit()
    print("REPORT SAVED TO DATABASE")

    return jsonify({
        "message": "Report uploaded successfully",
        "report": report.to_dict()
    }), 201

    print("DOWNLOAD ROUTE LOADED")
## Download Endpoint
    @samples_bp.route(
        "/reports/download/<int:report_id>",
        methods=["GET"]
    )
    @jwt_required()
    def download_report(report_id):

        current_user_id = int(
            get_jwt_identity()
        )

        report = ExplorationReport.query.get_or_404(
                report_id
            )

        if report.user_id != current_user_id:

            return jsonify({
                "error": "Unauthorized"
            }), 403

        return send_from_directory(
            current_app.config["UPLOAD_FOLDER"],
            report.filename,
            as_attachment=True
        )

# ==================================
# GET ALL SAMPLES
# ==================================
@samples_bp.route("/samples", methods=["GET"])
def get_samples():

    samples = GeologicalSample.query.all()

    return jsonify([
        sample.to_dict()
        for sample in samples
    ])


# ==================================
# SEARCH SAMPLES
# ==================================
@samples_bp.route("/samples/search", methods=["GET"])
def search_samples():

    mineral = request.args.get("mineral")
    location = request.args.get("location")

    query = GeologicalSample.query

    if mineral:
        query = query.filter(
            GeologicalSample.mineral.ilike(
                f"%{mineral}%"
            )
        )

    if location:
        query = query.filter(
            GeologicalSample.location.ilike(
                f"%{location}%"
            )
        )

    samples = query.all()

    return jsonify([
        sample.to_dict()
        for sample in samples
    ])


# ==================================
# GET ONE SAMPLE
# ==================================
@samples_bp.route("/samples/<int:sample_id>", methods=["GET"])
def get_sample(sample_id):

    sample = GeologicalSample.query.get(sample_id)

    if not sample:
        return jsonify({
            "error": "Sample not found"
        }), 404

    return jsonify(
        sample.to_dict()
    )


# ==================================
# CREATE SAMPLE
# ==================================
@samples_bp.route("/samples", methods=["POST"])
@jwt_required()
def create_sample():
    
    try:

        data = request.get_json()

        current_user_id = int(
            get_jwt_identity()
        )

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        mineral = data.get("mineral")
        location = data.get("location")
        depth_meters = data.get("depth_meters")

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not mineral:
            return jsonify({
                "error": "Mineral is required"
            }), 400

        if not location:
            return jsonify({
                "error": "Location is required"
            }), 400

        if depth_meters is None:
            return jsonify({
                "error": "Depth is required"
            }), 400

        try:
            depth_meters = float(depth_meters)
        except ValueError:
            return jsonify({
                "error": "Depth must be numeric"
            }), 400

        if latitude is not None:

            latitude = float(latitude)

            if latitude < -90 or latitude > 90:
                return jsonify({
                    "error": "Latitude must be between -90 and 90"
                }), 400

        if longitude is not None:

            longitude = float(longitude)

            if longitude < -180 or longitude > 180:
                return jsonify({
                    "error": "Longitude must be between -180 and 180"
                }), 400

        new_sample = GeologicalSample(
            mineral=mineral,
            location=location,
            depth_meters=depth_meters,
            latitude=latitude,
            longitude=longitude,
            user_id=current_user_id
        )

        db.session.add(new_sample)

        log_activity(
            user_id=current_user_id,
            action="CREATE_SAMPLE",
            details=f"Created sample {mineral}"
        )

        db.session.commit()

        return jsonify({
            "message": "Sample created successfully",
            "sample": new_sample.to_dict()
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500


# ==================================
# UPDATE SAMPLE
# ==================================
@samples_bp.route("/samples/<int:sample_id>", methods=["PUT"])
@jwt_required()
def update_sample(sample_id):

    sample = GeologicalSample.query.get(sample_id)

    if not sample:
        return jsonify({
            "error": "Sample not found"
        }), 404

    current_user_id = int(
        get_jwt_identity()
    )

    if sample.user_id != current_user_id:
        return jsonify({
            "error": "Unauthorized"
        }), 403

    data = request.get_json()

    sample.mineral = data.get(
        "mineral",
        sample.mineral
    )

    sample.location = data.get(
        "location",
        sample.location
    )

    sample.depth_meters = data.get(
        "depth_meters",
        sample.depth_meters
    )

    if "latitude" in data:
        sample.latitude = data["latitude"]

    if "longitude" in data:
        sample.longitude = data["longitude"]
        
        log_activity(
            user_id=current_user_id,
            action="UPDATE_SAMPLE",
            details=f"Updated sample ID {sample.id}"
        )
    db.session.commit()

    return jsonify({
        "message": "Sample updated successfully",
        "sample": sample.to_dict()
    })


# ==================================
# DELETE SAMPLE
# ==================================
@samples_bp.route("/samples/<int:sample_id>", methods=["DELETE"])
@jwt_required()
def delete_sample(sample_id):

    sample = GeologicalSample.query.get(sample_id)

    if not sample:
        return jsonify({
            "error": "Sample not found"
        }), 404

    current_user_id = int(
        get_jwt_identity()
    )

    if sample.user_id != current_user_id:
        return jsonify({
            "error": "Unauthorized"
        }), 403

    sample_id_deleted = sample.id
    db.session.delete(sample)

    log_activity(
        user_id=current_user_id,
        action="DELETE_SAMPLE",
        details=f"Deleted sample ID {sample_id_deleted}"
    )

    db.session.commit()

    return jsonify({
        "message": "Sample deleted successfully"
    })


# ==================================
# MY SAMPLES
# ==================================
@samples_bp.route("/my-samples", methods=["GET"])
@jwt_required()
def my_samples():

    current_user_id = int(
        get_jwt_identity()
    )

    samples = GeologicalSample.query.filter_by(
        user_id=current_user_id
    ).all()

    return jsonify([
        sample.to_dict()
        for sample in samples
    ])

# CSV IMPORT
@samples_bp.route("/samples/import", methods=["POST"])
@jwt_required()
def import_samples():

    if "file" not in request.files:
        return jsonify({
            "error": "CSV file is required"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    current_user_id = int(
        get_jwt_identity()
    )

    try:

        csv_file = TextIOWrapper(
            file,
            encoding="utf-8"
        )

        reader = csv.DictReader(csv_file)

        imported_count = 0
        failed_count = 0
        errors = []

        for row_number, row in enumerate(reader, start=2):

            try:

                mineral = row.get("mineral")
                location = row.get("location")
                depth_meters = row.get("depth_meters")
                latitude = row.get("latitude")
                longitude = row.get("longitude")

                # REQUIRED FIELD VALIDATION

                if not mineral:
                    raise ValueError(
                        "Mineral is required"
                    )

                if not location:
                    raise ValueError(
                        "Location is required"
                    )

                if not depth_meters:
                    raise ValueError(
                        "Depth is required"
                    )

                # NUMERIC VALIDATION

                depth_meters = float(
                    depth_meters
                )

                latitude = float(
                    latitude
                )

                longitude = float(
                    longitude
                )

                # GEOSPATIAL VALIDATION

                if latitude < -90 or latitude > 90:
                    raise ValueError(
                        "Latitude must be between -90 and 90"
                    )

                if longitude < -180 or longitude > 180:
                    raise ValueError(
                        "Longitude must be between -180 and 180"
                    )

                sample = GeologicalSample(
                    mineral=mineral,
                    location=location,
                    depth_meters=depth_meters,
                    latitude=latitude,
                    longitude=longitude,
                    user_id=current_user_id
                )

                db.session.add(sample)

                imported_count += 1

            except Exception as row_error:

                failed_count += 1

                errors.append({
                    "row": row_number,
                    "error": str(row_error)
                })

        log_activity(
            user_id=current_user_id,
            action="IMPORT_SAMPLES",
            details=f"Imported {imported_count} samples, failed {failed_count}"
        )

        db.session.commit()

        return jsonify({
            "message": "Import completed",
            "imported": imported_count,
            "failed": failed_count,
            "errors": errors
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500
    

#ACTIVITY
@samples_bp.route("/activity", methods=["GET"])
@jwt_required()
def get_activity():

    current_user_id = int(
        get_jwt_identity()
    )

    activities = ActivityLog.query.filter_by(
        user_id=current_user_id
    ).order_by(
        ActivityLog.created_at.desc()
    ).all()

    return jsonify([
        activity.to_dict()
        for activity in activities
    ])

#ACTIVITY HISTORY ROUTE
@samples_bp.route("/activity-logs", methods=["GET"])
@jwt_required()
def get_activity_logs():

    current_user_id = int(
        get_jwt_identity()
    )

    logs = ActivityLog.query.filter_by(
        user_id=current_user_id
    ).order_by(
        ActivityLog.created_at.desc()
    ).all()

    return jsonify([
        log.to_dict()
        for log in logs
    ])


# ==================================
# REPORTS FOR SAMPLE
# ==================================
@samples_bp.route(
    "/samples/<int:sample_id>/reports",
    methods=["GET"]
)
@jwt_required()
def get_sample_reports(sample_id):

    current_user_id = int(
        get_jwt_identity()
    )

    sample = GeologicalSample.query.get(
        sample_id
    )

    if not sample:
        return jsonify({
            "error": "Sample not found"
        }), 404

    if sample.user_id != current_user_id:
        return jsonify({
            "error": "Unauthorized"
        }), 403

    reports = ExplorationReport.query.filter_by(
        sample_id=sample_id
    ).all()

    return jsonify([
        report.to_dict()
        for report in reports
    ])

# ==================================
# DOWNLOAD REPORT
# ==================================
@samples_bp.route(
    "/reports/<int:report_id>/download",
    methods=["GET"]
)
@jwt_required()
def download_report(report_id):

    current_user_id = int(
        get_jwt_identity()
    )

    report = ExplorationReport.query.get(
        report_id
    )

    if not report:
        return jsonify({
            "error": "Report not found"
        }), 404

    if report.user_id != current_user_id:
        return jsonify({
            "error": "Unauthorized"
        }), 403

    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        report.filename,
        as_attachment=True
    )

# ==================================
# SAMPLE MAP DATA (GEOJSON)
# ==================================
@samples_bp.route("/map/samples", methods=["GET"])
@jwt_required()
def sample_map_data():

    current_user_id = int(
        get_jwt_identity()
    )

    samples = GeologicalSample.query.filter_by(
        user_id=current_user_id
    ).all()

    features = []

    for sample in samples:

        if (
            sample.latitude is None or
            sample.longitude is None
        ):
            continue

        report_count = ExplorationReport.query.filter_by(
            sample_id=sample.id
        ).count()

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    sample.longitude,
                    sample.latitude
                ]
            },
            "properties": {
                "id": sample.id,
                "mineral": sample.mineral,
                "location": sample.location,
                "depth_meters": sample.depth_meters,
                "report_count": report_count
            }
        })

    return jsonify({
        "type": "FeatureCollection",
        "features": features
    })

#SAMPLE MAP DETAILS
@samples_bp.route(
    "/map/samples/<int:sample_id>",
    methods=["GET"]
)
@jwt_required()
def sample_map_detail(sample_id):

    current_user_id = int(
        get_jwt_identity()
    )

    sample = GeologicalSample.query.filter_by(
        id=sample_id,
        user_id=current_user_id
    ).first()

    if not sample:
        return jsonify({
            "error": "Sample not found"
        }), 404

    reports = ExplorationReport.query.filter_by(
        sample_id=sample.id
    ).all()

    return jsonify({
        "sample": sample.to_dict(),
        "reports": [
            report.to_dict()
            for report in reports
        ]
    })

#SEARCH MAP AREA
@samples_bp.route("/map/search", methods=["GET"])
@jwt_required()
def search_map_area():

    current_user_id = int(
        get_jwt_identity()
    )

    min_lat = float(
        request.args.get("min_lat")
    )

    max_lat = float(
        request.args.get("max_lat")
    )

    min_lon = float(
        request.args.get("min_lon")
    )

    max_lon = float(
        request.args.get("max_lon")
    )

    samples = GeologicalSample.query.filter(
        GeologicalSample.user_id == current_user_id,
        GeologicalSample.latitude >= min_lat,
        GeologicalSample.latitude <= max_lat,
        GeologicalSample.longitude >= min_lon,
        GeologicalSample.longitude <= max_lon
    ).all()

    return jsonify([
        sample.to_dict()
        for sample in samples
    ])

# ==================================
# DASHBOARD SUMMARY
# ==================================
@samples_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():

    current_user_id = int(
        get_jwt_identity()
    )

    sample_count = GeologicalSample.query.filter_by(
        user_id=current_user_id
    ).count()

    report_count = ExplorationReport.query.filter_by(
        user_id=current_user_id
    ).count()

    activity_count = ActivityLog.query.filter_by(
        user_id=current_user_id
    ).count()

    return jsonify({
        "samples": sample_count,
        "reports": report_count,
        "activities": activity_count
    })

# ==================================
# MINERAL STATISTICS
# ==================================
@samples_bp.route("/dashboard/minerals", methods=["GET"])
@jwt_required()
def mineral_statistics():

    current_user_id = int(
        get_jwt_identity()
    )

    results = db.session.query(
        GeologicalSample.mineral,
        func.count(GeologicalSample.id)
    ).filter(
        GeologicalSample.user_id == current_user_id
    ).group_by(
        GeologicalSample.mineral
    ).all()

    return jsonify([
        {
            "mineral": mineral,
            "count": count
        }
        for mineral, count in results
    ])

@samples_bp.route(
    "/samples/nearby",
    methods=["GET"]
)
@jwt_required()
def nearby_samples():

    current_user_id = int(
        get_jwt_identity()
    )

    latitude = float(
        request.args.get("lat")
    )

    longitude = float(
        request.args.get("lon")
    )

    radius = float(
        request.args.get(
            "radius",
            50
        )
    )

    samples = GeologicalSample.query.filter_by(
        user_id=current_user_id
    ).all()

    results = []

    for sample in samples:

        if (
            sample.latitude is None
            or
            sample.longitude is None
        ):
            continue

        distance = haversine(
            latitude,
            longitude,
            sample.latitude,
            sample.longitude
        )

        if distance <= radius:

            results.append({
                **sample.to_dict(),
                "distance_km": round(
                    distance,
                    2
                )
            })

    return jsonify(results)

#AI SAMPLE SUMMARY
@samples_bp.route(
    "/ai/sample-summary/<int:sample_id>",
    methods=["POST"]
)
@jwt_required()
def sample_summary(sample_id):

    current_user_id = int(
        get_jwt_identity()
    )

    sample = GeologicalSample.query.filter_by(
        id=sample_id,
        user_id=current_user_id
    ).first()

    if not sample:
        return jsonify({
            "error": "Sample not found"
        }), 404

    report_count = ExplorationReport.query.filter_by(
        sample_id=sample.id
    ).count()

    # Risk Assessment

    if report_count == 0:
        risk_level = "High"

    elif report_count < 3:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    # Opportunity Score

    score = 50

    if sample.depth_meters > 100:
        score += 20

    if report_count >= 3:
        score += 20

    if sample.mineral.lower() == "copper":
        score += 10

    if score > 100:
        score = 100

    # Recommendation

    if score >= 80:
        recommendation = (
            "High exploration potential. "
            "Further drilling recommended."
        )

    elif score >= 60:
        recommendation = (
            "Moderate exploration potential."
        )

    else:
        recommendation = (
            "Low exploration potential."
        )

    summary = (
        f"{sample.mineral} sample collected "
        f"in {sample.location} "
        f"at depth {sample.depth_meters}m. "
        f"{report_count} exploration reports attached."
    )

    return jsonify({
        "sample_id": sample.id,
        "mineral": sample.mineral,
        "location": sample.location,
        "depth": sample.depth_meters,
        "report_count": report_count,
        "risk_level": risk_level,
        "opportunity_score": score,
        "recommendation": recommendation,
        "summary": summary
    })

## AI OVERVIEW
@samples_bp.route(
    "/ai/overview",
    methods=["GET"]
)
@jwt_required()
def ai_overview():

    current_user_id = int(
        get_jwt_identity()
    )

    samples = GeologicalSample.query.filter_by(
        user_id=current_user_id
    ).all()

    reports = ExplorationReport.query.filter_by(
        user_id=current_user_id
    ).all()

    total_samples = len(samples)
    total_reports = len(reports)

    average_depth = 0

    if total_samples > 0:

        average_depth = round(
            sum(
                sample.depth_meters
                for sample in samples
            ) / total_samples,
            2
        )

    mineral_counts = {}

    for sample in samples:

        mineral = sample.mineral

        mineral_counts[mineral] = (
            mineral_counts.get(mineral, 0) + 1
        )

    top_mineral = None

    if mineral_counts:
        top_mineral = max(
            mineral_counts,
            key=mineral_counts.get
        )

    return jsonify({
        "total_samples": total_samples,
        "total_reports": total_reports,
        "average_depth": average_depth,
        "top_mineral": top_mineral,
        "minerals": mineral_counts
    })

## AI INSIGHTS
@samples_bp.route(
    "/ai/insights",
    methods=["GET"]
)
@jwt_required()
def ai_insights():

    current_user_id = int(
        get_jwt_identity()
    )

    samples = GeologicalSample.query.filter_by(
        user_id=current_user_id
    ).all()

    reports = ExplorationReport.query.filter_by(
        user_id=current_user_id
    ).all()

    insights = []

    if not samples:

        return jsonify({
            "insights": [
                "No geological samples available."
            ]
        })

    # --------------------------
    # TOP MINERAL
    # --------------------------

    mineral_counts = {}

    for sample in samples:

        mineral = sample.mineral

        mineral_counts[mineral] = (
            mineral_counts.get(mineral, 0) + 1
        )

    top_mineral = max(
        mineral_counts,
        key=mineral_counts.get
    )

    insights.append(
        f"{top_mineral} is the dominant mineral "
        f"in your dataset."
    )

    # --------------------------
    # AVERAGE DEPTH
    # --------------------------

    avg_depth = round(
        sum(
            sample.depth_meters
            for sample in samples
        ) / len(samples),
        2
    )

    insights.append(
        f"Average drilling depth is "
        f"{avg_depth} meters."
    )

    # --------------------------
    # REPORT STATISTICS
    # --------------------------

    report_counts = {}

    for report in reports:

        if report.sample_id not in report_counts:
            report_counts[report.sample_id] = 0

        report_counts[report.sample_id] += 1

    samples_without_reports = len([
        sample
        for sample in samples
        if report_counts.get(sample.id, 0) == 0
    ])

    insights.append(
        f"{samples_without_reports} samples "
        f"have no supporting reports."
    )

    # --------------------------
    # RISK DISTRIBUTION
    # --------------------------

    high_risk = 0
    medium_risk = 0
    low_risk = 0

    for sample in samples:

        report_count = report_counts.get(
            sample.id,
            0
        )

        if report_count == 0:
            high_risk += 1

        elif report_count < 3:
            medium_risk += 1

        else:
            low_risk += 1

    insights.append(
        f"{high_risk} samples are classified "
        f"as high risk."
    )

    insights.append(
        f"{medium_risk} samples are classified "
        f"as medium risk."
    )

    insights.append(
        f"{low_risk} samples are classified "
        f"as low risk."
    )

    # --------------------------
    # GEOGRAPHIC EXTREMES
    # --------------------------

    geo_samples = [
        sample
        for sample in samples
        if sample.latitude is not None
        and sample.longitude is not None
    ]

    if geo_samples:

        northernmost = max(
            geo_samples,
            key=lambda s: s.latitude
        )

        southernmost = min(
            geo_samples,
            key=lambda s: s.latitude
        )

        insights.append(
            f"Northernmost sample is "
            f"{northernmost.mineral} "
            f"at latitude "
            f"{northernmost.latitude}."
        )

        insights.append(
            f"Southernmost sample is "
            f"{southernmost.mineral} "
            f"at latitude "
            f"{southernmost.latitude}."
        )

    # --------------------------
    # AVERAGE COORDINATES
    # --------------------------

        avg_lat = round(
            sum(
                sample.latitude
                for sample in geo_samples
            ) / len(geo_samples),
            4
        )

        avg_lon = round(
            sum(
                sample.longitude
                for sample in geo_samples
            ) / len(geo_samples),
            4
        )

        insights.append(
            f"Average exploration location "
            f"is centered near "
            f"({avg_lat}, {avg_lon})."
        )

    # ----------------------------
    # SAMPLES CLUTERED WITHIN 10KM
    # ----------------------------
   
        clustered_samples = set()

        for i in range(len(geo_samples)):

            for j in range(i + 1, len(geo_samples)):

                distance = haversine(
                    geo_samples[i].latitude,
                    geo_samples[i].longitude,
                    geo_samples[j].latitude,
                    geo_samples[j].longitude
                )

                if distance <= 10:

                    clustered_samples.add(
                        geo_samples[i].id
                    )

                    clustered_samples.add(
                        geo_samples[j].id
                    )

        insights.append(
            f"{len(clustered_samples)} samples "
            f"are located within "
            f"10 km of another sample."
        )

    # --------------------------
    # MINERAL HOTSPOTS WITH ADVANCED
    # --------------------------
        hotspot_counts = {}

        for sample in geo_samples:

            mineral = sample.mineral

            hotspot_counts[mineral] = (
                hotspot_counts.get(mineral, 0) + 1
            )

        hotspot_mineral = max(
            hotspot_counts,
            key=hotspot_counts.get
        )

        insights.append(
            f"{hotspot_mineral} represents "
            f"the strongest exploration hotspot "
            f"with {hotspot_counts[hotspot_mineral]} samples."
        )

        sorted_hotspots = sorted(
            hotspot_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        hotspot_summary = ", ".join(
            [
                f"{mineral} ({count})"
                for mineral, count
                in sorted_hotspots
            ]
        )

        insights.append(
            f"Mineral hotspot ranking: "
            f"{hotspot_summary}."
        )

    # --------------------------
    # DEEP SAMPLE ANALYSIS
    # --------------------------

    deep_samples = len([
        sample
        for sample in samples
        if sample.depth_meters > 100
    ])

    insights.append(
        f"{deep_samples} samples exceed "
        f"100 meters depth."
    )

    # --------------------------
    # REPORT COVERAGE
    # --------------------------

    insights.append(
        f"{len(reports)} exploration reports "
        f"are linked to your samples."
    )

    return jsonify({
        "insights": insights
    })

# ==================================
# AI RECOMMENDATIONS
# ==================================
@samples_bp.route(
    "/ai/recommendations",
    methods=["GET"]
)
@jwt_required()
def ai_recommendations():

    current_user_id = int(
        get_jwt_identity()
    )

    samples = GeologicalSample.query.filter_by(
        user_id=current_user_id
    ).all()

    reports = ExplorationReport.query.filter_by(
        user_id=current_user_id
    ).all()

    recommendations = []

    if not samples:

        return jsonify({
            "recommendations": [
                "No samples available for analysis."
            ]
        })

    # --------------------------
    # REPORT COVERAGE
    # --------------------------

    report_counts = {}

    for report in reports:

        report_counts[report.sample_id] = (
            report_counts.get(
                report.sample_id,
                0
            ) + 1
        )

    samples_without_reports = len([
        sample
        for sample in samples
        if report_counts.get(
            sample.id,
            0
        ) == 0
    ])

    if samples_without_reports:

        recommendations.append(
            f"Upload supporting reports for "
            f"{samples_without_reports} samples."
        )

    # --------------------------
    # DEEP SAMPLES
    # --------------------------

    deep_samples = len([
        sample
        for sample in samples
        if sample.depth_meters > 100
    ])

    if deep_samples:

        recommendations.append(
            f"Prioritize analysis of "
            f"{deep_samples} deep drilling samples."
        )

    # --------------------------
    # MINERAL HOTSPOT
    # --------------------------

    mineral_counts = {}

    for sample in samples:

        mineral_counts[sample.mineral] = (
            mineral_counts.get(
                sample.mineral,
                0
            ) + 1
        )

    top_mineral = max(
        mineral_counts,
        key=mineral_counts.get
    )

    recommendations.append(
        f"Focus exploration efforts on "
        f"{top_mineral} deposits, "
        f"which dominate the dataset."
    )

    # --------------------------
    # REPORT QUALITY
    # --------------------------

    well_documented = len([
        sample
        for sample in samples
        if report_counts.get(
            sample.id,
            0
        ) >= 3
    ])

    if well_documented:

        recommendations.append(
            f"{well_documented} samples have strong "
            f"documentation and should be prioritized "
            f"for advanced evaluation."
        )

    return jsonify({
        "recommendations": recommendations
    })

# ==================================
# AI HIGH PRIORITY TARGETS
# ==================================
@samples_bp.route(
    "/ai/high-priority-targets",
    methods=["GET"]
)
@jwt_required()
def high_priority_targets():

    current_user_id = int(
        get_jwt_identity()
    )

    samples = GeologicalSample.query.filter_by(
        user_id=current_user_id
    ).all()

    targets = []

    for sample in samples:

        report_count = ExplorationReport.query.filter_by(
            sample_id=sample.id
        ).count()

        score = 0

        if sample.depth_meters > 100:
            score += 40

        if report_count >= 3:
            score += 40

        if sample.mineral.lower() == "copper":
            score += 20

        targets.append({
            "sample_id": sample.id,
            "mineral": sample.mineral,
            "location": sample.location,
            "score": score
        })

    targets.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return jsonify(
        targets[:5]
    )

# ==================================
# AI EXPLORATION HOTSPOTS
# ==================================
@samples_bp.route(
    "/ai/exploration-hotspots",
    methods=["GET"]
)
@jwt_required()
def exploration_hotspots():

    current_user_id = int(
        get_jwt_identity()
    )

    samples = GeologicalSample.query.filter_by(
        user_id=current_user_id
    ).all()

    hotspots = {}

    for sample in samples:

        mineral = sample.mineral

        hotspots[mineral] = (
            hotspots.get(
                mineral,
                0
            ) + 1
        )

    ranking = sorted(
        hotspots.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return jsonify([
        {
            "mineral": mineral,
            "sample_count": count
        }
        for mineral, count in ranking
    ])

# ==================================
# AI NARRATIVE REPORT
# ==================================
@samples_bp.route(
    "/ai/narrative-report",
    methods=["GET"]
)
@jwt_required()
def narrative_report():

    current_user_id = int(
        get_jwt_identity()
    )

    samples = GeologicalSample.query.filter_by(
        user_id=current_user_id
    ).all()

    reports = ExplorationReport.query.filter_by(
        user_id=current_user_id
    ).all()

    if not samples:

        return jsonify({
            "report": "No geological samples available."
        })

    total_samples = len(samples)
    total_reports = len(reports)

    avg_depth = round(
        sum(
            sample.depth_meters
            for sample in samples
        ) / total_samples,
        2
    )

    mineral_counts = {}

    for sample in samples:

        mineral_counts[sample.mineral] = (
            mineral_counts.get(
                sample.mineral,
                0
            ) + 1
        )

    dominant_mineral = max(
        mineral_counts,
        key=mineral_counts.get
    )

    report_counts = {}

    for report in reports:

        report_counts[report.sample_id] = (
            report_counts.get(
                report.sample_id,
                0
            ) + 1
        )

    samples_without_reports = len([
        sample
        for sample in samples
        if report_counts.get(
            sample.id,
            0
        ) == 0
    ])

    narrative = (
        f"The exploration dataset contains "
        f"{total_samples} geological samples "
        f"and {total_reports} supporting reports. "

        f"The dominant mineral is "
        f"{dominant_mineral}, representing the "
        f"largest concentration of exploration activity. "

        f"Average drilling depth is "
        f"{avg_depth} meters. "

        f"{samples_without_reports} samples "
        f"currently lack supporting reports, "
        f"indicating opportunities for additional "
        f"documentation and validation. "

        f"Based on current data, "
        f"{dominant_mineral} exploration appears "
        f"to represent the strongest development "
        f"opportunity within the portfolio."
    )

    return jsonify({
        "report": narrative
    })

# ==================================
# AI EXECUTIVE BRIEFING
# ==================================
@samples_bp.route(
    "/ai/executive-briefing",
    methods=["GET"]
)
@jwt_required()
def executive_briefing():

    current_user_id = int(
        get_jwt_identity()
    )

    samples = GeologicalSample.query.filter_by(
        user_id=current_user_id
    ).all()

    reports = ExplorationReport.query.filter_by(
        user_id=current_user_id
    ).all()

    if not samples:

        return jsonify({
            "overview": "No exploration data available.",
            "risks": "",
            "opportunities": "",
            "recommendations": ""
        })

    total_samples = len(samples)
    total_reports = len(reports)

    # --------------------------
    # DOMINANT MINERAL
    # --------------------------

    mineral_counts = {}

    for sample in samples:

        mineral_counts[sample.mineral] = (
            mineral_counts.get(
                sample.mineral,
                0
            ) + 1
        )

    dominant_mineral = max(
        mineral_counts,
        key=mineral_counts.get
    )

    # --------------------------
    # REPORT COVERAGE
    # --------------------------

    report_counts = {}

    for report in reports:

        report_counts[report.sample_id] = (
            report_counts.get(
                report.sample_id,
                0
            ) + 1
        )

    samples_without_reports = len([
        sample
        for sample in samples
        if report_counts.get(
            sample.id,
            0
        ) == 0
    ])

    # --------------------------
    # DEEP SAMPLES
    # --------------------------

    deep_samples = len([
        sample
        for sample in samples
        if sample.depth_meters > 100
    ])

    overview = (
        f"The exploration portfolio contains "
        f"{total_samples} samples and "
        f"{total_reports} supporting reports. "
        f"{dominant_mineral} is the dominant "
        f"mineral in the dataset."
    )

    risks = (
        f"{samples_without_reports} samples lack "
        f"supporting reports and may require "
        f"additional validation."
    )

    opportunities = (
        f"{deep_samples} deep drilling samples "
        f"represent potential high-value "
        f"exploration targets."
    )

    recommendations = (
        f"Prioritize documentation of samples "
        f"without reports and focus future "
        f"exploration efforts on "
        f"{dominant_mineral} occurrences."
    )

    return jsonify({
        "overview": overview,
        "risks": risks,
        "opportunities": opportunities,
        "recommendations": recommendations
    })

# ==================================
# AI PORTFOLIO HEALTH
# ==================================
@samples_bp.route(
    "/ai/portfolio-health",
    methods=["GET"]
)
@jwt_required()
def portfolio_health():

    current_user_id = int(
        get_jwt_identity()
    )

    samples = GeologicalSample.query.filter_by(
        user_id=current_user_id
    ).all()

    reports = ExplorationReport.query.filter_by(
        user_id=current_user_id
    ).all()

    if not samples:

        return jsonify({
            "score": 0,
            "status": "No Data"
        })

    health_score = 100

    report_counts = {}

    for report in reports:

        report_counts[report.sample_id] = (
            report_counts.get(
                report.sample_id,
                0
            ) + 1
        )

    samples_without_reports = len([
        sample
        for sample in samples
        if report_counts.get(
            sample.id,
            0
        ) == 0
    ])

    health_score -= (
        samples_without_reports * 5
    )

    geo_missing = len([
        sample
        for sample in samples
        if sample.latitude is None
        or sample.longitude is None
    ])

    health_score -= (
        geo_missing * 3
    )

    well_documented = len([
        sample
        for sample in samples
        if report_counts.get(
            sample.id,
            0
        ) >= 3
    ])

    health_score += (
        well_documented * 2
    )

    if health_score > 100:
        health_score = 100

    if health_score < 0:
        health_score = 0

    # --------------------------
    # STATUS
    # --------------------------

    if health_score >= 80:
        status = "Excellent"

    elif health_score >= 60:
        status = "Good"

    elif health_score >= 40:
        status = "Fair"

    else:
        status = "Needs Attention"

    return jsonify({
        "score": health_score,
        "status": status,
        "samples": len(samples),
        "reports": len(reports),
        "samples_without_reports": samples_without_reports,
        "missing_coordinates": geo_missing
    })

## Report Management 
@samples_bp.route("/reports", methods=["GET"])
@jwt_required()
def get_reports():

    user_id = get_jwt_identity()

    reports = ExplorationReport.query.filter_by(
        user_id=user_id
    ).all()

    return jsonify([
        {
            "id": report.id,
            "title": report.title,
            "filename": report.filename,
            "sample_id": report.sample_id
        }
        for report in reports
    ])