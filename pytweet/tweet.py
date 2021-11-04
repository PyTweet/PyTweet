import datetime
from typing import Any, Dict, List, NoReturn, Optional, TypeVar, Union

from .attachments import Media, Poll
from .enums import MessageTypeEnum
from .metrics import TweetPublicMetrics
from .user import User
from .utils import time_parse_todt

TT = TypeVar("TT", bound="Tweet")

__all__ = (
    "EmbedsImages",
    "Embed",
    "Tweet",
)


class EmbedsImages:
    """Represent the tweets embed images
    .. versionadded: 1.1.3

    Parameters:
    -----------
    data: Dict[str, Any]
        The full data of the images keep inside a dictionary.

    Attributes:
    -----------
    _payload
        The data parameters.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        self._payload = data

    def __repr__(self) -> str:
        return "EmbedsImages(url={0.url} width={0.width} height={0.height})".format(self)

    def __str__(self) -> str:
        return self.url

    @property
    def width(self) -> int:
        """int: Return the image's width
        .. versionadded: 1.1.3
        """
        return int(self._payload.get("width"))

    @property
    def height(self) -> int:
        """int: Return the image's height
        .. versionadded: 1.1.3
        """
        return int(self._payload.get("height"))

    @property
    def url(self) -> str:
        """int: Return the image's url
        .. versionadded: 1.1.3
        """
        return self._payload.get("url")


class Embed:
    """Represent the embedded urls in a tweet.
    .. versionadded: 1.1.3

    Parameters:
    ------------
    data: Dict[str, Any]
        The full data of the embed keep inside a dictionary.

    Attributes:
    ------------
    _payload
        The data parameters.
    """

    def __init__(self, data: Dict[str, Any]):
        self._payload = data

    def __repr__(self) -> str:
        return "Embed(title={0.title} description={0.description} url={0.url})".format(self)

    def __str__(self) -> str:
        return self.url

    @property
    def title(self) -> str:
        """str: Return the embed's title
        .. versionadded: 1.1.3
        """
        return self._payload.get("title")

    @property
    def description(self) -> str:
        """str: Return the embed's description
        .. versionadded: 1.1.3
        """
        return self._payload.get("description")

    @property
    def start(self) -> int:
        """int: Return the embed's url startpoint start
        .. versionadded: 1.1.3
        """
        return int(self._payload.get("start"))

    @property
    def end(self) -> int:
        """int: Return the embed's url endpoint.
        .. versionadded: 1.1.3
        """
        return int(self._payload.get("end"))

    @property
    def url(self) -> str:
        """str: Return the embed's url
        .. versionadded: 1.1.3
        """
        return self._payload.get("url")

    @property
    def expanded_url(self) -> str:
        """str: Return the expanded url
        .. versionadded: 1.1.3
        """
        return self._payload.get("expanded_url")

    @property
    def display_url(self) -> str:
        """str: Return the display url
        .. versionadded: 1.1.3
        """
        return self._payload.get("display_url")

    @property
    def unwound_url(self) -> str:
        """str: Return the unwound url
        .. versionadded: 1.1.3
        """
        return self._payload.get("unwound_url")

    @property
    def images(self) -> Optional[List[EmbedsImages]]:
        """List[EmbedsImages]: Return a list of Embed's Images
        .. versionadded: 1.1.3
        """
        if self._payload.get("images"):
            return [EmbedsImages(data) for data in self._payload.get("images")]

        return None

    @property
    def status_code(self) -> int:
        """int: Return the embed's url HTTP status code"""
        return int(self._payload.get("status"))


