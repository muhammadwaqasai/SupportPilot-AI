import os
from datetime import timedelta

from dotenv import load_dotenv


load_dotenv()



# ---------------- DATABASE CONFIGURATION ----------------

DB_HOST = os.getenv("DB_HOST")

DB_PORT = int(os.getenv("DB_PORT", "10285"))

DB_USER = os.getenv("DB_USER")

DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_NAME = os.getenv("DB_NAME")



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
