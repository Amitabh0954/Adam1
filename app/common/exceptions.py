class AppError(Exception):
    """
    Base exception class for application errors.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class ValidationError(AppError):
    """
    Exception raised for input validation errors.
    """
    pass
