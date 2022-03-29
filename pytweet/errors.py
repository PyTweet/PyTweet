import requests
from typing import Optional
from json import decoder


class PytweetException(Exception):
    """This is the base class of all exceptions Raise by PyTweet. This inherits :class:`Exception`.

    .. versionadded:: 1.2.0
    """

    def __init__(
        self,
        message: str = None,
    ):
        self.message = message
        super().__init__(self.message)


class APIException(PytweetException):
    """A custom error that will be Raise whenever a request returns an HTTP status code 200. This inherits :class:`PytweetException`.

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
    """A custom error that will be Raise whenever a request returns an HTTP status code above 200. This inherits :class:`PytweetException`.

    .. versionadded:: 1.2.0
    """

    def __init__(
        self,
        response: Optional[requests.models.Response] = None,
        message: str = None,
    ):
        self.response = response
        self.message = message
        self.detail = None
        if response is not None:
            try:
                res = self.response.json()
                if res.get("errors"):
                    self.message = res.get("errors")[0].get("message") if not message else message
                    self.detail = res.get("errors")[0].get("detail")

                else:
                    self.message = res.get("error")
                    if not self.message:
                        self.detail = res.get("detail")

            except decoder.JSONDecodeError:
                super().__init__(
                    f"Request returned an Exception (status code: {self.response.status_code}): {self.response.text}",
                )

            else:
                super().__init__(
                    f"Request returned an Exception (status code: {self.response.status_code}): {self.message if self.message else self.detail}",
                )

        else:
            super().__init__(
                f"Exception Raise: {self.message}",
            )

    @property
    def status_code(self) -> Optional[int]:
        if not self.response:
            return None
        return self.response.status_code


class BadRequests(HTTPException):
    """This class inherits :class:`HTTPException`. Raise when a request return status code: 400.

    .. versionadded:: 1.2.0
    """

    pass


class Unauthorized(HTTPException):
    """This class inherits :class:`HTTPException`. Raise when the credentials you passed are invalid and a request returns status code: 401

    .. versionadded:: 1.0.0
    """

    pass


class Forbidden(HTTPException):
    """This class inherits :class:`HTTPException`. Raises when a request returns status code: 403.

    .. versionadded:: 1.2.0
    """

    pass


class FieldsTooLarge(HTTPException):
    """ "This class inherits :class:`HTTPException`. Raises when a request returns status code: 431"""

    pass


class NotFound(HTTPException):
    """This class inherits :class:`HTTPException`. Raise when a request returns status code: 404.

    .. versionadded:: 1.2.0
    """

    pass


class TooManyRequests(HTTPException):
    """This class inherits :class:`HTTPException`. Raise when ratelimit exceeded and a request return status code 429.

    .. versionadded:: 1.1.0
    """

    pass


class ConnectionException(HTTPException):
    """This error class inherits :class:`HTTPException`. This error is Raise when a stream connection throw an error.

    .. versionadded:: 1.3.5
    """

    pass


class Conflict(HTTPException):
    """This error class inherits :class:`HTTPException`. This error is Raise when a request return 409 status code."""

    pass


class UnKnownSpaceState(APIException):
    """This error class inherits :class:`APIException`. This error is Raise when a user specified an invalid space state.

    .. versionadded:: 1.5.0
    """

    def __init__(self, given_state):
        super().__init__(message="Unknown state passed: %s" % given_state)


class NoPageAvailable(APIException):
    """This error class inherits :class:`APIException`. This error is Raise when a user try to lookup a new page in a pagination object that does not exist. These following methods can Raise this error:

    * :meth:`UserPagination.next_page` and :meth:`UserPagination.previous_page`
    * :meth:`TweetPagination.next_page` and :meth:`TweetPagination.previous_page`
    * :meth:`ListPagination.next_page` and :meth:`ListPagination.previous_page`
    * :meth:`MessagePagination.next_page` and :meth:`MessagePagination.previous_page`

    .. versionadded:: 1.5.0
    """

    def __init__(self):
        super().__init__(message="Pagination has no more page available!")


class UnauthorizedForResource(APIException):
    """This error class inherits :class:`APIException`. This error is Raise when the client is unauthorized to view certain resource like for example: viewing a protected user's tweets using :meth:`User.fetch_timelines`.

    .. versionadded:: 1.5.0
    """

    def __init__(self, message):
        super().__init__(message=message)


class ResourceNotFound(APIException):
    """This error class inherits :class:`APIException`. This error is a result of finding a none existent resource .

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.5.0

        Changed name from `NotFoundError` to `ResourceNotFound`
    """

    def __init__(self, message):
        super().__init__(message=message)

class DisallowedResource(APIException):
    """This error class inherits :class:`APIException`. This error is a result of finding a none existent resource .

    .. versionadded:: 1.5.0
    """

    def __init__(self, message):
        super().__init__(message=message)