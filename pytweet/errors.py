class Unauthorized(Exception):
    """Raised when the Credentials you passed is invalid!"""

    pass


class NotFoundError(Exception):
    """Raised when the api return NotFoundError, meaning it cant find an object in the database."""

    pass


class TooManyRequests(Exception):
    """Raised when ratelimit exceeded and a request return status code: 429"""

    pass


class Forbidden(Exception):
    """Raised when a request return status code: 403"""

    pass


class PytweetException(Exception):
    """Raise whenever the client failed executing a function. This usually happen due to user input."""

    pass
