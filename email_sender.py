import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_email(receiver_email, subject, message):

    msg = MIMEText(message)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(EMAIL, APP_PASSWORD)

    server.send_message(msg)

    server.quit()

    print("Email sent successfully!")