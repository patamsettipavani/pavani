from datetime import datetime, timezone
from extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    resumes = db.relationship("Resume", backref="user", lazy=True)
    interviews = db.relationship("Interview", backref="user", lazy=True)
    coding_rounds = db.relationship("CodingRound", backref="user", lazy=True)

class Resume(db.Model):
    __tablename__ = "resumes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    extracted_text = db.Column(db.Text, nullable=True)  # Fixed: LongText -> Text
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    analyses = db.relationship("ResumeAnalysis", backref="resume", lazy=True)

class ResumeAnalysis(db.Model):
    __tablename__ = "resume_analyses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    ats_score = db.Column(db.Float, nullable=True)
    grammar_score = db.Column(db.Float, nullable=True)
    skills_match = db.Column(db.Float, nullable=True)
    overall_score = db.Column(db.Float, nullable=True)
    matched_skills = db.Column(db.JSON, nullable=True)
    missing_skills = db.Column(db.JSON, nullable=True)
    suggestions = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Interview(db.Model):
    __tablename__ = "interviews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=True)
    company = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(200), nullable=True)
    branch = db.Column(db.String(200), nullable=True)
    difficulty = db.Column(db.String(50), nullable=True)
    mode = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), default="in_progress")
    overall_score = db.Column(db.Float, nullable=True)
    total_questions = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)
    questions = db.relationship("InterviewQuestion", backref="interview", lazy=True)
    answers = db.relationship("InterviewAnswer", backref="interview", lazy=True)
    report = db.relationship("InterviewReport", backref="interview", uselist=False, lazy=True)
    events = db.relationship("InterviewEvent", backref="interview", lazy=True)

class InterviewQuestion(db.Model):
    __tablename__ = "interview_questions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    answer = db.relationship("InterviewAnswer", backref="question", uselist=False, lazy=True)

class InterviewAnswer(db.Model):
    __tablename__ = "interview_answers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey("interview_questions.id"), nullable=False)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False)
    user_answer = db.Column(db.Text, nullable=False)
    score = db.Column(db.Float, nullable=True)
    verdict = db.Column(db.String(50), nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    strengths = db.Column(db.Text, nullable=True)
    improvements = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class InterviewReport(db.Model):
    __tablename__ = "interview_reports"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False, unique=True)
    overall_score = db.Column(db.Float, nullable=True)
    strengths = db.Column(db.JSON, nullable=True)
    weaknesses = db.Column(db.JSON, nullable=True)
    recommendations = db.Column(db.JSON, nullable=True)
    interview_dna = db.Column(db.JSON, nullable=True)
    resume_match = db.Column(db.JSON, nullable=True)
    heatmap = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class CodingRound(db.Model):
    __tablename__ = "coding_rounds"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=True)
    branch = db.Column(db.String(200), nullable=True)
    language = db.Column(db.String(100), nullable=True)
    difficulty = db.Column(db.String(50), nullable=True)
    question_text = db.Column(db.Text, nullable=True)
    user_code = db.Column(db.Text, nullable=True)  # Fixed: LongText -> Text
    ai_review = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class InterviewEvent(db.Model):
    __tablename__ = "interview_events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    event_data = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))