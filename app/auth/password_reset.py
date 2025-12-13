# password_reset.py

"""
Module for handling password reset functionality.
"""

import logging
from flask import Blueprint, request, jsonify
from app.models import User
from app.common.utils import send_reset_email, verify_reset_token
from datetime import datetime, timedelta
import hashlib
import secrets

logger = logging.getLogger(__name__)

password_reset_bp = Blueprint('password_reset', __name__)


@password_reset_bp.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    """
    Request a password reset link.
    """
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "If your email is registered, a reset link will be sent."}), 200

    token = user.get_reset_token()
    send_reset_email(user.email, token)

    return jsonify({"message": "If your email is registered, a reset link will be sent."}), 200


@password_reset_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token: str):
    """
    Reset the user's password using the token.
    """
    user = verify_reset_token(token)
    if not user:
        return jsonify({"error": "Token is invalid or expired."}), 400

    data = request.get_json()
    new_password = data.get('password')
    if not new_password or len(new_password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long."}), 400

    user.set_password(new_password)
    user.save()

    return jsonify({"message": "Your password has been reset successfully."}), 200
