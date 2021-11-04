from typing import Optional

class PytweetException(Exception):
    """Exception: This is the base class of all exceptions.
    .. versionadded:: 1.2.0
    """
    def __init__(self, response, message):
        self.res = response
        self.message = message
        super().__init__(self.message)

    @property
    def status_code(self) -> Optional[int]:
        if not self.res:
            return None
            
        return self.res.status_code

class APIException(PytweetException):
    """:class:`PytweetException`: Raise When an error is incurred during a request with HTTP Status code 200.
    .. versionadded:: 1.2.0
    """
    pass

class HTTPException(PytweetException):
    """:class:`PytweetException`: A custom error that will be raised when ever a request return HTTP status code above 200. 
    .. versionadded:: 1.2.0
    """
    pass

class Unauthorized(HTTPException):
    """:class:`HTTPException`: Raised when the Credentials you passed is invalid and a request return status code: 401
    .. versionadded:: 1.0.0
    """
    pass

class TooManyRequests(HTTPException):
    """:class:`HTTPException`: Raised when ratelimit exceeded and a request return status code: 429
    .. versionadded:: 1.1.0
    """
    pass

class Forbidden(HTTPException):
    """:class:`HTTPException`: Raised when a request return status code: 403
    .. versionadded:: 1.2.0
    """
    pass

class NotFound(APIException):
    """This error is returned when a given Tweet, User, etc. does not exist.
    .. versionadded:: 1.0.0
    """
    pass






