from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import CodingRound, Interview
from services.gemini_service import generate_json

coding_bp = Blueprint("coding", __name__)


@coding_bp.route("/api/generate-coding-question", methods=["POST"])
@jwt_required()
def generate_coding_question():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    branch = (data.get("branch") or "general").strip()
    language = (data.get("language") or "python").strip()
    difficulty = (data.get("difficulty") or "medium").strip()
    interview_id = data.get("interview_id")

    if interview_id:
        iv = Interview.query.get(interview_id)
        if not iv or iv.user_id != user_id:
            return jsonify({"success": False, "message": "Interview not found."}), 404

    prompt = f"""You are an expert coding interviewer.

Generate ONE coding problem for:
- Branch/Domain: {branch}
- Language: {language}
- Difficulty: {difficulty}

Return ONLY JSON:
{{
  "title": "problem title",
  "description": "full problem description with examples",
  "constraints": "any constraints",
  "example_input": "sample input",
  "example_output": "sample output"
}}"""

    try:
        result = generate_json(prompt)
    except RuntimeError as exc:
        return jsonify({"success": False, "message": str(exc)}), 502

    question_text = (
        f"Title: {result.get('title', '')}\n\n"
        f"Description: {result.get('description', '')}\n\n"
        f"Constraints: {result.get('constraints', '')}\n\n"
        f"Example Input: {result.get('example_input', '')}\n"
        f"Example Output: {result.get('example_output', '')}"
    )

    cr = CodingRound(
        user_id=user_id,
        interview_id=interview_id,
        branch=branch,
        language=language,
        difficulty=difficulty,
        question_text=question_text,
    )
    db.session.add(cr)
    db.session.commit()

    return jsonify({
        "success": True,
        "coding_round_id": cr.id,
        "question_text": question_text,
    }), 200


@coding_bp.route("/api/submit-coding", methods=["POST"])
@jwt_required()
def submit_coding():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    coding_round_id = data.get("coding_round_id")
    user_code = (data.get("code") or "").strip()

    if not coding_round_id or not user_code:
        return jsonify({"success": False, "message": "coding_round_id and code are required."}), 400

    cr = CodingRound.query.get(coding_round_id)
    if not cr or cr.user_id != user_id:
        return jsonify({"success": False, "message": "Coding round not found."}), 404

    if not cr.question_text:
        return jsonify({"success": False, "message": "No question associated with this coding round."}), 400

    prompt = f"""You are an expert code reviewer. You do NOT execute code — you review it statically.

PROBLEM:
{cr.question_text}

CANDIDATE'S CODE ({cr.language}):
{user_code}

Review the code for correctness, efficiency, edge cases, and style. Return ONLY JSON:
{{
  "score": <float 0-100>,
  "review": "detailed review paragraph",
  "issues": ["issue1", "issue2"],
  "suggestions": ["suggestion1"]
}}

Do NOT claim you compiled or executed the code. Base your review on static analysis only."""

    try:
        result = generate_json(prompt)
    except RuntimeError as exc:
        return jsonify({"success": False, "message": str(exc)}), 502

    cr.user_code = user_code
    cr.ai_review = result.get("review", "")
    cr.score = float(result.get("score", 0))
    db.session.commit()

    return jsonify({
        "success": True,
        "coding_round_id": cr.id,
        "score": cr.score,
        "review": cr.ai_review,
        "issues": result.get("issues", []),
        "suggestions": result.get("suggestions", []),
        "note": "This is an AI static review, not actual code execution.",
    }), 200