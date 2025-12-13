import os

class Config:
    """
    Application configuration class.
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    EMAIL_SERVICE_API_KEY = os.getenv("EMAIL_SERVICE_API_KEY", "placeholder_key")
