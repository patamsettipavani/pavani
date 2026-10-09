import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from extensions import db
from models import Resume, ResumeAnalysis
from services.pdf_service import extract_text_from_pdf
from services.gemini_service import generate_json

resume_bp = Blueprint("resume", __name__)

ALLOWED_EXT = {"pdf"}

def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@resume_bp.route("/api/upload-resume", methods=["POST"])
@jwt_required()
def upload_resume():
    user_id = int(get_jwt_identity())
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file provided."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "message": "Empty filename."}), 400

    if not _allowed(file.filename):
        return jsonify({"success": False, "message": "Only PDF files are allowed."}), 400

    safe_name = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, unique_name)

    try:
        file.save(filepath)
    except Exception as exc:
        current_app.logger.error("File save error: %s", exc)
        return jsonify({"success": False, "message": "Failed to save file."}), 500

    try:
        extracted = extract_text_from_pdf(filepath)
    except Exception as exc:
        current_app.logger.error("PDF extraction error: %s", exc)
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"success": False, "message": "Failed to extract text from PDF."}), 400

    if not extracted or not extracted.strip():
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"success": False, "message": "PDF contains no extractable text."}), 400

    resume = Resume(user_id=user_id, filename=safe_name, filepath=filepath, extracted_text=extracted)
    db.session.add(resume)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Resume uploaded successfully.",
        "resume_id": resume.id,
        "filename": safe_name,
        "text_length": len(extracted),
    }), 201


@resume_bp.route("/api/analyze-resume", methods=["POST"])
@jwt_required()
def analyze_resume():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)
    
    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Valid JSON object required."}), 400

    resume_id = data.get("resume_id")
    job_description = (data.get("job_description") or "").strip()

    if not resume_id or not job_description:
        return jsonify({"success": False, "message": "resume_id and job_description are required."}), 400

    resume = Resume.query.get(resume_id)
    if not resume or resume.user_id != user_id:
        return jsonify({"success": False, "message": "Resume not found or unauthorized."}), 404

    if not resume.extracted_text or not resume.extracted_text.strip():
        return jsonify({"success": False, "message": "Resume has no extracted text. Re-upload the PDF."}), 400

    prompt = f"""You are an expert ATS and resume analyst. Analyze the following resume against the job description.
RESUME TEXT: {resume.extracted_text[:6000]}
JOB DESCRIPTION: {job_description[:3000]}
Return ONLY a JSON object with these exact keys:
{{
  "ats_score": <float 0-100>,
  "grammar_score": <float 0-100>,
  "skills_match": <float 0-100>,
  "overall_score": <float 0-100>,
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill3", "skill4"],
  "suggestions": ["suggestion1", "suggestion2"]
}}"""

    try:
        result = generate_json(prompt)
    except RuntimeError as exc:
        return jsonify({"success": False, "message": str(exc)}), 502

    required_keys = {"ats_score", "grammar_score", "skills_match", "overall_score", "matched_skills", "missing_skills", "suggestions"}
    if not required_keys.issubset(result.keys()):
        return jsonify({"success": False, "message": "AI returned incomplete analysis."}), 502

    analysis = ResumeAnalysis(
        resume_id=resume.id,
        job_description=job_description,
        ats_score=float(result["ats_score"]),
        grammar_score=float(result["grammar_score"]),
        skills_match=float(result["skills_match"]),
        overall_score=float(result["overall_score"]),
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
        suggestions=result["suggestions"],
    )
    db.session.add(analysis)
    db.session.commit()

    return jsonify({
        "success": True,
        "analysis_id": analysis.id,
        "ats_score": analysis.ats_score,
        "grammar_score": analysis.grammar_score,
        "skills_match": analysis.skills_match,
        "overall_score": analysis.overall_score,
        "matched_skills": analysis.matched_skills,
        "missing_skills": analysis.missing_skills,
        "suggestions": analysis.suggestions,
    }), 200