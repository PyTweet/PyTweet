import requests
from typing import Optional
from json import decoder


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
    """:class:`PytweetException`: raises when an error is incurred during a request with HTTP Status code 200.

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
    """:class:`PytweetException`: A custom error that will be raises whenever a request returns an HTTP status code above 200.

    .. versionadded:: 1.2.0
    """

    def __init__(
        self,
        response: Optional[requests.models.Response] = None,
        message: str = None,
    ):
            self.res = response
            try:
                self.json = response.json() if response else None
            except Exception:
                pass
            self.message = message
            super().__init__(f"Request returned an Exception (status code: {self.res.status_code}): {self.message}")

    @property
    def status_code(self) -> Optional[int]:
        if not self.res:
            return None

        return self.res.status_code


class BadRequests(HTTPException):
    """This class inherits :class:`HTTPException`. raises when a request return status code: 400.

    .. versionadded:: 1.2.0
    """

    def __init__(
        self,
        response: Optional[requests.models.Response] = None,
        message: Optional[str] = None,
    ):
        msg = response.json().get("error")
        super().__init__(msg if msg else "Bad Request!")


class Unauthorized(HTTPException):
    """This class inherits :class:`HTTPException`. raises when the credentials you passed are invalid and a request returns status code: 401

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
    """This class inherits :class:`HTTPException`. raises when a request returns status code: 403.

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


class FieldsTooLarge(HTTPException):
    def __init__(self, response, message: str = None):
        msg = None
        detail = None
        try:
            if response.json().get("errors"):
                msg = response.json().get("errors")[0].get("message") if not message else message
                detail = response.json().get("errors")[0].get("detail")

            else:
                detail = response.json().get("detail")
        except decoder.JSONDecodeError:
            super().__init__(response, response.text)

        else:
            super().__init__(
                response,
                msg if msg else detail if detail else "Request Header Fields Too Large",
            )


class NotFound(HTTPException):
    """This class inherits :class:`HTTPException`. raises when a request returns status code: 404.

    .. versionadded:: 1.2.0
    """

    def __init__(
        self,
        response: Optional[requests.models.Response] = None,
        message: Optional[str] = None,
    ):
        try:
            msg = response.json().get("errors")[0].get("message") if not message else message
            detail = response.json().get("errors")[0].get("detail")
            super().__init__(response, msg if msg else detail if detail else "Not Found!")
        except decoder.JSONDecodeError:
            super().__init__(response, response.text)


class TooManyRequests(HTTPException):
    """This class inherits :class:`HTTPException`. raises when ratelimit exceeded and a request return status code: 429

    .. versionadded:: 1.1.0
    """

    pass


class ConnectionException(HTTPException):
    """This error class inherits :class:`HTTPException`. This error is raises when a stream connection throw an error.

    .. versionadded:: 1.3.5
    """

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


class Conflict(HTTPException):
    """This error class inherits :class:`HTTPException`. This error is raises when a request return 409 status code."""

    def __init__(
        self,
        response: Optional[requests.models.Response] = None,
        message: Optional[str] = None,
    ):
        msg = response.json().get("errors")[0].get("message") if not message else message
        detail = response.json().get("errors")[0].get("detail")
        super().__init__(response, msg if msg else detail if detail else "Not Found!")


class NotFoundError(APIException):
    """This error class inherits :class:`APIException`. This error is usually raises when trying to find specific Tweet or User that does not exist.

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
    """This error class inherits :class:`APIException`. This error is raises when a user specified an invalid space state.

    .. versionadded:: 1.5.0
    """

    def __init__(self, given_state):
        super().__init__(message="Unknown state passed: %s" % given_state)
