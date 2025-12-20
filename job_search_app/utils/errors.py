"""
Custom exception classes for the application
"""


class APIError(Exception):
    """Base exception for API errors"""
    def __init__(self, message, status_code=500, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        rv['status'] = 'error'
        return rv


class ValidationError(APIError):
    """Raised when input validation fails"""
    def __init__(self, message, payload=None):
        super().__init__(message, status_code=400, payload=payload)


class ScrapingError(APIError):
    """Raised when job scraping fails"""
    def __init__(self, message, payload=None):
        super().__init__(message, status_code=503, payload=payload)


class ResourceNotFoundError(APIError):
    """Raised when a requested resource is not found"""
    def __init__(self, message, payload=None):
        super().__init__(message, status_code=404, payload=payload)
