# utils.py

"""
Common utility functions.
"""

import os
import smtplib
from email.mime.text import MIMEText
from app.models import User
from datetime import datetime, timedelta
import jwt

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')


def send_reset_email(to_email: str, token: str) -> None:
    """
    Send a password reset email.
    """
    msg = MIMEText(f"Click the link to reset your password: {token}")
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = 'no-reply@example.com'
    msg['To'] = to_email

    with smtplib.SMTP('localhost') as server:
        server.sendmail('no-reply@example.com', to_email, msg.as_string())


def verify_reset_token(token: str):
    """
    Verify if the reset token is valid.
    """
    try:
        email = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])['email']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
    return User.query.filter_by(email=email).first()
