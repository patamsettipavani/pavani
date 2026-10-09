import os
from flask import Flask, jsonify
from config import Config
from extensions import db, jwt, cors

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    
    try:
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    except Exception:
        pass

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    from routes.auth_routes import auth_bp
    from routes.resume_routes import resume_bp
    from routes.interview_routes import interview_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.coding_routes import coding_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(coding_bp)
    app.register_blueprint(coding_bp)

    # ✅ Ikkada pettu
    CORS(app, origins=["https://frontend-2-gold-chi.vercel.app", "https://frontend-2-7zo4ms8bi-pavani-ab70.vercel.app"], supports_credentials=True)

    with app.app_context():
    # FIX: Vercel lo db.create_all() vaddu - timeout vastundi
    # So try-except lo pettali
    with app.app_context():
        import models
        try:
            db.create_all()
        except Exception as e:
            print(f"DB create skipped: {e}")

    @app.route("/")
    def root():
        return jsonify({"message": "InterviewX AI Backend is Running!"}), 200

    @app.route("/api/health")
    def health():
        db_status = "connected"
        try:
            db.session.execute(db.text("SELECT 1"))
        except Exception as exc:
            db_status = f"error: {exc}"
        return jsonify({"status": "ok", "database": db_status}), 200

    return app


app = create_app()
def create_app():
    app = Flask(__name__)
    
    # ✅✅✅ IDI ADD CHEY - LINKING CODE ✅✅✅
    CORS(app, origins=[
        "https://frontend-2-gold-chi.vercel.app",
        "https://frontend-2-7zo4ms8bi-pavani-ab70.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173"
    ], supports_credentials=True)

    app.config.from_object(Config)
    # ... migilina code ala ne undani