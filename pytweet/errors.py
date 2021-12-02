from typing import Optional

import requests


class PytweetException(Exception):
    """Exception: This is the base class of all exceptions.

    .. versionadded:: 1.2.0
    """

    def __init__(
        self,
        message: str = None,
    ):
        self.message = message
        super().__init__(self.message)


class APIException(PytweetException):
    """:class:`PytweetException`: Raised when an error is incurred during a request with HTTP Status code 200.

    .. versionadded:: 1.2.0
    """

    def __init__(
        self,
        response: Optional[requests.models.Response] = None,
        message: str = "No Error Message Provided",
    ):
        self.res = response
        self.message = message
        super().__init__(f"API returned an Exception: {self.message}")


class HTTPException(PytweetException):
    """:class:`PytweetException`: A custom error that will be raised whenever a request returns an HTTP status code above 200.

    .. versionadded:: 1.2.0
    """

    def __init__(
        self,
        response: Optional[requests.models.Response] = None,
        message: str = None,
    ):
        self.res = response
        self.json = response.json() if response else None
        self.message = message
        super().__init__(f"Request returned an Exception (status code: {self.res.status_code}): {self.message}")

    @property
    def status_code(self) -> Optional[int]:
        if not self.res:
            return None

        return self.res.status_code


class BadRequests(HTTPException):
    """:class:`HTTPException`: Raised when a request return status code: 400.

    .. versionadded:: 1.2.0
    """

    def __init__(
        self,
        response: Optional[requests.models.Response] = None,
        message: Optional[str] = None,
    ):
        msg = response.json().get("errors")[0].get("message") if not message else message
        detail = response.json().get("errors")[0].get("detail")
        super().__init__(response, msg if msg else detail if detail else "Not Found!")


class Unauthorized(HTTPException):
    """:class:`HTTPException`: Raised when the credentials you passed are invalid and a request returns status code: 401

    .. versionadded:: 1.0.0
    """

    def __init__(self, response, message: str = None):
        msg = None
        detail = None
        if response.json().get("errors"):
            msg = response.json().get("errors")[0].get("message") if not message else message
            detail = response.json().get("errors")[0].get("detail")

        else:
            detail = response.json().get("detail")

        super().__init__(
            response,
            msg if msg else detail if detail else "Unauthorized to do that action!",
        )


class Forbidden(HTTPException):
    """:class:`HTTPException`: Raised when a request returns status code: 403.

    .. versionadded:: 1.2.0
    """

    def __init__(
        self,
        response: Optional[requests.models.Response] = None,
        message: Optional[str] = None,
    ):
        msg = None
        detail = None
        if response.json().get("errors"):
            msg = response.json().get("errors")[0].get("message") if not message else message
            detail = response.json().get("errors")[0].get("detail")

        else:
            detail = response.json().get("detail")

        super().__init__(
            response,
            msg if msg else detail if detail != "Forbidden" else "Forbidden to do that action.",
        )


class NotFound(HTTPException):
    """:class:`HTTPException`: Raised when a request returns status code: 404.

    .. versionadded:: 1.2.0
    """

    def __init__(
        self,
        response: Optional[requests.models.Response] = None,
        message: Optional[str] = None,
    ):
        msg = response.json().get("errors")[0].get("message") if not message else message
        detail = response.json().get("errors")[0].get("detail")
        super().__init__(response, msg if msg else detail if detail else "Not Found!")


class TooManyRequests(HTTPException):
    """:class:`HTTPException`: Raised when ratelimit exceeded and a request return status code: 429

    .. versionadded:: 1.1.0
    """

    pass


class NotFoundError(APIException):
    """:class:`APIException`: This error is usually raised when trying to find specific Tweet or User that does not exist.

    .. versionadded:: 1.0.0
    """

    def __init__(
        self,
        response: Optional[requests.models.Response] = None,
        message: Optional[str] = None,
    ):
        msg = response.json().get("errors")[0].get("message") if not message else message
        detail = response.json().get("errors")[0].get("detail")
        super().__init__(response, msg if msg else detail if detail else "Not Found!")


class UnKnownSpaceState(APIException):
    def __init__(self, given_state):
        super().__init__(message="Unknown state passed: %s" % given_state)


class ConnectionException(HTTPException):
    def __init__(
        self,
        response: Optional[requests.models.Response] = None,
        message: Optional[str] = None,
    ):
        json = response.json()
        if "errors" in json and not message:
            msg = response.json().get("errors")[0].get("message") if not message else message
            detail = response.json().get("errors")[0].get("detail")

        else:
            msg = None
            detail = json.get("detail")

        super().__init__(response, msg if msg else detail)
