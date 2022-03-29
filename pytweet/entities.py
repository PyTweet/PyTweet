from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING

from .enums import MediaType
from .dataclass import NonPublicMediaMetrics, OrganicMediaMetrics, PromotedMediaMetrics
from .utils import convert

if TYPE_CHECKING:
    from .http import HTTPClient


class Hashtag:
    """Represents a hashtag in a message."""

    __slots__ = ("_payload", "_text", "_startpoint", "_endpoint")

    def __init__(self, data: Dict[str, Any]):
        self._payload = data
        self._text: Optional[str] = self._payload.get("text")
        self._startpoint, self._endpoint = self._payload.get("indices")

    @property
    def text(self) -> Optional[str]:
        """Optional[:class:`str`]: Returns the hashtag's text."""
        return self._text

    @property
    def points(self) -> Optional[Tuple]:
        """Optional[:class:`Tuple`]: Returns a tuple with the hashtag's startpoint and endpoint."""
        return self._startpoint, self._endpoint


class UserMention:
    """Represents a user mention in a message."""

    __slots__ = ("_payload", "_name", "_screen_name", "_id", "_startpoint", "_endpoint")

    def __init__(self, data: Dict[str, Any]):
        self._payload: Dict[str, Any] = data
        self._name: str = self._payload.get("name")
        self._screen_name: str = self._payload.get("screen_name")
        self._id: int = self._payload.get("id")
        self._startpoint, self._endpoint = self._payload.get("indices")

    @property
    def name(self) -> str:
        """:class:`str`: Returns the mention user's name."""
        return self._name

    @property
    def username(self) -> str:
        """:class:`str`: Returns the mention user's username."""
        return self._screen_name

    @property
    def id(self) -> int:
        """:class:`id`: Returns the mention user's id."""
        return int(self._id)

    @property
    def points(self) -> Optional[Tuple]:
        """Optional[:class:`Tuple`]: Returns a tuple with the mention's startpoint and endpoint."""
        return self._startpoint, self._endpoint


class Url:
    """Represents Url in a message."""

    __slots__ = (
        "_payload",
        "_url",
        "_display_url",
        "_expanded_url",
        "_startpoint",
        "_endpoint",
    )

    def __init__(self, data: Dict[str, Any]):
        self._payload: Dict[str, Any] = data
        self._url: str = self._payload.get("url")
        self._display_url: str = self._payload.get("display_url")
        self._expanded_url: str = self._payload.get("expanded_url")
        self._startpoint, self._endpoint = self._payload.get("indices")

    @property
    def url(self) -> str:
        """:class:`str`: Returns the message's url."""
        return self._url

    @property
    def display_url(self) -> str:
        """:class:`str`: Returns the message's display url"""
        return self._display_url

    @property
    def expanded_url(self) -> str:
        """:class:`str`: Returns the message's expanded url"""
        return self._expanded_url

    @property
    def points(self) -> Tuple:
        """Optional[:class:`Tuple`]: Returns a tuple with the url's startpoint and endpoint."""
        return self._startpoint, self._endpoint


class Symbol:
    """Represents a Symbol in a message."""

    __slots__ = ("_payload", "_text", "_startpoint", "_endpoint")

    def __init__(self, data=Optional[Dict[str, Any]]):
        self._payload: Dict[str, Any] = data
        self._text: str = self._payload.get("text")
        self._startpoint, self._endpoint = self._payload.get("indices")

    @property
    def text(self) -> str:
        """:class:`str`: Returns the symbol's text."""
        return self._text

    @property
    def points(self) -> Tuple:
        """Optional[:class:`Tuple`]: Returns a tuple with the url's startpoint and endpoint."""
        return self._startpoint, self._endpoint
