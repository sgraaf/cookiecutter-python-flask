"""Main application config."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"

# load environment variable file
load_dotenv(BASE_DIR / ".flaskenv")


class Config:
    """Flask config object."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or ""

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URI") or f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JSON_SORT_KEYS = False

    PER_PAGE = 10

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    ADMINS = [os.environ.get("ADMIN_EMAIL_ADDRESS")]
