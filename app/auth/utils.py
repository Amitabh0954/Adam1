# app/auth/utils.py

"""
This module contains utility functions for the authentication module.
"""

import re

def validate_email_format(email: str) -> bool:
    """
    Validates the format of an email address.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None
