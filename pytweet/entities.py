from typing import Any, Dict, Tuple, Optional


class Media:
    """Represent media in a message."""

    def __init__(self, data: Dict[str, Any]):
        self._payload = data
        self._url = self._payload.get("url")
        self._media_key = self._payload.get("media_key")
        self._type = self._payload.get("type")
        self._width, self._height = self._payload.get("width"), self._payload.get(
            "_height"
        )

    @property
    def url(self) -> str:
        """:class:`str`: Returns the image's url"""
        return self._url

    @property
    def media_key(self) -> str:
        """:class:`str`: Returns the image's media key"""
        return self._media_key

    @property
    def type(self) -> str:
        """:class:`str`: Returns the image's type"""
        return self._type

    @property
    def width(self) -> int:
        """:class:`str`: Returns the image's width"""
        return int(self._width)

    @property
    def height(self) -> int:
        """:class:`str`: Returns the image's height"""
        return int(self._height)


class Hashtags:
    """Represent hashtags in a message"""

    def __init__(self, data=Dict[str, Any]):
        self._payload = data
        self._text: Optional[str] = self._payload.get("text")
        self._startpoint, self._endpoint = self._payload.get("indices")

    @property
    def text(self) -> Optional[str]:
        """Optional[:class:`str`]: Returns the hashtag's text.OSError"""
        return self._text

    @property
    def points(self) -> Optional[Tuple]:
        """Optional[:class:`Tuple`]: Returns a tuple with the hashtag's startpoint and endpoint"""
        return self._startpoint, self._endpoint


class UserMentions:
    """Represent user mention in a message."""

    def __init__(self, data=Dict[str, Any]):
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
    def screen_name(self) -> str:
        """:class:`str`: Returns the mention user's screen name."""
        return self._screen_name

    @property
    def id(self) -> int:
        """:class:`id`: Returns the mention user's id."""
        return int(self._id)

    @property
    def points(self) -> Optional[Tuple]:
        """Optional[:class:`Tuple`]: Returns a tuple with the mention's startpoint and endpoint."""
        return self._startpoint, self._endpoint


class Urls:
    """Represent Urls in a message."""

    def __init__(self, data=Dict[str, Any]):
        self._payload: Dict[str, Any] = data
        self._url: str = self._payload.get("url")
        self._display_url: str = self._payload.get("display_url")
        self._expanded_url: str = self._payload.get("expanded_url")
        self._startpoint, self._endpoint = self._payload.get("indices")

    @property
    def url(self) -> str:
        """:class:`str`: Returns the image's url"""
        return self._url

    @property
    def display_url(self) -> str:
        """:class:`str`: Returns the image's display url"""
        return self._display_url

    @property
    def expanded_url(self) -> str:
        """:class:`str`: Returns the image's expanded url"""
        return self._expanded_url

    @property
    def points(self) -> Tuple:
        """Optional[:class:`Tuple`]: Returns a tuple with the url's startpoint and endpoint."""
        return self._startpoint, self._endpoint


class Symbols:
    """Represent Symbols in a message."""

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
