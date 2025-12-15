import logging
from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from typing import Union
import re
from app.common.custom_exceptions import AuthenticationError

# Configure logging
logger = logging.getLogger("auth_service")
logger.setLevel(logging.INFO)

# Blueprint for authentication
auth_blueprint = Blueprint("auth", __name__)

# Mock database for demonstration purposes
MOCK_USERS = {
    "user1@example.com": {
        "password_hash": "pbkdf2:sha256:260000$mypasswordhash",
        "lockout_count": 0,
        "rate_limit": 0
    },
    "user2@example.com": {
        "password_hash": "pbkdf2:sha256:260000$anotherpasswordhash",
        "lockout_count": 0,
        "rate_limit": 0
    }
}

LOCKOUT_THRESHOLD = 5
RATE_LIMIT_THRESHOLD = 5
RATE_LIMIT_RESET_TIME = 60  # seconds

class SessionManager:
    """
    Handles user session operations.
    """

    @staticmethod
    def create_session(user_email: str) -> None:
        session['user'] = user_email
        session['timeout'] = 1800  # 30 minutes inactivity timeout

    @staticmethod
    def clear_session() -> None:
        session.clear()

class AuthenticationService:
    """
    Manages user authentication.
    """

    @staticmethod
    def validate_email(email: str):
        """Validates email using a regular expression."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise AuthenticationError("Invalid email format.")

    @staticmethod
    def login(email: str, password: str) -> Union[str, None]:
        AuthenticationService.validate_email(email)

        if email not in MOCK_USERS:
            raise AuthenticationError("Invalid credentials.")
        user_data = MOCK_USERS[email]

        # Rate limiting check
        if user_data["rate_limit"] >= RATE_LIMIT_THRESHOLD:
            raise AuthenticationError("Too many requests. Please try again later.")

        if user_data["lockout_count"] >= LOCKOUT_THRESHOLD:
            raise AuthenticationError("Account temporarily locked. Check your email for recovery options.")

        if check_password_hash(user_data["password_hash"], password):
            user_data["lockout_count"] = 0  # Reset lockout count on successful login
            user_data["rate_limit"] = 0  # Reset rate limit on successful login
            logger.info(f"User {email} successfully logged in.")
            return email
        else:
            user_data["lockout_count"] += 1
            user_data["rate_limit"] += 1
            logger.warning(f"Failed login attempt {user_data['lockout_count']} for user {email}.")

            if user_data["lockout_count"] >= LOCKOUT_THRESHOLD:
                # Trigger account lockout notifications here
                logger.error(f"User {email} account locked due to repeated failures.")
            raise AuthenticationError("Invalid credentials.")

@auth_blueprint.route("/login", methods=["POST"])
def login_handler():
    """
    API endpoint for user login.
    """
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400

        user_email = AuthenticationService.login(email, password)

        # Create user session
        SessionManager.create_session(user_email)

        return jsonify({"message": "Login successful."}), 200

    except AuthenticationError as auth_err:
        return jsonify({"error": str(auth_err)}), 401

    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        return jsonify({"error": "Internal server error."}), 500
