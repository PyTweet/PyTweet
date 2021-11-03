class HTTPException(Exception):
    pass


class Unauthorized(HTTPException):
    """Raised when the Credentials you passed is invalid!"""

    pass


class NotFoundError(HTTPException):
    """Raised when the api return NotFoundError, meaning it cant find an object in the database."""

    pass


class TooManyRequests(HTTPException):
    """Raised when ratelimit exceeded and a request return status code: 429"""

    pass


class Forbidden(HTTPException):
    """Raised when a request return status code: 403"""

    pass


class PytweetException(HTTPException):
    """Raise whenever the client failed executing a function. This usually happen due to user input."""

    pass
