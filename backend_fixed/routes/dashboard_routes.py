from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from models import Interview

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/api/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    user_id = int(get_jwt_identity())

    total = Interview.query.filter_by(user_id=user_id).count()
    completed = Interview.query.filter_by(user_id=user_id, status="completed").count()

    avg_row = (
        Interview.query
        .filter_by(user_id=user_id, status="completed")
        .with_entities(func.avg(Interview.overall_score))
        .scalar()
    )
    average_score = round(float(avg_row), 2) if avg_row is not None else None

    recent = (
        Interview.query
        .filter_by(user_id=user_id)
        .order_by(Interview.created_at.desc())
        .limit(10)
        .all()
    )

    history = []
    for iv in recent:
        history.append({
            "interview_id": iv.id,
            "company": iv.company,
            "role": iv.role,
            "status": iv.status,
            "overall_score": iv.overall_score,
            "created_at": iv.created_at.isoformat() if iv.created_at else None,
        })

    return jsonify({
        "success": True,
        "data": {
            "total_interviews": total,
            "completed_interviews": completed,
            "average_score": average_score,
            "recent_interviews": history,
        },
    }), 200


# Alias in case frontend calls /api/dashboard-stats
@dashboard_bp.route("/api/dashboard-stats", methods=["GET"])
@jwt_required()
def dashboard_stats():
    return dashboard()