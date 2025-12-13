import logging
import re
from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from typing import Union
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
        "lockout_count": 0
    },
    "user2@example.com": {
        "password_hash": "pbkdf2:sha256:260000$anotherpasswordhash",
        "lockout_count": 0
    }
}

LOCKOUT_THRESHOLD = 5
RATE_LIMIT_SECONDS = 60
RATE_LIMIT_MAX_ATTEMPTS = 3
RATE_LIMIT_TRACKER = {}

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
    def validate_email_format(email: str) -> bool:
        """
        Validates the format of an email.
        """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def rate_limit_check(email: str) -> bool:
        """
        Checks if the user has exceeded rate limit.
        """
        from time import time
        current_time = time()

        if email in RATE_LIMIT_TRACKER:
            timestamps = RATE_LIMIT_TRACKER[email]
            timestamps = [t for t in timestamps if t > current_time - RATE_LIMIT_SECONDS]
            RATE_LIMIT_TRACKER[email] = timestamps

            if len(timestamps) >= RATE_LIMIT_MAX_ATTEMPTS:
                logger.warning(f"Rate limit exceeded for {email}. Attempts in {RATE_LIMIT_SECONDS} seconds: {len(timestamps)}")
                return True

        return False

    @staticmethod
    def record_attempt(email: str) -> None:
        """
        Records login attempt timestamps.
        """
        from time import time
        if email not in RATE_LIMIT_TRACKER:
            RATE_LIMIT_TRACKER[email] = []
        RATE_LIMIT_TRACKER[email].append(time())

    @staticmethod
    def login(email: str, password: str) -> Union[str, None]:
        if not AuthenticationService.validate_email_format(email):
            raise AuthenticationError("Invalid email format.")

        if email not in MOCK_USERS:
            raise AuthenticationError("Invalid credentials. Email not found.")

        if AuthenticationService.rate_limit_check(email):
            raise AuthenticationError("Rate limit exceeded. Please wait and try again later.")

        AuthenticationService.record_attempt(email)

        user_data = MOCK_USERS[email]
        if user_data["lockout_count"] >= LOCKOUT_THRESHOLD:
            raise AuthenticationError("Account temporarily locked. Check your email for recovery options.")

        if check_password_hash(user_data["password_hash"], password):
            user_data["lockout_count"] = 0  # Reset lockout count on successful login
            logger.info(f"User {email} successfully logged in.")
            return email
        else:
            user_data["lockout_count"] += 1
            logger.warning(f"Failed login attempt {user_data['lockout_count']} for user {email}.")

            if user_data["lockout_count"] >= LOCKOUT_THRESHOLD:
                # Trigger account lockout notifications here
                logger.error(f"User {email} account locked due to repeated failures.")

            raise AuthenticationError("Invalid credentials. Incorrect password.")

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
            return jsonify({"error": "Missing email or password."}), 400

        user_email = AuthenticationService.login(email, password)

        # Create user session
        SessionManager.create_session(user_email)

        return jsonify({"message": "Login successful."}), 200

    except AuthenticationError as auth_err:
        return jsonify({"error": str(auth_err)}), 401

    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        return jsonify({"error": "Internal server error."}), 500
