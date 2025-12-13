class ServiceException(Exception):
    """
    Exception class for service-level errors
    """
    def __init__(self, message: str):
        super().__init__(message)