class Tweet:
    """Represent a tweet message from Twitter.
    A Tweet is any message posted to Twitter which may contain photos, videos, links, and text.
    .. versionadded: 1.0.0

    .. describe:: x == y
        Check if one tweet id is equal to another.


    .. describe:: x != y
        Check if one tweet id is not equal to another.


    .. describe:: str(x)
        Get the Tweet's text.

    Parameters:
    -----------
    data: Dict[str, Any]
        The complete data of a tweet keep inside a dictionary.

    Attributes:
    -----------
    original_payload
        Represent the main data of a tweet.

    _payload
        Same as original_payload but its inside the 'data' key.

    _includes
        Same as original_payload but its inside the '_includes' key..

    tweet_metrics
        Represent the public metrics of the tweet.
    """

    def __init__(self, data: Dict[str, Any], **kwargs: Any) -> None:
        self.original_payload = data
        self._payload = data.get("data") or None
        self._includes = self.original_payload.get("includes")
        self.tweet_metrics: TweetPublicMetrics = TweetPublicMetrics(self._payload)
        self.http_client = kwargs.get("http_client") or None

    def __repr__(self) -> str:
        return "Tweet(text={0.text} id={0.id} author={0.author})".format(self)

    def __str__(self) -> str:
        return self.text

    def __eq__(self, other: TT) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("== operation cannot be done with one of the element not a valid Tweet object")
        return self.id == other.id

    def __ne__(self, other: TT) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("!= operation cannot be done with one of the element not a valid User object")
        return self.id != other.id

    @property
    def text(self) -> str:
        """str: Return the tweet's text."""
        return self._payload.get("text")

    @property
    def id(self) -> int:
        """int: Return the tweet's id."""
        return int(self._payload.get("id"))

    @property
    def author(self) -> User:
        """Optional[:class:`User`]: Return a user (object) who posted the tweet."""
        return User(self._includes.get("users")[0], http_client=self.http_client)

    @property
    def retweeted_by(self) -> Union[List[User], int]:
        """Optional[List[:class:`User`]]: Return a list of users thats retweeted the specified tweet's id. Maximum users is 100. Return 0 if no one retweeted."""
        return self._payload.get("retweeted_by")

    @property
    def liking_users(self) -> Union[List[User], int]:
        """Optional[List[:class:`User`]]: Return a list of users that liked the specified tweet's id. Maximum users is 100. Return 0 if no one liked."""
        return self._payload.get("liking_users")

    @property
    def sensitive(self) -> bool:
        """bool: Return True if the tweet is possible sensitive to some users, else False"""
        return self._payload.get("possibly_sensitive")

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Return a datetime object with the tweet posted age."""
        return time_parse_todt(self._payload.get("created_at"))

    @property
    def source(self) -> str:
        """str: Return the source of the tweet. e.g if you post a tweet from a website, the source is gonna be 'Twitter Web App'"""
        return self._payload.get("source")

    @property
    def reply_setting(self) -> str:
        """str: Return the reply setting. If everyone can replied, reply_setting return 'Everyone'"""
        return self._payload.get("reply_settings")

    @property
    def lang(self) -> str:
        """str: Return the tweet's lang, if its english it return en."""
        return self._payload.get("lang")

    @property
    def convertion_id(self) -> int:
        """int: Return the tweet's convertion id."""
        return int(self._payload.get("convertion_id"))

    @property
    def link(self) -> str:
        """str: Return the tweet's link."""
        return f"https://twitter.com/{self.author.username.split('@', 1)[1]}/status/{self.id}"

    @property
    def reply_to(self) -> Optional[User]:
        """:class:`Optional[User]`: Return the user that you reply with the tweet, a tweet count as reply tweet if the tweet startswith @Username or mention a user.
        .. versionadded: 1.1.3
        """
        user = (
            self.http_client.fetch_user(
                int(self._payload.get("in_reply_to_user_id")),
                http_client=self.http_client,
            )
            if self._payload.get("in_reply_to_user_id")
            else None
        )
        return user

    @property
    def mentions(self) -> Optional[List[User]]:
        """:class:`Optional[List[User]]`: Return the mentioned users, if there isnt it return None.
        .. versionadded: 1.1.3
        """
        if self._includes:
            if self._includes.get("mentions"):
                return [
                    self.http_client.fetch_user_byusername(user.get("username"), http_client=self.http_client)
                    for user in self._includes.get("mentions")
                ]
        return None

    @property
    def poll(self) -> Optional[Poll]:
        """:class:`Poll`: Return a Poll object with the tweet's poll.
        .. versionadded: 1.1.0
        """
        if self._includes:
            if self._includes.get("polls"):
                return Poll(self._includes.get("polls")[0])

        return None

    @property
    def media(self) -> Optional[Media]:
        """:class:`List[Media]` -> Return a list of media(s) in a tweet.
        .. versionadded: 1.1.0
        """
        if self._includes:
            if self._includes.get("media"):
                return [Media(img) for img in self._includes.get("media")]
        return None

    @property
    def embeds(self) -> Optional[List[Embed]]:
        """:class:`List[Embed]`: Return a list of Embedded url from that tweet
        .. versionadded: 1.1.3
        """
        if self._payload.get("entities"):
            if self._payload.get("entities").get("urls"):
                return [Embed(url) for url in self._payload.get("entities").get("urls")]
        return None

    @property
    def type(self) -> MessageTypeEnum:
        """MessageTypeEnum: Return the Message type.
        .. versionadded: 1.2.0
        """
        return MessageTypeEnum(1)

    @property
    def like_count(self) -> int:
        """int: Return the total of likes in a tweet."""
        return self.tweet_metrics.like_count

    @property
    def retweet_count(self) -> int:
        """int: Return the total of retweetes in a tweet."""
        return self.tweet_metrics.retweet_count

    @property
    def reply_count(self) -> int:
        """int: Return the total of replies in a tweet."""
        return self.tweet_metrics.reply_count

    @property
    def quote_count(self) -> int:
        """int: Return the total of quotes in a tweet."""
        return self.tweet_metrics.quote_count
