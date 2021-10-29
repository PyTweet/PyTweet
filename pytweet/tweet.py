"""
MIT License

Copyright (c) 2021 TheFarGG & TheGenocides

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime
from typing import Optional, Dict, Any, List, Union
from .attachments import Poll, Media
from .user import User
from .metrics import TweetPublicMetrics
from .utils import time_parse_todt


class EmbedsImages:
    """Represent the tweets embed images
    .. versionadded: 1.1.3

    Parameters:
    =============
    data: Dict[str, Any]
        The full data of the images keep inside a dictionary.

    Attributes:
    =============
    _payload
        The data paramaters.
    """

    def __init__(self, data: Dict[str, Any]):
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
    """Represent the embeded urls in a tweet.
    .. versionadded: 1.1.3

    Parameters:
    =============
    data: Dict[str, Any]
        The full data of the embed keep inside a dictionary.

    Attributes:
    =============
    _payload
        The data paramaters.
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
        """int: Return the embed's start
        .. versionadded: 1.1.3
        """
        return int(self._payload.get("start"))

    @property
    def end(self) -> int:
        """int: Return the embed's end
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
    def images(self) -> List[EmbedsImages]:
        """List[:class:EmbedsImages]: Return a list of Embed's Images
        .. versionadded: 1.1.3
        """
        return [EmbedsImages(data) for data in self._payload.get("images")]

    @property
    def status_code(self) -> int:
        """int: Return the embed's url HTTP status code"""
        return int(self._payload.get("status"))


class Tweet:
    """Represent a tweet message from Twitter.
    A Tweet is any message posted to Twitter which may contain photos, videos, links, and text.
    .. versionadded: 1.0.0

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

    @property
    def text(self) -> str:
        """str: Return the tweet's text."""
        return self._payload.get("text")

    @property
    def id(self) -> int:
        """int: Return the tweet's id."""
        return self._payload.get("id")

    @property
    def author(self) -> Optional[User]:
        """Optional[:class:User]: Return a user (object) who posted the tweet."""
        return User(self._includes.get("users")[0], http_client=self.http_client)

    @property
    def retweeted_by(self) -> Union[List[User], int]:
        """Optional[List[:class:User]]: Return a list of users thats retweeted the specified tweet's id. Maximum users is 100. Return 0 if no one retweeted."""
        return self._payload.get("retweeted_by")

    @property
    def liking_users(self) -> Union[List[User], int]:
        """Optional[List[:class:User]]: Return a list of users that liked the specified tweet's id. Maximum users is 100. Return 0 if no one liked."""
        return self._payload.get("liking_users")

    @property
    def sensitive(self) -> bool:
        """bool: Return True if the tweet is possible sensitive to some users, else False"""
        return self._payload.get("possibly_sensitive")

    @property
    def created_at(self) -> datetime.datetime:
        """:class: datetime.datetime: Return a datetime object with the tweet posted age."""
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
        return self._payload.get("convertion_id")

    @property
    def reply_to(self) -> Optional[User]:
        """Optional[:class:User]: Return the user that you reply with the tweet, a tweet count as reply tweet if the tweet startswith @Username or mention a user.
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
    def mentions(self) -> Union[List[User], bool]:
        """Union[List[:class:User], bool]: Return the mentioned users, if there isnt it return False.
        .. versionadded: 1.1.3
        """
        if self._includes.get("mentions"):
            return [
                self.http_client.fetch_user_byusername(user.get("username"), http_client=self.http_client)
                for user in self._includes.get("mentions")
            ]
        return False

    @property
    def poll(self) -> Poll:
        """:class:Poll: Return a Poll object with the tweet's poll.
        .. versionadded: 1.1.0
        """
        return Poll(self._includes.get("polls")[0])

    @property
    def media(self) -> Media:
        """List[:class:Media] -> Return a list of media(s) in a tweet.
        .. versionadded: 1.1.0
        """
        return [Media(img) for img in self._includes.get("media")]

    @property
    def embeds(self) -> List[Embed]:
        """List[:class:Embed]: Return a list of Embeded url from that tweet
        .. versionadded: 1.1.3
        """
        return [Embed(url) for url in self._payload.get("entities").get("urls")]

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
