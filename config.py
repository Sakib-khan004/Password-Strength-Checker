import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "securepass-dev-secret-key-change-in-production")
    DATABASE = os.path.join(BASE_DIR, "database.db")

    # Admin login credentials (change these before deploying anywhere real)
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

    COMMON_PASSWORDS_FILE = os.path.join(BASE_DIR, "data", "common_passwords.txt")
    DICTIONARY_FILE = os.path.join(BASE_DIR, "data", "dictionary.txt")
