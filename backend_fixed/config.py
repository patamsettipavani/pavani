import os
import urllib.parse
from dotenv import load_dotenv

# Load .env from the same folder as this config.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_FILE, override=True)

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-CHANGE-ME"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "jwt-dev-CHANGE-ME"
    )

    # --- FIX 1: DATABASE_URL support for Vercel ---
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        # Vercel Postgres / Neon DB (postgres)
        # postgres:// to postgresql:// ga marchali
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Local MySQL
        MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
        MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
        MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "interview_x_ai")
        MYSQL_USER = os.getenv("MYSQL_USER", "root")
        MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
        encoded_password = urllib.parse.quote_plus(MYSQL_PASSWORD)
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{encoded_password}"
            f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash"
    )

    # --- FIX 2: Vercel writable folder ---
    UPLOAD_FOLDER = "/tmp/uploads"

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024