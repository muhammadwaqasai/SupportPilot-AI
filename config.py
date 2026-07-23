import os
from datetime import timedelta

from dotenv import load_dotenv


load_dotenv()



# ---------------- DATABASE CONFIGURATION ----------------

DB_HOST = os.getenv(
    "DB_HOST",
    "localhost"
)

DB_USER = os.getenv(
    "DB_USER",
    "root"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD",
    "waqas@050675"
)

DB_NAME = os.getenv(
    "DB_NAME",
    "ai_support"
)



# ---------------- OPENAI CONFIGURATION ----------------

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)



# ---------------- FLASK SECURITY ----------------

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "9f7c2a1d8e4b6f3a9c2e7d1f5a8b0c4e"
)


PERMANENT_SESSION_LIFETIME = timedelta(
    hours=8
)